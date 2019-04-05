from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .forms import LoginForm, UserRegisterForm, UserEditForm, \
    ProfileEditForm, OtherProfileEditForm, FullnameForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from .models import Contact
from actions.utils import create_action
from actions.models import Action
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from images.models import Image
from images.forms import CommentForm
from images.views import image_detail

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None and user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse('Invalid login')
    elif request.user.is_authenticated:
        return HttpResponseRedirect('/')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        fullname_form = FullnameForm(request.POST)
        if user_form.is_valid() and fullname_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            profile = Profile.objects.create(user=new_user, full_name=fullname_form.cleaned_data['full_name'])
            contact = Contact.objects.create(user_from=new_user, user_to=new_user)
            return render_to_response('account/register_done.html', locals())
        else:
            messages.error(request, '用戶名稱已使用')
            return HttpResponseRedirect(request.path)
    elif request.user.is_authenticated:
        return HttpResponseRedirect('/')
    else:
        user_form = UserRegisterForm()
        fullname_form = FullnameForm()
    return render(request, 'account/register.html', {'user_form': user_form,
                                                     'fullname_form': fullname_form})
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login')


def user_detail(request, username):
    images = Image.objects.all()
    paginator = Paginator(images, 15)
    page = request.GET.get('page')
    users = User.objects.filter(is_active=True)
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # If the request is AJAX and the page is out of range return an empty page
            return HttpResponse('')
        # If page is out of range deliver last page of results
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,
                      'images/image/list_ajax.html',
                      {'section': 'images', 'images': images})
    if request.method == 'POST':
        user = get_object_or_404(User,
                                 username=username,
                                 is_active=True)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if profile_form.is_valid():
            profile_form.save()
            if request.user.profile.photo:
                request.user.profile.photo = request.user.profile.photo
            else:
                Profile.objects.filter(user=request.user).update(photo='https://raw.githubusercontent.com/v8661087/v8661087.github.io/master/media/users/default.jpg')
            messages.success(request, '已變更大頭貼照')
        else:
            messages.error(request, 'Error updating your profile')
        return HttpResponseRedirect(request.path)
    else:
        user = get_object_or_404(User,
                                username=username,
                                is_active=True)
        profile_form = ProfileEditForm()
    return render(request, 'account/user/detail.html', {'user': user,
                                            'profile_form': profile_form,
                                                        'users': users})

@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request,
                  'account/user/list.html',
                  {'users': users})

def index(request):
    actions = Action.objects.all()
    paginator = Paginator(actions, 15)
    page = request.GET.get('page')


    try:
        actions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        actions = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # If the request is AJAX and the page is out of range return an empty page
            return HttpResponse('')
        # If page is out of range deliver last page of results
        actions = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,
                      'actions/action/detail.html',
                      {'section': 'images', 'actions': actions})
    if request.user.is_authenticated:
        actions = Action.objects.all()
        following_ids = request.user.following.values_list('id', flat=True)
        users = User.objects.filter(is_active=True)
    #    post = get_object_or_404(Image, id=, slug=)
     #   comments = post.comments
     #   new_comment = None

        if following_ids:
            # If user is following others, retrieve only their actions
            actions = actions.filter(user_id__in=following_ids).select_related('user',
                                            'user__profile').prefetch_related('target')

        actions = actions[:]
        return render(request, 'index.html', {'actions': actions,
                                              'following_ids': following_ids,
                                              'users':users})
    elif request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        fullname_form = FullnameForm(request.POST)
        if user_form.is_valid() and fullname_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            profile = Profile.objects.create(user=new_user, full_name=fullname_form.cleaned_data['full_name'])
            return render_to_response('account/register_done.html', locals())
    else:
        user_form = UserRegisterForm()
        fullname_form = FullnameForm()
    return render(request, 'mate.html', {'user_form': user_form,
                                         'fullname_form': fullname_form})

