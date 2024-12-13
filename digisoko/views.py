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
    q = request.GET.get('q', '')
    category = request.GET.get('category', None)

    # Base queryset for products
    products = Products.objects.all()

    # Filter by search query if provided
    if q:
        products = products.filter(
            Q(Type__name__icontains=q) |
            Q(name__icontains=q) |
            Q(description__icontains=q)
        )

    # Filter by category name if provided
    if category:
        products = products.filter(Type__name=category)

    # Get all categories for the frontend filter
    categories = Category.objects.all()

    # Serialize and respond with both products and categories
    product_serializer = ProductSerializer(products, many=True)
    category_serializer = CategorySerializer(categories, many=True)

    response_data = {
        'products': product_serializer.data,
        'categories': category_serializer.data
    }

    return Response(response_data)



@api_view(['GET','PUT','DELETE'])
def product_details(request, id):

    try:
        products = Products.objects.get(pk = id)
    except Products.DoesNotExist:
        return Response(status= status.HTTP_404_NOT_FOUND)
    

    if request.method == 'GET':
        serializer = ProductSerializer(products)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductsSerializer(products, data = request.data)
        if serializer.is_valid():
            serializer.save()    
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)   
    elif request.method == 'DELETE':
        products.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)  


@api_view (['GET'])
def related_products(request, category_name):
    try:
        # fetch products by category
        related_products = Products.objects.filter(Type__name__iexact= category_name)
        serializer = ProductSerializer(related_products, many= True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)    


