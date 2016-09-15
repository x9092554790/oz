$(document).ready(function(){
    var img_count = 1;
    var speed = 500;
    var cur_order = $('.quest-carousel-list img').data('img-order');
    getImgWithOrder(cur_order).css('z-index', 2);
    var quest_id = $('.quest-carousel').data('quest-id');
    var ul =  $('.quest-carousel-list');
    var orders = [cur_order];
    var is_animated = false;

    $.get('/quest/get_remain_imgs', {'quest_id': quest_id}).done(
        function(imgs)
        {
            var sorted = [];
            if(imgs)
            {
                for (var id in imgs)
                    sorted.push([id, imgs[id]['url'], imgs[id]['order'] ]);
                sorted.sort(function(a,b) {a[2] < b[2]});
            }

            for(var i = 0; i < sorted.length; i++)
            {
                var img_id = sorted[i][0];
                var url = sorted[i][1];
                var order = sorted[i][2];

                var img_ctrl = new Image();
                img_ctrl.src = url;
                img_ctrl.className += " quest-img";
                img_ctrl.style.zIndex="0";
                img_ctrl.setAttribute('data-img-order', order);
                orders.push(order);
                orders.sort(function(a,b){return a-b;});
                img_ctrl.onload = function()
                {
                    ul.append($(this));
                    img_count += 1;
                };
        }
    });

    function getImgWithOrder(o){
        return $('.quest-carousel-list img[data-img-order='+o+']');
    }

    function getNextOrder()
    {
        var id = orders.indexOf(cur_order);
        id += 1;
        if(id >= orders.length)
            id = 0;
        return orders[id];
    }

    function getPrevOrder()
    {
        var id = orders.indexOf(cur_order);
        id -= 1;
        if(id < 0)
            id = orders.length-1;
        return orders[id];
    }

    function showNext(e)
    {
        e.preventDefault();
        if(is_animated)
            return;
        var cur = getImgWithOrder(cur_order);
        var next_ord = $(this).hasClass('carousel-nav-left-bt') ? getPrevOrder() : getNextOrder();
        var next = getImgWithOrder(next_ord);
        next.css('z-index',1);
        is_animated = true;
        cur.animate({opacity: 0}, speed, function()
        {
            cur_order = next_ord;
            cur.css('z-index', 0);
            cur.css('opacity', 1);
            next.css('z-index', 2);
            is_animated = false;
        });
    }

    $('.carousel-nav-left-bt').click(showNext);
    $('.carousel-nav-right-bt').click(showNext);
});