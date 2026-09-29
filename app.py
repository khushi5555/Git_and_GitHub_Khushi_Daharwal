from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from dotenv import load_dotenv
import json
import os

app = Flask(__name__)

# MongoDB Atlas Connection
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000
)

db = client["todo_database"]
collection = db["todo_items"]


# Home Page
@app.route('/')
def home():
    return render_template('index.html')


# JSON API
@app.route('/api')
def api():
    with open('data.json', 'r') as file:
        data = json.load(file)

    return jsonify(data)
@app.route('/todo')
def todo():
    return render_template('todo.html')


# MongoDB To-Do API
@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():

    item_name = request.form.get('itemName')
    item_description = request.form.get('itemDescription')

    if not item_name or not item_description:
        return jsonify({
            "error": "Both fields are required"
        }), 400

    item = {
        "itemName": item_name,
        "itemDescription": item_description
    }

    try:
        result = collection.insert_one(item)

        return jsonify({
            "message": "To-Do item saved successfully",
            "id": str(result.inserted_id)
        }), 201

    except Exception:
        app.logger.exception("MongoDB insertion failed")
        return jsonify({
            "error": "Unable to save To-Do item"
        }), 500


if __name__ == '__main__':
    app.run(debug=True)