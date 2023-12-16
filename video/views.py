import json
import random
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from .models import Video, Channel, Video_Likes, Comment_Likes, Comment, History
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.paginator import Paginator

# index video
def index(request):
    try:
        videos = Video.objects.all()
        paginator = Paginator(videos, 10)  # Show 10 videos per page

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'videos/index.html', {'page_obj': page_obj, 'title': 'Inicio'})
    except Video.DoesNotExist:
        return render(request, 'videos/index.html', {'videos': [], 'title': 'Inicio', 'user_is_auth': request.user.is_authenticated})
    
def history(request):
    if not request.user.is_authenticated:
        return redirect('login')
    #get user history
    history = History.objects.filter(user_id=request.user.id)
    #get videos from history
    videos = []
    for item in history:
        videos.append(Video.objects.get(id=item.video_id))
    
    paginator = Paginator(videos, 10)  # Show 10 videos per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'videos/index.html', {'page_obj': page_obj, 'title': 'History', 'user_is_auth': request.user.is_authenticated})

#popular videos
def popular(request):
    #get videos with timestamp today
    today_videos = Video.objects.filter(timestamp__day=timezone.now().day)
    #add 100 points to videos
    for video in today_videos:
        video.popularity += 100
    
    #get videos with timestamp this month and except today
    month_videos = Video.objects.filter(timestamp__month=timezone.now().month).exclude(timestamp__day=timezone.now().day)
    if len(month_videos) == 0 and len(today_videos) == 0:
        random_videos = list(Video.objects.all())
        if len(random_videos) < 10:
            month_videos = random_videos
        else:
            month_videos = random.sample(random_videos, 5)
    #sort by popularity between videos and month_videos
    videos = sorted(list(today_videos) + list(month_videos), key=lambda x: x.popularity, reverse=True)
    
    paginator = Paginator(videos, 10)  # Show 10 videos per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'videos/index.html', {'page_obj': page_obj, 'title': 'Popular', 'user_is_auth': request.user.is_authenticated})

# create video
def create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        embed_url = request.POST.get('embed_url')
        description = request.POST.get('description')
        thumbnail = request.POST.get('embed_url').replace('https://www.youtube.com/embed/', 'https://img.youtube.com/vi/')
        #now split by ? and get the first element
        thumbnail = thumbnail.split('?')[0] + '/0.jpg'
        #get the channel by the id
        channel = Channel.objects.get(id=request.POST.get('channel'))
        video = Video(title=title, embed_url=embed_url, channel=channel, description=description, timestamp=timezone.now(), thumbnail=thumbnail, popularity=0)    
        video.save()
        return redirect('index')
    else:
        #get the user channels
        channels = Channel.objects.filter(owner_id=request.user.id)
        #check if user has channels
        if len(channels) == 0:
            return redirect('create_channel')
        else:
            return render(request, 'videos/create_video.html', {'channels': channels})

# show video by id        
def show(request, video_id):
    #add video to history
    if request.user.is_authenticated:
        history = History(user_id=request.user.id, video_id=video_id, timestamp=timezone.now())
        history.save()

    video = Video.objects.get(id=video_id)
    video.liked = False
    video.disliked = False
    
    # Query comments and their respective owner names
    comments = Comment.objects.filter(video_id=video_id)
    for comment in comments:
        comment.owner_name = User.objects.get(id=comment.author_id).username
    
    # Check if already liked or disliked the video
    try:
        like = Video_Likes.objects.get(video_id=video_id, user_id=request.user.id)
        if like.like == True:
            video.liked = True
        else:
            video.disliked = True
    except Video_Likes.DoesNotExist:
        pass
    
    # Count video likes and dislikes
    video.likes = Video_Likes.objects.filter(video_id=video_id, like=True).count()
    video.dislikes = Video_Likes.objects.filter(video_id=video_id, like=False).count()
    
    return render(request, 'videos/video_detail.html', {'video': video, 'comments': comments, 'user_is_auth': request.user.is_authenticated})

# like video by id
def like_video(request, video_id):
    video = Video.objects.get(id=video_id)
    # Check if user has liked the video before
    response_data = {}
    try:
        like = Video_Likes.objects.get(video_id=video_id, user_id=request.user.id)
        #if already liked, remove like
        if like.like == True:
            like.delete()
            response_data['message'] = 'removed like'
            response_data['liked'] = False
        else:
            like.like = True
            like.save()
            response_data['message'] = 'you liked the video'
            response_data['liked'] = True
    except Video_Likes.DoesNotExist:
        #if not liked, add like
        like = Video_Likes(video_id=video_id, user_id=request.user.id, like=True)
        like.save()
        response_data['message'] = 'you liked the video'
        response_data['liked'] = True

    
    response_data['likes'] = Video_Likes.objects.filter(video_id=video_id, like = True).count()
    response_data['dislikes'] = Video_Likes.objects.filter(video_id=video_id, like = False).count()
    #update video likes
    video.likes = response_data['likes']
    video.popularity = response_data['likes']*10 - response_data['dislikes']*5 + Comment.objects.filter(video_id=video_id).count()
    video.save()
    #return success in json format
    return JsonResponse(response_data)
        

