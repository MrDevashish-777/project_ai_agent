"""test_client_local.py
Runs FastAPI TestClient in-process without needing to run uvicorn; great for getting output quickly.
"""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def run_tests():
    print('Chat ->', client.post('/chat', json={'message': 'Hi', 'user_id': 'u100'}).json())
    print('Hotels ->', client.get('/hotels').json())
    print('Budget 2500 ->', client.post('/chat', json={'message': 'Budget 2500', 'user_id': 'u101'}).json())
    book = client.post('/book', json={'name':'Alice','phone':'+919999999999','hotel_id':'h2','checkin_date':'2025-12-12','nights':2})
    print('Book ->', book.json())

if __name__ == '__main__':
    run_tests()
