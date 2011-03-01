
function showInfoWindow(marker)
{
    var infowindow = new google.maps.InfoWindow({  
                  content: '<img src="'+ marker.icon+ '"><strong>' + marker.my_name  + '</strong><br/><a href="' + marker.my_link + '">View Webpage</a><br/>' + marker.my_hover
         });  
    infowindow.open(map, marker); 
}

function attachURL(marker) {
    google.maps.event.addListener(marker, 'click', function(e) { showInfoWindow(marker); });
}


function setMarkerIcon(marker)
{
    path = markerIconPath  + markerInfoTable[marker.my_kind].icon;
    marker.setIcon(path);
}

function loadMarkers(map, data)
{
    var mlist = data.markers;
    for (i = 0; i < mlist.length; i++)
    {
        m = mlist[i];
        var latlng = new google.maps.LatLng(m.latitude, m.longitude);
        marker = new google.maps.Marker({ title: m.name,
                    position: latlng, map: map});

        marker.my_kind = m.kind;
        marker.my_link = m.link;
        marker.my_hover = m.hover
        marker.my_name = m.name;
        marker.my_pk = m.pk;
        setMarkerIcon(marker);
        attachURL(marker);
        // need a little closure here
        allMarkers.push(marker);
    }
}

function saveMarker()
{
    var minfo =  {
        pk: currentMarker.my_pk,
        latitude : currentMarker.position.lat(),
        longitude : currentMarker.position.lng(),
        link: $('#marker_link').val(),
        name:  $('#marker_name').val(),
        kind:  $('#marker_kind').val()
    };
    $.ajax({type: 'POST', url: '/sharider/spot/save/', data: JSON.stringify(minfo), dataType : 'text', success: null});
}
function markerTypeChanged()
{
    currentMarker.my_kind = $('#marker_kind').val();
    setMarkerIcon(currentMarker);
}

function markerToViewCenter()
{
    currentMarker.setPosition(map.getCenter());
}
function updateMarker(zoom)
{
    map.setCenter( currentMarker.position);
    if(zoom)
        map.setZoom(zoom);
    currentMarker.setDraggable(true);
    $('#marker_name').val(currentMarker.my_name);
    $('#marker_link').val(currentMarker.my_link);
}

function  loadMarker(currentMarkerId, newKind)
{
    for (i = 0; i < allMarkers.length; i++)
    {
        m = allMarkers[i];
        if(m.my_pk == currentMarkerId)
        {
            currentMarker = m;
            updateMarker(17);
            return;
        }
    }
    // No marker found make one
     var latlng = new google.maps.LatLng(m.latitude, m.longitude);
        name = 'New Spot'
        marker = new google.maps.Marker({ title: name,
                    position: map.getCenter(),
                    map: map});
        marker.my_pk = 0;
        marker.my_link = '';
        marker.my_kind = newKind;
        marker.my_hover = null;
        marker.my_name = name;
        setMarkerIcon(marker);

        attachURL(marker);

    currentMarker = marker;
    updateMarker(0);
}


function setupMarkerOptions(div_name, callback_maker)
{
   
    // Make the html for the checkboxes
    options = '';
    
    for (var key in markerInfoTable)
    {
        mi = markerInfoTable[key];
        if (mi.enabled == true)
        {
            options += '<input type="checkbox" id="MO_' + mi.option_tag;
            options += '" checked="' + mi.show + '"/> <label for="MO_' + mi.option_tag + '">';
            options += mi.option_name + '</label>';
        }
    }
    // Set up the checkboxes
    $(div_name).html(options);

    // Attach handlers
    for (var key in markerInfoTable)
    {
        mi = markerInfoTable[key];
        if (mi.enabled == true)
        {
            $('#MO_' + mi.option_tag).change(callback_maker(key));
        }
    }
}
/////////////////////////
//
// Chart stuff
// 
///////////////////////

function createChart(div_id, xsize, ysize)
{
    return Raphael(div_id, xsize, ysize);
}

function resizeChart(chart, xsize, ysize)
{
    chart.setSize(xsize, ysize);
}

function drawChart(display, display_xoff, display_yoff,
        display_xsize, display_ysize, xmin, xmax,
        ymin, ymax, points, index1, index2, color)
{
    xscale = display_xsize / (xmax - xmin);
    yscale = display_ysize / (ymax - ymin);
    var str = '';
    var i;
    for (i = 0; i < points.length; i++)
    {
        p = points[i];
        if (i == 0)
        {
            str += 'M';
        }
        else
        {
            str += 'L';
        }
        str += (p[index1] - xmin) * xscale + display_xoff + ' ' +
                (display_ysize - (p[index2] - ymin) * yscale) + display_yoff;
    }
    display.path(str).attr({fill: 'none', stroke: color});
}

function drawChartBox(xsize, ysize)
{
    chart.clear();
    chart.rect(0, 0, xsize, ysize, 5).attr({fill: '#fff', stroke: 'black'});
    chartMark = chart.path('M  0 0 L4.0 ' + ysize).attr(
            {stroke: '#0f0', fill: 'none'});
}



