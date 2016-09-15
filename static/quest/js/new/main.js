$(document).ready(function(){
	$( "header .fa-bars" ).click(function() {
		$( "nav ul" ).slideToggle();
	});

	$( "footer .fa-bars" ).click(function() {
		$( ".nav" ).slideToggle();
	});
});