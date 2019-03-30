counter=12;
chars = [];
pass_position_counter= 0;
pressures_map = {};
deleted = false;
password=null;
var stepper1= null

$(document).ready(function(){
  stepper1 = new Stepper($('#stepper1')[0])

  Webcam.set({
  width: 320,
  height: 240,
  image_format: 'jpeg',
  jpeg_quality: 90
});


  $(window).keydown(function(event){
    if(event.keyCode == 13) {
      event.preventDefault();
      return false;
    }
  });

  $("#pass").on({
    keydown: function(e){
      if(e.which == 13){
        if(counter == 12 && !deleted){
          //the first time the user enter his password
          password = $("#pass").val();
        }
        if($("#pass").val()!= null && $("#pass").val() == password && !deleted){

          counter_text = counter > 1 ? `${counter-1} passwords left`: "Thank you!"
          $("#counter").text(counter_text);
          counter --;

          if(counter == 0){
            $("#next").prop('disabled', false);
            $("#hidden").val(JSON.stringify(chars));
            $("#hidden_pass").val(password);
            Webcam.attach( '#my_camera' );


          }
        }
        else if($("#pass").val()!= null && ($("#pass").val() != password || deleted )){
          alert("Retype the password please")
          if(chars.length > 0){
            position_to_delete = chars[0].length
            for(i=0; i<chars.length;i++){
              if(chars[i].length == position_to_delete)
              chars[i].pop(chars[i].length);
            }
          }
        }

        if(counter != 0)
        $("#pass").val("")

        pass_position_counter = 0;
        deleted = false;
      }
      else if(e.which != 8 && e.which != 9 && !deleted && password!=null){

        pressures_map[e.key]={"start":new Date().getTime(),"position":pass_position_counter};
        pass_position_counter++;
      }

      if (e.which == 8){

        deleted = true;
      }


    },
    keyup: function(e){

      if(e.which != 8 && e.which != 9 && e.which != 13 && !deleted && password!=null  ){

        if(e.key in pressures_map) {
          let pass_position = pressures_map[e.key]["position"];

          if(pass_position_counter<=password.length && e.key == password[pass_position]){

            chars[pass_position]= chars[pass_position]==null? []:chars[pass_position];
            let pressureDelta = new Date().getTime() - pressures_map[e.key]["start"];
            chars[pass_position].push(pressureDelta);
          }
        }
      }
    }
  });
});

function takeSnapshot() {

  Webcam.snap( function(data_uri) {
    // display results in page
    document.getElementById('results').innerHTML =
    '<img src="'+data_uri+'"/>';
    $("#image_data").val(data_uri)
  } );
}
