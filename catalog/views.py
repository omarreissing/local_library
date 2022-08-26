from django.views import generic
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

from .models import Book, Author, BookInstance, Genre

# para controlar login requeridos
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# para controlar permisos requeridos
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import UserPassesTestMixin


#from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

import datetime

from .forms import RenewBookForm


# Create your views here.
#-----------------------------------------------------------------------------
# Vistas genericas basadas en clases: lista y detalle

class BookListView(PermissionRequiredMixin, generic.ListView):
    model = Book

    permission_required = ('catalog.can_mark_returned',)

    #queryset = Book.objects.filter(title__icontains='reino')
    context_object_name = 'book_list'

    #paginate_by = 10

    def get_queryset(self):
        return Book.objects.filter(title__icontains='el')[:5]

class BookDetailView(PermissionRequiredMixin, generic.DetailView):
    model = Book
    permission_required = ('catalog.add_book',)


#class AuthorListView(PermissionRequiredMixin, generic.ListView):

class AuthorListView( PermissionRequiredMixin, generic.ListView):
    model= Author
    permission_required = 'catalog.can_mark_returned'

class AuthorDetailView(generic.DetailView):
    model= Author



#@login_required
#@permission_required('catalog.can_mark_returned')
def index(request):
    # if  not request.user.email.endswith('@yahoo.com'):
    #     num_books = 0
    #     num_instances = 0
    #     num_instances_available = 0
    #     num_genre = 0
    #     num_authors = 0
    #
    # else:
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_genre = Genre.objects.all().count()
    num_authors = Author.objects.all().count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits']=num_visits + 1

    context = {
        'libros': num_books,
        'instancias': num_instances,
        'disponibles': num_instances_available,
        'autores': num_authors,
        'generos': num_genre,
        'num_visits':num_visits}

    return render(request, 'index.html', context=context,)



class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class LoanedBooksListView(PermissionRequiredMixin,generic.ListView):
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed.html'
    paginate_by = 10
    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    book_inst = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date},)

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst': book_inst})




#================================================================================================
# Vistas genericas de edicion para formularios
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author

class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '05/01/2018',}

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth']
    # fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

#================================================================================================

# Vistas genericas de edicion para formularios
#from django.views.generic.edit import CreateView, UpdateView, DeleteView
#from django.urls import reverse_lazy

from .models import Book

class BookCreate(CreateView):
    model = Book
    fields = '__all__'
    # initial={'date_of_death': '05/01/2018',}

class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = '__all__'
    # fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    permission_required = ('catalog.change_book',)

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')
#================================================================================================
