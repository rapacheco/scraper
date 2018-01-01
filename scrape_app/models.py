from django.db import models

# Create your models here.
# class User(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.CharField(max_length=100, unique=True)
#     password = models.CharField(max_length=100)
#
#     def __str__(self):
#         return name

class WebPage(models.Model):
    # user = models.ForeignKey(User)
    url = models.URLField(unique=True)
    title = models.CharField(max_length=100)
    number_of_tags = models.IntegerField()
    date_scraped = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Tag(models.Model):
    page = models.ForeignKey(WebPage)
    tag = models.URLField()

    def __str__(self):
        return self.tag

# class Image(models.Model):
#     page = models.ForeignKey(WebPage)
#     image = models.FileField()
