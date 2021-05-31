from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from .models import Book, Category, Myrating
from django.contrib.auth.forms import UserCreationForm
from  .forms import CreateUserForm, EditUserProfileForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Case, When
import pandas as pd


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
    
    books = get_object_or_404(Book, slug= slug)
    #Rating a book
    books = Book.objects.filter(slug = slug).values('id')[0]
    if request.method == "POST":
        rate = request.POST['rating']
        if Myrating.objects.all().values().filter(books_id = books['id'], user = request.user):
            Myrating.objects.all().values().filter(books_id=books['id'], user=request.user).update(ratings = rate)
        else:
            ratingObject = Myrating()
            ratingObject.user = request.user
            ratingObject.books = book
            ratingObject.ratings = rate
            # ratingObject.date = DateTimeField
            ratingObject.save()

        return redirect('home')
        
    out = list(Myrating.objects.filter(user=request.user.id).values())
    book_rating = 0
    rate_flag = False
    # books = Book.objects.filter(slug = slug).values('id')[0]
    # print(books[0])
    for each in out:
        print(each)
        print(slug)
        if each['books_id'] == books['id']:
            book_rating = each['ratings']
            rate_flag = True
            break
        # messages.success(request, "Thanks for rating.")

        

    return render(request, 'book_detail.html', {'book': book, 'similar_books': similar_books, 'book_rating': book_rating, 'rate_flag' : rate_flag})

#Search
def search_book(request):
    searched_books = Book.objects.filter(title__icontains = request.POST.get('name_of_book'))
    return render(request, 'search_book.html', {'searched_books': searched_books})


# User registration
def registerView(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        special_characters = "!@#$%^&*()-+?_=,<>/"

        if password1 == password2:
            if User.objects.filter(username = username).exists():
                messages.error(request, "Username already exists. Please choose different username.")
                return redirect('register')
            elif User.objects.filter(email = email).exists():
                messages.error(request, "Please try another email, The given email is already registered.")
                return redirect('register')
            elif len(username) > 10:
                messages.error(request, "Username must be under 10 characters.")
                return redirect('register')
            elif not username.isalnum():
                messages.error(request, "Username should only contain letters and numbers.")
                return redirect('register')
            elif len(password1) <= 8:
                messages.error(request, "Password must contain more than 8 characters.")
                return redirect('register')
            elif not first_name.isalpha():
                messages.error(request, "Name must not contain numbers.")
                return redirect('register')
            elif not last_name.isalpha():
                messages.error(request, "Name must not contain numbers.")
                return redirect('register')
            else:
                user = User.objects.create_user(username = username, password = password1, email = email, first_name = first_name, last_name = last_name)
                user.save()
                print("User is created")
                messages.success(
                    request,
                    "Your account has been successfully created. Please login to continue.",
                )

        else:
            messages.error(request, 'Password not matching.')
            return redirect('register')
        return redirect('login')
     
    else:
        return render(request, "register.html", {'register': registerView})


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
@login_required(login_url='login')
def profile_page(request):
    if request.user.is_authenticated == False:
        return redirect('login')
    user = User.objects.all().get(id = request.user.id)
    print(f"Request user ID = {request.user.id}")

    return render(request, 'profile.html')

#Edit Profile
def edit_profile(request):
    if request.method == "POST":
        user = User.objects.get(id = request.user.id)
        name = request.POST.get('username')
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        user.username = name
        user.first_name = fname
        user.last_name = lname
        user.save()

        messages.success(request, ("Your name has been edited."))
        return redirect('profile')
    else:
        update_name = User.objects.get(id = request.user.id)
        return render(request, 'edit_profile.html', {'update_name' : update_name})

#Recommend starts here...

# To get similar movies based on User rating
def get_similar(book_name, rating, corrMatrix):
    similar_ratings = corrMatrix[book_name]*(rating-2.5)
    similar_ratings = similar_ratings.sort_values(ascending = False)
    return similar_ratings

# Recommendation Algorithm
def recommend(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.is_active:
        raise Http404
    
    book_rating = pd.DataFrame(list(Myrating.objects.all().values()))

    new_user = book_rating.user_id.unique().shape[0]
    current_user_id = request.user.id

    # if new user has not rated any movie 
    if current_user_id > new_user:
        book = Book.objects.get(id = 19)
        q = Myrating(user = request.user, books = book, ratings = 0)
        q.save()
    
    userRatings = book_rating.pivot_table(index = ['user_id'], columns = ['books_id'], values = 'ratings')
    userRatings = userRatings.fillna(0, axis = 1)
    corrMatrix = userRatings.corr(method = 'pearson')

    user = pd.DataFrame(list(Myrating.objects.filter(user = request.user).values())).drop(['user_id', 'id','date'], axis = 1)
    user_filtered = [tuple(x) for x in user.values]
    book_id_watched = [each[0] for each in user_filtered]

    similar_books = pd.DataFrame()
    print(user_filtered)
    for book, rating in user_filtered:
        similar_books = similar_books.append(get_similar(book, rating, corrMatrix), ignore_index = True)

    books_id = list(similar_books.sum().sort_values(ascending = False).index)
    books_id_recommend = [each for each in books_id if each not in book_id_watched]
    preserved = Case(*[When(pk = pk, then = pos) for pos, pk in enumerate(books_id_recommend)])
    book_list = list(Book.objects.filter(id__in = books_id_recommend).order_by(preserved)[:10])

    context = {'book_list' : book_list}
    return render(request, 'recommend.html', context)

    