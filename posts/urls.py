from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name="register"),
    path('homepage', views.homepage, name="homepage"),
    path('logout', views.logout, name="logout"),
    path('blogs', views.blogs, name="blogs"),
    path('<str:username>', views.profile, name="profile"),
    path('<str:username>/<str:id>', views.post, name="post"),
    path('post/edit/<str:pk>', login_required(views.UpdatePostView.as_view()), name="update_post"),
    path('post/delete/<str:pk>', login_required(views.DeletePostView.as_view()), name="delete_post")
]