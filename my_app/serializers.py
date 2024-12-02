"""
В этом модуле представлен классы серализаторы DeliverySerializerSet для ModelViewSet и DeliverySerializer для APIView
"""

from rest_framework import serializers
from .models import Delivery

class DeliverySerializerSet(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = '__all__'


class DeliverySerializer(serializers.Serializer):
    load_data = serializers.DateTimeField(read_only=True)
    customer_name = serializers.CharField(max_length=150)
    delivery_city = serializers.CharField(max_length=150)
    delivery_address = serializers.CharField(max_length=250)
    delivery_date = serializers.DateField(read_only=True)
    delivery_time = serializers.TimeField(read_only=True)
    package_type = serializers.CharField(max_length=150)
    comment = serializers.CharField()

    def create(self, validate_data):
        return Delivery.objects.create(**validate_data)

    def update(self, instance, validated_data):
        instance.customer_name = validated_data.get('customer_name', instance.customer_name)
        instance.delivery_city = validated_data.get('delivery_city', instance.delivery_city)
        instance.delivery_address = validated_data.get('delivery_address', instance.delivery_address)
        # instance.delivery_date = validated_data.get('delivery_date', instance.delivery_date)
        # instance.delivery_time = validated_data.get('delivery_time', instance.delivery_time)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        return instance


class DeliveryStatusSerializer(serializers.Serializer):
    status_name = serializers.CharField()

    def update(self, instance, validated_data):
        instance.status_name = validated_data.get('status_name', instance.status_name)
        instance.save()
        return instance
