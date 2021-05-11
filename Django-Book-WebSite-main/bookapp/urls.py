from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name = 'home'),
    path('all_books', views.all_books, name = 'all_books'),
    path('genre/<str:slug>', views.category_detail, name = 'category_detail'),
    path('pdf/<str:slug>', views.book_detail, name = 'book_detail'),
    path('searched_books', views.search_book, name = 'book_search'),
    path('register', views.registerView, name = 'register'),
    path('login', views.login_page, name = 'login'),
    path('reset', views.resetPassword, name = 'reset'),
    path('logout', views.logout_user, name = 'logout'),
    path('profile', views.profile_page, name = 'profile'),
    path('edit_profile', views.edit_profile, name = 'edit_profile'),
    path('', views.index, name = 'index')
]