from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from .models import Post, Board, User
from django.core.exceptions import ObjectDoesNotExist


def visitor_ip(request):

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_user_or_create(request):
    my_ip = visitor_ip(request)
    try:
        User.objects.get(ip=my_ip)
        user = get_object_or_404(User, ip=my_ip)
    except ObjectDoesNotExist:
        user = User(ip=my_ip)
        user.save()
    return user


def index(request):
    my_ip = visitor_ip(request)
    latest_board_list = get_list_or_404(Board)
    context = {
        'latest_board_list': latest_board_list,
        'ip': my_ip
    }
    return render(request, 'main/index.html', context)


def board(request, board_id):
    user = get_user_or_create(request)
    board = get_object_or_404(Board, pk=board_id)
    allowed = True
    if board.protected:
        allowed = False
        if str(board.id) in user.allowed_board_id.split(','):
            allowed = True
    latest_post_list = reversed(get_list_or_404(Post, board=board)[:20])
    context = {
        'board': board,
        'latest_post_list': latest_post_list,
        'allowed': allowed,
        'ip': user.ip
    }
    return render(request, 'main/board.html', context)


def post(request, board_id):
    text = request.POST.get('post_text')
    board = get_object_or_404(Board, pk=board_id)
    writer = get_user_or_create(request)
    post = Post(board=board, writer=writer, text=text, likes=0)
    post.save()
    return HttpResponseRedirect(reverse('main:board', args=(board.id,)))


def like(request, post_id):
    user = get_user_or_create(request)
    post = get_object_or_404(Post, pk=post_id)
    if post.writer.ip != user.ip:
        liked_list = user.liked_post_id.split(',')
        if str(post.id) in liked_list:
            post.likes -= 1
            post.save()
            liked_list.remove(str(post.id))
            user.liked_post_id = ','.join(liked_list)
            user.save()
        else:
            post.likes += 1
            post.save()
            liked_list.append(str(post.id))
            user.liked_post_id = ','.join(liked_list)
            user.save()
    return HttpResponseRedirect(reverse('main:board', args=(post.board.id,)))


def setting(request):
    user = get_user_or_create(request)
    context = {
        'ip': user.ip,
        'user': user,
    }
    return render(request, 'main/setting.html', context)


def change_name(request):
    text = request.POST.get('nickname')
    user = get_user_or_create(request)
    user.username = text
    user.save()
    return HttpResponseRedirect(reverse('main:setting'))


def delete_post(request, post_id):
    my_ip = visitor_ip(request)
    post = get_object_or_404(Post, pk=post_id)
    if post.writer.ip == my_ip:
        post.delete()
    return HttpResponseRedirect(reverse('main:board', args=(post.board.id,)))
