from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Product
from . import validators

from api.serializers import UserPublicSerializer

class ProductInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(view_name="product-detail", lookup_field = 'pk', read_only=True)
    title = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)

class ProductSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)
    # want to call the user 'owner'?
    # owner = UserPublicSerializer(source='user', read_only=True)

    # this was just to illustrait how related records could be shown
    # related_products = ProductInlineSerializer(source='user.product_set.all', read_only=True, many=True)
    
    # my_user_data = serializers.SerializerMethodField(read_only=True)
    # my_discount = serializers.SerializerMethodField(read_only=True)
    # edit_url = serializers.SerializerMethodField(read_only=True)
    # url = serializers.HyperlinkedIdentityField(view_name="product-detail", lookup_field = 'pk')

    title = serializers.CharField(validators=[validators.validate_title_no_hello, validators.unique_product_title])
    # cool way to show associated info from ForeignKey field w/o actually having to list it on the model:
    # email = serializers.CharField(source='user.email', read_only=True)
    body = serializers.CharField(source='content')
    class Meta:
        model = Product
        fields = [
            'user',
            # 'owner',
            # 'id',
            # 'url',
            # 'edit_url',
            'pk',
            'title',
            # 'name',
            # when we incorperated articles app we switched this to body to unify
            # 'content',
            'body',
            'price',
            'sale_price',
            # 'my_discount',
            # 'my_user_data',
            # 'related_products',
            'public',
            'path',
            'endpoint',
        ]

    def get_my_user_data(self, obj):
        return {
            "username": obj.user.username
        }

    # def validate_title(self, value):
    #     # lets see if this title already exists within db
    #     # title__exact = case sensitive... title__iexact = case insensitive
    #     qs = Product.objects.filter(title__iexact=value)
    #     if qs.exists():
    #         raise serializers.ValidationError(f"'{value}' is already a product name :-(")
    #     return value

    # def update(self, instance, validated_data):
    #     instance.title = validated_data.get('title')
    #     return instance

    def get_edit_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("product-edit", kwargs={"pk": obj.pk}, request=request)

    def get_my_discount(self, obj):
        if not hasattr(obj, 'id'):
            return None
        if not isinstance(obj, Product):
            return None
        return obj.get_discount()