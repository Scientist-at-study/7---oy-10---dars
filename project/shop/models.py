from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse_lazy
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to="category/image/", null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        if not self.parent:
            return self.name
        return f"{self.parent.name}: {self.name}"

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return ("https://img.tamindir.com/ti_e_ul/BarisYanik/h/kaybolan-yada-silinen-web-sayfalarini-bulma"
                    "-1_640x360.png")


class Additional(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


VOLUMES = {
    "kg": "Kilogram",
    "l": "Litr",
    "dona": "Dona"
}


class Product(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    quantity = models.IntegerField(default=50)
    volume = models.CharField(max_length=4, choices=VOLUMES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    additional = models.ForeignKey(Additional, on_delete=models.PROTECT, related_name='products')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('product_detail', kwargs={'product_id': self.pk})

    def get_discounted_price(self):
        if self.discount > 0:
            discounted_price = self.price * (1 - self.discount / 100)
            return round(discounted_price, 2)
        return self.price


class ProductImage(models.Model):
    image = models.ImageField(upload_to="products/images/")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")

    def __str__(self):
        return self.product.name


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Author")
    comment = models.TextField(verbose_name="Comment by author")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}: {self.comment[:30]}..."
