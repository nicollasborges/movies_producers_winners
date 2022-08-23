from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.orm import sessionmaker
import pytest

from settings import Base, Engine
from main import app
from models.movie import load_movies, Movie
from models.winners import calculate_winner, Winners


client = TestClient(app)


def test_load_db():
    Base.metadata.drop_all(Engine)
    Base.metadata.create_all(Engine)
    load_movies('models/movielist.csv')
    calculate_winner()
    session = sessionmaker(bind=Engine)()
    assert session.query(Movie).count() > 0
    assert session.query(Winners).count() > 0


@pytest.mark.anyio
async def test_get_movie():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.get("/movie")
    assert response.status_code == 200


@pytest.mark.anyio
async def test_post_movie():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.post("/movie",  json={
            "title": "Friday the 13th",
            "producers": "Sean S. Cunningham",
            "studios": "Paramount Pictures",
            "year": 1000,
            "winner": True
        })
    assert response.status_code == 201


@pytest.mark.anyio
async def test_put_movie():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.put("/movie/1",  json={
            "title": "Friday the 13th",
            "producers": "Sean S. Cunningham",
            "studios": "Paramount Pictures",
            "year": 1000,
            "winner": True
        })
    assert response.status_code == 204


@pytest.mark.anyio
async def test_patch_movie():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.patch("/movie/1",  json={
            "title": "Friday the 13th"
        })
    assert response.status_code == 204


@pytest.mark.anyio
async def test_delete_movie():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.delete("/movie/1")
    assert response.status_code == 200


@pytest.mark.anyio
async def test_get_min_max():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.get("/min_max")
    assert response.status_code == 200
