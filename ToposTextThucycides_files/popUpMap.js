var modal2 = document.querySelector(".modal2");


function getCords(evt) {
	mymap.setView(new L.LatLng(evt.lat.value, evt.long.value), 14);
}

function showHideMap(place, evt) {
	modal2.classList.toggle("show-modal2");
}

function windowOnClick(event) {
	if (event.target === modal2) {
		showHideMap();
	}
}

window.addEventListener("click", windowOnClick);


function getPlaceNames() {

	let placeNames = document.querySelectorAll('.place, .demonym, .person, .ethnic');
	for (let i = 0; i < placeNames.length; i++) {
		placeNames[i].classList.add("modal-trigger");
		placeNames[i].addEventListener('click', function () {
			showHideMap();
			getCords(event.target.attributes);
		})
	}
}

document.addEventListener('DOMContentLoaded', function () {
	getPlaceNames();
}, false);