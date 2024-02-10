var count = 0;

const letters = ["~", "あ","か","が","さ","ざ","た","だ","な","は","ば","ぱ","ま","や","ら","わ","#","?", "NEW", "P"];
const lettersMap = {
        "~" : ["~"],
        "あ": ["あ","い","う","え","お"],
        "か": ["か","き","く","け","こ"],
        "が": ["が","ぎ","ぐ","げ","ご"],
        "さ": ["さ","し","す","せ","そ"],
        "ざ": ["さ","じ","ぢ","ず","ぜ","ぞ"],
        "た": ["た","つ","て","と"],
        "だ": ["だ","ぢ","づ","で","ど"],
        "な": ["な","に","ぬ","ね","の"],
        "は": ["は","ひ","ふ","へ","ほ"],
        "ば": ["ば","び","ぶ","べ","ぼ"],
        "ぱ": ["ぱ","ぴ","ぷ","ぺ","ぽ"],
        "ま": ["ま","み","む","め","も"],
        "や": ["や","ゆ","よ"],
        "ら": ["ら","り","る","れ","ろ"],
        "わ": ["わ"]
};

function initInterface(len, defcount) {
	var divFilters = document.getElementById('glossary-filters');
	document.getElementById('search-input').value = "";
    document.getElementById('search-input').onclick = () => document.getElementById("search-input").setAttribute("placeholder", "Search " + len + " terms and " + defcount + " definitions")

	// make the letter filters
	letters.forEach(function(d) {
		var a = document.createElement('a');
		a.setAttribute("class","glossary-header");
		a.innerHTML = d;
		var e = d.replace(/[~あかがさざただなはばぱまやらわ]/g, function (m) {
    	return lettersMap[m].toString().replace(/,/g, " ");
		});
		a.title = "Terms starting with " + (d === '#' ? 'a number' : e);
		if(d === '?') a.title = "Terms in random order";
    if(d === 'NEW') a.title = "Newest terms";
    if(d === 'NEW') a.title = "Printable version";
    a.onmouseover = function() {
      if(d == "?") {
        document.getElementById("search-input").setAttribute("placeholder", "Terms in random order");
      }
      else if(d == "#") {
        document.getElementById("search-input").setAttribute("placeholder", "Terms starting with a number");
      }
      else if(d == "NEW") {
        document.getElementById("search-input").setAttribute("placeholder", "Newest terms");
      }
      else if(d == "P") {
        document.getElementById("search-input").setAttribute("placeholder", "Printable version");
      }
      else {
        document.getElementById("search-input").setAttribute("placeholder", "Terms starting with " + e);
      }
    }
    a.onmouseout = function() {
      document.getElementById("search-input").setAttribute("placeholder", "Search " + len + " terms and " + defcount + " definitions")
    }
		a.onclick = function() {
      if (d == "?") {
        window.open(window.location.origin + "/random", "_self");
      }
      else if (d == "#") {
        window.open(window.location.origin + "/numbers", "_self");
      }
      else if (d == "NEW") {
        window.open(window.location.origin + "/new", "_self");
      }
      else if (d == "P") {
        window.open(window.location.origin + "/print", "_self");
      }
      else {
        window.open(window.location.origin + "/l/" + d, "_self");
      }
      
			return false;
		}
		divFilters.appendChild(a);
	});
}

function searchKeyDown(event) {
	var s = document.getElementById('search-input').value;
	var key = event.which || event.keyCode;

	if((s.length < 2 && !Kuroshiro.Util.isJapanese(s)) || key != 13) // minimum length of 2 and hit the enter key
		return;

    window.open(window.location.origin + "/search/" + s, "_self");
}
