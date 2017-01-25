import uuid

from flask import Flask, request, jsonify, redirect, render_template, send_from_directory

import json
import random
import requests
import os
import pyrebase
import pyvona
import re
import json
from os import listdir
from os.path import isfile, join

app = Flask(__name__, static_url_path="/static")
url = 'http://184.107.80.44:8080/examples/servlets/getanalytics?limit=300'
DIR_PATH = os.path.dirname(os.path.realpath(__file__))

tts = pyvona.create_voice('GDNAI2DMZ564XADE7TNA', 'OjIyLMbH0X4LAHKlkMh6E5zgQlE5yi4Sklu/QyLt')

config = {
    "apiKey": "AIzaSyB74UF2Phk6AiBUsOthxQYKCFDj39Nphzk",
    "authDomain": "tempimage-5b31b.firebaseapp.com",
    "databaseURL": "https://tempimage-5b31b.firebaseio.com",
    "storageBucket": "tempimage-5b31b.appspot.com",
}

firebase = pyrebase.initialize_app(config)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/fc')
def foo():
    data_json = get_data_json('video4')
    #return data_json
    return render_template('fc.html', data_json=data_json)

def get_data_json(v_id):
    files_path="/static/%s"%(v_id)
    mypath=DIR_PATH
    mypath=mypath+files_path

    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    data=[]
    audio_file=""
    for i in onlyfiles:
        if  i.endswith(".mp4"):
            inner=[]

            a= i.split("_")[1]
            b=a.split(".")[0]
            inner.append(b)
            inner.append("face")
            inner.append(files_path+"/"+i)
            data.append(inner)
        if i.endswith(".png"):
            inner=[]

            a= i.split("_")[1]
            b=a.split(".")[0]
            inner.append(b)
            inner.append("slide")
            inner.append(files_path+"/"+i)
            data.append(inner)

        if i.endswith(".aac"):
            audio_file=files_path+"/"+i
            data.append(['0','audio',audio_file])
    
    
    data_json = json.dumps(data)
    return data_json

@app.route('/v/<v_id>')
def faceslide(v_id):
    
    files_path="/static/%s"%(v_id)
    mypath=DIR_PATH
    mypath=mypath+files_path

    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    data=[]
    audio_file=""
    for i in onlyfiles:
        if  i.endswith(".mp4"):
            inner=[]

            a= i.split("_")[1]
            b=a.split(".")[0]
            inner.append(b)
            inner.append("face")
            inner.append(files_path+"/"+i)
            data.append(inner)
        if i.endswith(".png"):
            inner=[]

            a= i.split("_")[1]
            b=a.split(".")[0]
            inner.append(b)
            inner.append("slide")
            inner.append(files_path+"/"+i)
            data.append(inner)

        if i.endswith(".aac"):
            audio_file=files_path+"/"+i

    
    data_json = []
    for i in data:
        data_json.append(i)
    
    data_json = json.dumps(data_json)
    
    return render_template('faceslide.html',data_json=data_json,audio_file=audio_file,v_id=v_id)


@app.route('/foo/<path:path>')
def send_js(path):
    return send_from_directory('static/video4', path)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'GET':

        narrator_list = []
        music_files = []

        return render_template('dashboard.html',
                               narrator_list=narrator_list,
                               music_files=music_files,
                               DIR_PATH=DIR_PATH)

    else:
        video_title = request.form['video_title']
        video_script = request.form['video_script']

        source = request.form['source']
        writer = request.form['writer']
        uploader = request.form['uploader']
        category = request.form['category']
        music = request.form['music']
        video_type = request.form['video_type']

        timer = request.form['timer']
        slide1_img = request.form['slide1_img']
        slide2_img = request.form['slide2_img']
        slide3_img = request.form['slide3_img']
        slide4_img = request.form['slide4_img']
        slide5_img = request.form['slide5_img']
        slide6_img = request.form['slide6_img']

        slide1_title = request.form['slide1_title']
        slide2_title = request.form['slide2_title']
        slide3_title = request.form['slide3_title']
        slide4_title = request.form['slide4_title']
        slide5_title = request.form['slide5_title']
        slide6_title = request.form['slide6_title']

        file_name = str(uuid.uuid4().hex.upper()[0:6])

        '''
        tts.codec = 'mp3'
        tts.voice_name = 'Raveena'
        tts.fetch_voice(video_script, file_name)
        os.system('mv %s.mp3 facecrop_raw/%s.mp3' % (file_name, file_name))
        '''

        data = {
            'narration_url': 'http://orch.in/newsmeme_raw/%s.mp3' % file_name,
            'published': False,
            'data_json': {
                'data_1': {'image': slide1_img, 'title': slide1_title, 'time': 5},
                'data_2': {'image': slide2_img, 'title': slide2_title, 'time': 5},
                'data_3': {'image': slide3_img, 'title': slide3_title, 'time': 5},
                'data_4': {'image': slide4_img, 'title': slide4_title, 'time': 5},
                'data_5': {'image': slide5_img, 'title': slide5_title, 'time': 5},
                'data_6': {'image': slide6_img, 'title': slide6_title, 'time': 5},
            },
            'video_title': video_title,
            'video_script': video_script,
            'narrator': '1HfjOEgiJj',
            'narrator_name': 'Bot',
            'writer': writer,
            'uploader': uploader,
            'source': source,
            'category': category,
            'timer': timer,
            'music': music,
            'video_type': video_type
        }

        db = firebase.database().child('facecrop')
        db.push(data)

        return redirect('/dashboard')


def wiki_search(title="tomato"):
    
    
    url = 'https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles=%s'%(title)
    resp = requests.get(url=url).text
    data = json.loads(resp)
    scoped_data = data['query']['pages']
        
    # page_id = data['query']['pages'].keys()[0]
    page_id = next(iter(data['query']['pages'])) 
    wiki_url = 'https://en.m.wikipedia.org/?curid=%s'%(page_id)
    try:
        wiki_content = scoped_data[page_id]['extract']
        wiki_content = re.sub(r'[^\x00-\x7F]+',' ', wiki_content)
        wiki_content = re.sub(r'\([^)]*\)', '', wiki_content)
            
            
        wiki_content = wiki_content[:140] 
    except KeyError:
        wiki_content = ''

        
        
    return wiki_content


@app.route('/turing', methods=['GET', 'POST'])
def turing():
    if request.method == 'GET':
        random_words=["tomato", "australia", "facebook","mars","ocean","x-rays"]    

        key=random.choice(random_words)
        wiki_content=wiki_search(key)
        if len(wiki_content)==0:
            wiki_content= wiki_search("earth")
        else: 
            pass
        
        return render_template('turing.html',wiki_content=wiki_content,
                               DIR_PATH=DIR_PATH)

    else:
       

        return redirect('/turing')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

