from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages

# Create your views here.
def HomePageView(request):
    """Login manager"""
    if request.method == 'POST':
        username = request.POST['email_id']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request, user)
            if user.is_superuser:
                return redirect('news/api/create')
            return redirect('news/home') #change to blog
        else:
            messages.info(request,'Whoops! These are invalid credentials.')
            return redirect('/')

    else:
        return render(request,'home.html')

def SignUpView(request):
    """Sign up manager"""
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email_id = request.POST['email_id']
        username = request.POST['email_id']
        password = request.POST['password']
        retypePassword = request.POST['retypePassword']

        if password == retypePassword:
            if User.objects.filter(username=username).exists():
                messages.info(request,"This email id is already in use. Please sign in or reset your password.")
                return redirect('/')
            else:
                user =  User.objects.create_user(username=username, password=password,
                email=email_id, first_name=first_name, last_name=last_name)
                user.save()
                messages.info(request,"Hurray! You're all set. Please sign in now.")
                return redirect('/')
        else:
            messages.info(request,"Oops! Passwords do not match. Please try again.")
            return redirect('register')

    return render(request,'register.html')

def ForgotPwdView(request):
    """Forgot password manager"""
    if request.method == "POST":
        username = request.POST['email_id']
        password = request.POST['password']
        retypePassword = request.POST['retypePassword']

        if password == retypePassword:
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
                user.set_password(password)
                user.save()  
                messages.info(request,"Hurray! You're all set. Please sign in now.")
                return redirect('/')    
            else:
                messages.info(request,"Your email id doesn't exist in our records. Please try again.")
                return redirect('forgotPwd')
        else:
            messages.info(request,"Oops! Passwords do not match. Please try again.")
            return redirect('forgotPwd')

    return render(request,'forgotPwd.html')


