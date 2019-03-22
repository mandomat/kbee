pressions=[]
chars = []
pass_position_counter= 0;
pressions_map = {}

$("#pass").on({
  keydown: function(e){
    if(e.which != 8 && e.which != 9 && e.which != 13){
      //pressions_map[e.key] = new Date().getTime();
      console.log("ok")
      pressions_map[e.key]={"start":new Date().getTime(),"position":pass_position_counter};
      pass_position_counter++;
    }
  },
  keyup: function(e){
    if(e.which != 8 && e.which != 9 && e.which != 13){

      if(e.key in pressions_map) {
        let pass_position = pressions_map[e.key]["position"];
        chars[pass_position]= new Date().getTime() - pressions_map[e.key]["start"];
      }

      $("#hidden").val(JSON.stringify(chars))

    }
  }
});
