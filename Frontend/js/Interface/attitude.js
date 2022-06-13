var first_attitude = $.flightIndicator('#attitudeNavigation', 'attitude', {size:350, roll:30, pitch:20, showBox : true});
var first_attitude = $.flightIndicator('#attitudeIndicator', 'attitude', {size:100, roll:10, pitch:0, showBox : true});

// Update at 20Hz
var increment = 0;
setInterval(function() {
   
    // Airspeed update
    airspeed.setAirSpeed(80+80*Math.sin(increment/10));

    // Attitude update
    attitude.setRoll(30*Math.sin(increment/10));
    attitude.setPitch(50*Math.sin(increment/20));

    // Altimeter update
    altimeter.setAltitude(10*increment);
    altimeter.setPressure(1000+3*Math.sin(increment/50));
    increment++;
    
    // TC update - note that the TC appears opposite the angle of the attitude indicator, as it mirrors the actual wing up/down position
    turn_coordinator.setTurn((30*Math.sin(increment/10))*-1);

    // Heading update
    heading.setHeading(increment);
    
    // Vario update
    variometer.setVario(2*Math.sin(increment/10));
}, 50);