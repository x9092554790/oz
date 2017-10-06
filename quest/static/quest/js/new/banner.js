$(document).ready(function(){
    var mySwiper = new Swiper ('.swiper-container', {
        // Optional parameters
        loop: true,
        autoplay: 5000,
        paginationClickable: true,
        grabCursor: false,

        // If we need pagination
        pagination: '.swiper-pagination',

        // Navigation arrows
        nextButton: '.swiper-button-next',
        prevButton: '.swiper-button-prev',

        // And if we need scrollbar
        scrollbar: '.swiper-scrollbar',
      });

    function update_video()
    {
        $('.swiper-slide.swiper-slide-active video').each(function(){this.play()});
        $('.swiper-slide').not('.swiper-slide-active').find('video').each(function(){this.pause()});
    }

    mySwiper.on('slideChangeEnd', update_video);

    update_video()
});

