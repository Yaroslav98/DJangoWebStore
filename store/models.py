from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

def brand_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/brand_<id>/<filename>
    return 'brand_{0}/{1}'.format(instance.id, filename)


def category_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/category_<id>/<filename>
    return 'category_{0}/{1}'.format(instance.id, filename)


def product_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/product_<id>/<filename>
    return 'product_{0}/{1}'.format(instance.product.id, filename)

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Brand(models.Model):
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    h1 = models.CharField(max_length=50)
    description = models.TextField()
    sales = models.IntegerField(default=0)
    image = models.ImageField(upload_to=brand_directory_path)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    h1 = models.CharField(max_length=50)
    image = models.ImageField(upload_to=category_directory_path)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    h1 = models.CharField(max_length=50)
    description = models.TextField()
    category = models.ForeignKey(Category,null=True,on_delete=models.SET_NULL)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    sales = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=15,decimal_places=2)
    rate=models.FloatField(null=True,default=None)
    def __str__(self):
        return self.name


class ProductReview(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    rating = models.IntegerField()
    text = models.TextField()

    def __str__(self):
        return str(self.product.id) + str(self.user.id)

def product_review_post_save(sender,instance,created,**kwargs):
    product=instance.product
    all_product_reviews=ProductReview.objects.filter(product=product)
    product_rate=0
    count=len(all_product_reviews)
    for item in all_product_reviews:
        product_rate+=item.rating
    product_rate=product_rate/count
    instance.product.rate=round(product_rate,1)
    instance.product.save(force_update=True)

post_save.connect(product_review_post_save,sender=ProductReview)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=product_directory_path)
    is_main = models.BooleanField()

    def __str__(self):
        return str(self.product_id)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title=models.CharField(max_length=50)
    h1=models.CharField(max_length=50)
    date = models.DateField(auto_now=False,auto_now_add=True)
    price = models.DecimalField(max_digits=15,decimal_places=2,default=0)
    products = models.ManyToManyField(Product,through="ProductInOrder")

    def __str__(self):
        return str(self.id)

    def save(self,*args,**kwargs):
        self.title="Order №"+str(self.id)
        self.h1="Order №"+str(self.id)
        super(Order,self).save(*args,**kwargs)

class ProductInOrder(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    price=models.DecimalField(max_digits=15,decimal_places=2,default=1)

    def __str__(self):
        return str(self.order.id)

def product_in_order_post_save(sender,instance,created,**kwargs):
    #order_price_update
    order=instance.order
    all_products_in_order=ProductInOrder.objects.filter(order=order)
    order_price=0
    for item in all_products_in_order:
        order_price+=item.price
    instance.order.price=order_price
    instance.order.save(force_update=True)
    #product_sales_update
    instance.product.sales+=instance.count
    instance.product.save(force_update=True)
    #manufacturer_sales_update
    instance.product.brand.sales+=instance.count
    instance.product.brand.save(force_update=True)


post_save.connect(product_in_order_post_save,sender=ProductInOrder)


class UserInfo(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    info=models.TextField(null=True,blank=True)
    regdate=models.DateField(auto_now_add=True,auto_now=False)
    phonenumber=models.CharField(max_length=25,null=True,blank=True)
    photo=models.ImageField(upload_to=user_directory_path,default='default_user_icone.jpg')

    def __str__(self):
        return str(self.id)

    @receiver(post_save,sender = User)
    def create_user_profile(sender, instance,created,**kwargs):
        if created:
            UserInfo.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userinfo.save()
