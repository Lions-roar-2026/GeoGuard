import pytest
from app import app

client = app.test_client()

def test_home_page_allowed():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}
    response = client.get('/', headers=headers)
    assert response.status_code == 200
    assert b"Home Page" in response.data

def test_block_gptbot():
    headers = {'User-Agent': 'GPTBot/2.1'}
    response = client.get('/welcome-in', headers=headers)
    assert response.status_code == 403
    assert b"Access Denied" in response.data

def test_block_case_insensitive():
    headers = {'User-Agent': 'gptbot'}
    response = client.get('/', headers=headers)
    assert response.status_code == 403

def test_allowed_human_user():
    headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0)'}
    response = client.get('/runners-world/', headers=headers)
    assert response.status_code == 200
    assert b"Welcome to runners-world" in response.data

def test_block_semrush():
    headers = {'User-Agent': 'SemrushBot/7.0'}
    response = client.get('/welcome-in', headers=headers)
    assert response.status_code == 403