from django.db import models

# Create your models here.

class Profile(models.Model):
    Type_Users = [
        ("SP","ServiceProvider"),
        ("SC","ServiceConsumer")
        ]
    username = models.CharField(max_length=15,null=True,blank=True)
    email = models.TextField(null=True,blank=True)
    password = models.TextField(blank=True,null=True)
    phone_number = models.CharField(max_length=15,null=True,blank=True)
    firstname = models.CharField(max_length=15,null=True,blank=True)
    secondname = models.CharField(max_length=15,null=True,blank=True)
    thirdname = models.CharField(max_length=15,null=True,blank=True)
    surname = models.CharField(max_length=15,null=True,blank=True)
    otp = models.CharField(max_length=4,null=True,blank=True)
    image = models.ImageField( upload_to="users", null=True,blank=True)
    type_users = models.CharField(max_length=5,choices=Type_Users,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)
    updated_at = models.DateTimeField(auto_now = True, blank = True)
    def __str__(self):
        return str(self.phone_number) + " " + str(self.firstname) + " " + str(self.surname)
    
class Address(models.Model):
    user_id = models.ForeignKey(Profile,on_delete=models.CASCADE,blank=True,null=True)
    longitude = models.TextField(blank=True,null=True)
    latitude = models.TextField(blank=True,null=True)
    address_line_1 = models.CharField(max_length=100,null=True,blank=True)
    address_line_2 = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=50,null=True,blank=True)
    region = models.CharField(max_length=50,null=True,blank=True)
    country = models.CharField(max_length=50,null=True,blank=True)
    postal_code = models.CharField(max_length=20,null=True,blank=True)
    phone_number = models.CharField(max_length=20,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)
    updated_at = models.DateTimeField(auto_now = True, blank = True)

    def __str__(self):
        return str(self.user_id) + " | " + str(self.address_line_1)+ " | " + str(self.address_line_2)
class UserAttachments(models.Model):
    user_id =models.ForeignKey(Profile,on_delete=models.CASCADE,blank=True,null=True)
    file_name = models.CharField(max_length=255,null=True,blank=True)
    file_path = models.ImageField( upload_to="userattachments", null=True,blank=True)
    file_size =  models.CharField(max_length=255,null=True,blank=True)
    file_type = models.CharField(max_length=255,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)
    updated_at = models.DateTimeField(auto_now = True, blank = True)

    def __str__(self):
        return str(self.user_id) + " | " + str(self.file_name)