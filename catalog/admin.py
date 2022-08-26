from django.contrib import admin
from .models import Genre, Book, Author, BookInstance, Language

# Register your models here.
admin.site.register(Genre)

#admin.site.register(Book)
#admin.site.register(Author)
#admin.site.register(BookInstance)

admin.site.register(Language)

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death', 'display_books')
    fields = ['first_name','last_name',('date_of_birth','date_of_death')]

class BooksInstanceInline(admin.TabularInline):
    model= BookInstance
    extra =  0

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')

    inlines = [BooksInstanceInline]


class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'status','borrower')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields':('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields':('status', 'due_back','borrower')
        }),
    )

admin.site.register(BookInstance,BookInstanceAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)

