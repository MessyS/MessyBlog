window.alert = alert;
function alert(data) {
	a = document.createElement("span"),
	p = document.createElement("p"),
	btn = document.createElement("div"),
	textNode = document.createTextNode(data ? data : ""),
	btnText = document.createTextNode("确定");
	
	css(a, {
		"position" : "fixed",
		"left" : "0",
		"right" : "0",
		"top" : "30%",
		"width" : "300px",
		"height" : "300px",
		"margin" : "0 auto",
		"background-color" : "rgba(0,0,0,0.8)",
		"font-size" : "20px",
		"text-align" : "center",
		'border-radius':'51%',
		'color':'white',
		'display':'none'
	});
	
	css(p,{
		'position':'relative',
		'top':'45%',
		'text-align': 'center'
	})
	
	css(btn, {
		'position':'relative',
		"width" : "100px",
		'top':'60%',
		'left':'35%',
		'text-align': 'center',
		'border-radius':'6%',
		'color':'black',
		"background" : "white",
	})
	
	p.appendChild(textNode);
	btn.appendChild(btnText);
	a.appendChild(p);
	a.appendChild(btn);
	document.getElementsByTagName("body")[0].appendChild(a);
	
	btn.onclick = function(){
			a.parentNode.removeChild(a);
		}
	}
	
	function css(targetObj, cssObj) {
	var str = targetObj.getAttribute("style") ? targetObj.getAttribute("style") : "";
	for(var i in cssObj) {
		str += i + ":" + cssObj[i] + ";";
	}
	targetObj.style.cssText = str;
}