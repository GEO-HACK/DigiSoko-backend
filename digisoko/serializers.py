from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'   

class ProductSerializer(serializers.ModelSerializer):
    Type = CategorySerializer() #use the category serializer

    class Meta:
        model = Products
        fields = ['id', 'name', 'price', 'image', 'description', 'Type']

 