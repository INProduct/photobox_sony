
img = document.getElementById('liveview');
i = 0;

window.setInterval(function(){
const xhttp = new XMLHttpRequest();
xhttp.onload = function(){
img.src = this.responseText;
}
xhttp.open("GET", "last_liveview_picture");
xhttp.send();

}, 200)