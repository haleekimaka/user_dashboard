from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
import bcrypt
import time
import datetime

# Create your views here.

def index(request):
    if 'id' in request.session:
        return redirect("/show/user/" + request.session['id'])
    else:
        return render(request, "dash_app/index.html")

def signin(request):
    if 'id' in request.session:
        return redirect("/show/user/" + request.session['id'])
    else:
        return render(request, "dash_app/login.html")

def login(request):
    if 'id' in request.session:
        return redirect("/show/user/" + request.session['id'])
    else:
        check = User.objects.login_validation(request.POST)
        print check
        if check[0] == True:
            for tag, error in check[1].iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/signin')
        else:
            user_id = check[1]
            request.session['id'] = str(user_id)
            return redirect("/show/user/" + request.session['id'])

def register(request):
    if 'id' in request.session:
        return redirect("/show/user/" + request.session['id'])
    else:
        return render(request, "dash_app/register.html")

def registration(request):
    if request.method == "POST":
        if 'id' in request.session:
            return redirect('/show/user/' + request.session['id'])
        else:
            check = User.objects.registration_validation(request.POST)
            print check
            if check[0] == True:
                for tag, error in check[1].iteritems():
                    messages.error(request, error, extra_tags=tag)
                return redirect('/register')
            else:
                user_id = check[1]
                request.session['id'] = str(user_id)
                return redirect("/show/user/" + request.session['id'])
    else:
        messages.error(request, "Oops, something went wrong.")
        return redirect('/register')

def wall(request,user_id):
    if 'id' not in request.session:
        return redirect('/signin')

    else:
        errors= {}
        user_info = User.objects.get(id=user_id)
        try:
            message_query = Message.objects.filter(receiver=user_id).order_by("-created_at")
            comment_query = Comment.objects.all()
        except: 
            errors['msgs'] = 'No posts to display yet'

        if 'msgs' in errors or 'comments' in errors:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            context = {
                'user': user_info,
            }
            return render(request, "dash_app/wall.html", context)

        else:
            context = {
                'user': user_info,
                'msgs': message_query,
                'comments': comment_query
            }
            return render(request, "dash_app/wall.html", context)

def process_message(request,user_id):
    if 'id' not in request.session:
        return redirect('/signin')
    else:
        if request.method == 'POST':
            entry = Message.objects.message_validation(request.POST, user_id, request.session['id'])

            if entry[0] == True:
                for tag, error in check[1].iteritems():
                    messages.error(request, error, extra_tags=tag)
                    return redirect('/show/user/' + user_id)
            else:
                return redirect("/show/user/" + user_id)
        else:
            messages.error(request, "Oops, something went wrong.")
            return redirect('/show/user/' + user_id)

def process_comment(request, user_id):
    if 'id' not in request.session:
        return redirect('/signin')
    else:
        if request.method == 'POST':
            if request.POST['commentor'] != request.session['id']:
                messages.error(request, "Oops, something went wrong.")
                return redirect('/show/user/' + user_id)
            
            entry = Comment.objects.comment_validation(request.POST, request.session['id'])

            if entry[0] == True:
                for tag, error in check[1].iteritems():
                    messages.error(request, error, extra_tags=tag)
                    return redirect('/show/user/' + user_id)
            else:
                return redirect("/show/user/" + user_id)
        else:
            messages.error(request, "Oops, something went wrong.")
            return redirect('/show/user/' + user_id)

def delta_wall(request, user_id):
    if 'id' not in request.session:
        return redirect('/signin')

    return redirect("/show/user/" + user_id)

def showdash(request):
    if 'id' not in request.session:
        return redirect('/signin')

    admin_check = User.objects.is_admin(request.session['id'])
    if admin_check[0] == False:
        get_info = User.objects.all()
        context = {
            'users': get_info
        }
        return render(request, "dash_app/dashboard.html", context)
    else:
        return redirect('/dashboard/admin')

def admindash(request):
    if 'id' not in request.session:
        return redirect('/signin')
    
    admin_check = User.objects.is_admin(request.session['id'])

    if admin_check[0] == True:
        get_info = User.objects.all()
        context = {
            'users': get_info
        }
        return render(request, "dash_app/dashboard_admin.html", context)
    else:
        return redirect('/dashboard')