function highlight(index)
{
    var latlng = new google.maps.LatLng(
                                pointsData[index][0],
                                pointsData[index][1]);

    posMarker.setPosition(latlng);

    xpos = (pointsData[index][2] - distanceMin) / (distanceMax) * chartX;

    $('#cur_distance').text((pointsData[index][2] * 0.000621371192).toFixed(2) + ' mi');
    $('#cur_altitude').text((pointsData[index][3] * 3.2808399).toFixed(0) + ' ft');
    $('#cur_speed').text((pointsData[index][4] * 2.23693629).toFixed(2) + ' mph');

    chartMark.transformations[1] = 'translate(' + xpos + ',' + 0.0 + ')';
    chartMark[0].setAttribute('transform', chartMark.transformations.join(' '));
}


function chartPick(ex, ey, id)
{
    pos = $('#' + id).offset();
    x = (ex - pos.left) / chartX;
    y = 1.0 - (ey - pos.top) / chartY;
    distance = distanceMin + x * (distanceMax - distanceMin);
    close = distanceMax;
    found = 0;
    for (i = 0; i < pointsData.length; i++)
    {
        p = pointsData[i];
        d = Math.abs(p[2] - distance);

        if (d <= close)
        {
            close = d;
            found = i;
        }
    }
    highlight(found);
}

function mouseMoved(event) 
{
    chartPick(event.pageX, event.pageY,'chart_canvas');
    console.log("Moved");
}

function touchUpdate(event)
{
    event.preventDefault();
    chartPick(event.targetTouches[0].pageX, event.targetTouches[0].pageY,'chart_canvas');
 //   alert("moved" + event.touches[0].pageX);
}

////////////////////
//
// Route Stuff
//
////////////////////

function saveRoute(routeGuid, latestDirections, successFunction)
{
    var pts = new Array;
    
    for(var i = 0; i < latestDirections.routes.length; i++)
    {
        var route =  latestDirections.routes[i];
        
        for(var j = 0; j < route.legs.length; j++)
        {
            var leg = route.legs[j];
            pts.push([ leg.start_location.lat(), leg.start_location.lng()]);
            
            for(var k = 0; k < leg.via_waypoint.length; k++)
            {

                wp = leg.via_waypoint[k];
                pts.push([ wp.location.lat(), wp.location.lng()]);
            }
            if(j ==  route.legs.length -1)
            {
                pts.push([ leg.end_location.lat(), leg.end_location.lng()]);
            }
        }
    }
    
    var name_input = document.getElementById('route_name').value
    
    var foo =  {name : name_input,  points: pts , route_guid: routeGuid, distance: 0.0};
    
    $.ajax({type: 'POST', url: '/sharider/route/save/', data: JSON.stringify(foo), dataType : 'text', success: successFunction});
}

function loadRoute(routeGuid, routeEditing)
{
    if (routeGuid.length == 0)
    {
        clearRoute();
    }
    else
    {
        $.ajax({ url: '/sharider/route/json/' + routeGuid + '/', dataType: 'json', context: document.body, 
            success: function (data)
            {
                var p;
                
                wayPoints = new Array;
                for(var i = 0 ; i < data.wayPoints.length; i++)
                {
                     p = data.wayPoints[i];
                     wayPoints.push({ location: new google.maps.LatLng(p[0],p[1])});
                }
                
                document.getElementById('route_name').value = data.name;
                
                var sw = new google.maps.LatLng(data.bounds.min_latitude, data.bounds.min_longitude);
                var ne = new google.maps.LatLng(data.bounds.max_latitude, data.bounds.max_longitude);

                var mapBounds = new google.maps.LatLngBounds(sw, ne);
        
                map.fitBounds(mapBounds);
                
                currentRouteGuid = data.guid;
               
                requestUpdatedRoute();
            }
        });
    }
}

var segPath = null;
var posMarker = null;

function clearRide()
{
    if (segPath != null)
    {
        segPath.setMap(null);
        
        posMarker.setMap(null);
        segPath = null;
        posMarker = null;
    }
    $('#chart_canvas').hide();
    rideInfo = null;
}

function loadRide(rideGuid, img_path)
{
    if (rideGuid.length == 0)
    {
        clearRide();
    }
    else
    {
        $.ajax({ url: '/sharider/ride/json/' + rideGuid  + '/LAT,LON,DST,ALT,SPD/', dataType: 'json', context: document.body,
            success: function(data)
            {
                clearRide();
                rideInfo = data;
                pointsData = rideInfo.points;
                distanceMax = rideInfo.distance;
        
                var coords = new Array;
                for (i in pointsData)
                {
                    d = pointsData[i];
                    coords.push(new google.maps.LatLng(d[0], d[1]));
                }
                
                 $('#chart_canvas').show();
                
                segPath = new google.maps.Polyline({ path: coords,
                    strokeColor: '#FF0000',
                    strokeOpacity: 1.0,
                    strokeWeight: 2
                });
        
                segPath.setMap(map);
                drawChartDisplay(chart, rideInfo);
                
                var latlng = new google.maps.LatLng(pointsData[0][0], pointsData[0][1]);
                posMarker = new google.maps.Marker({position: latlng,
                                                    map: map,
                                                    icon: img_path+ '/marker_ride_pos.png'});
            
                var sw = new google.maps.LatLng(rideInfo.bounds.min_latitude, rideInfo.bounds.min_longitude);
                var ne = new google.maps.LatLng(rideInfo.bounds.max_latitude, rideInfo.bounds.max_longitude);

                var mapBounds = new google.maps.LatLngBounds(sw, ne);
        
                map.fitBounds(mapBounds);
               
                 $('#chart_canvas').mousemove(mouseMoved);
                highlight(0);
            }
        });
    }
}

