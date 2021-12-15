from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from datetime import datetime
from django.urls.base import reverse
from newsapi import NewsApiClient
from django import forms
# from .models import Image
from django.views import generic
from .models import Post
from .forms import PostForm
from django.urls import reverse_lazy

import  smtplib
import os

from .serializers import PostSerializer
from rest_framework import generics, permissions

from dotenv import load_dotenv
load_dotenv()

# Create your views here.
def newsView(request):
    """Requests data from newsapi"""
    newsapi = NewsApiClient(api_key=os.getenv("API_KEY"))
    topheadlines = newsapi.get_top_headlines(sources='techcrunch')

    articles = topheadlines['articles']

    desc = []
    news = []
    img = []
    date = []
    redirectURL =[]
    def_string=""

    if request.method == "POST":
        search = request.POST["search"]
        for i in range(len(articles)):
            myarticles = articles[i]
            if search.lower() in myarticles['title'].lower():
                news.append(myarticles['title'])
                desc.append(myarticles['description'])
                img.append(myarticles['urlToImage'])
                redirectURL.append(myarticles['url'])
                date.append(datetime.strftime(datetime.strptime(myarticles['publishedAt'],"%Y-%m-%dT%H:%M:%SZ"),"%b %d, %Y"))
            
            
            
        if news==[]:
            def_string = "Oops! Looks like your search has hit a dead end."
            return render(request, 'index.html', context={"def_string":def_string})

        mylist = zip(news, desc, img, date, redirectURL)

        return render(request, 'index.html', context={"search":mylist})

    for i in range(len(articles)):
        myarticles = articles[i]

        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])
        redirectURL.append(myarticles['url'])
        date.append(datetime.strftime(datetime.strptime(myarticles['publishedAt'],"%Y-%m-%dT%H:%M:%SZ"),"%b %d, %Y"))

    mylist = zip(news, desc, img, date, redirectURL)


    return render(request, 'index.html', context={"mylist":mylist})

def aboutView(request):
    """Redirects to about.html page"""
    return render(request, 'about.html')

def subscribeView(request):
    """Sends an email to subscribed users"""
    if request.method == "POST":
        recepient = request.POST['emailId']
        
        SENDER_EMAIL = os.getenv('SENDER_EMAIL')
        SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')

        subject = "Blogs & News"
        body = os.getenv('BODY')
        message = 'Subject: {}\n\n{}'.format(subject, body)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, recepient, message)

    return render(request, 'newsletter.html')

def LikeView(request, pk):
    """Like a blog"""
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return redirect('single', post.pk)

class PostListView(generic.ListView):
    """Lists all the blogs"""
    model = Post
    template_name = 'myBlogs.html'

class PostDetailView(generic.DetailView):
    """Lists a blog"""
    model = Post
    template_name = 'single.html'

    def get_context_data(self,**kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        likes_cnt = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = likes_cnt.total_likes()

        liked = False
        if likes_cnt.likes.filter(id=self.request.user.id).exists():
            liked = True
        
        context["total_likes"] = total_likes
        context["liked"] = liked

        return context

class CreateBlogView(generic.CreateView):
    """Create a blogs"""
    model = Post
    template_name = 'create.html'
    #fields = '__all__'
    form_class = PostForm
    success_url = reverse_lazy('myBlogs')

class UpdateBlogView(generic.UpdateView):
    """Edit a blog"""
    model = Post
    template_name = 'edit.html'
    form_class = PostForm
    def get_success_url(self):
        return reverse('single', kwargs={'pk': self.kwargs['pk']})


class DeleteBlogView(generic.DeleteView):
    """Delete a blog"""
    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('myBlogs')

# section for APIs

class APICreateView(generics.ListCreateAPIView):
    """Sets permissions and creates blog through API"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,permissions.IsAdminUser)

class APIListView(generics.ListAPIView):
    """Sets permissions and lists all blogs through API"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,permissions.IsAdminUser)

class APIDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Sets permissions and lists a blog through API"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,permissions.IsAdminUser)
