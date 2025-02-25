from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer, CategorySerializer
from .models import Products, Category
from django.db.models import Q



# from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework.decorators import api_view, parser_classes
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Products, Category
# from .serializers import ProductSerializer, CategorySerializer

@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, FormParser])  # Applies parsers for POST requests
def products(request):
    # Handle GET requests
    if request.method == 'GET':
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

    # Handle POST requests
    elif request.method == 'POST':
        # Manually handle the 'Type' field if it's being sent as a string (category name)
        type_data = request.data.get('Type', None)
        if type_data:
            try:
                category = Category.objects.get(name=type_data)
                request.data['Type'] = category.id  # Replace with category ID
            except Category.DoesNotExist:
                return Response({"detail": "Category not found."}, status=status.HTTP_400_BAD_REQUEST)

        # Parse multipart data with the serializer
        serializer = ProductSerializer(data=request.data)
        
        if serializer.is_valid():
            product = serializer.save()

            # Save the uploaded image if present
            if 'image' in request.FILES:
                product.image = request.FILES['image']
                product.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
def product_details(request, id):
    product = get_object_or_404(Products, pk=id)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def related_products(request, category_name):
    try:
        # Fetch products by category
        related_products = Products.objects.filter(Type__name__iexact=category_name)
        serializer = ProductSerializer(related_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    






 