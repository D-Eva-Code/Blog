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
    
    
    
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("Blog:postdetail", args=[self.publish.year, self.publish.month, self.publish.day,self.slug])
    
class Meta:
    ordering = ['-publish']
    indexes= [models.Index(fields=['-publish'])]
    
    