def edit(request):
    if 'id' not in request.session:
        return redirect('/signin')

    get_user = User.objects.get(id=request.session['id'])
    context = {
        'user': get_user
    }
    return render(request, "dash_app/edit.html", context)

def process_edit(request):
    if request.method == "POST":
        if 'id' not in request.session:
            return redirect('/signin')
        else:
            check = User.objects.update_validation(request.POST, request.session['id'])
            print check
            if check[0] == True:
                for tag, error in check[1].iteritems():
                    messages.error(request, error, extra_tags=tag)
                return redirect('/users/edit')
            else:
                messages.success(request, check[1])
                return redirect("/users/edit")
    else:
        messages.error(request, "Processing error. Invalid submission.")
        return redirect('/users/edit')

def remove(request, user_id):
    if 'id' not in request.session:
        return redirect('/signin')

    admin_check = User.objects.is_admin(request.session['id'])

    if admin_check[0] == False:
        messages.error(request, admin_check[1])
        return redirect('/dashboard')
    else:
        user_info = User.objects.get(id=user_id)
        context = {
            'user': user_info
        }
        return render(request, "dash_app/confirm.html", context)

    

def delete(request, user_id):
    if 'id' not in request.session:
        return redirect('/signin')

    admin_check = User.objects.is_admin(request.session['id'])

    if admin_check[0] == False:
        messages.error(request, admin_check[1])
        return redirect('/users/remove/'+ user_id)
    else:
        errors = {}

        delete_user = User.objects.delete_user(user_id)
        
        if delete_user[0] == False:
            errors["user"] = delete_user[1]
        if len(errors) > 0:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/users/remove/' + user_id)
        else:
            messages.success(request, "Successfully deleted entire user record")
            return redirect('/dashboard/admin')


def edit_admin(request,user_id):
    if 'id' not in request.session:
        return redirect('/signin')

    admin_check = User.objects.is_admin(request.session['id'])

    if admin_check[0] == False:
        messages.error(request, admin_check[1])
        return redirect('/signin')
    else:
        user_info = User.objects.get(id=user_id)
        context = {
            'user': user_info
        }
        return render(request, "dash_app/edit_admin.html", context)
    
def process_admin_edit(request, user_id):
    if request.method == "POST":
        if 'id' not in request.session:
            return redirect('/signin')
        else:
            admin_check = User.objects.is_admin(request.session['id'])
            if admin_check[0] == False:
                messages.error(request, admin_check[1])
                return redirect('/signin')
            else:
                check = User.objects.admin_update_validation(request.POST,user_id)
                if check[0] == True:
                    for tag, error in check[1].iteritems():
                        messages.error(request, error, extra_tags=tag)
                    return redirect('/users/edit/' + user_id)
                else:
                    messages.success(request, check[1])
                    return redirect('/users/edit/'+ user_id)
    else:
        messages.error(request, "Processing error. Invalid submission.")
        return redirect('/users/edit/' + user_id)


def new(request):
    if 'id' not in request.session:
        return redirect('/signin')

    admin_check = User.objects.is_admin(request.session['id'])
    
    if admin_check[0] == False:
        messages.error(request, admin_check[1])
        return redirect('/signin')
    else:
        return render(request, "dash_app/new.html")


def process_add(request):
    if request.method == "POST":
        if 'id' not in request.session:
            return redirect('/signin')

        admin_check = User.objects.is_admin(request.session['id'])
        
        if admin_check[0] == False:
            messages.error(request, admin_check[1])
            return redirect('/signin')
        
        else:
            check = User.objects.registration_validation(request.POST)
            print check
            if check[0] == True:
                for tag, error in check[1].iteritems():
                    messages.error(request, error, extra_tags=tag)
                return redirect('/users/new')
            else:
                success="Successfully added ID #" + str(check[1])
                messages.success(request, success)
                return redirect("/dashboard/admin")
    else:
        messages.error(request, "Oops, something went wrong.")
        return redirect('/users/new')


def logout(request):
    request.session.clear()
    return render(request, "dash_app/login.html")
