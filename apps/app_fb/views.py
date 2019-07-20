from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from apps.helpers import copy_dict_partial, print_items_new_line
import bcrypt
import re


def index(request):
    return render(request, "app_fb/index.html")

def create_user(request):

    print(request.POST['dateofbirth'])

    if User.objects.registration_valid(request):
        hash_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

        new_user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = hash_pw, birthdate = request.POST['dateofbirth'])

        print(new_user)

        request.session['user_id']= new_user.id 
        request.session['logged_in'] = True


        context = {
            "id": new_user.id,
            "fn": new_user.first_name,
            "ln": new_user.last_name,
            "user": User.objects.get(id = request.session['user_id'])
        }

        return redirect('/books')

    return redirect('/')

def login(request):
    check_usr = User.objects.filter(email = request.POST['username'])

    if check_usr:
        usr = check_usr[0]
        
        if bcrypt.checkpw(request.POST['password'].encode(), usr.password.encode()):

            request.session['user_id']= usr.id 
            request.session['logged_in'] = True

            return redirect('/books')

        else:
            messages.error(request, "Bad credentials")  
    else:
        messages.error(request, "Bad credentials")
    return redirect('/')


def success(request):
    if not request.session.get('user_id'):
        messages.error(request, "Bruh register or login")
        return redirect("/")

    in_usr = User.objects.filter(id = request.session['user_id'])
    usr = in_usr[0]

    all_books = Book.objects.all()


    context = {
        "id": usr.id,
        "fn": usr.first_name,
        "ln": usr.last_name,
        "all_books": all_books,
        "user": User.objects.get(id = request.session['user_id'])
       
        }
    return render(request, "app_fb/success.html", context)     

def logout(request):
    request.session.clear()
    return redirect('/')

def add_book(request):
    usr = User.objects.get(id = request.session['user_id'])

    newbk = Book.objects.create(title = request.POST['book_title'], description = request.POST['desc'], uploaded_by = User.objects.get(id = request.session['user_id']))

    newbk.users_who_like.add(usr)

    return redirect('/books')

def fave_book(request, book_id):
    bk = Book.objects.get(id = book_id)
    usr = User.objects.get(id = request.session['user_id'])
    bk.users_who_like.add(usr)
    return redirect('/books')

def edit(request, book_id):
    new_user = User.objects.get(id = request.session['user_id'])
    bk = Book.objects.get(id = book_id)

    if(bk.uploaded_by.id == new_user.id):
        context = {
            "id": new_user.id,
            "fn": new_user.first_name,
            "ln": new_user.last_name,
            "bk": bk,
            "user": User.objects.get(id = request.session['user_id'])
        }
        return render(request, "app_fb/description-admin.html", context)

    context = {
            "id": new_user.id,
            "fn": new_user.first_name,
            "ln": new_user.last_name,
            "bk": bk,
            "user": User.objects.get(id = request.session['user_id'])
        }

    return render(request, "app_fb/description.html", context)

def delete(request, book_id):
    dbk = Book.objects.get(id = book_id)
    dbk.delete()
    return redirect('/books')


def update(request, book_id):
    ubk = Book.objects.get(id = book_id)
    ubk.title = request.POST['book_title']
    ubk.description = request.POST['desc']
    ubk.save()
    return redirect('/books')