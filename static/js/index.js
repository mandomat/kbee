counter=12
pressions=[]
chars = []
pass_position= 0,array_position=0;
pressions_map = {}
deleted = false;
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
          console.log(deleted)

          switch(counter){
            case 12: //the first time the user enter his password
            password = $("#pass").val(); // save the password for further checks
            break;
            case 1:
            $("#hidden").val(JSON.stringify(chars))
            $("#counter").text(`Premi invia BUSONE`);
          }
          if($("#pass").val() == password && counter > 1 && !deleted){
            $("#counter").text(`${counter-1} passwords left`);
            $("#pass").val("")
            counter --;
          }
          else if(($("#pass").val() != password && counter != 1) || deleted){
            alert("Wrong password ()")
            chars.pop(array_position)
            $("#pass").val("")
          }

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
