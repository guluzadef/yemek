import uuid

from django.db import models
from base_user.models import MyUser
from image_cropping import ImageRatioField,ImageCropField
User=MyUser

# Create your models here.
def token_generator():
    id = uuid.uuid4()
    return str(id)

class TokenModel(models.Model):
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    expired = models.BooleanField(default=False)
    create_date = models.DateField(auto_now=True)
    token = models.CharField(max_length=55,default=token_generator)
class Photos_Pages(models.Model):
    main_page=models.ImageField(upload_to='images',null=True,blank=True)
    detail_page = models.ImageField(upload_to='images',null=True,blank=True)
    example_page = models.ImageField(upload_to='images',null=True,blank=True)
    example1_page = models.ImageField(upload_to='images',null=True,blank=True)


class Texts_Pages(models.Model):
    detail_page=models.CharField(max_length=255,null=True,blank=True)
    addfood_page = models.CharField(max_length=255,null=True,blank=True)
    example_page = models.CharField(max_length=255,null=True,blank=True)
    example_page1_page = models.CharField(max_length=255,null=True,blank=True)




class Site_name(models.Model):
    icon=models.ImageField(upload_to="site_icon")
    name=models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class Menu(models.Model):
    name=models.CharField(max_length=255)
    url=models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"

class Main(models.Model):
    title=models.CharField(max_length=255)
    description=models.CharField(max_length=400)
    icon_food=models.ImageField(upload_to="main_icon")
    food_count=models.PositiveIntegerField(null=True,blank=True)
    video_url=models.CharField(max_length=255)


    def __str__(self):
        return f"{self.title}"



class First(models.Model):
    name=models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"

class Second(models.Model):
    name=models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"



class Meals(models.Model):
    choices = (('User', ("User")),
               ('Shef', ("Shef")))
    name=models.CharField(max_length=255)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    category=models.CharField(choices=(('Morning',("Morning")),
                                       ('Lunch',("Lunch")),
                                       ('Supper',("Supper")),
                                       ),default=2,max_length=244)

    aditional_info=models.TextField()
    delivery_type = models.CharField(max_length=244,choices=choices,default=choices[0][0])
    delivery_price = models.PositiveIntegerField(null=True,blank=True)
    # image=models.ImageField(upload_to="meals/photo")
    cord_lng = models.FloatField()
    cord_lat = models.FloatField()
    location = models.CharField(max_length=55,null=True,blank=True)
    price=models.PositiveIntegerField()
    quantity=models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.name},{self.author}"

    class Meta:
        ordering = ["-id"]



class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Meals, on_delete=models.CASCADE)
    status = models.IntegerField(choices=(
        (0, "Like"),
        (1, "Unlike")
    ),
        default=0
    )
    created_time = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"


class MealsImages(models.Model):
    post = models.ForeignKey(Meals, on_delete=models.CASCADE,null=True,blank=True)
    image = models.ImageField(upload_to="meals/photo")
    image_token = models.CharField(max_length=55,null=True,blank=True)

class Footer(models.Model):
    description=models.CharField(max_length=300)
    number=models.CharField(max_length=255)
    email=models.CharField(max_length=255)

    copyright=models.CharField(max_length=255)

    def __str__(self):
        return f"{self.description}"

class Instagramfield(models.Model):
    instagram = models.CharField(max_length=255,null=True,blank=True)
    instagram_img = models.ImageField(upload_to="media_insta",null=True,blank=True)
    url=models.CharField(max_length=255,null=True,blank=True)
    def __str__(self):
        return f"{self.instagram}"

class CommentPost(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Meals, on_delete=models.CASCADE)
    comment=models.CharField(max_length=130)

    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post}"

    class Meta:
        ordering = ["-id"]

class Ordering(models.Model):
    choices =(('User', ("User")),
              ('Shef', ("Shef")))

    customer=models.ForeignKey(User,on_delete=models.CASCADE,related_name='customer')
    meal=models.ForeignKey(Meals,on_delete=models.CASCADE)
    author_of_meal = models.ForeignKey(User,on_delete=models.CASCADE,related_name='author_of_meal')
    total_price=models.PositiveIntegerField()
    quantity=models.PositiveIntegerField()
    location=models.CharField(max_length=255)
    status=models.BooleanField(default=False)
    order_date=models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=9, null=True, blank=True)
    delivery_type = models.CharField(max_length=244,null=True,blank=True,choices=choices,default=choices[0][0])
    expire = models.BooleanField(default=False)
    ordering = ['-order_date']
    def __str__(self):
        return f"{self.customer} {self.total_price}"




class Notifications(models.Model):
    ACTIVITY_TYPES = (
        (0, "ReadyToCooker"),
        (1, "ReadyToUser"),
        (2, "Delete"),
        (3, "Accept Friend request"),
        (4, "Reject Friend request"),
        (5, "Send you money"),
        (6, "Accept your advertisement"),
        (7, "Reject your advertisement"),
    )
    from_user= models.ForeignKey(MyUser,on_delete=models.CASCADE,related_name='from_user')
    to_user = models.ForeignKey(MyUser,on_delete=models.CASCADE,related_name='to_user')
    create_date= models.DateTimeField(auto_now=True)
    activity_type = models.IntegerField(default=0,choices=ACTIVITY_TYPES)
    read = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.from_user} => {self.to_user}'