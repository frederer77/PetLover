from django.urls import include, path
from . import views

# (. significa que importa views da mesma directoria)
app_name = 'feed'
urlpatterns = [
    path('feed/login', views.loginview, name='login'),

    path('', views.post_list, name="post_detail"),

    path('criarProfile', views.criarUser, name='criarUser'),

    path('logout', views.logoutview, name='logout'),

    path('profile/<str:username>/', views.profile, name='profile'),

    path('selfProfile', views.myProfile, name="myProfile"),

    path('edit_profile', views.edit_profile, name='edit_profile'),

    path('criar_post', views.criar_post, name="criar_post"),

    #opçoes de comentário
    path('post/<int:post_id>/', views.post_comments, name='post_comments'),

    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),

    #superuser delete staff
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),

    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),

    path('post/<int:comment_id>/delete', views.delete_comment, name='delete_comment')

]
