from django.db import models
#from django.db.models import F
from ckeditor.fields import RichTextField


# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=50)
    body = RichTextField(blank=True,config_name='special')
    # img = RichTextField(blank=True,config_name='image')
    img = models.ImageField(upload_to="article", blank=True, null=True)
    author = models.ForeignKey('userProfile.Profile', on_delete=models.CASCADE, related_name="author",
                               blank=True)  # later you can access this by author.id
    num_of_likes = models.IntegerField(default=0)
    date_uploaded = models.DateField(auto_now=False, auto_now_add=True)
    # date = models.DateTimeField(default=timezone.now)
    last_modified = models.DateField(auto_now=True, auto_now_add=False)
    approved = models.BooleanField(default=False)
    tags = models.ManyToManyField("Tag", related_name="articles", blank=True)


    def approve(self):
        self.approved = True
        self.save()
    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('userProfile.Profile', on_delete=models.CASCADE, related_name="profile")
    text = RichTextField(blank=True,config_name='comment')
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.text


class Like(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='likes')
    likeUser = models.ForeignKey('userProfile.Profile', on_delete=models.CASCADE, related_name="likeUser")
    bool = models.BooleanField(default=False)

    def __str__(self):
        return self.article.title + " > " + self.likeUser.user.username

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['article','likeUser'],  name="unique_like")
        ]


class Tag(models.Model):
    name = models.CharField(unique=True, blank=True, max_length=255)
    count = models.IntegerField(default=0)

    class Meta:
        ordering = ["count"]

    def __str__(self):
        return self.name
