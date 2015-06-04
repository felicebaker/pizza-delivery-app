// Use ES6 javascript, auto transpiled into ES5 - see http://babeljs.io
//
// jQuery already loaded as external Browserify dependency, availble here as $
//
// Pizza Impulse Main Entrypoint
//
require('./vendor/swiper.jquery.min')
require('./vendor/jquery.autotab')
require('./vendor/jquery.is')

if($('.promo').length > 0) {
    var tourSwiper = new Swiper('.swiper-container', {
        pagination: '.swiper-pagination'
    })
}

$('.js-delivery-times-toggle').on('click', function(ev) {
    $(this).parent('.preferences-folder').toggleClass('is-open')
    $(this).siblings('.preferences-folder__content').slideToggle()
})

$('.js-time-selector-toggle').on('click', function(ev) {
    $('.time-selector').slideToggle()
})

$('.js-day-selector-toggle').on('click', function(ev) {
    // we can't stopPropagation and preventDefault here as that stops
    // the default label:checked behaviour - therefore we need to manually
    // simulate a slideToggle() call to prevent on click event firing twice
    if ($(this).data('isOpen') === true) {
        $(this).parent().siblings('.time-selector__times').slideUp()
        $(this).data('isOpen', false)
    } else {
        $(this).parent().siblings('.time-selector__times').slideDown()
        $(this).data('isOpen', true)
    }
})

$('.js-creditcard-autotab').autotab({
    format: 'number',
    maxlength: 4
})

$('.js-creditcard-year').on('change', function() {
    if ($(this).is(/\d{4}/)) {
        $(this).removeClass('is-error')
    } else {
        $(this).addClass('is-error')
    }
})

$('.js-creditcard-pin').on('change', function() {
    if ($(this).is(/\d{3}/)) {
        $(this).removeClass('is-error')
    } else {
        $(this).addClass('is-error')
    }
})
