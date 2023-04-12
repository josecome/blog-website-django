from django.db import models

#Here are models for users. To see models for posts look at contents/model
# Create your models here.
class blogUsers(models.Model):
    # my_id = models.AutoField(primary_key=True) If column has different name than id  
    id = models.AutoField(primary_key=True)
    title_of_post = models.CharField(max_length=120)
    username = models.CharField(max_length=40)  
    first_name = models.CharField(max_length=60)  
    last_name = models.CharField(max_length=40)  
    email = models.CharField(max_length=40)  
    pic_of_user = models.TextField()     
    date_created = models.DateField()
    date_updated = models.DateField(null=True)
    link = models.CharField(max_length=100)  

    class Meta:  
        db_table = "blog_users"

