from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Products(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    image = models.ImageField(null=True,blank=True)
    Type = models.ForeignKey('Category', on_delete=models.CASCADE)
    description = models.TextField()
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


