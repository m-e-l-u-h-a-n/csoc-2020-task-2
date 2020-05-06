from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from store.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,Http404,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import datetime
from decimal import Decimal
from django.views.decorators.cache import cache_control

# Create your views here.

def index(request):
    return render(request, 'store/index.html')
@cache_control(must_revalidate=True,no_store=True)
def bookDetailView(request, bid):
    template_name = 'store/book_detail.html'
    try:
        book = Book.objects.get(pk=bid)
    except:
        raise Http404('Book not found!')
    else: # to be checked for returning
        num_available = BookCopy.objects.filter(book__exact=book,
        status__exact=True).count()
        context = {
            'book': book, # set this to an instance of the required book
            'num_available': num_available, # set this to the number of copies of the book available, or 0 if the book isn't available
        }
        # START YOUR CODE HERE
        return render(request, template_name, context=context)


@csrf_exempt
def bookListView(request):
    template_name = 'store/book_list.html'
    get_data = request.GET
    books = Book.objects.filter(
        title__icontains = get_data.get('title',''),
        author__icontains = get_data.get('author',''),
        genre__icontains = get_data.get('genre',''),
    )
    context = {

        'books': books, # set this to the list of required books upon filtering using the GET parameters
                       # (i.e. the book search feature will also be implemented in this view)
    }

    # START YOUR CODE HERE
    
    
    return render(request, template_name, context=context)
#@cache_control(must_revalidate=True,no_store=True)
@login_required
def viewLoanedBooks(request):
    template_name = 'store/loaned_books.html'
    books = BookCopy.objects.filter(borrower__exact=request.user)
    context = {
        'books': books,
    }
    '''
    The above key 'books' in the context dictionary should contain a list of instances of the 
    BookCopy model. Only those book copies should be included which have been loaned by the user.
    '''
    # START YOUR CODE HERE
    
    return render(request, template_name, context=context)

@csrf_exempt
@login_required
def loanBookView(request):
    book_id = request.POST['bid'] # get the book id from post data
    try:
        book = Book.objects.get(pk=book_id)
    except:
        raise Http404('Book not available')
    else:
        books = BookCopy.objects.filter(book__exact=book,status__exact=True)

        if books:
            books[0].borrower = request.user
            books[0].borrow_date = datetime.date.today()
            books[0].status = False
            books[0].save()# to be reviewed
            message = 'success'
        else:
            message = 'failure'
        response_data = {
            'message': message,
        }
    '''
    Check if an instance of the asked book is available.
    If yes, then set the message to 'success', otherwise 'failure'
    '''
    # START YOUR CODE HERE
    return JsonResponse(response_data)

'''
FILL IN THE BELOW VIEW BY YOURSELF.
This view will return the issued book.
You need to accept the book id as argument from a post request.
You additionally need to complete the returnBook function in the loaned_books.html file
to make this feature complete
''' 
@csrf_exempt
@login_required
def returnBookView(request):
    if request.method == 'POST':
        book_id = request.POST['id']
        try:
            book = BookCopy.objects.get(pk=book_id)
        except:
            return JsonResponse({'message':'Book not found'})  

        else:
            book.status = True
            book.borrower = None
            book.borrow_date = None
            book.save()
            return JsonResponse({'message':'success'})
    else:
        return JsonResponse({'message':'Invalid request method'})
@csrf_exempt
@login_required
def rateBookView(request):
    if request.method == "POST":
        bid = request.POST['bid']
        new_rating = Decimal(request.POST['rating'])
        if new_rating >= 0 and new_rating <= 10:
            try:
                book = Book.objects.get(pk=bid)
                user = User.objects.get(username = request.user.username)
                previous_user_rating = BookRating.objects.filter(book = book, user = user)
                previous_user_rating.delete()
                obj = BookRating()
                obj.user = user
                obj.book = book
                obj.rate = new_rating
                obj.save()
                books = BookRating.objects.filter(book = book)
                total = 0
                for i in books:
                    total+=i.rate
                book.rating = total/books.count()
                book.save()
            except:
                return JsonResponse({'message':"error"})
            else:
                return JsonResponse({'message':'success'})
        else:
            return JsonResponse({'message':'Rating Value should lie in range 0-10'})

    else:
        return JsonResponse({'message':"invalid request method"})


