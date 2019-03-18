pressions=[]
chars = []
pass_position= 0;
pressions_map = {}
$("#pass").on({
  keydown: function(e){
    if(e.which != 8 && e.which != 9){
    pressions_map[e.key] = new Date().getTime();
  }
  },
  keyup: function(e){
    if(e.which != 8 && e.which != 9 && e.which != 13){

      let pressionEndMoment = new Date().getTime();
      let pressionDelta = pressionEndMoment - pressions_map[e.key];

      chars[pass_position]=pressionDelta;
      $("#hidden").val(JSON.stringify(chars))
      pass_position++;
}
  }
});
