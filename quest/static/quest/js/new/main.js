$(document).ready(function(){
	$( "header .fa-bars" ).click(function() {
		$( "nav ul" ).slideToggle();
	});

	$( "footer .fa-bars" ).click(function() {
		$( ".nav" ).slideToggle();
	});

    var phone_states = {work: 2000, delay: 10000};
    var phone_state = phone_states.delay;
    var phone_timer = null;

    function phone_timer_callback()
    {
        if(phone_timer) {
            clearInterval(phone_timer);
            phone_state = phone_state == phone_states.delay ? phone_states.work : phone_states.delay;
            var p = $('nav a.phone');

            if(phone_state == phone_states.work)
                p.addClass('anim');
            else
                p.removeClass('anim');
        }

        phone_timer = setInterval(phone_timer_callback, phone_state);
    }

    phone_timer_callback();

    var visitors_notify_time = 5000;
    var visitors_notify_timer = setInterval(function(){
        $.get("/ajax_get_visitors", function(data){
            if(data) {
                common.funcs.notify("Сейчас вместе с Вами квестами интересуются " + data['visitors'] +" человек");
            }
        });

        clearInterval(visitors_notify_timer);
    }, visitors_notify_time);

    if(!common.funcs.isMobile())
    {
        $('.tooltip_container').mouseleave(function(){
            var tooltip = $(this).find('.tooltip');
            tooltip.hide();
            return false;
        }).mouseenter(function(){
            var tooltip = $(this).find('.tooltip');
            tooltip.show();
            return false;
        });
    }


     $('.tooltip_container').click(function(e){
        e.preventDefault();
        var tooltip = $(this).find('.tooltip');
        if(tooltip.is(":visible"))
            tooltip.hide();
        else
            tooltip.show();
         return false;
    });
    $('.tooltip_container .tooltip').click(function(e){
        e.preventDefault();
        $(this).hide();
        return false;
    });

    $('.btn[data-href]').click(function(e){
        e.preventDefault();
        e.stopImmediatePropagation();
        var url = $(this).attr('data-href');
        window.location = url;
        return false;
    });
});