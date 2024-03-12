import json
import os
import sqlite3
import shutil

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


@app.post('/api/upload')
def upload_file():
    images = request.files.getlist('image')
    filenames = []
    for image in images:
        image.save('static/images/' + image.filename)
    insert_images()
    return {
        'msg': 'Images uploaded successfully.',
        'data': filenames
    }


@app.post('/api/match_img')
def match_img():
    conn = sqlite3.connect('images.db')
    cur = conn.cursor()
    uploaded_file = request.files['image']
    uploaded_file.save('match/' + uploaded_file.filename)
    return {
        'code': 200,
        'msg': 'Images uploaded successfully.',
        'data': uploaded_file.filename
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
        'msg': 'success',
        'code': '200'
    }


def insert_result():
    conn = sqlite3.connect('results.db')
    cur = conn.cursor()
    uploads = 'E://Ideaproject//SuperGluePretrainedNetwork-master/static/result'
    # 遍历文件夹中的所有文件
    for filename in os.listdir(uploads):
        sql_text_2 = '''INSERT INTO Imgs VALUES(?);'''
        cur.execute(sql_text_2, (filename,))
        conn.commit()


def insert_images():
    conn = sqlite3.connect('images.db')
    cur = conn.cursor()
    uploads = 'E://Ideaproject//SuperGluePretrainedNetwork-master/static/images'
    # 遍历文件夹中的所有文件
    for filename in os.listdir(uploads):
        sql_text_2 = '''INSERT INTO Imgs VALUES(?);'''
        cur.execute(sql_text_2, (filename,))
        conn.commit()


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


@app.get('/api/delAllimg')
@app.output(ApiResponse)
def del_all_img():
    folder_path = 'E:\Ideaproject\SuperGluePretrainedNetwork-master\static\images'
    conn = sqlite3.connect('images.db')
    cur = conn.cursor()
    # 执行sql语句
    cur.execute('DELETE FROM Imgs')
    conn.commit()
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('删除 %s 时出错。原因: %s' % (file_path, e))
            return {
                'code': 1001,
                'msg': '删除失败：' + str(e),
                'data': ''
            }
    return {
        'code': 200,
        'msg': 'SUCCESS',
        'data': ''
    }


if __name__ == '__main__':
    app.run()
