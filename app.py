import pymongo
from datetime import datetime
from flask import Flask, url_for,render_template, redirect, request


app = Flask(__name__)
# 数据库实例
content = pymongo.MongoClient('127.0.0.1', 27017)
db = content.todo
# mongo    TODO文档结构
class Todo(object):
    """
    一行待办事项数据结构；
    字段：事项内容，添加创建时间，状态(未完成、已完成：完成时间)
    """
    @staticmethod
    def create_doc(self, content):
        return {
            'content': content,
            'create_time': datetime.now(),
            'status': 0,  # 0未完成 1已完成     'unfinish' 'done'
            'finish_time': None
        }

@app.route('/')
def index():
    return redirect(url_for('get'))

@app.route('/get')
def get():
    """展示todo列表"""
    todo_list = db.todo.find({})
    print(todo_list)
    return render_template('index.html', todo_list= todo_list)

@app.route('/add', methods=['POST'])
def add():
    """添加一条todo"""
    form = request.form
    content = form['content']
    print(content)
    if content:
        affected_id = db.todo.insert({
            "content": content,
            "create_time": datetime.now(),
            "status": 0,
            "finish_time": None
        })
        print(affected_id)
        if affected_id:
            return redirect(url_for('index'))

@app.route('/finish')
def finish():
    """更新状态为已完成"""
    pass

@app.route('/delete')
def delete():
    """删除无用的todo"""
    args = request.args
    content = args['content']
    print(content)
    affect_id = db.todo.remove({
      "content": content
    })
    print(affect_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
