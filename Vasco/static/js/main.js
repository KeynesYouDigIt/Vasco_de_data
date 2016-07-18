console.log("herp derp js works");
window.onload = function prepForms(){
	function preloader(){
	            var loadMessage = document.getElementById("loading");
	            loadMessage.innerHTML = "status: getting data <br><br> (or awaiting next your selection!)";
	        };

	var targetForm = document.getElementById('main_form');
	targetForm.onsubmit = preloader;
};