from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, PostImage, Like
from .forms import PostForm
from django.http import JsonResponse

def post_list(request):
    posts = Post.objects.all().order_by("-created_at").prefetch_related("comments", "images", "likes")

    if request.user.is_authenticated:
        liked_post_ids = set(
            Like.objects.filter(user=request.user, post__in=posts).values_list("post_id", flat=True)
        )
    else:
        liked_post_ids = set()

    return render(request, "post_list.html", {
        "post_form": PostForm(),
        "posts": posts,
        "liked_post_ids": liked_post_ids,
    })

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().order_by("-created_at")

    return render(request, "post_detail.html", {
        "post": post,
        "comments": comments,
    })

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        text = request.POST.get("comment", "").strip()

        if text:
            comment = Comment.objects.create(
                post=post,
                user=request.user,
                text=text
            )

            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({
                    "username": comment.user.username,
                    "text": comment.text,
                    "avatar": comment.user.profile.profile.url if comment.user.profile.profile else "",
                })

    next_url = request.POST.get("next") or "post_list"
    return redirect(next_url)

@login_required
def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        images = request.FILES.getlist("images")

        if not form.is_valid():
            pass  
        elif not form.cleaned_data.get("caption") and not images:
            form.add_error(None, "Add a caption, an image, or both.")
        else:
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            for img in images:
                PostImage.objects.create(post=post, image=img)
            return redirect("post_list")
    else:
        form = PostForm()

    return render(request, "post_list.html", {
        "post_form": form,
        "posts": Post.objects.all().order_by("-created_at").prefetch_related("comments", "images"),
    })

@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({
        "liked": liked,
        "count": post.likes.count(),
    })