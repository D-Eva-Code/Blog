from django.shortcuts import render
from .models import Post
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView 

# Create your views here.
def post_list(request):
    posts= Post.published.all()
    paginator= Paginator(posts, 2)
    pagenumber= request.GET.get("page")
    try:
        posts= paginator.page(pagenumber)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts= paginator.page(paginator.num_pages)
   
    return render(request, 'postlist.html', {'posts':posts})

class Postlistview(ListView):
    queryset= Post.published.all()
    context_object_name= 'posts'
    paginate_by=(2)
    template_name='postlist.html'
    

def post_detail(request, year, month, day, post):
    detail_post = get_object_or_404(Post, status= Post.Status.PUBLISHED,slug=post, publish__year=year, publish__month=month, publish__day=day)
    return render(request, 'postdetail.html', {'detail_post': detail_post})
        