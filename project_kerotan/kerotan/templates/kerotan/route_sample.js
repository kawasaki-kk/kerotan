rendererOptions = {
draggable: true,
preserveViewport:false
};
var directionsDisplay =
  new google.maps.DirectionsRenderer(rendererOptions);
var directionsService =
  new google.maps.DirectionsService();
var map;

function initialize() {
 var zoom = 7;
 var mapTypeId = google.maps.MapTypeId.ROADMAP

 var opts = {
 zoom: zoom,
 mapTypeId: mapTypeId
 };
 map = new google.maps.Map
 (document.getElementById("map_canvas"),opts);
   directionsDisplay.setMap(map);

 google.maps.event.addListener(directionsDisplay,
   'directions_changed', function(){
 });
 calcRoute();
 console.log("a");
}


//二点間の経路(パラメータを決め打ち)
function calcRoute() {
 var request = {
 origin: "東京",
 destination: "大阪",
 travelMode: google.maps.DirectionsTravelMode.DRIVING,
 unitSystem: google.maps.DirectionsUnitSystem.METRIC,
 optimizeWaypoints: true,
 avoidHighways: false,
 avoidTolls: false
 };
 directionsService.route(request,
  function(response,status){
  if (status == google.maps.DirectionsStatus.OK){
  directionsDisplay.setDirections(response);}
  });
}
