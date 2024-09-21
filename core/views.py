from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Avg, F, ExpressionWrapper, DecimalField
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from core.models import Product, Category, Vendor,Cart, CartItem, CartOrder, CartOrderItems, \
ProductImages, ProductReview, Wishlist, Address, ContactUs
from core.forms import ProductReviewFrom
from taggit.models import Tag

from django.views.decorators.cache import cache_page

@cache_page(60 * 10)  # Cache page for 10 minutes
def index(request):
    # Combine related queries to reduce DB hits
    featured_products = Product.objects.filter(product_status='published', featured=True)\
        .annotate(average_rating=Avg('reviews__rating'))
    
    special_offers = Product.objects.filter(product_status='published')\
        .annotate(
            discount_percentage=ExpressionWrapper(
                ((F('old_price') - F('price')) / F('old_price')) * 100,
                output_field=DecimalField()
            )
        ).order_by('-discount_percentage')[:9]
    
    oldest_products = Product.objects.filter(product_status='published').order_by('date')[:9]

    context = {
        "featured_products": featured_products,
        "special_offers": special_offers,
        "oldest_products": oldest_products,
    }
    
    return render(request, 'core/index.html', context)

def products_list_view(request):
	products = Product.objects.filter(product_status='published')
	categories = request.GET.getlist('category[]')
	vendors = request.GET.getlist('vendor[]')
	page_number = request.GET.get('page',1)
	min_price = request.GET.get('min_price')
	max_price = request.GET.get('max_price')
	if min_price or max_price:
		products = products.filter(price__gte=min_price)
		products = products.filter(price__lte=max_price)

	if categories:
		products = products.filter(category__id__in=categories).distinct()
	if len(vendors) > 0:
		products = products.filter(vendor__id__in=vendors).distinct()
	
	paginator = Paginator(products, per_page=5)

	try:
		page_object = paginator.get_page(page_number)
	except PageNotAnInteger:
		page_object = paginator.get_page(1)
	except EmptyPage:
        # If page is out of range deliver last page of results
		page_object = paginator.get_page(paginator.num_pages)

	context = {
		'page_object': page_object,
		'category' : categories
	}

	if request.headers.get('x-requested-with') == 'XMLHttpRequest':
		toolbox = render_to_string('partials/toolbox.html', context)
		product_list = render_to_string('partials/product-list.html', context)
		pagination = render_to_string('partials/pagination.html', context)

		return JsonResponse({
			'toolbox': toolbox,
			'html': product_list,
			'pagination':pagination
			})
	
	return render(request, 'core/product-list.html', context)

def category_list_view(request):
	categories = Category.objects.all()
	context = {
		"categories": categories,
	}
	return render(request, 'core/category-list.html', context)

def category_product_list_view(request, cid):
	category = Category.objects.get(cid=cid)
	products = Product.objects.filter(product_status='published', category=category)
	context = {
		"category": category,
		"products": products,
	}
	return render(request, 'core/category-products-list.html', context)

def vendor_list_view(request):
	vendors = Vendor.objects.all()
	context = {
		'vendors': vendors,
	}
	return render(request, 'core/vendor-list.html', context)

def vendor_detail_view(request, vid):
	vendor = Vendor.objects.get(vid=vid)
	products = Product.objects.filter(product_status='published', vendor=vendor)
	context = {
		'vendor': vendor,
		'products': products,
	}
	return render(request, 'core/vendor-detail.html', context)

def product_detail_view(request, pid):
	product = Product.objects.get(pid=pid)
	# product = get_object_or_404(Product, pid=pid)
	products = Product.objects.filter(category=product.category).exclude(pid=pid)
	p_image = product.p_images.all()

	reviews = ProductReview.objects.filter(product=product).order_by('-date')
	average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
	review_form = ProductReviewFrom()

	make_review = True
	if request.user.is_authenticated:
		user_review_count = ProductReview.objects.filter(user=request.user, product=product).count() 

		if user_review_count > 0:
			make_review = False

	context = {
		'product': product,
		'p_image': p_image,
		'products': products,
		'reviews': reviews,
		'average_rating': average_rating,
		'review_form': review_form,
		'make_review': make_review,
	}
	return render(request, 'core/product-detail.html', context)

def tags_list(request, tag_slug=None):
	products = Product.objects.filter(product_status='published').order_by('-id')

	tag = None
	if tag_slug:
		tag = Tag.objects.get(slug=tag_slug)
		# tag = get_object_or_404(Tag, slug=tag_slug)
		products = products.filter(tags__in=[tag])

	context = {
		'products': products,
		'tag': tag,
	}

	return render(request, 'core/tag.html', context)

def ajax_add_review(request, pid):
	product = Product.objects.get(pk=pid)
	user = request.user
	image = user.image.url

	if request.user.is_authenticated:
		user_review_count = ProductReview.objects.filter(user=request.user, product=product).count() 

		if user_review_count > 0:
			make_review = False
		else:
			review = ProductReview.objects.create(
			user=user,
			product=product,
			review=request.POST['review'],
			rating=request.POST['rating'],
		)
	
	context = {
		'user': user.username,
		'review': request.POST['review'],
		'rating': request.POST['rating'],
		'image': image
	}

	average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))

	
	return JsonResponse(
		{
			'bool': True,
			'context': context,
			'average_reviews': average_reviews,
		}
	)

def search_view(request):
	# query = request.GET['q'] OR
	query = request.GET.get('q') 

	products = Product.objects.filter(title__icontains=query).order_by('-date')

	context = {
		'products': products,
		'query': query,
	}

	return render(request, 'core/search.html', context)

