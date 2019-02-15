from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .forms import LoginForm, UserRegisterForm, UserEditForm, ProfileEditForm
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
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            return render_to_response('account/register_done.html', locals())
    elif request.user.is_authenticated:
        return HttpResponseRedirect('/')
    else:
        user_form = UserRegisterForm()
    return render(request, 'account/register.html', {'user_form': user_form})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login')


def user_detail(request, username):
    if request.method == 'POST':
        user = get_object_or_404(User,
                                 username=username,
                                 is_active=True)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if profile_form.is_valid():
           profile_form.save()
        #  messages.success(request, '已新增大頭貼照')
       # else:
          #  messages.error(request, 'Error updating your profile')
    else:
        user = get_object_or_404(User,
                                username=username,
                                is_active=True)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render_to_response('account/user/detail.html', locals())

@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request,
                  'account/user/list.html',
                  {'users': users})

def index(request):
    if request.user.is_authenticated:
        actions = Action.objects.all()
        following_ids = request.user.following.values_list('id', flat=True)
        if following_ids:
            # If user is following others, retrieve only their actions
            actions = actions.filter(user_id__in=following_ids).select_related('user',
                                            'user__profile').prefetch_related('target')
        actions = actions[:10]
        return render_to_response('index.html', locals())
    elif request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            profile = Profile.objects.create(user=new_user)

            return render_to_response('account/register_done.html', locals())
    else:
        user_form = UserRegisterForm()
    return render(request, 'mate.html', {'user_form': user_form})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form,
                                                 'profile_form': profile_form})



@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(
                    user_from=request.user,
                    user_to=user)

            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'ko'})
    return JsonResponse({'status': 'ko'})

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

def password_change_done(request):
    return render_to_response('registration/password_change_done.html')