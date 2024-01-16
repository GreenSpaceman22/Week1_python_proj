from flask import Flask, request, jsonify
from pymongo import MongoClient


conn_str = "mongodb+srv://GreenSpaceman22:GreenGoose22!@stickynoteapp.7vdetmi.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(conn_str)
db = client['stickynoteapp']
collection = db['user_note_app']
app = Flask(__name__)

@app.get('/on_page_load')
def load_it():
    cursor = collection.find()
    each_user_data = {}
    for document in cursor:
        user_returning = document.get('user_name')
        user_returned_notes = document.get('Note')
        each_user_data[user_returning] = user_returned_notes
        with open(f'{user_returning}.txt', 'w') as returning_user:
            returning_user.write(user_returned_notes)
    return jsonify(each_user_data)


@app.post('/post_it')
def post_it():
    cursor = collection.find()
    data = request.json
    user_id = data.get("user_name")
    user_id = user_id.replace(" ", "")
    notes = data.get("Note")
    notes = f"{notes}"
    count_documents = collection.count_documents({})
    user_to_find = {'user_name' : f'{user_id}'}
      
    if count_documents == 0:
        collection.insert_one({'user_name' : user_id, 'Note' : notes})
        with open(f'{user_id}.txt', 'w') as new_user_notes:
            new_user_notes.write(f"{notes}\n")
        
    else: 
        user_list = []
        for document in cursor:
            user_list.append(document.get('user_name'))
        if user_id in user_list:
            with open(f'{user_id}.txt', 'a') as user_notes:
                user_notes.write(f"{notes}\n")
                user_notes.close()
            with open(f'{user_id}.txt', 'r') as user_notes_read:
                new_notes = user_notes_read.read()
                update_data = {'$set' : {'user_name' : user_id, 'Note' : new_notes}}
                collection.update_one(user_to_find, update_data) 
        else:
            with open(f'{user_id}.txt', 'w') as new_user_notes:
                new_user_notes.write(f"{notes}\n")
                collection.insert_one({'user_name' : user_id, 'Note' : notes})   
       
    return jsonify({user_id : notes}) 
if __name__ == '__main__':
    app.run(debug=True)

    