def filter_product(request):
	categories = request.GET.getlist('category[]')
	vendors = request.GET.getlist('vendor[]')

	min_price = request.GET.get('min_price')
	max_price = request.GET.get('max_price')

	products = Product.objects.filter(product_status='published').order_by('-id').distinct()

	products = products.filter(price__gte=min_price)
	products = products.filter(price__lte=max_price)

	if len(categories) > 0:
		products = products.filter(category__id__in=categories).distinct()
	if len(vendors) > 0:
		products = products.filter(vendor__id__in=vendors).distinct()

	paginator = Paginator(products, per_page=5)

	try:
		page_object = paginator.get_page(1)
    
	except PageNotAnInteger:
		page_object = paginator.get_page(1)
    
	except EmptyPage:
        # If page is out of range deliver last page of results
		page_object = paginator.get_page(paginator.num_pages)

	context = {
		'page_object': page_object,
	}
	toolbox = render_to_string('partials/toolbox.html', context)
	product_list = render_to_string('partials/product-list.html', context)
	pagination = render_to_string('partials/pagination.html', context)

	return JsonResponse({
		'toolbox': toolbox,
		'html': product_list,
		'pagination':pagination
		})


#### Cart Views ##########

def get_or_create_cart(user):
	if user.is_authenticated:
		cart, created = Cart.objects.get_or_create(user=user)
	else:
		cart = Cart.objects.get_or_create(user=None)[0]
	return cart


def cart_view(request):
	try:
		cart = get_or_create_cart(request.user)
		context = {
			'cart': cart,
			'cart_items': cart.items.all(),
			'cart_total': cart.total_price
		}
	except:
		context = {
		}
		cart = None
	return render(request, 'core/cart.html', context)

def add_to_cart(request):
	product_id = request.GET['id']
	try:
		quantity = int(request.GET['qty'])
	except:
		quantity = 1
	product = Product.objects.get(id=product_id)
	cart, created = Cart.objects.get_or_create(user=request.user)
	cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

	context = { 
		'totalcartitems': cart.unique_product_count
	}
	if created:
		cart_item.quantity = quantity
	else:
		cart_item.quantity += quantity
	cart_item.save()
	return JsonResponse(context)


def delete_from_cart(request):
	product_id = request.GET['id']
	cart = get_or_create_cart(request.user)
	product = get_object_or_404(Product, pid = product_id)
	cart_item= CartItem.objects.filter(cart_id=cart.id, product=product).first()
	if cart_item:
		cart_item.delete()

	count = cart.unique_product_count
	context = {
			'cart_items': cart.items.all(),
			'cart_total': cart.total_price,
		}
	
	cart = render_to_string('partials/cart.html', context)
	cart_summary = render_to_string('partials/cart_summary.html', context)

	return JsonResponse({
		'cart': cart,
		'cart_summary': cart_summary,
		'totalcartitems': count
	})

def update_cart(request):
	items = request.GET.getlist('items[]')
	for item in items:
		item_id, quantity = item.split('|')
		cart_item = get_object_or_404(CartItem, id = item_id)
		cart_item.quantity = int(quantity)
		cart_item.save()
	cart = get_or_create_cart(request.user)

	count = cart.unique_product_count
	context = {
			'cart_items': cart.items.all(),
			'cart_total': cart.total_price,
		}
	
	cart = render_to_string('partials/cart.html', context)
	cart_summary = render_to_string('partials/cart_summary.html', context)

	return JsonResponse({
		'cart': cart,
		'cart_summary': cart_summary,
		'totalcartitems': count
	})

###### Cart View Ends ##############

@login_required
def wishlist_view(request):
	try:
		wishlist = Wishlist.objects.filter(user=request.user)
	except:
		wishlist = None

	context = {
		'wishlist': wishlist
	}
	return render(request, 'core/wishlist.html', context)

@login_required
def add_to_wishlist(request):
	product_id = request.GET['id']
	product = Product.objects.get(id=product_id)

	context = {}

	wishlist_count = Wishlist.objects.filter(product=product, user=request.user).count()

	if wishlist_count > 0:
		context	= {
			'bool': True,
			'wishlist_count': Wishlist.objects.filter(user=request.user).count()
		}
	else:
		new_wishlist = Wishlist.objects.create(
			product=product,
			user=request.user
		)
		context = {
			'bool': True,
			'wishlist_count': Wishlist.objects.filter(user=request.user).count()
		}

	return JsonResponse(context)

def remove_from_wishlist(request):
	product_id = request.GET['id']
	wishlist = Wishlist.objects.filter(user=request.user)

	product = Wishlist.objects.get(id=product_id)
	product.delete()

	context = {
		'bool': True,
		'wishlist': wishlist
	}
	qs_json = serializers.serialize('json', wishlist)
	data = render_to_string('core/async/wishlist-list.html', context)
	wishlist_count = Wishlist.objects.filter(user=request.user).count()
	return JsonResponse({'data': data, 'wishlist': qs_json, 'wishlist_count':wishlist_count})

def contact(request):
	return render(request, 'core/contact.html')

def ajax_contact_form(request):
	name = request.GET['name']
	email = request.GET['email']
	message = request.GET['message']
	phone = request.GET['message']
	subject = request.GET['message']
	
	contact = ContactUs.objects.create(
		name=name,		
		email=email,	
		phone=phone,
		subject=subject,	
		message=message,		
	)

	data = {
		'bool': True,
	}

	return JsonResponse({'data': data})

def about(request):
	return render(request, 'core/about.html')


def error_404(request, exception):
	return render(request, 'core/404.html',status=404)

def error_500(request):
	return render(request, 'core/404.html', status =500)