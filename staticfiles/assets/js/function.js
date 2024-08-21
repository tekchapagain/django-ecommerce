
const monthNames = ["Jan", "Feb", "Mar", "April", "May",
	"June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"];


$('#commentForm').submit(function(e){
	e.preventDefault();

	let dt = new Date();
	let time = dt.getDate() + " " + monthNames[dt.getUTCMonth()] + ", " + dt.getFullYear();

	$.ajax({
		data: $(this).serialize(),

		method: $(this).attr('method'),

		url: $(this).attr('action'),

		dataType: 'json',

		success: function(res){
			console.log('Comment saved to DB!..');

			if(res.bool == true){
				$('#reviewRes').html('Review Added Successfully!')
				$('.hide-review').hide()
				$('.add-review').hide()

				let _html = '<div class="comment-block">'
					_html += '<img src="' + res.context.image + '" alt="User" style="width: 55px; height: 55px;">'
					_html += '<span>'+ res.context.user +'</span>'
					_html += '<span> - </span>'
					_html += '<span>'+ time +'</span>'
					_html += '<span> - </span>'

					for(let i = 1; i<=res.context.rating; i++){
						_html += '<i class="fas fa-star"></i>'
					}

					_html += '<p>'+ res.context.review +'</p>'

					_html += '</div>'

					$('.reviews-block').prepend(_html)
			}			
		}
	})
})


$(document).ready(function (){

	 // Handle filtering and price button click
	 $('.filter-checkbox, #price-filter-btn').on('click', function(){
        applyFilters(1);  // Apply filters and load the first page
    });

    // Handle pagination click
    $(document).on('click', '.pagination a', function(e){
        e.preventDefault();  // Prevent default link behavior
        let page = $(this).attr('data-page');
        applyFilters(page);  // Apply filters for the selected page
    });

    function applyFilters(page) {
        var slider  = document.getElementById('price-slider');
        var sliderValues = slider.noUiSlider.get();
        let filter_object = {};
        let min_price = sliderValues[0].replace('$','');
        let max_price = sliderValues[1].replace('$','');

        filter_object.min_price = min_price;
        filter_object.max_price = max_price;
        filter_object.page = page; 

        $('.filter-checkbox').each(function(){
            let filter_value = $(this).val();
            let filter_key = $(this).data('filter');

            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter=' + filter_key + ']:checked')).map(function(element){
                return element.value;
            });
        });

        console.log('Filter Object is:', filter_object);

        $.ajax({
            url: '/products',
            data: filter_object,
            dataType: 'json',
            beforeSend: function(){
                console.log('Filtering products...')
            },
            success: function(data){
                console.log(data);
                $('#toolbox').html(data.toolbox);
                $('#filtered-product').html(data.html);
                $('#pagination').html(data.pagination);
            }
        });
	}

	$(document).on('submit', '#ajax-contact-form', function(e){
		e.preventDefault()
	
		let name = $('#name').val()
		let email = $('#email').val()
		let message = $('#message').val()
		let phone = $('#phone').val()
		let subject = $('#subject').val()
	
		$.ajax({
			url: '/ajax-contact-form',
			data: {
				'name': name,
				'email': email,
				'message': message,
				'phone' : phone,
				'subject':subject
			},
			dataType: 'json',
			beforeSend: function(){
				console.log('Sending data to server...')
			},
			success: function(response){
				console.log('Data send to server successfully.')
				$('#ajax-contact-form')[0].reset();
				$('#ajax-contact-form').hide()
				$('.contact__form__title').html('<p>Form submitted successfully!</p>')
			}
		})
	})
})

$('.btn-cart').on('click', function(){

    let this_val = $(this)
    let index = this_val.attr('data-index')

    let quantity = $('#qty').val()
    let id = $('#product-id').val()
    let title = $('#product-title').val()
    let price = $('#product-price').val()
    let pid = $('#product-pid').val()
    let image = $('#product-image').val()
    data ={
        'id': id,
        'pid': pid,
        'qty': quantity,
        'title': title,
        'price': price,
        'image': image,
    }
    console.log(data)
    $.ajax({
        url: '/add-to-cart',
        data: {
            'id': id,
            'pid': pid,
            'qty': quantity,
            'title': title,
            'price': price,
            'image': image,
        },
        dataType: 'json',
        beforeSend: function(){
            console.log('Adding product to cart...')
        },
        success: function(response){
            this_val.html('<i class="fa fa-check"></i>')
            console.log('Added product to cart.')
            $('.cart-items-count').text(response.totalcartitems)
        },
    })
})

// Delete from cart

$(document).on('click', '.delete-product', function(){


    let product_id = $(this).attr("data-product")
    let this_val = $(this)

    $.ajax({
        url: '/delete-from-cart',
        data: {
            'id': product_id,
        },
        dataType: 'json',
        beforeSend: function(){
            this_val.hide()
        },
        success: function(response){
            this_val.show()
            $('.cart-items-count').text(response.totalcartitems)
            $('#cart-list').html(response.data)
        }
    })
})

// Update products

$(document).on('click', '.update-product', function(){

    let productIds = [];
    $('.product-list').each(function(){
        productIds.push($(this).data('product-id'));
    });
    console.log(productIds)
    let product_id = $(this).attr("data-product")
    let this_val = $(this)
    let product_quantity = $('.product-qty-' + product_id).val()
    

    $.ajax({
        url: '/update-cart',
        data: {
            'id': productIds,
            'qty': product_quantity,
        },
        dataType: 'json',
        beforeSend: function(){
            console.log("Updating prices.....")
        },
        success: function(response){
            this_val.show()
            $('#cart-list').html(response.data)
        }
    })
})


$(document).on('click', '.add-to-wishlist', function(){
    let product_id = $(this).attr('data-product-item')
    let this_val = $(this)

    $.ajax({
        url: '/add-to-wishlist',
        data: {
            'id': product_id,
        },
        dataType: 'json',
        beforeSend: function(){
            console.log('Saving to wishlist...')
        },
        success: function(response){
            if (response.bool === true) {
                this_val.html('<span>Add to Wishlist</span>')
                $('.wishlist-items-count').text(response.wishlist_count)
            }
        }
    })
})

$(document).on('click', '.delete-wishlist-product', function(){
    let wishlist_id = $(this).attr("data-wishlist-product")
    let this_val = $(this)

    console.log('id', wishlist_id)

    $.ajax({
        url: '/remove-from-wishlist',
        data: {
            'id': wishlist_id,
        },
        dataType: 'json',
        beforeSend: function(){
            console.log('Deleting from wishlist...')
        },
        success: function(response){
            console.log(response.data)
            $('.wishlist-items-count').text(response.wishlist_count)
            $('#wishlist-list').html(response.data)
        }
    })
})
