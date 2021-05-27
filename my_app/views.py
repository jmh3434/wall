from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.

def index(request):
    return render(request,"index.html")

def success(request):
    # user is logged in? 
    if "user_id" not in request.session:
        return redirect('/')

    context = {
        "facebook_posts": Facebook_Post.objects.all()
    }

    return render(request,"success.html",context)

def register(request):

    if request.method == "POST":
        # make validation 

        errors = User.objects.validate(request.POST)

        if errors:
            for error in errors.values():
                messages.error(request,error)
            return redirect('/')


        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        password = request.POST["password"]

        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  

        user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=pw_hash)

        request.session["user_id"] = user.id
        request.session["user_name"] = f"{user.first_name} {user.last_name}"

        return redirect('/success')


    return redirect('/')


def login(request):
    if request.method == "POST":
        ## [user 1  user 2]
        email = request.POST["email"]
        password = request.POST["password"]

        logged_user = User.objects.filter(email=email) 

        if logged_user:
            logged_user = logged_user[0]

            if bcrypt.checkpw(password.encode(), logged_user.password.encode()):
                request.session["user_id"] = logged_user.id
                request.session["user_name"] = f"{logged_user.first_name} {logged_user.last_name}"
                return redirect('/success')
            else:
                messages.error(request,"this password isn't correct")
                return redirect('/')

        else:
            messages.error(request,"this user doesn't exist")
            return redirect('/')


    return redirect('/')

def logout(request):

    request.session.flush()

    return redirect('/')

def create_post(request):

    message = request.POST["message"]

    poster = User.objects.get(id=request.session["user_id"])

    Facebook_Post.objects.create(message=message,poster=poster)


    return redirect('/success')