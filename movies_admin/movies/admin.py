from django.contrib import admin
from .models import Genre, Filmwork, Person, GenreFilmwork, PersonFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "created", "modified")

    search_fields = ("name", "id")


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("full_name", "created", "modified")

    search_fields = ("full_name", "id")


@admin.register(GenreFilmwork)
class GenreFilmworkAdmin(admin.ModelAdmin):
    pass


@admin.register(PersonFilmwork)
class PersonFilmworkAdmin(admin.ModelAdmin):
    pass


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


class PersonFilmWorkInline(admin.TabularInline):
    model = PersonFilmwork


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmWorkInline)

    list_display = ("title", "type", "get_genres",
                    "creation_date", "rating",
                    "created", "modified")

    list_filter = ("type",)

    search_fields = ("title", "description", "id")

    @admin.display(description='genres',
                   ordering='-name',)
    def get_genres(self, obj):
        return ', '.join([genre.name for genre in obj.genres.all()])
