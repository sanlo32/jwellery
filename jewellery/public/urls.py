from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_selection, name='product_selection'),
    path('create_bill/<str:include_tax>/', views.create_bill, name='create_bill'),
    path('print_bill/<int:bill_id>/<str:include_tax>/', views.print_bill, name='print_bill'),
    path('search_bill/', views.search_bill, name='search_bill'),
]
