console.log("herp derp js works");
window.onload = function prepForms(){
	function preloader(){
	            var loadMessage = document.getElementById("loading");
	            loadMessage.innerHTML = "let me get that for you";
	        };

	var targetForm = document.getElementById('main_form');
	targetForm.onsubmit = preloader;
};