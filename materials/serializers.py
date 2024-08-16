from rest_framework import serializers

from .models import Category, Product, SubForProductUpdate
from .validators import UrlsValidator


# from users.serializers import UserSerializer


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'
        validators = [UrlsValidator(field='url')]


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField(read_only=True)
    products = ProductSerializer(source='product_set', many=True, required=False, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'

    def get_products_count(self, instance):
        if instance.product_set.all().last():
            return instance.product_set.all().count()
        return 0

    def get_validation_exclusions(self):
        exclusions = super(CategorySerializer, self).get_validation_exclusions()
        return exclusions + ['owner']


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubForProductUpdate
        fields = '__all__'
        validators = [UrlsValidator(field='url')]
