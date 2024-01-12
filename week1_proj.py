from flask import Flask, request, jsonify
from pymongo import MongoClient

conn_str = "mongodb+srv://GreenSpaceman22:GreenGoose22!@stickynoteapp.7vdetmi.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(conn_str)
db = client['stickynoteapp']
collection = db['user_note_app']

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'
@app.post('/post_it')
def post_it():
    data = request.json
    print(data)

    result = collection.insert_one(data)

    return jsonify({'message': 'Data saved successfully', 'id': str(result.inserted_id)})

if __name__ == '__main__':
    app.run(debug=True)
