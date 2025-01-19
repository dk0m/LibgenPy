from lib.libgen import Libgen

def onDownload(path: str, deltaTime: float):
    print(path, deltaTime)

libgen = Libgen()

res = libgen.search('cooking', page = 1)
book = res.books[0]

# Print the book's title
print(book.title)

# Print the book's authors
print(book.authors)

# Print the book's publisher
print(book.publisher)

# Print the book's publication year
print(book.year)

# Print the book's language
print(book.language)

# Print the book's size
print(book.size)

# Print the book's file extension
print(book.extension)

# Print the book's links
print(book.links)

# Downloads the book and saves it to 'CookingBook.pdf'
book.download('CookingBook.pdf', onDownload)
