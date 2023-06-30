'''
Given a string, find the first non-repeating character in it and return it's index. If it doesn't exist, return -1.

Examples:

s = "leetcode"
return 0.

s = "loveleetcode",
return 2.

Note: You may assume the string contain only lowercase letters.
'''
class Solution:
    def firstUniqChar(self, s: str) -> int:
        count = {}
        for char in s:
            count[ch] = count.get(ch, 0) + 1
        for idx, char in enumerate(s):
            if char in count and count[ch] == 1:
                return idx
        return -1
