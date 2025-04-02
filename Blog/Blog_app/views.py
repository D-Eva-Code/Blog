from django.shortcuts import render,redirect
from .models import Post
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView 
from .forms import EmailPostForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from .forms import CommentForm

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
    comments = detail_post.comments.filter(active= True)
    form= CommentForm()
    return render(request, 'postdetail.html', {'detail_post': detail_post, 'comments':comments, 'form':form})

def post_share(request, id):
    share_post= get_object_or_404(Post, pk= id, status = Post.Status.PUBLISHED)
    sent = False
    if request.method=='POST':
        new_form= EmailPostForm(request.POST)
        if new_form.is_valid():
            print("DEBUG: Form is valid")
            cd= new_form.cleaned_data #send email in a clean format
            post_url= request.build_absolute_uri(share_post.get_absolute_url())
            subject= (f"{cd['name']} ({cd['email']}) " f"recommends you read post {share_post.title}")
            message= (f"Read \'{share_post.title}\' at {post_url}\n\n" f"{cd['name']}\'s comment: {cd['comments']}")
            send_mail(subject=subject, message=message, from_email=None, recipient_list=[cd['to']])
            sent=True
            return render(request, 'forms.html', {'share_post': share_post, 'new_form': new_form, 'sent':sent})

        print("invalid")
        print(new_form.errors)

    else:
        new_form= EmailPostForm()
        return render(request, 'forms.html', {'share_post': share_post, 'new_form': new_form, 'sent':sent})

            
@require_POST
def post_comment(request, id):
    post = get_object_or_404(Post, status= Post.Status.PUBLISHED, pk= id)
    comments= None
    new_comment= CommentForm(data=request.POST)
    if new_comment.is_valid():
        comments= new_comment.save(commit=False)#assign the comments variable to the comments object(using save) and dont save yet (having that commit=False)
        comments.post= post# assign the post to the comment we created
        comments.save()#finally save the comment to database
        return render(request, 'comment.html', {'comments': comments, 'post':post, 'new_comment':new_comment})