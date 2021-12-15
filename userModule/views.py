from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.views.generic import DetailView, UpdateView
from django.views.generic.edit import CreateView
from blogsNewsModule.models import Profile
from django.urls import reverse_lazy
from .forms import ProfileForm

# Create your views here.

class CreateProfilePageView(CreateView):
    """Create profile"""
    model = Profile
    template_name = 'create_user_profile.html'
    # fields = '__all__'
    form_class = ProfileForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ShowProfilePageView(DetailView):
    """Shows profile of a person"""
    model = Profile
    template_name = 'user_profile.html'

    def get_context_data(self,**kwargs):
        # users = Profile.objects.all()
        context = super(ShowProfilePageView, self).get_context_data(**kwargs)
        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
        context["page_user"] = page_user
        return context

class EditProfilePageView(UpdateView):
    """Updates the profile of a person"""
    model = Profile
    template_name = 'edit_profile_page.html'
    form_class = ProfileForm
    # success_url = reverse_lazy('news/home')


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
            return redirect('/') #change to blog
        else:
            messages.warning(request,'Whoops! These are invalid credentials.')
            return redirect('login')

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
                messages.warning(request,"This email id is already in use. Please sign in or reset your password.")
                return redirect('login')
            else:
                user =  User.objects.create_user(username=username, password=password,
                email=email_id, first_name=first_name, last_name=last_name)
                user.save()
                messages.success(request,"Hurray! You're all set. Please sign in now.")
                return redirect('login')
        else:
            messages.warning(request,"Oops! Passwords do not match. Please try again.")
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
                messages.success(request,"Hurray! You're all set. Please sign in now.")
                return redirect('login')    
            else:
                messages.warning(request,"Your email id doesn't exist in our records. Please try again.")
                return redirect('forgotPwd')
        else:
            messages.warning(request,"Oops! Passwords do not match. Please try again.")
            return redirect('forgotPwd')

    return render(request,'forgotPwd.html')


def EditProfileView(request):
    """Edit account"""
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email_id = request.POST['email_id']
        username = request.POST['email_id']
        password = request.POST['password']
        retypePassword = request.POST['retypePassword']

        if password == retypePassword:
            user = User.objects.filter(username=email_id).update(first_name=first_name, last_name=last_name)
            if user and password is not None:
                user = User.objects.get(username=username)
                user.set_password(password)
                user.save()
            
            user = auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request, user)
                messages.success(request,"Your details have been updated.")
            return redirect('edit_profile')
        else:
            messages.warning(request,"Oops! Passwords do not match. Please try again.")
            return redirect('edit_profile')

    return render(request,'edit_profile.html')


