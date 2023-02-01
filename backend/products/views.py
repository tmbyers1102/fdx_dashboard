from rest_framework import generics, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_list_or_404, get_object_or_404

from api.mixins import (StaffEditorPermissionMixin, UserQuerySetMixin)
from .models import Product
from .serializers import ProductSerializer

# this is a view that either creates a product or shows a list of all products
class ProductListCreateAPIView(StaffEditorPermissionMixin, UserQuerySetMixin, generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # auth class handled as default in settings
    # custom permission class is in the mixin now

    def perform_create(self, serializer):
        # this is how you attach the current user to a created record
        # serializer.save(user=self.request.user)
        # print(serializer.validated_data)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = title
        serializer.save(user=self.request.user, content=content)
        # you can also send a django signal from here

    # this is being handled via the UserQuerySetMixin
    # def get_queryset(self, *args, **kwargs):
    #     qs = super().get_queryset(*args, **kwargs)
    #     request = self.request
    #     # print(request.user)
    #     # want to run logic for if user is not authenticated? (3:57:32)
    #     return qs.filter(user=request.user)

product_list_create_view = ProductListCreateAPIView.as_view()

# this was the create view before we made it into the LIST create view
# not needed because of the list_create_view
# class ProductCreateAPIView(StaffEditorPermissionMixin, generics.CreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

#     def perform_create(self, serializer):
#         # this is how you attach the current user to a created record
#         # serializer.save(user=self.request.user)
#         print(serializer.validated_data)
#         title = serializer.validated_data.get('title')
#         content = serializer.validated_data.get('content') or None
#         if content is None:
#             content = title
#         serializer.save(content=content)
#         # you can also send a django signal from here

# product_create_view = ProductCreateAPIView.as_view()

class ProductDetailAPIView(StaffEditorPermissionMixin, UserQuerySetMixin, generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = 'pk'

# this was set up in the video (01:32:45) but he mentioned it isnt being used but is another way to set this up in relation to urls
product_detail_view = ProductDetailAPIView.as_view()

class ProductUpdateAPIView(StaffEditorPermissionMixin, UserQuerySetMixin, generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title
            # 

product_update_view = ProductUpdateAPIView.as_view()

class ProductDestroyAPIView(StaffEditorPermissionMixin, UserQuerySetMixin, generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        #
        super().perform_destroy(instance)

product_destroy_view = ProductDestroyAPIView.as_view()


# class ProductListAPIView(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     # lookup_field = 'pk'

# # this was set up in the video (01:32:45) but he mentioned it isnt being used but is another way to set this up in relation to urls
# product_list_view = ProductListAPIView.as_view()


# this is a view that is not actually being used, but just an example of how mixins work and can be used in the future if needed
class ProductMixingView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView
    ):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    
    # if it is a get method
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        # this is how you attach the current user to a created record or attach any data that was not given on external input
        # serializer.save(user=self.request.user)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = "This is a single view doing cool stuff"
        serializer.save(content=content)

product_mixin_view = ProductMixingView.as_view()




# this is is a custom function that is not being used, but it could if we wanted
# a custom view to handle custom things w/o having to override a bunch of stuff in the clas-based
# api views (01:53:00 ish)
@api_view(["GET", "POST"])
def product_alt_view(request, pk=None, *args, **kwargs):
    method = request.method

    # could add == "PUT" and == "DESTROY" logic in here as well
    if method == "GET":
        # url_args?? if so show detail view
        if pk is not None:
            # detail view
            obj = get_object_or_404(Product, pk=pk)
            data = ProductSerializer(obj, many=False).data
            return Response(data)
        # list view
        queryset = Product.objects.all() 
        data = ProductSerializer(queryset, many=True).data
        return Response(data)

    if method == "POST":
        # create an item
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content') or None
            if content is None:
                content = title
            serializer.save(content=content)
            return Response(serializer.data)
        return Response({"invalid": "not good data"}, status=400)
