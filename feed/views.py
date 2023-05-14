from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .forms import UserUpdateForm, ProfileUpdateForm, PostForm
from .models import Post, Profile, Comment
from django.utils import timezone
from django.urls import reverse
from .forms import CommentForm


# lista de todos os posts
@login_required(login_url='feed/login')
def post_list(request):
    posts = Post.objects.order_by('-created_at')
    users = Profile.objects.all()
    return render(request, 'post_detail.html', {'posts': posts, 'users': users, 'current_user': request.user})


# apagar um user
@login_required(login_url='feed/login')
def delete_user(request, user_id):
    if request.user.is_superuser:
        user = User.objects.get(id=user_id)
        user.delete()
    return redirect('feed:post_detail')


# apagar um post
@login_required
def delete_post(request, post_id):
    if request.user.is_superuser:
        post = get_object_or_404(Post, id=post_id)
        post.delete()
    return redirect('feed:post_detail')


# apagar um comentário
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Check if the user is a superuser or the owner of the comment
    if request.user.is_superuser or request.user == comment.user:
        comment.delete()

    return redirect('feed:post_comments', post_id=comment.post.id)


# lista de posts de um utilizador
@login_required(login_url='feed/login')
def profile(request, username):
    user_profile = get_object_or_404(Profile, user__username=username)
    post = Post.objects.filter(user=user_profile.user).order_by('-created_at')
    context = {'user': user_profile, 'posts': post}
    return render(request, 'user_profile.html', context)


# comentários de um post
@login_required(login_url='feed/login')
def post_comments(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.select_related('user__profile').order_by('-created_at')

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            comment = Comment(post=post, user=request.user, content=content)
            comment.save()

    return render(request, 'post_comments.html', {'post': post, 'comments': comments})


# adicionar um comentário
@login_required(login_url='feed/login')
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            comment = Comment(post=post, user=request.user, content=content)
            comment.save()

    return redirect('feed:post_comments', post_id=post.id)


# perfil de quem deu login
@login_required(login_url='feed/login')
def myProfile(request):
    user = request.user
    posts = Post.objects.filter(user=user).order_by('-created_at')
    return render(request, 'selfProfile.html', {'user': user, 'posts': posts})


# editar o profile
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


# criar um post
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
            return HttpResponseRedirect(reverse('feed:login'))
        else:
            return HttpResponseRedirect(reverse('feed:criarUser'))
    else:
        return render(request, 'criarProfile.html')


#login view
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
                return HttpResponseRedirect(reverse('feed:login'))
    else:
        return render(request, 'login.html')


#logout
@login_required(login_url='feed/login')
def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('feed:login'))
