app_name= "Blog"
from django.urls import path
from Blog_app import views


urlpatterns = [
    path('list', views.Postlistview.as_view(), name = 'list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name= 'postdetail')
]

 