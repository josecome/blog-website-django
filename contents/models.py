from django.db import models

# Create your models here.
class Content(models.Model):
    # my_id = models.AutoField(primary_key=True) If column has different name than id  
    id = models.IntegerField(primary_key=True)  
    c_title = models.CharField(max_length=120)  
    c_body = models.TextField()  
    c_author = models.CharField(max_length=40)  
    c_author_updated = models.CharField(max_length=40)      
    c_date_created = models.DateField()
    c_date_updated = models.DateField()

    class Meta:  
        db_table = "contents"