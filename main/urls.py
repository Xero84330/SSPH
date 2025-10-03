from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from .views import create_superuser
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    # readers path
    path('', views.home, name='home'),
    path('home/browse/', views.browse, name='browse'),
    path('home/ranking/', views.ranking, name='ranking'),
    path('home/contest/', views.contest, name='contest'),
    path('home/about/', views.about, name='about'),
    path('home/login/', views.login_view, name='login'),
    path('home/signup/', views.signup_view, name='signup'),
    path('home/logout/', views.logout_view, name='logout'),
    path('create/rbook/<int:book_id>/',views.rbook, name='rbook'),
    path('create/rread/<int:book_id>/<int:chapter_id>/', login_required(views.rread, login_url='login'), name='rread'),
    path("create-superuser/", create_superuser),

    # authors path (login required)
    path('create/', login_required(views.create, login_url='login'), name='create'),
    path('create/statistics', login_required(views.statistics, login_url='login'), name='statistics'),
    path('create/payment', login_required(views.payment, login_url='login'), name='payment'),
    path('create/addbook', login_required(views.addbook, login_url='login'), name='addbook'),
    path('create/addchapter/<int:book_id>/', login_required(views.addchapter, login_url='login'), name='addchapter'),
    path('create/abookpage/<int:book_id>/', login_required(views.abookpage, login_url='login'), name='abookpage'),
    path("create/<int:pk>/delete_chapter/", login_required(views.delete_chapter, login_url='login'), name="delete_chapter"),
    path('create/<int:chapter_id>/edit/', login_required(views.edit_chapter, login_url='login'), name='edit_chapter'),
    path("create/<int:pk>/delete_book/", login_required(views.delete_book, login_url='login'), name="delete_book"),
]
