function initMap() {
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 6.8,
        center: { lat: 47, lng: 3 },
    });

    map.addListener("click", (e) => {
        placeMarkerAndPanTo(e.latLng, map);
    });
}

function placeMarkerAndPanTo(latLng, map) {
    new google.maps.Marker({
        position: latLng,
        map: map,
        clickable: true,
    });
    console.log(latLng)
    map.panTo(latLng);
}

fetch('json/marker.json')
    then((response) => response.json())
    then((json) => console.log("test"));

// var infoWindowOptions = {
//     content: '<h3>Locronan</h3>'
//         + '<a href="http://www.locronan-tourisme.com/" target="_blank">Site de l office de tourisme de la ville</a>'
//         + '<br/><img src="google-marker/image.jpg" width="200px" />'
// };

// var infoWindow = new google.maps.InfoWindow(infoWindowOptions);

// google.maps.event.addListener(marker, 'click', function() {
//     infoWindow.open(map, marker);
// });

window.initMap = initMap;