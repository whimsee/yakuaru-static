/*
	Arcana by HTML5 UP
	html5up.net | @n33co
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
*/

/* please don't look at my bad javascript */
function loadMenu(current) {
	var str = "";
	str += '<ul>';
	str += '<li' + (current==1 ? ' class="current"' : '') + '><a href="/">Home</a></li>';
	str += '<li' + (current==2 ? ' class="current"' : '') + '><a href="donate.html">Donate</a></li>';
	str += '<li' + (current==3 ? ' class="current"' : '') + '><a href="stats.html">Stats & Updates</a></li>';
	str += '<li' + (current==4 ? ' class="current"' : '') + '><a href="credits.html">Credits</a></li>';
	str += '<li' + (current==5 ? ' class="current"' : '') + '><a href="contact.html">Contact</a></li>';
	str += '<li' + (current==6 ? ' class="current"' : '') + '><a href="bots.html">Twitch/Discord Bots</a></li>';
	str += '<li' + (current==7 ? ' class="current"' : '') + '><a href="https://ki.infil.net">The Complete KI Guide</a></li>';
	// str += '<li' + (current==3 ? ' class="current"' : '') + '><a href="meter.html">Meter</a>';
	// 	str += '<ul>';
	// 		str += '<li><a href="meter.html#smeter">Shadow Meter</a></li>';
	// 		str += '<li><a href="meter.html#smoves">Shadow Moves</a></li>';
	// 		str += '<li><a href="meter2.html#scounters">Shadow Counters</a></li>';
	// 		str += '<li><a href="meter2.html#instinct">Instinct</a></li>';
	// 	str += '</ul>';
	// 	str += '</li>';
	//str += '<li' + (current==8 ? ' class="current"' : '') + '><a href="words.html">Fightin\' Words</a></li>';
	str += '</ul>';
	
	document.getElementById('nav').innerHTML = str;
}

function loadFooter() {
	var str = "";
	str += '<div class="container"></div>';
	str += '<ul class="icons">';
	str += '<li><a href="https://www.twitter.com/Infilament" class="icon fa-twitter"><span class="label">Twitter</span></a></li>';
	str += '<li><a href="https://www.ask.fm/Infilament" class="icon fa-question"><span class="label">Ask.fm</span></a></li>';
	str += '<li><a href="donate.html" class="icon fa-paypal" style="font-size: 175%;"><span class="label">Donate</span></a></li>';
	str += '</ul>';
	str += '<div class="copyright">';
	str += '<ul class="menu">';
	str += '<li>An infil.net project</li><li>Design: Arcana by <a href="https://html5up.net">HTML5 UP</a></li>';
	str += '</ul>';
	str += '</div>';
	
	document.getElementById('footer').innerHTML = str;
}

function setRandomBannerImage() {
	var maxImages = 11;
	var banner = Math.floor(Math.random() * maxImages + 1);
	document.getElementById('topbanner').innerHTML = '<img src="images/banners/banner' + banner + '.png" />';
}

function showhide(textID, showhideID, str) {
	str = str || "terms"; // if you don't pass in "str", default to "terms"
	var div = document.getElementById(showhideID);
	var text = textID ? document.getElementById(textID) : null;
	if (div.style.display == "flex") {
	    div.style.display = "none";
		if(text != null)
			text.innerHTML = "Show " + str;
	}
	else {
	    div.style.display = "flex";
		if(text != null)
			text.innerHTML = "Hide " + str;
	}
	return false;
}

