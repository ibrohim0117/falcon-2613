import uuid
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify
from datetime import datetime, timedelta, timezone

from apps.models.base import BaseCreatedModel
from apps.models.user import Users


class Category(BaseCreatedModel):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    

class Tags(BaseCreatedModel):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
    

class Size(BaseCreatedModel):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
    

class Color(BaseCreatedModel):
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=50)

    def __str__(self):
        return self.name


    
class Product(BaseCreatedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=300, unique=True, editable=False)
    price = models.IntegerField()
    sale = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)], default=0)
    about = models.TextField()
    count = models.IntegerField()
    is_active = models.BooleanField(default=True)
    info = models.JSONField(default={
  "isbn": "978-9910-708-23-7",
  "yozuvi": "Lotincha",
  "yili": 2025,
  "tili": "O'zbekcha",
  "betlar_soni": 238,
  "nashriyot": "Yangi asr avlodi",
  "muqova": "Qattiq",
  "tarjimon": "Qodir Mirmuhammedov"
}
)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categores')
    tags = models.ManyToManyField(Tags, blank=True, null=True, related_name='tag_list')
    size = models.ManyToManyField(Size, blank=True, null=True)
    color = models.ManyToManyField(Color, blank=True, null=True)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        while Product.objects.filter(slug=self.slug).exists():
            slugger = str(uuid.uuid4()).split('-')[-1]
            self.slug = f"{slugify(self.name)}-{slugger}"

        return super().save(*args, **kwargs)
    

    @property
    def is_new(self):
        now = datetime.now(timezone.utc)
        farq = now - self.created_at
        # print(self.tags.all)
        
        if farq > timedelta(days=2):
            return False
        else:
            return True
    

    @property
    def sale_seller(self):
        return int(self.price - (self.price * self.sale / 100))
    
    class Meta:
        ordering = ['-created_at'] 
    

    def __str__(self):
        return self.name
    

class ProductImage(BaseCreatedModel):
    image = models.ImageField(upload_to='products/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.product.name
    


class ShoppingCart(BaseCreatedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_list')
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='my_carts')
    
    def __str__(self):
        return self.user.username
    
