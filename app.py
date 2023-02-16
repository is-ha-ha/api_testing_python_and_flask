import requests
from flask import Flask, jsonify, request

# creating flask app
app = Flask(__name__)


###CALL THE base API###
def get_json_file():
   get_author = requests.get("https://dev.ylytic.com/ylytic/test")

   if get_author.status_code != 204:
      print("Done")
      data = get_author.json()

   import json
   with open('db.json','w',encoding='utf8') as f:
      json.dump(data,f,ensure_ascii=False,indent=4)
   
   comments = data['comments']
   return comments


comments = get_json_file()

@app.route('/',methods=['GET'])
def get_main():
   return comments

### SEARCHING COMMENTS WITH AUTHOR NAME ###
@app.route('/author/<author_name>')
def search_by_author(author_name):
   global comments
   result = [] # for storing final result
   # matching with given author name
   for comment in comments:
      if comment['author'] == author_name:
         result.append(comment)

   # returning result
   return jsonify({'result': result})


### FOR NUMBER OF REPLIES AND NUMBER OF LIKES
@app.route('/<int:start_like>/<int:end_like>/<int:start_replies>/<int:end_replies>')
def range_for_like_replies(start_like, end_like,start_replies,end_replies):
   result = [] # for final result

   for comment in comments:
      if (start_replies <= comment['reply'] <= end_replies) and (start_like <= comment['like'] <= end_like):
         result.append(comment)

   return jsonify({'result': result})


### SEARCHING COMMENTS WITH SEARCH STRING IN THE TEXT FIELD ###
@app.route('/text/<text>')
def search_text(text):
   result = [] # for final result

   for comment in comments:
      if text in comment['text']:
         result.append(comment)

   return jsonify({'result': result})

## running app
app.run(debug=True)