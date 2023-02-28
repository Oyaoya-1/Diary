from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

client = MongoClient('mongodb+srv://coba:mencoba@cluster0.h6atr6m.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({}, {'_id': False}))
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    #sample_receive = request.form.get('sample_give')
   # print(sample_receive)
    title_receive = request.form.get('title_give')
    content_receive = request.form.get('content_give')

    today = datetime.now()
    mytime = today.strftime('%y-%m-%d %H-%M-%S')

    file = request.files['file_give']
    extension = file.filename.split('.')[-1]
    filename = f'post-{mytime}.{extension}'
    save_to = f'static/{filename}'
    file.save(save_to)

    profile = request.files['profile_give']
    extension = profile.filename.split('.')[-1]
    profilename = f'profile-{mytime}.{extension}'
    save_profile = f'static/{profilename}'
    profile.save(save_profile)

    doc = {
        'file': filename,
        'profile': profilename,
        'title': title_receive,
        'content': content_receive,
    }
    db.diary.insert_one(doc)
    return jsonify({'message': 'post complete' })


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)