from .models import Post


# list of profiles that liked this post
def get_post_and_liked_users(post_id):
    post = Post.objects.get(id=post_id)
    liked_users = post.likes.all()
    return post, liked_users

