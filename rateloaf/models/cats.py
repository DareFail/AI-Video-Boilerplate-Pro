from django.db import models


class CatLoaf(models.Model):
    is_rated = models.BooleanField(default=False)
    is_rating = models.BooleanField(default=False)
    has_cat_outline = models.BooleanField(default=False)
    unique_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=300, null=True, blank=True)
    only_cat_filter = models.IntegerField(null=True, blank=True)
    blemish_pass_1 = models.IntegerField(null=True, blank=True)
    blemish_pass_2 = models.IntegerField(null=True, blank=True)
    image_url_user = models.CharField(max_length=100)
    image_url_original = models.CharField(
        max_length=100, null=True, blank=True
    )
    image_url_blemish_1 = models.CharField(
        max_length=100, null=True, blank=True
    )
    image_url_blemish_2 = models.CharField(
        max_length=100, null=True, blank=True
    )
