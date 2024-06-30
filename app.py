#import re
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)
#from app import APP
#from app import db
#APP.app_context().push()
#db.create_all()
#from app import Book


class Book(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique = True, nullable = False)
    description = db.Column(db.String(120))
    author = db.Column(db.String(120))
    publisher = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.description}"

#book = Book(name = "Hunger Games", description = "Death Game")
#book -> output Hunger Games - Death Game
#db.session.add(book)
#db.session.commit()
#Drink.query.all()
#db.session.add(Drink(name="Bible", description="Book About Christianity"))
#db.session.commit
#Drink.query.all()


@app.route('/')
def index():
    return 'Hello!'

@app.route('/books')
def getBooks():
    books = Book.query.all()

    output = []
    for book in books:
        book_data = {'name':book.name, 'description': book.description, 
                     'author':book.author, 'publisher':book.publiher}

        output.append(book_data)
    return {"books": output}

@app.route('/books/<id>')
def get_book(id):
    book = Book.query.get_or_404(id)
    return {"name": book.name, "description": book.description,
            'author':book.author, 'publisher':book.publiher}

@app.route('/books', methods=['POST'])
def add_book():
    book = Book(name = request.json['name'], description = request.json['description'],
                 author = request.json['author'], publisher = request.json['publisher'])
    db.session.add(book)
    db.session.commit()
    return {'id':book.id}

@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if book is None:
        return {"error":"not found"}
    db.session.delete(book)
    db.session.commit()
    return {"message": "GONE!"}