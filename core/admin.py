from django.contrib import admin
from core.models import Product, Category, Vendor,Brand,Cart,CartItem, CartOrder, CartOrderItems, \
ProductImages, ProductReview, Wishlist, Address, ContactUs

class ProductImagesAdmin(admin.TabularInline):
	model = ProductImages

class ProductAdmin(admin.ModelAdmin):
	inlines = [ProductImagesAdmin]
	list_display = ['user', 'title', 'product_image', 'price','category', 'brand','featured', 'product_status', 'pid']

class CategotyAdmin(admin.ModelAdmin):
	list_display = ['title', 'category_image', 'cid']

class VendorAdmin(admin.ModelAdmin):
	list_display = ['title', 'vendor_image', 'vid']

class Branddmin(admin.ModelAdmin):
	list_display = ['title', 'brand_image', 'bid']

class CartAdmin(admin.ModelAdmin):
	list_display = ['user', 'created_at', 'updated_at']

class CartItemAdmin(admin.ModelAdmin):
	list_display = ['product', 'added_at']

class CartOrderAdmin(admin.ModelAdmin):
	list_display = ['user', 'price', 'paid_status', 'order_date', 'product_status']

class CartOrderItemsAdmin(admin.ModelAdmin):
	list_display = ['order', 'invoice_no', 'item', 'image', 'qty', 'price', 'total']

class ProductReviewAdmin(admin.ModelAdmin):
	list_display = ['user', 'product', 'rating']

class WishlistAdmin(admin.ModelAdmin):
	list_display = ['user', 'product', 'date']

# class AddressAdmin(admin.ModelAdmin):
# 	list_display = ['user', 'address', 'status']

class ContactUsAdmin(admin.ModelAdmin):
	list_display = ['name', 'email','message']

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategotyAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Brand, Branddmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
# admin.site.register(CartOrder, CartOrderAdmin)
# admin.site.register(CartOrderItems, CartOrderItemsAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Wishlist, WishlistAdmin)
# admin.site.register(Address, AddressAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
