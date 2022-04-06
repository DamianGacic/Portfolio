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
import json
from json2html import *


nlp = pipeline("question-answering")

application = fs.Flask(__name__)
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/liblog'
application.debug = True
db = SQLAlchemy(application)
ma = Marshmallow(application)

class Sources(db.Model):
    __tablename__ = 'Sources1'
    title = db.Column(db.String(200),primary_key=True)
    description = db.Column(db.String(1770), nullable=False)




def __init__(self, title, description):
    self.title = title
    self.description = description

@application.route('/')
def home():
    return render_template("home.html")

@application.route('/title')
def hoop1():
    global title
    title = request.args.get('title', '')

    return (render_template("test.html")).format(title)


@application.route('/addSource')
def postSource():
    return render_template("post.html")


@application.route('/postedSource', methods=['POST'])
def postedSource():
    form_data = request.form
    source = Sources(title=form_data['title'],description=form_data['description'])
    db.session.add(source)
    db.session.commit()
    form_data = form_data.to_dict(flat=True)
    output = json2html.convert(json=form_data)

    return (output)




@application.route('/viewTexts', methods=['GET'])
def viewSources():
    AllSources = Sources.query.all()
    output = []
    for source in AllSources:
        CurrSource = {}
        CurrSource['title'] = source.title
        CurrSource['text'] = source.description
        
        output.append(CurrSource)
    
    output = json2html.convert(json=output)

    return (output)        

@application.route('/postSource', methods=['POST'])
def postSource2():
    SourceData = request.get_json()
    source = Sources(title=SourceData['title'],description=SourceData['description'])
    db.session.add(source)
    db.session.commit()
    return jsonify(SourceData)

@application.route('/deleteSource/<title>', methods=['DELETE'])
def deleteSource(title):
    Sources.query.filter_by(title=title).delete()
    db.session.commit()
    return "Source was successfully deleted"

@application.route('/source/<title>', methods=["GET"])
def get_source(title):

    question = request.args.get('question', '')
    if question == "":
        return render_template(("new.html")).format("go back and ask a question","go back and ask a question!")
    source = Sources.query.get(title)
    context = source.description
    result = nlp(question=question, context=context)
    return (render_template("new.html")).format(result['answer'],result['score'])





