from django.shortcuts import render, redirect
from .models import Book, Category, Myrating
from django.contrib.auth.forms import UserCreationForm
from  .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='login')
def home(request):
    recommended_books = Book.objects.filter(recommended_books = True)
    fiction_books = Book.objects.filter(fiction_books = True)
    business_books = Book.objects.filter(business_books = True)
    return render(request, 'home.html', {'recommended_books': recommended_books,
    'business_books': business_books, 'fiction_books': fiction_books
    })

def all_books(request):
    books = Book.objects.all()
    return render(request, 'all_books.html', {'books':books})

def category_detail(request, slug):
    category = Category.objects.get(slug = slug)
    return render(request, 'genre_detail.html', {'category': category})

@login_required(login_url='login')
def book_detail(request, slug):
    book = Book.objects.get(slug = slug)
    book_category = book.category.first()
    similar_books = Book.objects.filter(category__name__startswith = book_category)
    #Rating
    if request.method == "POST":
        rate = request.POST['rating']
        ratingObject = Myrating()
        ratingObject.user = request.user
        ratingObject.book = books
        ratingObject.rating = ratings
        ratingObject.save()
        messages.success(request, "Thanks for rating.")
        return redirect('home')
    return render(request, 'book_detail.html', {'book': book, 'similar_books': similar_books})

def search_book(request):
    searched_books = Book.objects.filter(title__icontains = request.POST.get('name_of_book'))
    return render(request, 'search_book.html', {'searched_books':searched_books})

# def register_page(request):
#     register_form = CreateUserForm()
#     if request.method == 'POST':
#         register_form = CreateUserForm(request.POST)
#         if register_form.is_valid():
#             register_form.save()
#             messages.info(request, "Account Created Successfully!")
#             return redirect('login')
           
#     return render(request, 'register.html', {'register_form': register_form})

def registerView(request):
     if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username = username).exists():
                messages.info(request, "Try other new USERNAME!!")
                return redirect('register')
            elif User.objects.filter(email = email).exists():
                messages.info(request, "Email is already taken... ")
                return redirect('register')
            else:    
                user = User.objects.create_user(username = username, password = password1, email = email)
                user.save()
                print("User is created")
        else:
            messages.info(request, "Password is not matching...")
            return redirect('register')
        return redirect('login')    
     else:
        return render(request, 'register.html', {'register': registerView})

def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        #Using user authentication
        user = auth.authenticate(username = username, password = password)
        
        #check user is created or not
        if user is not None:
            auth.login(request, user)
            return redirect("home")
        else:
            #messages will show error in html page when username or password is not correct
            messages.info(request, "System detected invalid username or password")
            return redirect('login')
    else:
        return render(request, 'login.html')    

def logout_user(request):
    logout(request)
    return redirect('index')

def index(request):
    return render(request, 'index.html', {})

def profile_page(request):
    return(request, 'profile.html', {})
    