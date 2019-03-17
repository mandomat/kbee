isDown=false,isUp=false;
pressions=[]
chars = []
pass_position= 0;
pressionStartMoment=null;
$("#pass").on({
  keydown: function(e){
    if(!isDown && e.which != 8 && e.which != 9){
    isUp = false;
    isDown = true;
    pressionStartMoment = new Date().getTime();
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

      chars[pass_position]=pressionDelta;
      $("#hidden").val(JSON.stringify(chars))
      pass_position++;
}
  }
});
