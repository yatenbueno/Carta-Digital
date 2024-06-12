(function($) {
    "use strict";

    /*****************************
     * Commons Variables
     *****************************/
    var $window = $(window),
        $body = $('body');

    /****************************
     * Sticky Menu
     *****************************/
    $(window).on('scroll', function() {
        var scroll = $(window).scrollTop();
        if (scroll < 100) {
            $(".sticky-header").removeClass("sticky");
        } else {
            $(".sticky-header").addClass("sticky");
        }
    });

    $(window).on('scroll', function() {
        var scroll = $(window).scrollTop();
        if (scroll < 100) {
            $(".seperate-sticky-bar").removeClass("sticky");
        } else {
            $(".seperate-sticky-bar").addClass("sticky");
        }
    });


    /*****************************
     * Off Canvas Function
     *****************************/
    (function() {
        var $offCanvasToggle = $('.offcanvas-toggle'),
            $offCanvas = $('.offcanvas'),
            $offCanvasOverlay = $('.offcanvas-overlay'),
            $mobileMenuToggle = $('.mobile-menu-toggle');
        $offCanvasToggle.on('click', function(e) {
            e.preventDefault();
            var $this = $(this),
                $target = $this.attr('href');
            $body.addClass('offcanvas-open');
            $($target).addClass('offcanvas-open');
            $offCanvasOverlay.fadeIn();
            if ($this.parent().hasClass('mobile-menu-toggle')) {
                $this.addClass('close');
            }
        });
        $('.offcanvas-close, .offcanvas-overlay').on('click', function(e) {
            e.preventDefault();
            $body.removeClass('offcanvas-open');
            $offCanvas.removeClass('offcanvas-open');
            $offCanvasOverlay.fadeOut();
            $mobileMenuToggle.find('a').removeClass('close');
        });
    })();


    /**************************
     * Offcanvas: Menu Content
     **************************/
    function mobileOffCanvasMenu() {
        var $offCanvasNav = $('.offcanvas-menu'),
            $offCanvasNavSubMenu = $offCanvasNav.find('.mobile-sub-menu');

        /*Add Toggle Button With Off Canvas Sub Menu*/
        $offCanvasNavSubMenu.parent().prepend('<div class="offcanvas-menu-expand"></div>');

        /*Category Sub Menu Toggle*/
        $offCanvasNav.on('click', 'li a, .offcanvas-menu-expand', function(e) {
            var $this = $(this);
            if ($this.attr('href') === '#' || $this.hasClass('offcanvas-menu-expand')) {
                e.preventDefault();
                if ($this.siblings('ul:visible').length) {
                    $this.parent('li').removeClass('active');
                    $this.siblings('ul').slideUp();
                    $this.parent('li').find('li').removeClass('active');
                    $this.parent('li').find('ul:visible').slideUp();
                } else {
                    $this.parent('li').addClass('active');
                    $this.closest('li').siblings('li').removeClass('active').find('li').removeClass('active');
                    $this.closest('li').siblings('li').find('ul:visible').slideUp();
                    $this.siblings('ul').slideDown();
                }
            }
        });
    }
    mobileOffCanvasMenu();

    /********************************
     *   Product Slider - 3grids 1Row
     ********************************/
    var productSlider3grids1row = new Swiper('.product-item-slider-3grids-1row .swiper-container', {
        slidesPerView: 3,
        loop: true,
        autoplay: false,
        spaceBetween: 30,
        navigation: {
            nextEl: '.product-item-slider-3grids-1row .swiper-button-next',
            prevEl: '.product-item-slider-3grids-1row .swiper-button-prev',
        },

        breakpoints: {

            0: {
                slidesPerView: 1,
            },
            576: {
                slidesPerView: 1,
            },
            768: {
                slidesPerView: 2,
            },
            992: {
                slidesPerView: 3,
            },
        }
    });


    /********************************
     *  Testimonial Slider
     ********************************/
    var testimonial = new Swiper('.testimonial-slider .swiper-container', {
        slidesPerView: 1,
        loop: true,
        autoplay: false,
        spaceBetween: 30,
        pagination: {
            el: '.default-slider-pagination .swiper-pagination',
            clickable: true,
        },
    });


    /********************************
     *  About Slider
     ********************************/
    var about = new Swiper('.about-slider .swiper-container', {
        slidesPerView: 1,
        loop: true,
        autoplay: false,
        navigation: {
            nextEl: '.about-slider .swiper-button-next',
            prevEl: '.about-slider .swiper-button-prev',
        },
    });


    /********************************
    *  Parallax Motion Animation 
    *********************************/
   $('.scene').each(function () {
        new Parallax($(this)[0]);
    });

    /********************************
    *  Gallery Grid
    *********************************/
    // init Masonry
    var $grid = $('.gallery-grid').masonry({
        itemSelector: '.gallery-grid-single-item',
        percentPosition: true,
        columnWidth: '.grid-sizer',
    });
    // layout Masonry after each image loads
    $grid.imagesLoaded().progress( function() {
        $grid.masonry();
    });  

    /************************************************
     * Video  Popup
     ***********************************************/
    $('.venobox').venobox(); 

    /************************************************
     * Scroll Top
     ***********************************************/
    $('body').materialScrollTop();


})(jQuery);
