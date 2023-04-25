from marshmallow import Schema, fields, EXCLUDE


class BookSchema(Schema):
    title = fields.Str()
    author = fields.Str()
    description = fields.Str()


class Book:
    def __init__(self, title, author, description):
        self.title = title
        self.author = author
        self.description = description


incoming_book_data = {
    "title": "clean code",
    "author": "bob martin",
    "description": "a book about writing cleaner code",
}

book_schema = BookSchema(unknown=EXCLUDE)

book = book_schema.load(incoming_book_data)
book_obj = Book(**book)
print(book_obj.author)
