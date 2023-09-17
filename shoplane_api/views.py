from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, Http404, HttpResponseBadRequest
from .models import *
from .serializer import *
import json
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class SignUp(APIView):
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                'refresh':str(refresh),
                'access':str(refresh.access_token),
            },status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class SignIn(APIView):
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user =serializer.validated_data
            token = RefreshToken.for_user(user)
            return JsonResponse({
                'access':str(token.access_token),
                'refresh':str(token),
                
            },status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class ProductList(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        products = Product.objects.all().values()
        print(products)
        return JsonResponse(list(products),safe=False)



class ProductReviews(View):
    def get(self,request,product_id):
        try :
            product = product.objects.get(id=product_id)
            reviews=Review.objects.filter(product = product.id).values("id","review","rate")
            response = {
                "product_id":product.id,
                "name":product.name,
                "brand":product.brand,
                "reviews":list(reviews)    
            }
        except:
            return JsonResponse({"message":"product not found"})

class SearchProductApi(View):
    def get(self,request):
        try:
            query = request.GET.get("query","")
            page_number = request.GET.get("page",1)
            products = Product.objects.filter(description__icontains=query).order_by("id")
            paginate =Paginator(products,5)
            page = paginate.get_page(page_number)
            page_product = page.object_list
            serializer= ProductSerializer(page_product,many=True).data
            return JsonResponse(
            {
                "data":serializer,
                "total_pages":paginate.num_pages,
                "total_record":products.count(),
            },
            safe=False,)


        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class FilterProductApi(View):
    def get(self,request):
        category = request.GET.get("category",None)
        brand = request.GET.get("brand",None)
        active = request.GET.get("active",None)
        min=request.GET.get("min",None)
        max = request.GET.get("max",None)
        products = Product.objects.all()
        if category:
            products = products.filter(category__icontains=category)
        if brand:
            products = products.filter(brand__icontains=brand)
        if active:
            products = products.filter(active__in =[True])
        if min:
            products = products.filter(price__gte=int(min))
        if max:
            products = products.filter(price__leq=int(max))
        serializer = ProductSerializer(products,many=True).data
        return JsonResponse(serializer,safe=False)
    
class paginationApi(View):
    def get(self,request):
        page_number = request.GET.get("page",1)
        products = Product.objects.all().order_by("id") 
        paginate =Paginator(products,5)
        page = paginate.get_page(page_number)
        page_product = page.object_list
        serializer = ProductSerializer(page_product,many=True).data
        return JsonResponse(
            {
                "data":serializer,
                "total_pages":paginate.num_pages,
                "total_record":products.count(),
            }
        )

class PriceRange(View):
    def get(self,request):
        min = request.GET.get("min",None)
        max = request.GET.get("max",None)
        if min and max:
            products =Product.objects.filter(price__gt=min,price__lt=max)
            serializer =ProductSerializer(products,many=True).data
            return JsonResponse(serializer,safe=False)
        return JsonResponse({"message":"please provide both the parameters."})

class NameOrDescription(View):
    def get(self,request):
        query = request.GET.get("query",None)
        if query:
            products=Product.objects.filter(Q(name__icontains=query)|Q(description__icontains=query))
            serializer = ProductSerializer(products,many=True).data
            return JsonResponse(serializer,safe=False)
        return JsonResponse({"message":"please provide the query"})








