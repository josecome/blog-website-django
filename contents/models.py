from django.db import models

# Create your models here.
class Content(models.Model):
    # my_id = models.AutoField(primary_key=True) If column has different name than id  
    id = models.AutoField(primary_key=True)  #IntegerField
    title = models.CharField(max_length=120)
    topic = models.CharField(max_length=40, default="BLOG")  
    body = models.TextField()  
    author = models.CharField(max_length=40)  
    author_updated = models.CharField(max_length=40, null=True)      
    date_created = models.DateField()
    date_updated = models.DateField(null=True)
    lnk = models.CharField(max_length=100, default='lnk')  

    class Meta:  
        db_table = "contents"