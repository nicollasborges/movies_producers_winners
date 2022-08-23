from fastapi import FastAPI, Body, status
from sqlalchemy import desc, asc
from sqlalchemy.orm import sessionmaker
import uvicorn

from models.movie import load_movies, Movie
from models.winners import calculate_winner, Winners
from schema.movie import MovieBaseSchema, UpdateMovieSchema
from settings import Base, Engine


app = FastAPI()


def min_max_constructor(session, order) -> list:
    order_by = {
        'asc': asc,
        'desc': desc
    }.get(order)

    result = []
    interval = session.query(Winners).filter(Winners.followingWin >= 0).order_by(order_by(Winners.interval)).all()[0].interval
    for winner in session.query(Winners).filter(Winners.interval == interval).all():
        result.append({
            "producer": winner.producer,
            "interval": winner.interval,
            "previousWin": winner.previousWin,
            "followingWin": winner.followingWin
        })
    return result


@app.get("/min_max", status_code=status.HTTP_200_OK)
async def min_max():
    session = sessionmaker(bind=Engine)()
    result = {
        "min": min_max_constructor(session, 'asc'),
        "max": min_max_constructor(session, 'desc')
    }
    session.close()
    return result


@app.get("/movie", status_code=status.HTTP_200_OK)
async def movie():
    session = sessionmaker(bind=Engine)()
    result = session.query(Movie).all()
    session.close()
    return result


@app.post("/movie", status_code=status.HTTP_201_CREATED)
async def post_movie(movie_new: MovieBaseSchema):
    session = sessionmaker(bind=Engine)()
    movie = Movie(**movie_new.dict())
    session.add(movie)
    session.commit()
    calculate_winner()
    return ''


@app.put("/movie/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
async def put_movie(movie_id: int, movie: MovieBaseSchema):
    session = sessionmaker(bind=Engine)()
    session.query(Movie).filter(Movie.id == movie_id).update(movie.dict())
    session.commit()
    calculate_winner()
    return ''


@app.patch("/movie/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
async def patch_movie(movie_id: int, movie: UpdateMovieSchema):
    session = sessionmaker(bind=Engine)()
    fields_update = {}
    for field, value in movie.dict().items():
        if value != "":
            fields_update[field] = value
    session.query(Movie).filter(Movie.id == movie_id).update(fields_update)
    session.commit()
    calculate_winner()
    return ''


@app.delete("/movie/{movie_id}", status_code=status.HTTP_200_OK)
async def delete_movie(movie_id: int):
    session = sessionmaker(bind=Engine)()
    session.query(Movie).filter(Movie.id == movie_id).delete()
    session.commit()
    calculate_winner()
    return ''


if __name__ == "__main__":
    Base.metadata.drop_all(Engine)
    Base.metadata.create_all(Engine)
    load_movies('models/movielist.csv')
    calculate_winner()
    uvicorn.run(app, host="127.0.0.1", port=8000)
