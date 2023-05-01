from django.urls import include, path
from . import views
# (. significa que importa views da mesma directoria)
app_name = 'feed'
urlpatterns = [
    path('', views.post_list, name="post_detail"),

    path('feed/login', views.loginview, name='login'),

    path('criarProfile', views.criarUser, name='criarUser'),

    path('logout', views.logoutview, name='logout'),

    path('lista', views.users_list, name="users_list"),

    path('profile/<str:username>/', views.profile, name='profile'),

    path('like/<int:post_id>/', views.like_post, name='like_post'),

    path('selfProfile', views.myProfile, name="myProfile"),

    path('edit_profile', views.edit_profile, name='edit_profile'),

    path('criar_post', views.criar_post, name="criar_post")

    #path('profile/<str:username>/', views.user_posts, name='user_posts'),

]