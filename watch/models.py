from django.db import models
import datetime as dt 
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Neighbourhood(models.Model):
  '''
  class that contains Neighbourhood properties
  '''
  LOCATION_CHOICES = (
    ('Embakasi','Embakasi'),
    ('Westlands','Westlands'),
    ('Kahawa sukari','Kahawa sukari'),
    ('Ruaka','Ruaka'),
    ('Syokimau','Syokimau'),
    ('Zimmerman','Zimmerman'),
    ('Karen','Karen'),
    ('Ruiru','Ruiru'),
    ('Roysambu','Roysambu'),
  )
  name = models.CharField(max_length=200)
  location = models.CharField(max_length=30,choices=LOCATION_CHOICES)
  description = models.TextField(blank=True,null=True)
  posted_on = models.DateTimeField(auto_now_add=True)
  police_dept = models.IntegerField(default="0746393500")
  health_dept = models.IntegerField(default="0722567432")
  user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)

  def save_neighbourhood(self):
    self.save()

  def update_neighbourhood(self):
    self.update()

  def update_occupants(self):
    self.update()

  def delete_neighbourhood(self):
    self.delete()

  class Meta:
    ordering = ['posted_on']

  @classmethod
  def get_neighbourhoods(cls):
    neighbourhoods = Neighbourhood.objects.all()
    return neighbourhoods

  @classmethod
  def find_neighbourhood_by_id(cls,id):
    neighbourhood = Neighbourhood.objects.get(id=id)
    return neighbourhood

  @classmethod
  def search_by_title(cls,search_term):
    neighbourhood = cls.objects.filter(name__icontains=search_term)
    return neighbourhood

  def __str__(self):
    return self.name

class Profile(models.Model):
  '''
  class that contains user Profile properties
  '''
  bio = models.TextField()
  user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
  hood = models.OneToOneField(Neighbourhood,on_delete=models.CASCADE,blank=True,null=True)

  @receiver(post_save, sender=User)
  def create_user_profile(sender, instance, created, **kwargs):
          if created:
                  Profile.objects.create(user=instance)

  @receiver(post_save, sender=User)
  def save_user_profile(sender, instance, **kwargs):
          instance.profile.save()

  post_save.connect(save_user_profile, sender=User)

  def save_profile(self):
    self.save

  def delete_profile(self):
    self.delete

  def update_profile(self):
    self.update

  def __str__(self):
    return self.bio

class Business(models.Model):
  '''
  Business class with Business properties,methods and function 
  '''
  name = models.CharField(max_length=30)
  description = models.TextField(default="",blank=True,null=True)
  email = models.EmailField()
  user = models.ForeignKey(User,null=True,blank=True)
  neighbourhood = models.ForeignKey(Neighbourhood,null=True,blank=True)

  def save_business(self):
    self.save

  def delete_business(self):
    self.delete

  def update_business(self):
    self.update

  @classmethod
  def find_business(cls,id):
    business = Business.object.get(id=id)
    return business

  @classmethod
  def get_hood_businesses(cls, id):
      businesses = Business.objects.filter(hood_id=id).all()
      return businesses

  @classmethod
  def search_by_title(cls,search_term):
    business = cls.objects.filter(title__icontains=search_term)
    return business

  def __str__(self):
    self.name

class Join(models.Model):
  '''
  class that enables one join neighbourhoods
  '''
  user_id = models.OneToOneField(User)
  hood_id = models.ForeignKey(Neighbourhood)

  def __str__(self):
    return self.user_id.username

class Posts(models.Model):
  '''
  Class that enables one create a post on a neighbourhood
  '''
  topic = models.CharField(max_length=100)
  post = models.TextField()
  user = models.ForeignKey(User)
  hood = models.ForeignKey(Neighbourhood)

  def save_posts(self):
    self.save()

  def delete_posts(self):
    self.delete()

  @classmethod
  def get_post_by_hood(cls, id):
      post = Posts.objects.filter(hood_id=id).all()
      return post


  def __str__(self):
    return self.topic

  

class Comments(models.Model):
  '''
  Class that enables commenting on a posted topic
  '''
  comment = models.TextField()
  user = models.ForeignKey(User)
  post = models.ForeignKey(Posts)

  def save_comment(self):
    self.save()

  def delete_comment(self):
    self.delete()

  def __str__(self):
    return self.comment

