timer=10
$(document).ready(function(){
  Webcam.set({
  width: 320,
  height: 240,
  image_format: 'jpeg',
  jpeg_quality: 90
});

Webcam.attach( '#my_camera' );

});
    setInterval(function(){
      Webcam.snap( function(data_uri) {
        user = $("#user").val()
        $.post("/verify_image",{"image":data_uri,"user":user},function(res){
          $("#webcam_result").text(res)
        });
      });
    },10000)

    setInterval(function(){
      timer = timer == 1? 10: timer-1;
      $("#timer").text(timer)
    },1000)
