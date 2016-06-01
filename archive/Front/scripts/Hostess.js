/*This is hostess
the front end UI for pub data pub */
alert('Welcome to pubdatapub! a place where nasty, unorginized public data is first_mixed and served as you want it: a complex, rich, coctail, or a straight pour of a single data set.');
alert('sadly, my developer is a hardcore n00b at all this, but the great folks at blazing db are giving him a chance to build something special! email feedback to altereeeeego@gmail.com\n/////////\nbe sure to check out blazing db at http://blazingdb.com/\n/////////');
var countries=prompt('So right now, I have data from the World Bank on global economics and data from the UN Human development Report on Poverty and standard of living.\n Which countries in your custom data coctail tonight? Please seperate each with a comma, don\'t just throw em all me at once. \nThey are case sensitive (its an entire country! don\'t be lazy.');
var years=prompt('Got it! For which years do you need data? seperate each with a comma as well');
function uat () {
    document.write(countries+ '</br>'+ '</br>');
    document.write(years+ '</br>'+ '</br>');    
}
document.body.onClick=uat();
var chek = document.getElementById("check");
var Things = [0,1,2,3,4,5];
for (var i = 0; i < Things.length; i++) {
	document.write(chek);
};
//document.onclick = function() {
//    alert('Ouch! Stop poking me!');
//};

//code below is practice
var currentStatus='just getting started!';
if (1===1) {
	document.write(currentStatus+ '</br>'+ '</br>');
} else if (1===10){
	document.write('math is fail!!!!');
} else {
	document.write('whatever');
}
//the above annd below do the same thing, bottom is faster and specifies default if no case ==true
var one=1;
switch (one){
	case 1:
		document.write(currentStatus);
		alert('switch is working!');
		break;
	case 2:
		document.write('math is fail!!!!');
                break;
	default:
		document.write('whatever');
                break;
}

//now lets document.write number cause whatever
for (var i = 0; i < 11; i++) {
	document.write(i + '</br>'+'</br>'+'</br>');
}