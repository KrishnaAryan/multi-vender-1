from django.contrib import admin
from .models import *
# Register your models here.

class ProductImg(admin.TabularInline):
    model=ProductImage
    
class AdditionalInfo(admin.TabularInline):
    model=AdditionalInformation
    
class ProductAdmin(admin.ModelAdmin):
    inlines=(ProductImg,AdditionalInfo)
    list_display=('product_name','price','categories','section',)
    list_editable=('categories','section',)
    

admin.site.register(slider)
admin.site.register(banner_area)
admin.site.register(MainCategory)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Section)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(AdditionalInformation)


admin.site.register(CouponCode)
