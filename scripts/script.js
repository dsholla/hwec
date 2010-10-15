function slideSwitch() {
	var $active = $('#slideshow div.active');

	if ($active.length == 0) $active = $('#slideshow div:last');

	// use this to pull the divs in the order they appear in the markup
	// var $next = $active.next().length ? $active.next()
	//	: $('#slideshow div:first');

	// uncomment below to pull the divs randomly
 	var $sibs = $active.siblings();
  var rndNum = Math.floor(Math.random() * $sibs.length );
  var $next = $($sibs[rndNum]);

	$active.addClass('last-active');

	$next.css({opacity: 0.0})
		.addClass('active')
		.animate({opacity: 1.0}, 1000, function() {
		$active.removeClass('active last-active');
	});
}

$(function() {
	setInterval("slideSwitch()", 5000);
});

$(document).ready(function() {  
	function addMega(){
		$(this).addClass("hovering");
	}
	function removeMega(){
		$(this).removeClass("hovering");
	}
	var megaConfig = {
		interval: 0,
		sensitivity: 4,
		over: addMega,
		timeout: 50,
		out: removeMega
	};
	$("li.mega").hoverIntent(megaConfig)      
});