import requests

BASE_URL = "http://localhost:5001" 

books = [
    {
        "title": "Adventures of Huckleberry Finn",
        "ISBN": "9780520343641",
        "genre": "Fiction"
    },
    {
        "title": "The Best of Isaac Asimov",
        "ISBN": "9780385050784",
        "genre": "Science Fiction"
    },
    {
        "title": "Fear No Evil",
        "ISBN": "9780394558783",
        "genre": "Biography"
    },
    {
        "title": "No such book",
        "ISBN": "0000001111111",
        "genre": "Biography"
    },
    {
        "title": "The Greatest Joke Book Ever",
        "authors": "Mel Greene",
        "ISBN": "9780380798490",
        "genre": "Jokes"
    },
    {   
        "title":"The Adventures of Tom Sawyer",
        "ISBN":"9780195810400",
        "genre":"Fiction"
    },
    {   
        "title": "I, Robot",
        "ISBN":"9780553294385",
        "genre":"Science Fiction"
    },
    {   
        "title": "Second Foundation",
        "ISBN":"9780553293364",
        "genre":"Science Fiction"
    }
]

def test_post_books():
    ids = []
    for book in books[:3]:
        response = requests.post(f"{BASE_URL}/books", json=book)
        assert response.status_code == 201
        ids.append(response.json()["ID"])
    assert len(set(ids)) == 3

def test_get_book_by_id():
    response = requests.get(f"{BASE_URL}/books/1")
    assert response.status_code == 200
    data = response.json()
    assert data["authors"] == "Mark Twain"

def test_get_all_books():
    response = requests.get(f"{BASE_URL}/books")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3

def test_invalid_isbn():
    response = requests.post(f"{BASE_URL}/books", json=books[3])
    assert response.status_code in [400, 500]

def test_delete_book():
    response = requests.delete(f"{BASE_URL}/books/2")
    assert response.status_code == 200

def test_book_not_found():
    response = requests.get(f"{BASE_URL}/books/2")
    assert response.status_code == 404

def test_invalid_genre():
    response = requests.post(f"{BASE_URL}/books", json=books[4])
    assert response.status_code == 422
