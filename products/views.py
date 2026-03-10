from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Category, Product, Review
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer


class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(parent=None, is_active=True)


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)

        category_slug = self.request.query_params.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)

        sort = self.request.query_params.get('sort')
        if sort == 'low_to_high':
            queryset = queryset.order_by('price')
        elif sort == 'high_to_low':
            queryset = queryset.order_by('-price')

        return queryset


class ProductDetailView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_active=True)
    lookup_field = 'slug'


class ReviewCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, slug):
        product = Product.objects.get(slug=slug)
        existing = Review.objects.filter(product=product, user=request.user).first()
        if existing:
            serializer = ReviewSerializer(existing, data=request.data, partial=True)
        else:
            serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product, user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)