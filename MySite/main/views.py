from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from .models import Post, Board, User


def visitor_ip(request):

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def index(request):
    latest_board_list = get_list_or_404(Board)
    context = {
        'latest_board_list': latest_board_list
    }
    return render(request, 'main/index.html', context)


def board(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    latest_post_list = reversed(get_list_or_404(Post, board=board)[:20])
    context = {
        'board': board,
        'latest_post_list': latest_post_list
    }
    return render(request, 'main/board.html', context)


def post(request, board_id):
    text = request.POST.get('post_text')
    board = get_object_or_404(Board, pk=board_id)
    my_ip = visitor_ip(request)
    if get_object_or_404(User, ip=my_ip):
        writer = get_object_or_404(User, ip=my_ip)
    else:
        writer = User(ip=my_ip)
        writer.save()
    post = Post(board=board, writer=writer, text=text, likes=0)
    post.save()
    return HttpResponseRedirect(reverse('main:board', args=(board.id,)))


def like(request, post_id):
    my_ip = visitor_ip(request)
    post = get_object_or_404(Post, pk=post_id)
    if post.writer.ip != my_ip:
        post.likes += 1
        post.save()
    return HttpResponseRedirect(reverse('main:board', args=(post.board.id,)))


def setting(request):
    my_ip = visitor_ip(request)
    if get_object_or_404(User, ip=my_ip):
        user = get_object_or_404(User, ip=my_ip)
    else:
        user = User(ip=my_ip)
        user.save()
    context = {
        'vistor_ip': my_ip,
        'user': user,
    }
    return render(request, 'main/setting.html', context)


def change_name(request):
    my_ip = visitor_ip(request)
    text = request.POST.get('nickname')
    user = get_object_or_404(User, ip=my_ip)
    user.username = text
    user.save()
    return HttpResponseRedirect(reverse('main:setting'))
