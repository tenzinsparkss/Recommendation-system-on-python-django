from django.shortcuts import render, redirect
from .models import Book, Category, Myrating
from django.contrib.auth.forms import UserCreationForm
from  .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


# Create your views here.
@login_required(login_url='login')
def home(request):
    recommended_books = Book.objects.filter(recommended_books = True)
    fiction_books = Book.objects.filter(fiction_books = True)
    business_books = Book.objects.filter(business_books = True)
    return render(request, 'home.html', {'recommended_books': recommended_books,
    'business_books': business_books, 'fiction_books': fiction_books
    })

#It shows all books from Book model
def all_books(request):
    books = Book.objects.all()
    return render(request, 'all_books.html', {'books':books})

#It has categorized into book details using Slug
def category_detail(request, slug):
    category = Category.objects.get(slug = slug)
    return render(request, 'genre_detail.html', {'category': category})

#It shows book details but login must be required to access this page.
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


# User registration
def registerView(request):
     if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username = username).exists():
                messages.info(request, "Try other new USERNAME!!")
                return redirect('register')
            elif User.objects.filter(email = email).exists():
                messages.info(request, "System has detected existing an email that you have entered.")
                return redirect('register')
            else:    
                user = User.objects.create_user(username = username, password = password1, email = email, first_name = first_name, last_name = last_name)
                user.save()
                print("User is created")
        else:
            messages.info(request, "System has detected unmatched passwords.")
            return redirect('register')
        return redirect('login')    
     else:
        return render(request, 'register.html', {'register': registerView})

#User login page
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
            messages.info(request, "System has detected invalid username or password")
            return redirect('login')
    else:
        return render(request, 'login.html')    

#Reset Password
def resetPassword(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username__exact = username)
            user.set_password(password)
            user.save()
            # msg='you have successfully reset your password.'
            messages.info(request, "You have successfully reset your Password.")
        except:
            # msg='Sorry, please try again!'
            messages.info(request, "Invalid USERNAME")

        # return JsonResponse({'msg':msg})
        
    return render(request,'reset_password.html')

#log out
def logout_user(request):
    logout(request)
    return redirect('index')

#Dashboard
def index(request):
    return render(request, 'index.html', {})

#User profile
def profile_page(request):
    return(request, 'profile.html', {})
    