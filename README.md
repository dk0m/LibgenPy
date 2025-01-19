## PyLibGen

A Synchronous Library For Interacting With Library Genesis.

## Example

```python
def onDownload(path: str, timeToDownload: float):
    print(f'Saved To {path}')
    print(f'Time To Download: {timeToDownload:.2f}s')

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

# Download the book and save it to 'CookingBook.pdf', Call 'onDownload' once it has finished downloading.
book.download('CookingBook.pdf', onDownload)
```
