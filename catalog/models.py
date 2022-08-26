from django.db import models
from django.urls import reverse
import uuid
from datetime import date

from django.contrib.auth.models import User


# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=50, help_text="Ingrese el nombre de un género.", verbose_name="Nombre")

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=50, help_text="Ingrese el nombre de un lenguaje.", verbose_name="Nombre")

    def __str__(self):
        return self.name

class Author(models.Model):

    first_name = models.CharField(max_length=100, verbose_name="Nombre")
    last_name = models.CharField(max_length=100, verbose_name="Apellido")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Nacimeinto")
    date_of_death= models.DateField( null=True, blank=True, verbose_name="Fallecimiento")

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def get_update_url(self):
        return reverse('author_update', args=[str(self.id)])

    def __str__(self):
        return '%s, %s' % (self.last_name, self.first_name)

    def display_books(self):
        #return ', '.join([book.title for book in self.All()[:3]])
        return '---'

    class Meta:
        ordering= ["first_name"]

class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titulo")
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True, verbose_name="Autor")
    summary = models.CharField(max_length=1000, help_text="Ingrese una breve descripcion del libro", verbose_name="Resumen")
    isbn = models.CharField('ISBN',max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Seleccione un genero")
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def get_update_url(self):
        return reverse('book_update', args=[str(self.id)])

    def display_genre(self):
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genero'


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), help_text="ID único para este libro")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    LOAN_STATUS = (
                    ('grupo1',(('m', 'Mantenimiento'),),),
                    ('grupo2',(('o', 'On loan'),),),
                    ('grupo3',(('a', 'Disponible'), ('r', 'Reservado'),),),
                   )
    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Disponibilidad del libro')
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"), )

    def __str__(self):
        return '%s (%s) ' % (self.id, self.book.title)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False
