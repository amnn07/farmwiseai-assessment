from flask import Flask, jsonify, request, abort
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

# Dummy database (SQLite can be used for a real-world application)
books = [
    {"isbn": "978-1505255607", "title": "To Kill a Mockingbird", "author": "Harper Lee", "price": 10.99, "quantity": 5},
    {"isbn": "978-0061120084", "title": "1984", "author": "George Orwell", "price": 9.99, "quantity": 3}
]

# Dummy user credentials (replace with real authentication mechanism)
users = {
    "admin": "admin123"
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

@app.route('/books', methods=['GET'])
@auth.login_required
def get_books():
    return jsonify(books)

@app.route('/books/<isbn>', methods=['GET'])
@auth.login_required
def get_book(isbn):
    book = next((book for book in books if book['isbn'] == isbn), None)
    if book:
        return jsonify(book)
    else:
        abort(404)

@app.route('/books', methods=['POST'])
@auth.login_required
def add_book():
    if not request.json or not all(key in request.json for key in ['isbn', 'title', 'author', 'price', 'quantity']):
        abort(400)
    new_book = {
        'isbn': request.json['isbn'],
        'title': request.json['title'],
        'author': request.json['author'],
        'price': request.json['price'],
        'quantity': request.json['quantity']
    }
    books.append(new_book)
    return jsonify({'message': 'Book added successfully'}), 201

@app.route('/books/<isbn>', methods=['PUT'])
@auth.login_required
def update_book(isbn):
    book = next((book for book in books if book['isbn'] == isbn), None)
    if book:
        book.update(request.json)
        return jsonify({'message': 'Book updated successfully'})
    else:
        abort(404)

@app.route('/books/<isbn>', methods=['DELETE'])
@auth.login_required
def delete_book(isbn):
    global books
    books = [book for book in books if book['isbn'] != isbn]
    return jsonify({'message': 'Book deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
