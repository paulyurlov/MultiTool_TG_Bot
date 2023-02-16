from flask import Flask, redirect, render_template, session, request, jsonify
from pymongo import MongoClient
from flask import send_file
import gridfs
import io
import os

# from pygments import highlight
# from pygments.formatters import HtmlFormatter
# from pygments.lexers import guess_lexer, PythonLexer


CON_STRING = os.environ['CON_STRING']

'''
DataBase structure:

Collection Name = multi_tool

{
    "short_url": short_url, 
    'type': ['pastebin', 'file', 'link']
    'pastebin_txt': ['pastebin_txt', 'file_id', 'original_url']
}

'''


TMP = """
@app.route('/<short_key>')
def redirect_link(short_key):
    item = db['multi_tool'].find_one({'short_url': short_key})
    if item is not None:
        return redirect(item['original_url'])
    else:
        return render_template('error.html')
"""


app = Flask(__name__)
client = MongoClient(CON_STRING)
db = client['linkForwarder']
fs = gridfs.GridFS(db)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<short_key>')
def redirect_link(short_key):
    item = db['multi_tool'].find_one({'short_url': short_key})
    if item is not None:
        return redirect(item['original_url'])
    else:
        return render_template('error.html')


# @app.route('/file-<short_key>')
# def get_file(short_key):
#     if fs.exists(filename=short_key):
#         outputfile = fs.find_one({"filename": short_key})
#         with open(short_key, 'wb') as fileObject:
#             fileObject.write(outputfile.read())
#         return send_file(short_key, as_attachment=True)
#     else:
#         return render_template('error.html')


# @app.route('/pastebin')
# def get_pastebin():
#     formatter = HtmlFormatter()
#     lexer = guess_lexer(TMP)
#     result = highlight(TMP, lexer, formatter)
#     with open('templates/pastebin_code.html', 'w') as f:
#         f.write(result)
#     with open('static/styles/pastebin_code.css', 'w') as f:
#         f.write(formatter.get_style_defs())
#     # print(request.args['switch'])
#     print('lol')
#     return render_template('pastebin.html')


# @app.route('/change_theme', methods=['POST'])
# def theme_switcher():
#     data = request.get_json()
#     print(data)
#     return 'Data received'


# @app.route('/get_theme', methods=['GET'])
# def get_theme():
#     data = {'theme': 'dark'}
#     return jsonify(data)


if __name__ == '__main__':
    app.run(port=69, debug=True)
