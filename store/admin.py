from django.contrib import admin
from .models import *
# Register your models here.


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3

class ProductReviewInline(admin.TabularInline):
    model = ProductReview
    extra = 3

class ProductInline(admin.StackedInline):
    model = Product
    extra = 1


class ProductInOrderInline(admin.TabularInline):
    model = ProductInOrder
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline,ProductReviewInline]
    list_display = ('name','description','price','sales')
    list_filter = ['name']
    search_filds=['name']
class BrandAdmin(admin.ModelAdmin):
    inlines = [ProductInline]
    list_filter = ['name']
    list_display = ('name','description','sales')
    search_filds = ['name']
class CategoryAdmin(admin.ModelAdmin):
    inlines = [ProductInline]
    list_filter = ['id','name']
    search_filds = ['name']
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','user','date','price')
    list_filter = ['date']
    search_filds = ['name']
    inlines = [ProductInOrderInline]

admin.site.register(Product, ProductAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ProductImage)
admin.site.register(UserInfo)