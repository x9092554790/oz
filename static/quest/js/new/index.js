/**
 * Created by Admin on 08.09.2016.
 */
$(document).ready(function(){
	function slid_s(){
		$('.slider_d li').each(function(){
			$(this).removeClass('activ').fadeOut(500);
		})

		$('.slider_d li').eq(el_s).addClass('activ').fadeIn(500);
	}

	var max_sl = $('.slider_d li').size() - 1; //кількість слайдів
	var el_s = 0;
	//alert(max_sl);
	$('.arr_l').click(function(){
		el_s -= 1;
		if(el_s<0){
			el_s = max_sl;
		}
		slid_s();
	})
	$('.arr_r').click(function(){
		el_s += 1;
		if(el_s>max_sl){
			el_s = 0;
		}
		slid_s();
	})
});