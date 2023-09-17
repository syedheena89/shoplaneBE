from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    # path("products", csrf_exempt(ProductsView.as_view()), name="Products-add"),
    # path("category", csrf_exempt(CategoryView.as_view()), name="Productscat-add")
    path("search/", csrf_exempt(SearchProductApi.as_view()), name="Products-search"),
    path("filter/", csrf_exempt(FilterProductApi.as_view()), name="Products-search"),
    path("pagination/", csrf_exempt(paginationApi.as_view()), name="Products-pagination"),
    path("priceRange/",csrf_exempt(PriceRange.as_view()),name="products-in-priceRange"),
    path("nameOrDescription/",csrf_exempt(NameOrDescription.as_view()),name="products-name-or-description"),
    path("signup",csrf_exempt(SignUp.as_view()),name="sign-up"),
    path("signin",csrf_exempt(SignIn.as_view()),name="sign-in"),
    path("products",csrf_exempt(ProductList.as_view()),name="product-list")

]
