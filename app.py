from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from os.path import join, dirname
import requests
from bs4 import BeautifulSoup

# Load environment variables from .env file
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)

@app.route('/')
def index():
    songs = list(db.songs.find({}, {'_id': False})) 
    return render_template('index.html', songs=songs)

@app.route('/add_song', methods=['GET', 'POST'])
def add_song():
    if request.method == 'POST':
        url_receive = request.form['url_give']
        star_receive = request.form['star_give']
        comment_receive = request.form['comment_give']

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
        data = requests.get(url_receive, headers=headers)

        soup = BeautifulSoup(data.text, 'html.parser')

        og_image = soup.select_one('meta[property="og:image"]')
        og_title = soup.select_one('meta[property="og:title"]')
        og_description = soup.select_one('meta[property="og:description"]')

        image = og_image['content']
        title = og_title['content']
        description = og_description['content']

        doc = {
            'image': image,
            'title': title,
            'description': description,
            'star': star_receive,
            'comment': comment_receive,
        }

        db.songs.insert_one(doc)
        return redirect(url_for('index'))  
    return render_template('add_song.html')

@app.route('/database_song')
def database_song():
    songs = list(db.songs.find({}, {'_id': False})) 
    return render_template('database_song.html', songs=songs)

@app.route('/song', methods=['GET'])
def get_songs():
    songs = list(db.songs.find({}, {'_id': False})) 
    return jsonify({'songs': songs})

@app.route('/song', methods=['POST'])
def post_song():
    url = request.form['url_give']
    star = request.form['star_give']
    comment = request.form['comment_give']

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    og_image = soup.select_one('meta[property="og:image"]')
    og_title = soup.select_one('meta[property="og:title"]')
    og_description = soup.select_one('meta[property="og:description"]')

    image = og_image['content']
    title = og_title['content']
    description = og_description['content']

    doc = {
        'image': image,
        'title': title,
        'description': description,
        'star': star,
        'comment': comment,
    }

    db.songs.insert_one(doc)
    return jsonify({'msg': 'Song added successfully'})

@app.route('/song/<title>', methods=['PUT'])
def update_song(title):
    image = request.form['image_give']
    star = request.form['star_give']
    comment = request.form['comment_give']
    description = request.form['description_give']

    db.songs.update_one(
        {'title': title},
        {'$set': {
            'image': image,
            'star': star,
            'comment': comment,
            'description': description
        }}
    )
    return jsonify({'msg': 'Song updated successfully'})

@app.route('/song/<title>', methods=['DELETE'])
def delete_song(title):
    db.songs.delete_one({'title': title})
    return jsonify({'msg': 'Song deleted successfully'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
