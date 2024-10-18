from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer, CategorySerializer
from .models import *
from django.db.models import  Q



@api_view(['GET'])
def products(request):
    q = request.GET.get('q','')

    products = Products.objects.filter(
        Q(Type__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        
    )
    categories = Category.objects.all()

    product_serializer = ProductSerializer(products,many = True)
    category_serializer = CategorySerializer(categories, many = True)

    response_data = {
        'products': product_serializer.data,
        'categories':category_serializer.data
    }
    # this will help to avoid clutterd code in the ide

    return Response(response_data)

@api_view(['GET','PUT','DELETE'])
def product_details(request, id):

    try:
        products = Products.objects.get(pk = id)
    except Products.DoesNotExist:
        return Response(status= status.HTTP_404_NOT_FOUND)
    

    if request.method == 'GET':
        serializer = ProductSerializer(products)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductsSerializer(products, data = request.data)
        if serializer.is_valid():
            serializer.save()    
            return JsonResponse(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)   
    elif request.method == 'DELETE':
        products.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)        
