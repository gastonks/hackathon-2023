function initMap() {
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 6.8,
        center: { lat: 47, lng: 3 },
    });

    let compteur = 0;

    map.addListener("click", (e) => {
        if(compteur == 0) {
            placeMarkerAndPanTo(e.latLng, map);
            compteur++;
            document.getElementById("id_latitude").value = e.latLng.lat()
            document.getElementById("id_longitude").value = e.latLng.lng()
        }
    });
}

function placeMarkerAndPanTo(latLng, map) {
    var marker = new google.maps.Marker({
        position: latLng,
        map: map,
        draggable: true,
    });
    google.maps.event.addListener(marker, 'dragend', function() {
        document.getElementById("id_latitude").value = marker.getPosition().lat()
        document.getElementById("id_longitude").value = marker.getPosition().lng()
    });
    map.panTo(latLng);
}

window.initMap = initMap;