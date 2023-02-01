import random
from django.db import models
from django.conf import settings
from django.db.models import Q


User = settings.AUTH_USER_MODEL # adding 'settings' makes it a string version of auth.user (best practice)

TAGS_MODEL_VALUES = ['electronics', 'cars', 'boats', 'movies', 'cameras']

# added related to basic search
class ProductQuerySet(models.QuerySet):
    # this replaces the need to use .filter(public=True)... on the ProductManager class return
    def is_public(self):
        return self.filter(public=True)

    # this replaces the need to use .filter(title__icontains=query)... on the ProductManager class return
    def search(self, query, user=None):
        # checks to see if query is in title and/or content fields
        lookup = Q(title__icontains=query) | Q(content__icontains=query)
        qs = self.is_public().filter(lookup)
        if user is not None:
            qs2 = self.filter(user=user).filter(lookup)
            qs = (qs | qs2).distinct()
        return qs

# this was created to allow the basic search function (4:30:00ish)
class ProductManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        # that using=self._db is where you could actually use other dbs if needed
        return ProductQuerySet(self.model, using=self._db)

    def search(self, query, user=None):
        return self.get_queryset().is_public().search(query, user=user)

class Product(models.Model):
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=120)
    content = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=99.99)
    public = models.BooleanField(default=True)

    # added related to basic search
    objects = ProductManager()

    def get_absolute_url(self):
        return f"/api/products/{self.pk}/"

    @property
    def endpoint(self):
        return self.get_absolute_url()

    @property
    def path(self):
        return f"/products/{self.pk}/"

    @property
    def body(self):
        return self.content

    def is_public(self) -> bool:
        # you can add logic here that would check other fields and switch public values as needed
        # example: if a current date is before a publish date... make this False
        # this would switch it to true on the publish date without us having to toggle anything
        return self.public #returns True or False

    def get_tags_list(self):
        return [random.choice(TAGS_MODEL_VALUES)]

    @property
    def sale_price(self):
        return "%.2f" %(float(self.price) * 0.8)

    def get_discount(self):
        return "122"