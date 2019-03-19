counter=12
pressions=[]
chars = []
pass_position= 0,array_position=0;
pressions_map = {}
deleted = false;
password=null;
$(document).ready(function(){

  $(window).keydown(function(event){
    if(event.keyCode == 13) {
      event.preventDefault();
      return false;
    }
  });

    $("#pass").on({
      keydown: function(e){

        if(e.which == 13){
          console.log(counter)
          if(counter == 12 && !deleted){
            //the first time the user enter his password
            password = $("#pass").val();
          }
          if($("#pass").val()!= null && $("#pass").val() == password && !deleted){

            counter_text = counter > 1 ? `${counter-1} passwords left`: "Premi invia BUSONE"
            $("#counter").text(counter_text);
            counter --;

            if(counter == 0){
              $("#hidden").val(JSON.stringify(chars))
            }
          }
          else if($("#pass").val()!= null && ($("#pass").val() != password || deleted )){
            console.log($("#pass").val() != password)
            console.log(deleted)
            alert("Retype the password please")
            chars.pop(array_position)
          }

          if(counter != 0)
          $("#pass").val("")

          pass_position = 0;
          deleted = false;
          array_position ++;
        }
        else if(e.which != 8 && e.which != 9){
          pressions_map[e.key] = new Date().getTime();
        }
        else if (e.which == 8){

          deleted = true;
        }

      },
      keyup: function(e){
        if(e.which != 8 && e.which != 9 && e.which != 13){

          let pressionEndMoment = new Date().getTime();
          let pressionDelta = pressionEndMoment - pressions_map[e.key];
          if(chars[pass_position]== null){
            chars[pass_position]=[]
          }
          chars[pass_position].push(pressionDelta);
          console.log(chars[pass_position])
          pass_position++;
        }
      }
    });
  });
