from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm, CommentForm
from .models import Image
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from actions.utils import create_action


@login_required
def image_create(request):
    """
    View for creating an Image using the JavaScript Bookmarklet.
    """
    if request.method == 'POST':
        # form is sent
        form = ImageCreateForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            # form data is valid
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            # assign current user to the item
            new_item.user = request.user
            new_item.save()
     #       messages.success(request, 'Image added successfully')
            create_action(request.user, 'added image', new_item)
            # redirect to new created item detail view
            return HttpResponseRedirect('/')
     #       return redirect(new_item.get_absolute_url())
        else:
            messages.error(request, 'Image added failed')
    else:
        # build form with data provided by the bookmarklet via GET
        form = ImageCreateForm()
    return render(request, 'images/image/create.html', {'form': form})

def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    post = get_object_or_404(Image, id=id, slug=slug)
    comments = post.comments.filter()
    new_comment = None

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            new_comment.user = request.user
            # Save the comment to the database
            new_comment.save()
            #messages.success(request, '留言成功')
            return HttpResponseRedirect(request.path)
        else:
            messages.error(request, '留言失敗')
            return HttpResponseRedirect(request.path)

    else:
        comment_form = CommentForm()
    return render(request, 'images/image/detail.html',
                  {'image': image,
                   'post': post, 'comments': comments, 'comment_form': comment_form})

@ajax_required
@login_required
@require_POST
def image_saved(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'saved':
                image.users_save.add(request.user)
            else:
                image.users_save.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ko'})

@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ko'})


@login_required
def image_list(request):
    users = User.objects.filter(is_active=True)
    images = Image.objects.all()
    paginator = Paginator(images, 12)
    page = request.GET.get('page')
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
    return render(request,
                  'account/user/list.html',
                  {'section': 'images', 'images': images, 'users': users})