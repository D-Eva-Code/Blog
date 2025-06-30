from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse

# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)

class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    class Gender(models.TextChoices):
        MALE ='M', 'Male'
        FEMALE = 'F', 'Female'
    objects = models.Manager()
    published= PublishedManager()    
    title = models.CharField(max_length=250)
    publish= models.DateTimeField(default= timezone.now)
    slug= models.SlugField(max_length=250, unique_for_date="publish")
    body= models.TextField()
    create= models.DateTimeField(auto_now_add=True)
    update= models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status, default=Status.DRAFT)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blogs_post')
    gender= models.CharField(max_length=2, choices=Gender.choices, default= Gender.FEMALE)
    
    
    
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("Blog:postdetail", args=[self.publish.year, self.publish.month, self.publish.day,self.slug])
    
class Meta:
    ordering = ['-publish']
    indexes= [models.Index(fields=['-publish'])]
    db_table= 'Custom_database_table'
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name= models.CharField(max_length=80)
    email= models.EmailField()
    body = models.TextField()
    created= models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True) 
    active= models.BooleanField(default=True)

    def __str__(self):
        return f"comment by {self.name} on {self.created}"
class Meta:
    ordering=['created']
    indexes= [models.Index(fields=['created'])] 

    
