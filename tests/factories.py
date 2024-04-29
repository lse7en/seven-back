import factory

from schemas import user_schemas
from src.core.security import get_password_hash
from src.models.movie import Movie
from src.models.movie_import import ImportStatus, MovieImport
from src.models.user import User


class UserCreateSchemaFactory(factory.Factory):
    username = factory.Faker("user_name")
    password = factory.Faker("password")

    class Meta:
        model = user_schemas.UserCreate


class UserModelFactory(factory.Factory):
    username = factory.Faker("user_name")
    password = factory.Faker("password")
    hashed_password = factory.LazyAttribute(lambda o: get_password_hash(o.password))

    class Meta:
        model = User
        exclude = ("password",)


class MovieModelFactory(factory.Factory):
    title = factory.Faker("sentence")
    year = factory.Faker("year")

    class Meta:
        model = Movie


class MovieImportCreateSchemaFactory(factory.Factory):
    title = factory.Faker("sentence")

    class Meta:
        model = movie_import_schema.MovieImportCreate


class MovieImportSchemaFactory(MovieImportCreateSchemaFactory):
    id = factory.Faker("random_int", min=1)
    status = factory.Faker("random_element", elements=[s for s in ImportStatus])

    class Meta:
        model = movie_import_schema.MovieImport


class MovieImportModelFactory(factory.Factory):
    title = factory.Faker("sentence")
    status = factory.Faker("random_element", elements=[s for s in ImportStatus])

    class Meta:
        model = MovieImport


class MovieOmdbFactory(factory.Factory):
    Title = factory.Faker("sentence")
    Year = factory.Faker("year")
    Rated = factory.Faker("word")
    Released = factory.Faker("date")
    Runtime = factory.Faker("time")
    Genre = factory.Faker("word")
    Director = factory.Faker("name")
    Writer = factory.Faker("name")
    Actors = factory.Faker("name")
    Plot = factory.Faker("sentence")
    Language = factory.Faker("name")
    Country = factory.Faker("country")
    Awards = factory.Faker("sentence")
    Poster = factory.Faker("url")
    Metascore = factory.Faker("sentence")
    imdbRating = factory.Faker("sentence")
    imdbVotes = factory.Faker("sentence")
    imdbID = factory.Faker("sentence")
    DVD = factory.Faker("date")
    BoxOffice = factory.Faker("sentence")
    Production = factory.Faker("sentence")
    Website = factory.Faker("url")

    class Meta:
        model = movie_schema.MovieOmdb
