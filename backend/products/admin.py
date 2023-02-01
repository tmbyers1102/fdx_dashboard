from django.contrib import admin

# import the model Todo
from .models import Product

# create a class for the admin-model integration
class ProductAdmin(admin.ModelAdmin):

	# add the fields of the model here
	list_display = ("title","pk","content","price","sale_price","user","public")

# we will need to register the
# model class and the Admin model class
# using the register() method
# of admin.site class
admin.site.register(Product,ProductAdmin)