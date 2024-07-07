from rest_framework import *
from .models import *
from rest_framework import serializers

class FoodTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodType
        fields="__all__"


class FoodItemsSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    class Meta:
        model = FoodItem
        fields="__all__"
class orderDetailSerializer(serializers.ModelSerializer):
    fooditem = FoodItemsSerializer()

    class Meta:
        model = orderDetail
        fields = "__all__"

    def create(self, validated_data):
        fooditem_data = validated_data.pop('fooditem')
        fooditem = FoodItem.objects.get(id=fooditem_data['id'])
        order_detail = orderDetail.objects.create(fooditem=fooditem, **validated_data)
        return order_detail
class GrandOrderSerializer(serializers.ModelSerializer):
    orders = orderDetailSerializer(many=True)

    class Meta:
        model = GrandOrder
        fields = "__all__"
    def create(self, validated_data):
        orders_data = validated_data.pop('orders')
        grand_order = GrandOrder.objects.create(**validated_data)
        for order_data in orders_data:
            fooditem_data = order_data.pop('fooditem')
            fooditem = FoodItem.objects.get(id=fooditem_data['id'])
            order_detail = orderDetail.objects.create(fooditem=fooditem, **order_data)
            grand_order.orders.add(order_detail)
        grand_order.grand_total = sum(order.total_price for order in grand_order.orders.all())
        grand_order.save()
        return grand_order