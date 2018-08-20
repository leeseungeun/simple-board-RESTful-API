from datetime import datetime
from flask import (Flask, jsonify, request)
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)


# SQLAlchemy Board Model
class Board(db.Model):
    __tablename__ = 'boards'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String)
    title = db.Column(db.String)
    content = db.Column(db.String)
    pub_date = db.Column(db.DateTime)

    def __init__(self, author, title, content):
        self.author = author
        self.title = title
        self.content = content
        self.pub_date = datetime.utcnow()

db.create_all()
db.session.commit()

# test application
@app.route('/')
def index():
    return 'Hello World'

# api routing for listing / creating board
@app.route('/boards', methods=['GET', 'POST'])
def boards():
    if request.method == 'POST':
        return create_board()
    elif request.method == 'GET':
        return list_board()

# api routing for reading / updating / deleting a board
@app.route('/boards/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def board(id):
    if request.method == 'GET':
        return read_board(id)
    elif request.method == 'PATCH':
        return update_board(id)
    elif request.method == 'DELETE':
        return delete_board(id)

# function used for creating board
def create_board():

    # retrieve value from request
    author = request.form['author']
    title = request.form['title']
    content = request.form['content']

    # create a board model
    board = Board(author=author, title=title, content=content)
    
    # create a new record
    db.session.add(board)
    db.session.commit()

    # return created board 
    return jsonify({"author":author, "title":title, "content": content})

# function used for listing board
def list_board():
    #variable to save boards
    boards = []

    # query all board records
    query_results = Board.query.all()
    
    # retrieve information using queried results
    for result in query_results:
        board = dict()
        board["id"] = result.id
        board["author"] = result.author
        board["title"] = result.title
        board["content"] = result.content
        board["pub_date"] = result.pub_date
        boards.append(board)
        
    # return boards
    return jsonify(boards)

# function used for reading the board
def read_board(id):
    # query the board record
    query_result = Board.query.get(id)

    # query result to dict
    board = dict()
    board["id"] = query_result.id
    board["author"] = query_result.author
    board["title"] = query_result.title
    board["content"] = query_result.content
    board["pub_date"] = query_result.pub_date

    # return board
    return jsonify(board)

def update_board(id):

    # retrieve data from request
    title = request.form['title']
    content = request.form['content']

    # get a board to update
    query_result = Board.query.get(id)

    # update the board
    query_result.title = title
    query_result.content = content

    db.session.commit()

    # board to dict
    board = dict()
    board["id"] = query_result.id
    board["author"] = query_result.author
    board["title"] = query_result.title
    board["content"] = query_result.content
    board["pub_date"] = query_result.pub_date

    return jsonify(board)

def delete_board(id):

    # get a board to delete
    query_result = Board.query.get(id)

    db.session.delete(query_result)
    db.session.commit()

    return "board deleted"

# application run options
if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8000', debug=True)