# dislike video by id
def dislike_video(request, video_id):
    video = Video.objects.get(id=video_id)
    response_data = {}
    # Check if user has disliked the video before
    try:
        like = Video_Likes.objects.get(video_id=video_id, user_id=request.user.id)
        #if already disliked, remove dislike
        if like.like == False:
            like.delete()
            response_data['message'] = 'removed dislike'
            response_data['disliked'] = False
        #if already liked, remove like and add dislike
        else:
            like.like = False
            like.save()
            response_data['message'] = 'you disliked the video'
            response_data['disliked'] = True
    except Video_Likes.DoesNotExist:
        #if not disliked, add dislike
        like = Video_Likes(video_id=video_id, user_id=request.user.id, like=False)
        like.save()
        response_data['message'] = 'you disliked the video'
        response_data['disliked'] = True
    response_data['likes'] = Video_Likes.objects.filter(video_id=video_id, like = True).count()
    response_data['dislikes'] = Video_Likes.objects.filter(video_id=video_id, like = False).count()
    #update video dislikes
    video.dislikes = response_data['likes']
    video.popularity = response_data['likes']*10 - response_data['dislikes']*5 + Comment.objects.filter(video_id=video_id).count()
    video.save()
    return JsonResponse(response_data)

def add_comment(request, video_id):
    response_data = {}
    if request.method == 'POST':
        content = request.POST.get('content')
        video = Video.objects.get(id=video_id)
        comment = Comment(video=video, author_id=request.user.id, content=content, timestamp=timezone.now())
        comment.save()
        video.popularity = video.likes*10 - video.dislikes*5 + Comment.objects.filter(video_id=video_id).count()
        video.save()
        return redirect('show_video', video_id)
    else:
        return render(request, 'videos/video_detail.html', {'video': video, 'user_is_auth': request.user.is_authenticated})
    
def like_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment.likes += 1
    comment.save()
    # Check if user has liked the comment before
    try:
        like = Comment_Likes.objects.get(comment_id=comment_id, user_id=request.user.id)
        #if already liked, remove like
        if like.like == True:
            comment.likes -= 1
            comment.save()
            like.delete()
        #if already disliked, remove dislike and add like
        else:
            comment.dislikes -= 1
            comment.likes += 1
            comment.save()
            like.like = True
            like.save()
    except Comment_Likes.DoesNotExist:
        #if not liked, add like
        like = Comment_Likes(comment_id=comment_id, user_id=request.user.id, like=True)
        like.save()

    return redirect('show_video', comment.video.id)

def dislike_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment.dislikes += 1
    comment.save()
    # Check if user has disliked the comment before
    try:
        like = Comment_Likes.objects.get(comment_id=comment_id, user_id=request.user.id)
        #if already disliked, remove dislike
        if like.like == False:
            comment.dislikes -= 1
            comment.save()
            like.delete()
        #if already liked, remove like and add dislike
        else:
            comment.likes -= 1
            comment.dislikes += 1
            comment.save()
            like.like = False
            like.save()
    except Comment_Likes.DoesNotExist:
        #if not disliked, add dislike
        like = Comment_Likes(comment_id=comment_id, user_id=request.user.id, like=False)
        like.save()
    return redirect('show_video', comment.video.id)

# update view
def update(request, video_id):
    video = Video.objects.get(id=video_id)
    if request.method == 'POST':
        video.title = request.POST.get('title')
        video.embed_url = request.POST.get('embed_url')
        video.channel = request.POST.get('channel')
        video.save()
        return redirect('index')
    else:
        return render(request, 'videos/update_video.html', {'video': video, 'user_is_auth': request.user.is_authenticated})

# delete view
def delete(request, video_id):
    video = Video.objects.get(id=video_id)
    video.delete()
    return redirect('index')

# create channel
def create_channel(request):
    #check if user is logged in
    if request.user.is_authenticated:
        if request.method == 'POST':
            name = request.POST.get('name')
            owner = request.user.id
            channel = Channel(name=name, owner_id=owner, subscribers=0, timestamp=timezone.now())
            channel.save()
            return redirect('index')
        else:
            return render(request, 'channels/create_channel.html')
    else:
        return redirect('login')
    
# update channel
def update_channel(request, channel_id):
    channel = Channel.objects.get(id=channel_id)
    if request.method == 'POST':
        channel.name = request.POST.get('name')
        channel.save()
        return redirect('index')
    else:
        return render(request, 'channels/update_channel.html', {'channel': channel, 'user_is_auth': request.user.is_authenticated})
    
# delete channel
def delete_channel(request, channel_id):
    channel = Channel.objects.get(id=channel_id)
    channel.delete()
    return redirect('index')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    return LoginView.as_view(template_name='login.html')(request)


def logout(request):
    return LogoutView.as_view(template_name='logout.html')(request)