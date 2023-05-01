from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .utils import get_post_and_liked_users
from .models import Post, Profile
from django.utils import timezone
from django.urls import reverse


# lista de todos os posts
@login_required(login_url='feed/login')
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'post_detail.html', {'posts': posts})


# lista de todos os users
@login_required(login_url='feed/login')
def users_list(request):
    users = Profile.objects.all()
    return render(request, 'lista_users.html', {'list': users})


# lista de posts de um utilizador
@login_required(login_url='login')
def profile(request, username):
    user_profile = get_object_or_404(Profile, user__username=username)
    post = Post.objects.filter(user=user_profile.user).order_by('-created_at')
    context = {'user': user_profile, 'posts': post}
    return render(request, 'user_profile.html', context)


# lista de likes de um post
def post_detail(request, post_id):
    post, liked_users = get_post_and_liked_users(post_id)
    context = {'post': post, 'liked_users': liked_users}
    return render(request, 'post_detail.html', context)


# user dá like num post
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.likes.add(request.user)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})




# adicionar um post
def criar_post(request):
    if request.method == 'POST':
        try:
            content = request.POST.get("image")
        except KeyError:
            return render(request, 'feed/criar_post.html')
        if content:
            post = Post(content=content, created_at=timezone.now())
            post.save()



def loginview(request):
    if request.method == 'POST':
        try:
            nome = request.POST.get('nome')
            password = request.POST.get('password')
        except KeyError:
            return render(request, 'login.html')

        if nome and password:
            user = authenticate(username=nome, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('feed:post_detail'))
            else:
                #pagina de criar conta
                return HttpResponseRedirect(reverse('feed:users_list'))
    else:
        return render(request, 'login.html')


@login_required(login_url='login')
def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))