@login_required
def edit(request):

    if request.user.profile.photo:
        request.user.profile.photo = request.user.profile.photo
    else:
        Profile.objects.filter(user=request.user).update(photo='https://raw.githubusercontent.com/v8661087/v8661087.github.io/master/media/users/default.jpg')

    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        otherprofile_form = OtherProfileEditForm(instance=request.user.profile,
                                                 data=request.POST)
        if user_form.is_valid() and profile_form.is_valid() and otherprofile_form.is_valid():
            user_form.save()
            profile_form.save()
            otherprofile_form.save()
            if request.user.profile.photo:
                request.user.profile.photo = request.user.profile.photo
            else:
                Profile.objects.filter(user=request.user).update(photo='https://raw.githubusercontent.com/v8661087/v8661087.github.io/master/media/users/default.jpg')
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
        return HttpResponseRedirect(request.path)
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        otherprofile_form = OtherProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form,
                                                 'profile_form': profile_form,
                                                 'otherprofile_form': otherprofile_form})



@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == '追蹤':
                Contact.objects.get_or_create(
                    user_from=request.user,
                    user_to=user)

            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'ko'})
    return JsonResponse({'status': 'ko'})

@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return render_to_response('registration/password_change_done.html', locals())

    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/password_change.html', {'form': form})

@login_required
def password_change_done(request):
    return render_to_response('registration/password_change_done.html')
@login_required
def user_channel(request, username):
    if request.method == 'POST':
        user = get_object_or_404(User,
                                 username=username,
                                 is_active=True)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if profile_form.is_valid():
            profile_form.save()
            if request.user.profile.photo:
                request.user.profile.photo = request.user.profile.photo
            else:
                Profile.objects.filter(user=request.user).update(photo='https://raw.githubusercontent.com/v8661087/v8661087.github.io/master/media/users/default.jpg')
            messages.success(request, '已變更大頭貼照')
        else:
            messages.error(request, 'Error updating your profile')
        return HttpResponseRedirect(request.path)
    else:
        user = get_object_or_404(User,
                                username=username,
                                is_active=True)
        profile_form = ProfileEditForm()
    return render(request,'account/user/channel.html', {'user': user,
                                            'profile_form': profile_form})
@login_required
def user_saved(request, username):
    if request.method == 'POST':
        user = get_object_or_404(User,
                                 username=username,
                                 is_active=True)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if profile_form.is_valid():
            profile_form.save()
            if request.user.profile.photo:
                request.user.profile.photo = request.user.profile.photo
            else:
                Profile.objects.filter(user=request.user).update(photo='https://raw.githubusercontent.com/v8661087/v8661087.github.io/master/media/users/default.jpg')
            messages.success(request, '已變更大頭貼照')
        else:
            messages.error(request, 'Error updating your profile')
        return HttpResponseRedirect(request.path)
    else:
        user = get_object_or_404(User,
                                username=username,
                                is_active=True)
        profile_form = ProfileEditForm()
    return render(request,'account/user/saved.html', {'user': user,
                                            'profile_form': profile_form})
@login_required
def user_tagged(request, username):
    if request.method == 'POST':
        user = get_object_or_404(User,
                                 username=username,
                                 is_active=True)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if profile_form.is_valid():
            profile_form.save()
            if request.user.profile.photo:
                request.user.profile.photo = request.user.profile.photo
            else:
                Profile.objects.filter(user=request.user).update(photo='https://raw.githubusercontent.com/v8661087/v8661087.github.io/master/media/users/default.jpg')
            messages.success(request, '已變更大頭貼照')
        else:
            messages.error(request, 'Error updating your profile')
        return HttpResponseRedirect(request.path)
    else:
        user = get_object_or_404(User,
                                username=username,
                                is_active=True)
        profile_form = ProfileEditForm()
    return render(request, 'account/user/tagged.html', {'user': user,
                                            'profile_form': profile_form})
@login_required
def manage_access(request):
    return render(request, 'account/manage_access.html')

@login_required
def emails_settings(request):
    return render(request,'emails_settings.html')

@login_required
def contact_history(request):
    return render(request,'account/contact_history.html')

@login_required
def privacy_and_security(request):
    return render(request,'account/privacy_and_security.html')

@login_required
def explore_people_suggested(request):
    users = User.objects.filter(is_active=True)
    return render(request, 'explore_people_suggested.html', {'users': users})

