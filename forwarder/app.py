from flask import Flask, redirect, render_template
from pymongo import MongoClient
from dotenv import load_dotenv
from flask import send_file
import gridfs
import io
import os

load_dotenv()

CON_STRING = os.environ['CON_STRING']


app = Flask(__name__)
client = MongoClient(CON_STRING)
db = client['linkForwarder']

client = MongoClient(CON_STRING)
db = client['linkForwarder']
fs = gridfs.GridFS(db)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<short_key>')
def redirect_link(short_key):
    item = db['links'].find_one({'short_url': short_key})
    if item is not None:
        return redirect(item['original_url'])
    else:
        return render_template('error.html')


@app.route('/file-<short_key>')
def get_file(short_key):
    if fs.exists(filename=short_key):
        outputfile = fs.find_one({"filename": short_key})
        with open(short_key, 'wb') as fileObject:
            fileObject.write(outputfile.read())
        return send_file(short_key, as_attachment=True)
    else:
        return render_template('error.html')


if __name__ == '__main__':
    app.run(port=69, debug=True)
