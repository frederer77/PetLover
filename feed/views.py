from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from .forms import UserUpdateForm, ProfileUpdateForm, PostForm
from .utils import get_post_and_liked_users
from .models import Post, Profile
from django.utils import timezone
from django.urls import reverse


# lista de todos os posts
@login_required(login_url='feed/login')
def post_list(request):
    posts = Post.objects.order_by('-created_at')
    return render(request, 'post_detail.html', {'posts': posts})


# lista de todos os users
@login_required(login_url='feed/login')
def users_list(request):
    users = Profile.objects.all()
    return render(request, 'lista_users.html', {'list': users})


# lista de posts de um utilizador
@login_required(login_url='feed/login')
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


# perfil de quem deu login
@login_required(login_url='feed/login')
def myProfile(request):
    user = request.user
    posts = Post.objects.filter(user=user).order_by('-created_at')
    return render(request, 'selfProfile.html', {'user': user, 'posts': posts})


@login_required(login_url='feed/login')
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('feed:myProfile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)
    return render(request, 'edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})


# adicionar um post
@login_required(login_url='feed/login')
def criar_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.created_at = timezone.now()
            post.save()
            return redirect('feed:myProfile')
    else:
        form = PostForm()
    return render(request, 'criar_post.html', {'form': form})

# criar um user novo
def criarUser(request):
    if request.method == 'POST':
        try:
            fnome = request.POST.get('fnome')
            lnome = request.POST.get('lnome')
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
        except KeyError:
            return render(request, 'criarProfile.html')

        if fnome and lnome and username and email and password:
            user = User.objects.create_user(username, email, password)
            user.first_name = fnome
            user.last_name = lnome
            user.save()
            usuario = Profile.objects.create(user=user)
            usuario.save()
            return HttpResponseRedirect(reverse('feed:post_detail'))
        else:
            return HttpResponseRedirect(reverse('feed:criarUser'))
    else:
        return render(request, 'criarProfile.html')


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
                return HttpResponseRedirect(reverse('feed:criarUser'))
    else:
        return render(request, 'login.html')


@login_required(login_url='feed/login')
def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('feed:login'))
