app_name= "Blog"
from django.urls import path
from Blog_app import views


urlpatterns = [
    # path('list', views.Postlistview.as_view(), name = 'list'),
    path('list', views.post_list, name= 'list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name= 'postdetail'),
    path('<int:id>/share/', views.post_share, name= 'postshare'),
    path('<int:id>', views.post_comment, name= 'postcomment'),
]

 