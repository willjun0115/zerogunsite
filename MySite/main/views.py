from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from .models import Post, Board


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
    writer_ip = visitor_ip(request)
    post = Post(board=board, ip=writer_ip, text=text, likes=0)
    post.save()
    return HttpResponseRedirect(reverse('main:board', args=(board.id,)))


def like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.likes += 1
    post.save()
    return HttpResponseRedirect(reverse('main:board', args=(post.board.id,)))