(function($) {

	skel.init({
		reset: 'full',
		breakpoints: {
		/* used to be 1400, 1200, 960 containers size for global, wide, normal */
			global:		{ range: '*', href: 'css/style.css', containers: 960, grid: { gutters: 50 } },
			wide:		{ range: '-1680', href: 'css/style-wide.css', containers: 960, grid: { gutters: 40 } },
			normal:		{ range: '-1280', href: 'css/style-normal.css', containers: 960, grid: { gutters: 30 }, viewport: { scalable: false } },
			narrow:		{ range: '-980', href: 'css/style-narrow.css', containers: '95%' },
			narrower:	{ range: '-840', href: 'css/style-narrower.css', containers: '95%!', grid: { zoom: 2 } },
			mobile:		{ range: '-736', href: 'css/style-mobile.css', containers: '90%!', grid: { gutters: 20 } },
			mobilep:	{ range: '-480', href: 'css/style-mobilep.css', grid: { zoom: 3 }, containers: '100%' }
		},
		plugins: {
			layers: {
				navPanel: {
					animation: 'revealX',
					breakpoints: 'narrower',
					clickToHide: true,
					height: '100%',
					hidden: true,
					html: '<div data-action="navList" data-args="nav"></div>',
					orientation: 'vertical',
					position: 'top-left',
					side: 'left',
					width: 275
				},
				titleBar: {
					breakpoints: 'narrower',
					height: 44,
					html: '<span class="toggle" data-action="toggleLayer" data-args="navPanel"></span><span class="title" data-action="copyHTML" data-args="logo"></span>',
					position: 'top-left',
					side: 'top',
					width: '100%'
				}
			}
		}
	});

	$(function() {

		var	$window = $(window),
			$body = $('body');

		// Disable animations/transitions until the page has loaded.
			$body.addClass('is-loading');
			
			$window.on('load', function() {
				$body.removeClass('is-loading');
			});
			
		// Forms (IE<10).
			var $form = $('form');
			if ($form.length > 0) {
				
				$form.find('.form-button-submit')
					.on('click', function() {
						$(this).parents('form').submit();
						return false;
					});
		
				if (skel.vars.IEVersion < 10) {
					$.fn.n33_formerize=function(){var _fakes=new Array(),_form = $(this);_form.find('input[type=text],textarea').each(function() { var e = $(this); if (e.val() == '' || e.val() == e.attr('placeholder')) { e.addClass('formerize-placeholder'); e.val(e.attr('placeholder')); } }).blur(function() { var e = $(this); if (e.attr('name').match(/_fakeformerizefield$/)) return; if (e.val() == '') { e.addClass('formerize-placeholder'); e.val(e.attr('placeholder')); } }).focus(function() { var e = $(this); if (e.attr('name').match(/_fakeformerizefield$/)) return; if (e.val() == e.attr('placeholder')) { e.removeClass('formerize-placeholder'); e.val(''); } }); _form.find('input[type=password]').each(function() { var e = $(this); var x = $($('<div>').append(e.clone()).remove().html().replace(/type="password"/i, 'type="text"').replace(/type=password/i, 'type=text')); if (e.attr('id') != '') x.attr('id', e.attr('id') + '_fakeformerizefield'); if (e.attr('name') != '') x.attr('name', e.attr('name') + '_fakeformerizefield'); x.addClass('formerize-placeholder').val(x.attr('placeholder')).insertAfter(e); if (e.val() == '') e.hide(); else x.hide(); e.blur(function(event) { event.preventDefault(); var e = $(this); var x = e.parent().find('input[name=' + e.attr('name') + '_fakeformerizefield]'); if (e.val() == '') { e.hide(); x.show(); } }); x.focus(function(event) { event.preventDefault(); var x = $(this); var e = x.parent().find('input[name=' + x.attr('name').replace('_fakeformerizefield', '') + ']'); x.hide(); e.show().focus(); }); x.keypress(function(event) { event.preventDefault(); x.val(''); }); });  _form.submit(function() { $(this).find('input[type=text],input[type=password],textarea').each(function(event) { var e = $(this); if (e.attr('name').match(/_fakeformerizefield$/)) e.attr('name', ''); if (e.val() == e.attr('placeholder')) { e.removeClass('formerize-placeholder'); e.val(''); } }); }).bind("reset", function(event) { event.preventDefault(); $(this).find('select').val($('option:first').val()); $(this).find('input,textarea').each(function() { var e = $(this); var x; e.removeClass('formerize-placeholder'); switch (this.type) { case 'submit': case 'reset': break; case 'password': e.val(e.attr('defaultValue')); x = e.parent().find('input[name=' + e.attr('name') + '_fakeformerizefield]'); if (e.val() == '') { e.hide(); x.show(); } else { e.show(); x.hide(); } break; case 'checkbox': case 'radio': e.attr('checked', e.attr('defaultValue')); break; case 'text': case 'textarea': e.val(e.attr('defaultValue')); if (e.val() == '') { e.addClass('formerize-placeholder'); e.val(e.attr('placeholder')); } break; default: e.val(e.attr('defaultValue')); break; } }); window.setTimeout(function() { for (x in _fakes) _fakes[x].trigger('formerize_sync'); }, 10); }); return _form; };
					$form.n33_formerize();
				}

			}

		// Dropdowns.
			$('#nav > ul').dropotron({
				offsetY: -15,
				hoverDelay: 0,
				alignment: 'center'
			});

	});

})(jQuery);