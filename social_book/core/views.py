import email
from itertools import chain
from random import random
from django.shortcuts import render ,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Profile,Post,LikePost,FollowUser
import random
# Create your views here.

@login_required(login_url='signin')
def index(request):
    user_profile = Profile.objects.get(user = request.user)
    posts = Post.objects.all()

    user_following_list = []
    feed = []
    user_following = FollowUser.objects.filter(follower = request.user.username)
    for users in user_following:
        user_following_list.append(users.user)
    
    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))


    # user suggestion
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username = user.user)
        user_following_all.append(user_list)

    new_suggestions_list = [x for x in list(all_users) if x not in list(user_following_all)]
    current_user = User.objects.filter(username = request.user.username)
    final_list = [x for x in list(new_suggestions_list) if (x not in list(current_user))]
    random.shuffle(final_list)

    username_profile_list = []
    username_profile = []
    
    for user in final_list:
        username_profile.append(user.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user = ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))


    return render(request,"index.html",{'user_profile':user_profile,'posts':feed_list,'suggestions_username_profile_list':suggestions_username_profile_list[:4]})


def search(request):

    user_profile = Profile.objects.get(user = request.user)
    if request.method =='POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)
        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user = ids)
            username_profile_list.append(profile_lists)

        
        username_profile_list = list(chain(*username_profile_list))
        print(username_profile_list)

    return render(request,'search.html',{'user_profile':user_profile,'username_profile_list':username_profile_list})

@login_required(login_url='signin')
def follow(request):
    if request.method =='POST':
        follower = request.user.username
        user = request.POST['user']
        follow_object = FollowUser.objects.filter(user=user,follower=follower).first()
        if follow_object == None:
            follow_object = FollowUser.objects.create(user=user,follower=follower)
            follow_object.save()
            # return HttpResponse('hi')
            return redirect('/profile/'+user)
        else:
            follow_object.delete()
            # return HttpResponse('bye')
            return redirect('/profile/'+user)
    else:
        return redirect('index')
    # return HttpResponse("hi")

@login_required(login_url='signin')
def profile(request,pk):
    user = User.objects.get(username = pk)
    user_profile = Profile.objects.get(user=user)
    user_post = Post.objects.filter(user=pk)
    user_post_len = len(user_post)

    if FollowUser.objects.filter(follower = request.user.username , user = pk).first():
        button_text = "Unfollow"
    else:
        button_text = "Follow"

    follower_count = len(FollowUser.objects.filter(user = user))
    following_count = len(FollowUser.objects.filter(follower=user))

    context = {
        'user_profile':user_profile,
        'user_post':user_post,
        'user_post_len':user_post_len,
        'button_text' : button_text,
        'follower_count':follower_count,
        'following_count':following_count
    }
    return render(request , 'profile.html',context)

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(username=username,post_id=post_id).first()
    if like_filter == None:
        like = LikePost.objects.create(username=username,post_id = post_id)
        like.save()
        post.num_of_likes = post.num_of_likes+1
        post.save()
    else:
        like_filter.delete()
        post.num_of_likes = post.num_of_likes-1
        post.save()

    return redirect('index')

@login_required(login_url='signin')
def upload(request):

    if request.method == 'POST':
        caption = request.POST['caption']
        image = request.FILES.get('post_image')
        user = request.user.username
        new_post = Post.objects.create(user=user,caption=caption,image=image )
        new_post.save()
        return redirect('index')
    else:
        return redirect('index')


@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        if request.FILES.get('image') is None:
            image = user_profile.profileimg
        else :
            image = request.FILES.get('image')
        
        bio = request.POST['bio']
        location = request.POST['location']

        user_profile.profileimg = image
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()
        return redirect('settings')

    else:
        return render(request,"setting.html",{'user_profile':user_profile})






def signup(request):


    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request , "Email already exists")
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request , "Username taken")
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username,email=email,password = password1)
                user.save()

                user_login = authenticate(username = username , password = password1)
                login(request,user_login)

                user_model = User.objects.get(username = username)
                user_profile = Profile.objects.create(user = user_model,id_user = user_model.id)
                user_profile.save()
                return redirect('settings')

        else:
            messages.info(request , 'Passwords not matching')
            return redirect('signup')
    else:
        return render(request,"signup.html")


def signin(request):

    if request.method == 'POST':
        user = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = user , password = password)

        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            messages.info(request,"Credentials Invalid")
            return redirect('signin')
    else:
        return render(request,"signin.html")

@login_required(login_url='signin')
def logout_user(request):
    logout(request)
    return redirect('signin')
    