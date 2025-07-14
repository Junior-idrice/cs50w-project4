from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from.models import Posts
from django.http import JsonResponse
import json

from django.contrib.auth.decorators import login_required
from .models import User,Follow,Like
from django.core.paginator import Paginator

def index(request):
    #FOR THE POST & PAGINATION ISSUE
    posts = Posts.objects.all().order_by('id').reverse()
    pagi = Paginator(posts, 10)
    paginumber = request.GET.get('page')
    pagePosts = pagi.get_page(paginumber) 

    #FOR THE LIKES
    likes = Like.objects.all()
    liked = []
    try:
        for like in likes:
            if like.user.id == request.user.id:
                liked.append(like.post.id)
    except:
        liked=[]


    
    context = {
        "liked":liked,
        "posts":posts,
        "pagePosts":pagePosts
    }
   
    return render(request, "network/index.html", context)


#this is to add & remove a post
@login_required
def addlike(request, id_post):
    post = Posts.objects.get(pk=id_post)
    user = User.objects.get(pk=request.user.id)
    like = Like(user=user, post=post)
    like.save()
    return JsonResponse({
            "message":"added like successfully ",
            "likes":post.like_post.count()
            
        })

@login_required
def removelike(request, id_post):
    post = Posts.objects.get(pk=id_post)
    user = User.objects.get(pk=request.user.id)
    like = Like.objects.filter(user=user, post=post)
    like.delete()
    return JsonResponse({
            "message":"removed like successfully ",
            "likes":post.like_post.count()
            
        })




def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


#My code
#making new post

def post(request):
    if request.method == "POST":
        content = request.POST['content']
        user = User.objects.get(pk=request.user.id)
        post = Posts(content=content, user=user)
        post.save()
        return HttpResponseRedirect(reverse('index'))
    

def profile(request, user_id):
        user = User.objects.get(pk=user_id)
        Uposts = Posts.objects.filter(user=user).order_by('id').reverse()
        pagi = Paginator(Uposts, 10)
        paginumber = request.GET.get('page')
        pagePosts = pagi.get_page(paginumber) 

        #followers
        following = Follow.objects.filter(user=user)
        followers = Follow.objects.filter(user_follower=user)

        try:
            checkFollow = followers.filter(user=User.objects.get(pk=request.user.id))
            print(checkFollow)
            if len(checkFollow) != 0:
                isFollowing = True
            else:
                isFollowing = False
        except:
            isFollowing = False



        
        context = {
            "isFollowing":isFollowing,
            "user_profile":user,
            "following":following,
            "followers":followers,
            "name":user.username,
            "posts":Uposts,
            "pagePosts":pagePosts,
            
        }
    
        return render(request, "network/profile.html", context)

def follow(request):
    userFollow = request.POST['userFollow']
    UserP = User.objects.get(pk=request.user.id)
    userdata = User.objects.get(username=userFollow)
    per = Follow(user=UserP, user_follower = userdata)
    per.save()

    user_id = userdata.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id':user_id}))

def unfollow(request):
    userFollow = request.POST['userFollow']
    UserP = User.objects.get(pk=request.user.id)
    userdata = User.objects.get(username=userFollow)
    per = Follow.objects.get(user=UserP, user_follower = userdata)
    per.delete()

    user_id = userdata.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id':user_id}))


'''def following(request):
    currentUser = User.objects.get(pk=request.user.id)
    followers = Follow.objects.filter(user=currentUser)
    posts = Posts.objects.all().order_by('id').reverse()

    ffl = []

    for p in posts:
        for i in followers:
            ffl.append(p)
    
    pagi = Paginator(followers, 10)
    paginumber = request.GET.get('page')
    pagePosts = pagi.get_page(paginumber) 

    context = {
        "pagePosts":pagePosts
    }
   
    return render(request, "network/following.html", context)'''

@login_required
def following(request):
    current_user = request.user

    # Get the users this user is following
    following_users = Follow.objects.filter(user=current_user).values_list('user_follower', flat=True)

    # Get posts only from those users
    followed_posts = Posts.objects.filter(user__in=following_users).order_by('-id')

    # Paginate the posts
    paginator = Paginator(followed_posts, 10)
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "pagePosts": page_posts
    })


def edit(request,id_post):
    if request.method == "POST":
        value = json.loads(request.body)
        editPost = Posts.objects.get(pk=id_post)
        editPost.content = value["content"]
        editPost.save()
        return JsonResponse({
            "message":"changed",
            "value":value["content"]
        })
