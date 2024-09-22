import random
from core.models import Product, Category, Vendor,Cart,CartItem, CartOrder, \
CartOrderItems, ProductImages, ProductReview, Wishlist, Address
from django.db.models import Min, Max,Avg,Count
from django.contrib import messages
from taggit.models import Tag


def core_context(request):
    categories = Category.objects.annotate(product_count=Count('category'))
    vendors = Vendor.objects.all()

    latest_products = Product.objects.filter(product_status='published').prefetch_related('category') \
        .annotate(
            average_rating=Avg('reviews__rating'),
            review_count=Count('reviews')  # Count reviews
        ).order_by('-date')[:10]

    wishlist = None
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user)

    all_product_tags = Tag.objects.filter(product__isnull=False).distinct()
    random_product_tags = random.sample(list(all_product_tags), min(6, len(all_product_tags)))

    cart_item = None
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get_or_create(user=request.user)[0]
            cart_item = CartItem.objects.filter(cart=cart).all()
        except Cart.DoesNotExist:
            cart_item = None

    return {
        'categories': categories,
        'vendors': vendors,
        'wishlist': wishlist,
        'cart_item': cart_item,
        'latest_products': latest_products,
        'random_product_tags': random_product_tags,
    }