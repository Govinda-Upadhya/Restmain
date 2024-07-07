from django.shortcuts import render
from .models import *
from rest_framework.decorators import api_view
from .serializer import FoodTypeSerializer,FoodItemsSerializer
from django.http import JsonResponse
from rest_framework.response import Response
from .serializer import GrandOrderSerializer
from rest_framework import status
# Create your views here.
@api_view(['GET'])
def FoodTypes(request):
    foodtypes=FoodType.objects.all()
    serializer=FoodTypeSerializer(foodtypes,many=True)
    
    return Response(serializer.data)
@api_view(['GET'])   
def FoodItems(request):
    fooditems=FoodItem.objects.all()
    serializer=FoodItemsSerializer(fooditems,many=True)
    
    return Response(serializer.data)

@api_view(['POST'])
def place_order(request):
    order_ID=request.data['id']
    table_number=request.data['table_number']
    phoneno=request.data['phone_number']
    grand_order=GrandOrder.objects.create(table_number=table_number,phone_number=phoneno)
    for item in request.data['items']:
        food=FoodItem.objects.get(id=item['id'])
        quantity=item['quantity']
        orderdetail=orderDetail.objects.create(fooditem=food,quantity=quantity)
        orderdetail.save()
        grand_order.orders.add(orderdetail)
    grandprice=0
    for order in grand_order.orders.all():
        grandprice+=order.total_price
    print(grandprice)
    grand_order.grand_total=grandprice
    grand_order.save()
    print(request.data)
    return Response( status=status.HTTP_201_CREATED)
   
        