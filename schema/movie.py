from pydantic import BaseModel


class MovieBaseSchema(BaseModel):
    year: int
    title: str
    studios: str
    producers: str
    winner: bool

    class Config:
        orm_mode = True


class UpdateMovieSchema(MovieBaseSchema):
    year: str = ""
    title: str = ""
    studios: str = ""
    producers: str = ""
    winner: str = ""