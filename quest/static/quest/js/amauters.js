/**
 * Created by Adm on 05.08.2016.
 */
$(document).ready(function(){
    var animate_interval = 10;

    $( window ).resize(function() {
      update_block1_size();
    });

    function update_block1_size()
    {
        var wh = $(window).height();
        var navh = 54;//$('header').first().outerHeight();
        // var padh = parseInt($('.main-content').css('padding-top').replace("px",""));
        $("#block1").height(wh-navh);
    }

    function animate_cycle_backgrounds() {
         $('.cycle-background').animate({'background-position-x': '-=1px'}, animate_interval, animate_cycle_backgrounds);
    }

    $('#next-bt-1').click(function(){
        var navh = 54;//$('header').first().outerHeight();
        $("html, body").animate({ scrollTop: $('#block2').offset().top - navh }, 1000);
        return false;
    });

    update_block1_size();
    animate_cycle_backgrounds();

    common.carousel.Carousel({container: document.getElementById('carousel-1')});
    common.carousel.Carousel({container: document.getElementById('carousel-2')});
    common.carousel.Carousel({container: document.getElementById('carousel-3')});
});
