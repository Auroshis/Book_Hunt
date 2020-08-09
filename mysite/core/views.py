from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy

from .forms import BookForm
from .models import Book

from .pdf import Process

class Home(TemplateView):
    template_name = 'home.html'


def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {
        'books': books
    })

def search(request):
    keyword = request.GET.get('Search', 'default')
    print('keyword', keyword)
    try:
        books = Book.objects.filter(search_data__contains=keyword)
        return render(request, 'book_list.html', {'books': books})
    except:
        return render(request, 'error.html')
    '''
    if keyword != '' or keyword.isalnum() == False:
        return redirect('home')
    else:
        try:
            books = Book.objects.filter(search_data__contains=keyword)
            return render(request, 'book_list.html', {'books': books})
        except:
            return render(request, 'error.html')'''

def upload_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                index_list = []
                index_numbers = form.cleaned_data.get("index_number")
                index_list = list(index_numbers.split(","))
                final_list = [int(index) for index in index_list]
                book_name = form.cleaned_data.get("pdf")
                form_instance = form.save()
                book_instance = Process()
                search_ip = book_instance.search_preprocess(final_list, book_name)
                print(form_instance.id)
                update_instance = Book.objects.get(id=form_instance.id)
                update_instance.search_data = search_ip
                update_instance.save()
                return redirect('book_list')
            except:
                form = BookForm()
                return render(request, 'upload_book.html', {'form': form})
    else:
        form = BookForm()
    return render(request, 'upload_book.html', {
        'form': form
    })


def howtoindex(request):
    return render(request, 'howtoindex.html')

def delete_book(request, pk):
    if request.method == 'POST':
        book = Book.objects.get(pk=pk)
        book.delete()
    return redirect('book_list')

'''
class BookListView(ListView):
    model = Book
    template_name = 'class_book_list.html'
    context_object_name = 'books'


class UploadBookView(CreateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy('class_book_list')
    template_name = 'upload_book.html'
'''