from django.db import models
from django.contrib.auth.models import User


class UserDetails(models.Model):
    usr = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

class Movie_Category(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class Movies(models.Model):
    cat = models.ForeignKey(Movie_Category, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=500, null=True, blank=True)
    r_date = models.CharField(max_length=500, null=True, blank=True)
    director = models.CharField(max_length=500, null=True, blank=True)
    rate = models.FloatField(max_length=500, null=True, blank=True)
    pro_house = models.CharField(max_length=500, null=True, blank=True)
    des = models.CharField(max_length=2000, null=True, blank=True)
    img1 = models.FileField(null=True, blank=True)
    img2 = models.FileField(null=True, blank=True)
    img3 = models.FileField(null=True, blank=True)
    img4 = models.FileField(null=True, blank=True)
    trailer = models.CharField(max_length=5000, null=True, blank=True)

    def __str__(self):
        return self.title

class Cast(models.Model):
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    img = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.name



class Talkies(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class ShowTime(models.Model):
    talkies = models.ForeignKey(Talkies, on_delete=models.CASCADE, null=True, blank=True)
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE, null=True, blank=True)
    time = models.CharField(max_length=10, null=True, blank=True)
    Rs = models.IntegerField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.date)



class Sheets(models.Model):
    usr = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    talkies = models.ForeignKey(Talkies, on_delete=models.CASCADE, null=True, blank=True)
    st = models.ForeignKey(ShowTime, on_delete=models.CASCADE, null=True, blank=True)
    sn = models.CharField(max_length=10, null=True, blank=True)
    status = models.CharField(max_length=100, default="Blank")



class Payment_Id(models.Model):
    Usr = models.ForeignKey(User, on_delete=models.CASCADE)
    PayId = models.CharField(max_length=120, null=True, blank=True)