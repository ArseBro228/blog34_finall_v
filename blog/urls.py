from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("blog/post/<str:title>", views.post, name="post"),
    path("about", views.about, name="about"),
    path("contact", views.contact, name="contact"),
    path('category/<str:name>', views.category, name="category"),
    path('tags/<str:tag>', views.tag, name="tag"),
    path('comments/<str:comment>', views.comment, name="comment"),
    path("search", views.search, name="search"),
    path("create", views.create, name="create"),
    path("email", views.email, name="email"),
    path("comm", views.comm, name="comm"),
    path("blog/profile", views.profile, name="profile"),
    path("blog/update_profile", views.update_profile, name="update_profile"),
    path("blog/accept_update_profile", views.accept_update_profile, name="accept_update_profile"),
    path("blog/create_user", views.create_user, name="create_user"),
    path("blog/registration_user", views.registration_user, name="registration_user"),
    path("blog/login", LoginView.as_view(), name="blog_login"),
    path("blog/logout", LogoutView.as_view(), name="blog_logout"),
]
