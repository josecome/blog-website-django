from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class SharedFields(models.Model):
    date_created = models.DateField()
    date_updated = models.DateField(null=True)

    class Meta:
        abstract = True


class Posts(SharedFields):
    LIST_OF_TYPE_POST = (
        ('Private', 'Private'),
        ('Public', 'Public')
    )
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=120)
    post_content = models.TextField()   
    post_type = models.CharField(max_length=40, choices=LIST_OF_TYPE_POST) 
    link = models.CharField(max_length=100)  
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def username(self):
        return self.user.username

    class Meta:  
        db_table = "post"        


class Likes(SharedFields):
    id = models.AutoField(primary_key=True)
    type_of_like = models.CharField(max_length=120)
    post_liked_link = models.CharField(max_length=80)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:  
        db_table = "likes"        


class Comments(SharedFields):
    id = models.AutoField(primary_key=True)
    comment = models.TextField(default='Without comment')   
    post_commented_link = models.CharField(max_length=80)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:  
        db_table = "comments"     


class Shares(SharedFields):
    id = models.AutoField(primary_key=True)
    post_shared_link = models.CharField(max_length=80)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:  
        db_table = "shares"       