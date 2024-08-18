
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

	// Filter

	$('.filter-checkbox, #price-filter-btn').on('click', function(){
		// console.log('Its working Cliked..');
		var slider  = document.getElementById('price-slider');
		var sliderValues =slider.noUiSlider.get();
		let filter_object = {}
		let min_price =sliderValues[0].replace('$','');
		let max_price = sliderValues[1].replace('$','');

		filter_object.min_price = min_price
		filter_object.max_price = max_price

		$('.filter-checkbox').each(function(){
			let filter_value = $(this).val()
			let filter_key = $(this).data('filter')

			filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter='+ filter_key +']:checked')).map(function(element){
				return element.value
			})
		})
		// console.log('Filter Object is:', filter_object);
		$.ajax({
			url: '/filter-product',
			data: filter_object,
			dataType: 'json',
			beforeSend: function(){
				console.log('Trying to filter products...')
			},
			success: function(response){
				console.log(response)
				// console.log('Data filtered successfully')
				$('#filtered-product').html(response.data)
			}
		})
	})

	$("#max_price").on('blur', function(){
		let min_price = $(this).attr('min')
		let max_price = $(this).attr('max')
		let current_price = $(this).val()

		// console.log('current_price is:', current_price);
		// console.log('min_price is:', min_price);
		// console.log('max_price is:', max_price);

		if(current_price < parseInt(min_price) || current_price > parseInt(max_price)){
			// console.log('Price Error Occured')

			min_Price = Math.round(min_price * 100) / 100
			max_Price = Math.round(max_price * 100) / 100

			// console.log('Min price is:', min_Price)
			// console.log('Max price is:', max_Price)

			alert('Price must between $' +min_Price + ' and $' +max_Price)
			$(this).val(min_Price)
			$('#range').val(min_Price)

			$(this).focus()

			return false
		}
	})

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
