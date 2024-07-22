import requests
import pytest

BASE_URL = "http://localhost:5001/books"

# Test data
books = [
    {"title": "Adventures of Huckleberry Finn", "ISBN": "9780520343641", "genre": "Fiction"},
    {"title": "The Best of Isaac Asimov", "ISBN": "9780385050784", "genre": "Science Fiction"},
    {"title": "Fear No Evil", "ISBN": "9780394558783", "genre": "Biography"},
    {"title": "No such book", "ISBN": "0000001111111", "genre": "Biography"},
    {"title": "The Greatest Joke Book Ever", "authors": "Mel Greene", "ISBN": "9780380798490", "genre": "Jokes"}
]

# Helper function to add books
def add_book(book):
    response = requests.post(BASE_URL, json=book)
    return response

# Test cases
def test_post_books():
    ids = set()
    for i in range(3):
        response = add_book(books[i])
        assert response.status_code == 201
        book_id = response.json()["ID"]
        assert book_id not in ids
        ids.add(book_id)

def test_get_book_by_id():
    # Add book and get ID
    response = add_book(books[0])
    book_id = response.json()["ID"]

    # Get book by ID
    response = requests.get(f"{BASE_URL}/{book_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["authors"] == "Mark Twain"

def test_get_all_books():
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3

def test_post_invalid_isbn():
    response = add_book(books[3])
    assert response.status_code in [400, 500]

def test_delete_book():
    # Add book and get ID
    response = add_book(books[1])
    book_id = response.json()["ID"]

    # Delete book by ID
    response = requests.delete(f"{BASE_URL}/{book_id}")
    assert response.status_code == 200

def test_get_deleted_book():
    # Add book and get ID
    response = add_book(books[1])
    book_id = response.json()["ID"]

    # Delete book
    requests.delete(f"{BASE_URL}/{book_id}")

    # Get deleted book by ID
    response = requests.get(f"{BASE_URL}/{book_id}")
    assert response.status_code == 404

def test_post_invalid_genre():
    response = add_book(books[4])
    assert response.status_code == 422

if __name__ == "__main__":
    pytest.main(["-v", "assn3_tests.py"])
