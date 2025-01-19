import requests, time

from bs4 import BeautifulSoup
from os.path import abspath
from typing import Callable

class Book:
    def __init__(self, title: str, authors: list[str], publisher: str, year: str, language: str, size: str, extension: str, links: list[str]) -> None:
        self.title = title
        self.authors = authors
        self.publisher = publisher
        self.year = year
        self.language = language
        self.size = size
        self.extension = extension
        self.links = links

    def download(self, path: str, callback: Callable[[str, float], any]):
        mirrorLink = self.links[0]
        req = requests.get(mirrorLink)
        reqTxt = req.text

        htmlSoup = BeautifulSoup(reqTxt, 'html.parser')
        targetDiv = htmlSoup.find('div', {'id': 'download'})
        targetH2 = targetDiv.find('h2')

        downloadLink = targetH2.find('a').get('href')

        startTime = time.time()

        with requests.get(downloadLink, stream = True) as bookDataStream:

            with open(path, 'wb') as outputFile:

                for chunk in bookDataStream.iter_content(chunk_size = 1024): 
                    outputFile.write(chunk)

            outputFile.close()

        if (callback):
            callback(abspath(path), (time.time() - startTime))
        

    def __str__(self) -> str:
        return f'{self.title}, Published By {self.publisher}, Year {self.year}'
    
    def __repr__(self) -> str:
        return self.__str__()
        
        
class SearchResult:
    query: str
    books: list[Book]
    page: int = 1

    def __init__(self, query: str, books: list[Book]) -> None:
        self.query = query
        self.books = books

class Libgen:
    def __init__(self) -> None:
        self.baseUrl = 'https://libgen.is'
        self.searchUrl = f'{self.baseUrl}/search.php'

    def getBookId(self, bookData) -> int:
        return int(bookData[0].get_text())
    
    def getBookAuthors(self, bookData) -> list[str]:
        bookAuthorsData = bookData[1]
        authors = []

        for authorData in bookAuthorsData.find_all('a'):
            authorName = authorData.get_text().strip()

            if (authorName == ''):
                continue

            authors.append(authorName)

        return authors
    
    def getBookTitle(self, bookData) -> str:
        bookTitleData = bookData[2]
        return bookTitleData.find('a').get_text().strip()
    
    def getBookPublisher(self, bookData) -> str:
        bookPublisher = bookData[3].get_text()
        return bookPublisher if (bookPublisher != '') else 'Unknown'
    
    def getBookYear(self, bookData) -> str:
        bookYear = bookData[4].get_text()
        return bookYear if (bookYear != '') else 'Unknown'

    def getBookLanguage(self, bookData) -> str:
        return bookData[6].get_text()
    
    def getBookSize(self, bookData) -> str:
        return bookData[7].get_text()
    
    def getBookFormat(self, bookData) -> str:
        return bookData[8].get_text()
    
    def getBookLinks(self, bookData) -> list[str]:
        firstMirrorData = bookData[9]
        secondMirrorData = bookData[10]

        return [firstMirrorData.find('a').get('href'), secondMirrorData.find('a').get('href')]


    def search(self, query: str, page: int = 1) -> SearchResult:
        params = {
            'req': query,
            'view': 'simple',
            'phrase': 1,
            'sort': 'def',
            'sortmode': 'ASC',
            'column': 'def',
            'page': page
        }
        req = requests.get(self.searchUrl, params = params)
        reqTxt = req.text

        htmlSoup = BeautifulSoup(reqTxt, 'html.parser')
        books = []

        for book in htmlSoup.find_all('tr', {'valign': 'top'})[1:]:

            bookData = book.find_all('td')

            bookId = self.getBookId(bookData)
            bookTitle = self.getBookTitle(bookData)
            bookAuthors = self.getBookAuthors(bookData)
            bookLanguage = self.getBookLanguage(bookData)
            bookSize = self.getBookSize(bookData)
            bookFormat = self.getBookFormat(bookData)
            bookYear = self.getBookYear(bookData)
            bookPublisher = self.getBookPublisher(bookData)
            bookLinks = self.getBookLinks(bookData)
            
            book = Book(
                bookTitle,
                bookAuthors,
                bookPublisher,
                bookYear,
                bookLanguage,
                bookSize,
                bookFormat,
                bookLinks
            )

            books.append(book)
        
        return SearchResult(query, books)
