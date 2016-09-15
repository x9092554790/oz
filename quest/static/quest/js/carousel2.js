if (typeof common == 'undefined')
  common = {};
if (typeof common.carousel == 'undefined')
  common.carousel = {};

(function(){
    this.Carousel = function(options) {
        return new Carousel(options);
    };

    function slid_s(slider){
		slider.find('li').each(function(){
			$(this).removeClass('activ');
		});

		slider.find('li').eq(el_s).addClass('activ');
	}

    function Carousel(options) {
        if (!(this instanceof Carousel))
            return new Carousel(options);

        var _this = this;

        if(options.container && options.container instanceof jQuery)
            this.container = options.container;
        else if(options.container)
            this.container = $(options.container);

        if(!this.container)
            return;

        this.max_sl = this.container.find('ul:first-child li').size() - 1;
	    this.el_s = 0;

        this.container.find('.arr_l').click(function(){
            _this.el_s -= 1;
            if(_this.el_s < 0){
                _this.el_s = _this.max_sl;
            }
            _this.slid_s();
	    });
        this.container.find('.arr_r').click(function(){
            _this.el_s += 1;
            if(_this.el_s > _this.max_sl){
                _this.el_s = 0;
            }
            _this.slid_s();
        });
    }

    Carousel.prototype = {
        slid_s: function () {
            this.container.find('ul:first-child li').each(function () {
                $(this).removeClass('activ').fadeOut(500);
            });

            this.container.find('ul:first-child li').eq(this.el_s).addClass('activ').fadeIn(500);
        }
    }

}).call(common.carousel);
