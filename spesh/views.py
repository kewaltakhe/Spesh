from django.http import HttpResponseRedirect
from django.shortcuts import render,get_object_or_404, redirect
from django.views.generic import TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.forms import CustomUserChangeForm
from .forms import PhotoUploadForm
from .models import PhotoModel, CustomUser
from .models import Follow
from django.http import JsonResponse

def index_page_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'index.html')

@login_required
def homepage_view(request):
    logged_user = request.user
    following_user_ids = Follow.objects.filter(follower=logged_user).values_list('following', flat=True)
    feedpage_photos = PhotoModel.objects.filter(user__in =  following_user_ids).order_by('-created_at')
    return render(request, 'homepage.html',{'feedpage_photos':feedpage_photos})

@login_required
def userprofile_view(request):
    login_user = request.user
    followers = Follow.objects.filter(following=login_user)
    followings = Follow.objects.filter(follower=login_user)
    user_photos = PhotoModel.objects.filter(user=login_user)

    photo_count = user_photos.count()
    return render(request,'logged_in_pages/user_profile.html',{'user_photos':user_photos,'photo_count':photo_count,
                                                               'followers':followers,'followings':followings
                                                               ,'followers_count':followers.count,'followings_count':followings.count})

@login_required
def editprofile_view(request):
    if request.method == 'POST':
        pass
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'logged_in_pages/edit_profile.html', {'form': form})

@login_required
def uploadphoto_view(request):
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            return redirect('profile')
            
    else:
        form = PhotoUploadForm()
    return render(request,'logged_in_pages/upload_photo.html',{'form':form})     

@login_required
def deletephoto_view(request,photo_id):
    photo = get_object_or_404(PhotoModel, id=photo_id)
    if request.method=='POST':
        # User has confirmed the deletion
        photo.delete()
        print('PHOTO DELETED -----------------------',photo.id,'   url:',photo.image.url)
        return redirect('profile')
    print('PHOTO NOT DELETED -----------------------')
    return redirect('profile')

@login_required
def othersprofile_view(request,user_id):
    user = CustomUser.objects.get(id=user_id)
    user_photos = PhotoModel.objects.filter(user=user)
    followers = Follow.objects.filter(following=user)
    followings = Follow.objects.filter(follower=user)
    user_photos = PhotoModel.objects.filter(user=user)
    photo_count = user_photos.count()
    followers_count = str(followers.count())
    followings_count = str(followings.count())
    try:
        follow_object = Follow.objects.get(follower=request.user, following=user)
        if follow_object !=None:
            already_followed = True
        else:
            already_followed = True
        print("\033[92m {}\033[00m" .format("Already Followed"))
    except Exception as msg:
        print("\033[92m {}\033[00m" .format(msg))
        already_followed = False
    return render(request,'logged_in_pages/others_profile.html',{'otheruser':user,'user_photos':user_photos,'photo_count':photo_count,
                                                                 'followers':followers,'followings':followings
                                                               ,'followers_count':followers_count,'followings_count':followings_count
                                                               ,'already_followed':already_followed})

@login_required
def usersearch_view(request):
    if request.method == 'GET':
        searchterm = request.GET.get('searchterm')
        logged_user = request.user
        if searchterm:
            results = CustomUser.objects.filter(username__icontains=searchterm)
        else:
            results = None

        return render(request,'logged_in_pages/search_results.html',{'results':results,'logged_user':logged_user})
    

@login_required
def followsomeone_view(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        following_user = CustomUser.objects.get(id=user_id)
        follower_user = request.user
        try:
            follow_object = Follow.objects.get(follower=follower_user, following=following_user)
            raise Exception('Already Followed')
        except:
            Follow.objects.create(follower=follower_user, following=following_user)
        followers_count = str(Follow.objects.filter(following=following_user).count())
        return JsonResponse({'message': 'User followed successfully.','followers_count':followers_count})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
    
@login_required
def unfollowsomeone_view(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        following_user = CustomUser.objects.get(id=user_id)
        follower_user = request.user
        try:
            follow_object = Follow.objects.get(follower=follower_user, following=following_user)
            follow_object.delete()
        except:
            return JsonResponse({'error': 'Invalid request method.'}, status=400)
        followers_count = str(Follow.objects.filter(following=following_user).count())
        return JsonResponse({'message': 'User unfollowed successfully.','followers_count':followers_count})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)