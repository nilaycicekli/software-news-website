from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
UserModel = get_user_model()

#Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_photo = models.ImageField(upload_to="profile",default="profile.png", blank=True, null=True)
    
    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class UserFollowing(models.Model):

    user = models.ForeignKey(UserModel, related_name="following", on_delete=models.CASCADE)
    following_user = models.ForeignKey(UserModel, related_name="followers", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user','following_user'],  name="unique_followers")
        ]
        ordering = ["-created"]

    def __str__(self):
        return f"{self.user.username} follows {self.following_user.username}"

    # def follow(self,user_id,follow_user_id):
    #     self.objects.create(user_id=user_id, following_user_id=follow_user_id)

        # user = User.objects.get(id=id)
        # user.following.all()
        # user.followers.all()
