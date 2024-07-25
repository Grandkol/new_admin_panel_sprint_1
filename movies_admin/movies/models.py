import uuid
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"), blank=True)

    class Meta:
        db_table = 'content"."genre'
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_("full_name"), null=False)

    class Meta:
        db_table = 'content"."person'
        verbose_name = "Человек"
        verbose_name_plural = "Люди"

    def __str__(self):
        return self.full_name


class Filmwork(UUIDMixin, TimeStampedMixin):
    class Type(models.TextChoices):
        MOVIE = "movie", _("movie")
        TV_SHOW = "tv_show", _("tv_show")

    type = models.CharField(
        _("type"),
        choices=Type.choices,
        default=Type.MOVIE,
    )
    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"), blank=True)
    creation_date = models.DateField(_("creation_date"))
    file_path = models.FileField(_('file'), blank=True,
                                 null=True, upload_to='movies/')
    rating = models.FloatField(
        _("rating"),
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    genres = models.ManyToManyField(Genre, through="GenreFilmwork")
    persons = models.ManyToManyField(Person, through='PersonFilmwork')

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"

    def __str__(self):
        return self.title


class PersonFilmwork(UUIDMixin):
    film_work = models.ForeignKey("Filmwork",
                                  on_delete=models.CASCADE)
    person = models.ForeignKey("Person",
                               on_delete=models.CASCADE)
    role = models.TextField(_("role"))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."person_film_work'
        constraints = [models.UniqueConstraint(
            fields=['filmwork_id', 'person_id', 'role'],
            name='person_film_work_unique')]


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey("Filmwork",
                                  on_delete=models.CASCADE)
    genre = models.ForeignKey("Genre",
                              on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."genre_film_work'
        constraints = [models.UniqueConstraint(
            fields=['genre_id', 'film_work_id'],
            name='genre_film_work_unique')]
