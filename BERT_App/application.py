import flask as fs
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify, request
from flask import render_template
import datetime
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from flask_marshmallow import Marshmallow
from marshmallow import Schema
from transformers import pipeline


nlp = pipeline("question-answering")


# Kahneman example:
# context = r"""
#       (context)
#  """
# result = nlp(question="What are the three levels of knowledge?", context=context)
# print(f"Answer: '{result['answer']}'")
# print(result)





application = fs.Flask(__name__)
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/liblog'
application.debug = True
db = SQLAlchemy(application)
ma = Marshmallow(application)


class Schema(ma.Schema):
    
    fields = ('id','title','description')

schema = Schema()
soschema = Schema(many=True)

class Sources(db.Model):
    __tablename__ = 'todos2'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(1770), nullable=False)




    def __init__(self, id, title, description):
        self.id = id
        self.title = title
        self.description = description


@application.route('/')
def home():
    return render_template("home.html")

HOME_HTML = """
    <html><body>
        <h2>Welcome to the Future</h2>
        <form action="/id">
            What's your id? <input type='number' name='id'><br>
            <input type='submit' value='Continue'>
        </form>
    </body></html>"""

@application.route('/id')
def hoop1():
    global id
    id = request.args.get('id', '')

    return (render_template("test.html")).format(id)

TEST_HTML = """
    <html><body>
            <form action="/source/{0}">
            What's your question? <input type='text' name='question'><br>
            <input type='submit' value='Continue'>
    </body></html>
         """
@application.route('/addSource')
def postSource():
    return POST_HTML

POST_HTML = """
    <html><body>
<form action="postedSource" method = "POST">
    <p> id <input type = "number" step="1" name = "id" /></p>
    <p> title <input type = "text" name = "title" /></p>
    <p> description <input type = "text" name = "description" /></p>
    <p><input type = "submit" value = "submit" /></p>
</form>
    </body></html>"""

@application.route('/postedSource', methods=['POST'])
def postedSource():
    form_data = request.form
    todo = Sources(id=form_data['id'], title=form_data['title'],description=form_data['description'])
    db.session.add(todo)
    db.session.commit()
    return (form_data)

    #return render_template('data.html',form_data = form_data)

@application.route('/getSources', methods=['GET'])
def getSources():
    AllSources = Sources.query.all()
    output = []
    for source in AllSources:
        CurrSource = {}
        CurrSource['id']= source.id
        CurrSource['title'] = source.title
        CurrSource['description'] = source.description
        
        output.append(CurrSource)
    return jsonify(output)        

@application.route('/viewSources', methods=['GET'])
def viewSources():
    AllSources = Sources.query.all()
    output = []
    for source in AllSources:
        CurrSource = {}
        CurrSource['id']= source.id
        CurrSource['title'] = source.title
        CurrSource['description'] = source.description
        
        output.append(CurrSource)
    return jsonify(output)        

@application.route('/postSource', methods=['POST'])
def postSource2():
    SourceData = request.get_json()
    source = Sources(id=SourceData['id'], title=SourceData['title'],description=SourceData['description'])
    db.session.add(source)
    db.session.commit()
    return jsonify(SourceData)

@application.route('/sources/<id>', methods=['DELETE'])
def deleteSource(id):
    Sources.query.filter_by(id=id).delete()
    db.session.commit()
    return "Source was successfully deleted"

@application.route('/source/<id>', methods=["GET"])
def get_todo(id):

    question = request.args.get('question', '')
    
    source = Sources.query.get(id)
    context = source.description
    result = nlp(question=question, context=context)
    return (render_template("new.html")).format(result['answer'],result['score'])



