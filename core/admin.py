from django.contrib import admin
from core.models import Product, Category, Vendor,Brand,Cart,CartItem, CartOrder, CartOrderItems, \
ProductImages, ProductReview, Wishlist, Address, ContactUs, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')  # Display essential fields
    search_fields = ('username', 'email')  # Enable search on relevant fields

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('profile').prefetch_related('groups', 'user_permissions')
	
class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['user', 'title', 'product_image', 'price', 'category', 'brand', 'featured', 'product_status', 'pid']
    list_select_related = ['user', 'category', 'vendor']  # Add related fields here

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category_image', 'cid']
    list_select_related = []  # Add related fields if needed

class VendorAdmin(admin.ModelAdmin):
    list_display = ['title', 'vendor_image', 'vid']
    list_select_related = []  # Add related fields if needed

class BrandAdmin(admin.ModelAdmin):
    list_display = ['title', 'brand_image', 'bid']
    list_select_related = []  # Add related fields if needed

class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'updated_at']
    list_select_related = ['user']  # Add related fields if needed

class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'added_at']
    list_select_related = ['product']  # Add related fields if needed

class CartOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'price', 'paid_status', 'order_date', 'product_status']
    list_select_related = ['user']  # Add related fields if needed

class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ['order', 'invoice_no', 'item', 'image', 'qty', 'price', 'total']
    list_select_related = ['order', 'item']  # Add related fields if needed

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating']
    list_select_related = ['user', 'product']  # Add related fields if needed

class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'date']
    list_select_related = ['user', 'product']  # Add related fields if needed

class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'message']
    list_select_related = []  # Add related fields if needed

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
# admin.site.register(CartOrder, CartOrderAdmin)
# admin.site.register(CartOrderItems, CartOrderItemsAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Wishlist, WishlistAdmin)
# admin.site.register(Address, AddressAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
