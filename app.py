import json
import os
import sqlite3

from flask import Flask, send_file, Response
from flask import request
from flask_cors import CORS
from apiflask import APIFlask, Schema
from apiflask.fields import String, Integer, List, Nested
from marshmallow.validate import Length
from werkzeug.datastructures import FileStorage

from run import OptSuperGlue, superglue

app = APIFlask(__name__, template_folder='./templates', static_folder='static')
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
baseURL = 'http://127.0.0.1:5000'


class ImageSchema(Schema):
    name = String(required=True)
    image = String(required=True)
    description = String(required=True)


class ApiResponse(Schema):
    code = Integer()
    msg = String()
    data = List(Nested(ImageSchema))


def initDB():
    conn = sqlite3.connect('images.db')
    cur = conn.cursor()
    sql_text_1 = '''
    CREATE TABLE "Imgs" (
        "name" TEXT
     );
     '''
    # 执行sql语句
    cur.execute(sql_text_1)


def insert_result():
    conn = sqlite3.connect('results.db')
    cur = conn.cursor()
    uploads = 'E://Ideaproject//SuperGluePretrainedNetwork-master/static/result'
    # 遍历文件夹中的所有文件
    for filename in os.listdir(uploads):
        sql_text_2 = '''INSERT INTO Imgs VALUES(?);'''
        cur.execute(sql_text_2, (filename,))
        conn.commit()


def findAll():
    conn = sqlite3.connect('images.db')
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()
    print("数据库中的表有：", tables)
    # 获取特定表的结构
    cur.execute(f"PRAGMA table_info(Imgs);")
    table_info = cur.fetchall()
    print(f"表z的结构为：", table_info)
    sql_text_1 = '''SELECT * FROM Imgs'''
    cur.execute(sql_text_1)
    records = cur.fetchall()
    for record in records:
        print(record)
    conn.close()


@app.post('/upload')
def upload_file(json_data):
    conn = sqlite3.connect('images.db')
    cur = conn.cursor()
    images = json_data['images']
    filenames = []
    for image in images:
        file = FileStorage(image['image'])
        filename = file.filename
        file.save(filename)
        filenames.append(filename)
    file = request.files['file']
    file.save('images/' + file.filename)
    return {
        'message': 'Images uploaded successfully.',
        'filenames': filenames
    }


@app.post('/api/match_img')
def match_img():
    conn = sqlite3.connect('images.db')
    cur = conn.cursor()
    uploaded_file = request.files['image']
    uploaded_file.save('match/' + uploaded_file.filename)
    return {
        'message': 'Images uploaded successfully.',
        'filenames': uploaded_file.filename
    }


class QuerySchema(Schema):
    imageName = String(required=True)


@app.get('/api/run_match')
def run_match():
    conn = sqlite3.connect('results.db')
    cur = conn.cursor()
    # 执行sql语句
    cur.execute('DELETE FROM Imgs')
    conn.commit()
    name = request.args.get('imageName')
    opt = OptSuperGlue('static/images', 'static/result')
    opt.superglue = 'outdoor'
    opt.wait_match_img = 'match/' + name
    superglue(opt)
    insert_result()
    return {
        'msg': 'Images uploaded successfully.',
        'code': '200'
    }


@app.get('/api/images')
@app.output(ApiResponse)
def get_images():
    conn = sqlite3.connect('images.db')
    cur = conn.cursor()
    sql_text_1 = '''SELECT * FROM Imgs'''
    cur.execute(sql_text_1)
    records = cur.fetchall()
    data = []
    for record in records:
        data.append({
            "name": record[0],
            "image": baseURL + '/static/images/' + record[0],
            "description": record[0]
        })
    return {
        'code': 200,
        'msg': 'SUSSES',
        'data': data

    }


@app.get('/api/results')
@app.output(ApiResponse)
def get_results():
    conn = sqlite3.connect('results.db')
    cur = conn.cursor()
    sql_text_1 = '''SELECT * FROM Imgs'''
    cur.execute(sql_text_1)
    records = cur.fetchall()
    data = []
    for record in records:
        data.append({
            "name": record[0],
            "image": baseURL + '/static/result/' + record[0],
            "description": record[0]
        })
    return {
        'code': 200,
        'msg': 'SUSSES',
        'data': data

    }


if __name__ == '__main__':
    # initDB()
    # insert()
    # findAll()
    app.run()
