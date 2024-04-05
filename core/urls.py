from django.contrib import admin
from django.urls import path
# from django.urls import path,include
from .import views
from .views import createpost,createpostpic

urlpatterns = [
    path('', views.home,name="home"),
    path('signup',views.signup,name="signup"),
    path('signin',views.signin,name="signin"),
    path('activate/<uid64>/<token>',views.activate,name="activate"),
    # path('signout',views.signout,name="signout"),
    path('getstart', views.getstart,name="getstart"),
    path('uploadtext', views.uploadtext, name='uploadtext'),
    path('uploadpic', views.uploadpic, name='uploadpic'),
    path('createpost',views.createpost,name='createpost'),
    path('createpostpic',views.createpostpic,name='createpostpic'),
    # path('getstart/user/<str:username>',UserPostListView.as_view(),name="user-posts"),
    # path('getstart/post/<int:pk>/',PostDetailView.as_view(),name="post-detail"),
    # # path('getstart/post/new/',PostCreateView.as_view(),name="post-create"),
    # path('getstart/post/<int:pk>/update/',PostUpdateView.as_view(),name="post-update"),
    # path('getstart/post/<int:pk>/delete/',PostDeleteView.as_view(),name="post-delete"),
    
]
