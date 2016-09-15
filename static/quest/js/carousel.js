/**
 * Created by Adm on 08.08.2016.
 */
if (typeof common == 'undefined')
  common = {};
if (typeof common.carousel == 'undefined')
  common.carousel = {};

(function(){
    var _carousel_item_class = '.quest-carousel-item';
    var _carousel_left = '.quest-carousel-left';
    var _carousel_right = '.quest-carousel-right';
    var _this = this;

    function _getItems(container)
    {
        var order_min = null;
        var order_max = null;
        var carousel_items = [];

        container.find(_carousel_item_class).each(function() {
            var order = $(this).data('order');
            carousel_items.push([order, $(this)]);
            if(order_min == null)
                order_min = order;
            else if(order < order_min)
                order_min = order;

            if(order_max == null)
                order_max = order;
            else if(order > order_max)
                order_max = order;

        });

        return [order_min, carousel_items, order_max];
    }

    function _getElementAtOrder(container, order)
    {
        return container.find(_carousel_item_class + '[data-order="'+order+'"]').first();
    }

    function _createHandler(node, type, callback) {

        if(node instanceof jQuery && node.length > 0)
            node = node[0];
        node.addEventListener(type, function(e) {
            e.target.removeEventListener(e.type, arguments.callee);
            return callback(e);
        });

    }

    this.Carousel = function(options)
    {
        return new Carousel(options);
    }

    function Carousel(options) {
        if (!(this instanceof Carousel))
            return new Carousel(options);

        if(options.container && options.container instanceof jQuery)
            this.container = options.container;
        else if(options.container)
            this.container = $(options.container);
        var items = _getItems(this.container);
        var order_min = items[0];
        var order_max = items[2];
        items = items[1];
        var _this = this;

        if(options.order == 'asc')
            this.cur_item = [order_min, _getElementAtOrder(this.container, order_min)];
        else if(options.order == 'desc')
            this.cur_item = [order_max, _getElementAtOrder(this.container, order_max)];
        else {
            var order = common.funcs.getRandomInt(order_min, order_max);
            this.cur_item = [order, _getElementAtOrder(this.container, order)];
        }

        this.cur_item[1].addClass('active');
        this.animating = false;

        this.container.find(_carousel_left).click(function(){
            _this.prev();
        });

        this.container.find(_carousel_right).click(function(){
            _this.next();
        });
    }

    Carousel.prototype = {
        next: function() {
            return this._cycle_carousel(false, true);
        },
        prev: function() {
            return this._cycle_carousel(true, false);
        },
        _cycle_carousel: function(left = false, right = false)
        {
            if(this.animating)
                return;

            this.animating = true;
            var next = null;
            var min = null;
            var max = null;
            var carousel_items = _getItems(this.container)[1];
            var _this = this;

            for(var i = 0; i < carousel_items.length; i++) {
                if(carousel_items[i][1].find('img:first-child').attr('src') == this.cur_item[1].find('img:first-child').attr('src'))
                    continue;
                if (left) {
                    if(carousel_items[i][0] < this.cur_item[0] && (next && carousel_items[i][0] > next[0] || next == null))
                        next = carousel_items[i];
                }
                else if (right) {
                    if(carousel_items[i][0] > this.cur_item[0] && (next && carousel_items[i][0] < next[0] || next == null))
                        next = carousel_items[i];
                }
                if(min && min[0] > carousel_items[i][0] || min == null)
                    min = carousel_items[i];
                if(max && max[0] < carousel_items[i][0] || max == null)
                    max = carousel_items[i];
            }

            if(left && next == null)
                next = max;
            else if(right && next == null)
                next = min;

            if(next) {
                _createHandler(this.cur_item[1], 'transitionend', function() {
                    _this.animating = false;
                    _this.cur_item = next;
                } );
                this.cur_item[1].removeClass('active');
                next[1].addClass('active');
            }
        }
    }

}).call(common.carousel);