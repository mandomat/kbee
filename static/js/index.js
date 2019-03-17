counter=12
pressions=[]
chars = []
pass_position= 0;
isDown=false,isUp=false;
pressionStartMoment=null;
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
          pass_position = 0;
          switch(counter){
            case 12: //the first time the user enter his password
            password = $("#pass").val(); // save the password for further checks
            break;
            case 1:
            $("#hidden").val(JSON.stringify(chars))
            $("#counter").text(`Premi invia BUSONE`);
          }
          if($("#pass").val() == password && counter > 1){
            $("#counter").text(`${counter-1} passwords left`);
            $("#pass").val("")
            counter --;
          }
          else if($("#pass").val() != password && counter != 1){
            alert("wrong password")
            $("#pass").val("")
          }
        }
        else if(!isDown && e.which != 8 && e.which != 9){

          isUp = false;
          isDown = true;

          pressionStartMoment = new Date().getTime();
        }
        else if (e.which != 8){
          return false;
        }

      },
      keyup: function(e){
        if(!isUp && e.which != 8 && e.which != 9){
          console.log("up")

          isUp = true;
          isDown = false;
          //pression calc
          let pressionEndMoment = new Date().getTime();
          let pressionDelta = pressionEndMoment - pressionStartMoment;
          if(chars[pass_position]== null){
            chars[pass_position]=[]
          }
          chars[pass_position].push(pressionDelta);
          pass_position++;
        }
      }
    });
  });
