$(document).ready(function () {
    $('.single-select2-field').each(function () {
        $(this).select2({
            theme: 'bootstrap-5',
            language: 'ru'
        });
    });

    if (typeof currentUsername !== 'undefined' && currentUsername === 'test_vtb') {
        $('.sidebar-toggler').click()
        $('.sidebar-toggler').hide()
    }

    // Активация ближайшей формы
    $(".fileform-activator").each(function () {
        $(this).click(function () {
            var fileForm = $(this).parent().parent().find('input[type=file]');
            fileForm.click();
        })
        $(this).parent().parent().find('input[type=file]').change(function (event) {
            var files = event.target.files;
            if (files.length > 0) {
                var fileName = files[0].name;
                $(this).parent().find('input[type=text][disabled]').val(fileName);
                setTimeout(function () {
                    console.log(fileName);
                }, 100);

            }
        })
    })

});

// Основные функции сайта
(function ($) {
    "use strict";
    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();


    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({ scrollTop: 0 }, 300, 'swing');
        return false;
    });


    // Sidebar Toggler
    $('.sidebar-toggler').click(function () {
        if ($('.sidebar').hasClass('disabled')) {
            $('.sidebar, .content').removeClass('disabled');
        }
        $('.sidebar, .content').toggleClass("open");
        return false;
    });

    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: false,
        smartSpeed: 1000,
        items: 1,
        dots: true,
        loop: true,
        nav: false
    });

    // Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

})(jQuery);


