from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Filmwork:
    id: str = field(compare=False)
    title: str
    description: str
    creation_date: str
    file_path: str
    rating: float
    type: str
    created: datetime = field(compare=False)
    modified: datetime = field(compare=False)

    def __eq__(self, other):
        if other.__class__ is not self.__class__:
            return NotImplemented
        return (
            self.title,
            self.description,
            self.creation_date,
            self.file_path,
            self.rating,
            self.type,
        ) == (
            other.title,
            other.description,
            other.creation_date,
            other.file_path,
            other.rating,
            other.type,
        )


@dataclass
class Genre:
    id: str = field(compare=False)
    name: str
    description: str
    created: datetime = field(compare=False)
    modified: datetime = field(compare=False)

    def __eq__(self, other):
        if other.__class__ is not self.__class__:
            return NotImplemented
        return (
            self.name,
            self.description,
        ) == (
            other.name,
            other.description,
        )


@dataclass
class Person:
    id: str = field(compare=False)
    full_name: str
    created: datetime = field(compare=False)
    modified: datetime = field(compare=False)

    def __eq__(self, other):
        if other.__class__ is not self.__class__:
            return NotImplemented
        return (self.full_name,) == (other.full_name,)


@dataclass
class GenreFilmWork:
    id: str = field(compare=False)
    film_work_id: str = field(compare=False)
    genre_id: str = field(compare=False)
    created: datetime = field(compare=False)


@dataclass
class PersonFilmWork:
    id: str = field(compare=False)
    film_work_id: str = field(compare=False)
    person_id: str = field(compare=False)
    role: str
    created: datetime = field(compare=False)

    def __eq__(self, other):
        if other.__class__ is not self.__class__:
            return NotImplemented
        return (self.role) == (other.role)
