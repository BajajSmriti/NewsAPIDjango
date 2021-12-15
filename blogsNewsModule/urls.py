from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.newsView, name="home"),
    path("createBlog", views.CreateBlogView.as_view(), name="createBlog"),
    path("myBlogs", views.PostListView.as_view(), name="myBlogs"),
    path("single/<int:pk>", views.PostDetailView.as_view(), name="single"),
    path("subscribe", views.subscribeView,name="subscribe"),
    path("about", views.aboutView, name="about"),
    path("edit/<int:pk>", views.UpdateBlogView.as_view(), name="edit"),
    path("delete/<int:pk>", views.DeleteBlogView.as_view(), name="delete"),
    path("like/<int:pk>", views.LikeView, name="like_post"),

    
    # API urls for superuser
    path("api/create/", views.APICreateView.as_view()),
    path("api/posts/", views.APIListView.as_view()),
    path("api/posts/<int:pk>", views.APIDetailView.as_view()),
    
]