import random
from core.models import Product, Category, Vendor,Cart,CartItem, CartOrder, \
CartOrderItems, ProductImages, ProductReview, Wishlist, Address
from django.db.models import Min, Max,Avg,Count
from django.contrib import messages
from taggit.models import Tag


def core_context(request):
	categories = Category.objects.annotate(product_count=Count('category'))
	vendors = Vendor.objects.all()

	min_max_price = Product.objects.aggregate(Min('price'), Max('price'))

	latest_products = Product.objects.filter(product_status='published')\
        .prefetch_related('category')\
        .annotate(
        average_rating=Avg('reviews__rating'),
        count=Count('reviews')  # Add this line to count reviews
    )\
        .order_by('-date')[:10]

	try:
		wishlist = Wishlist.objects.filter(user=request.user)
	except:
		wishlist = None

	all_product_tags = Tag.objects.filter(product__isnull=False).distinct()
	random_product_tags = random.sample(list(all_product_tags), min(6, len(all_product_tags)))

	# try:
	# 	address = Address.objects.get(user=request.user)
	# except:
	# 	address = None
	cart_item = None
	try:
		cart, created = Cart.objects.get_or_create(user=request.user)
		cart_item = CartItem.objects.filter(cart_id= cart.id).all()
	except:
		cart_item: None

	return {
		'categories': categories,
		'vendors': vendors,
		'wishlist': wishlist,
		# 'address': address,
		'min_max_price': min_max_price,
		'cart_item': cart_item,
		'latest_products': latest_products,
		'random_product_tags': random_product_tags,
	}