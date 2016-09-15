$(window).ready(function(){
    var uri = window.location.href;
    var anchor_regex = /#([a-z0-9\-\_]+)/i;
    var anchor = uri.match(anchor_regex);
    if(anchor && anchor.length > 1) {
        anchor = anchor[1];
        $('#discounts-list li#' + anchor).addClass('opened');
    }



    $('#discounts-list li').click(function(){
        var opened = $(this).hasClass('opened');
        $('#discounts-list li').removeClass('opened');
        if(!opened)
            $(this).addClass('opened');
    });
});
