//def nest_config(config):
//    result = {}
//    for key, value in config.iteritems():
//        path = key.split(".")
//        if path[0]=="config":
//            if path[1] in result:
//                if(len(path)==2):
//                    result[path[1]]["value"] = value
//                #Either 2 or 3
//                else:
//                    result[path[1]][path[2]] = value
//            else:
//                if(len(path)==2):
//                    result[path[1]] = value
//                #Either 2 or 3
//                else:
//                    result[path[1]] = {}
//                    result[path[1]][path[2]] = value
//    return result

function nest_config(config){
  var result = {};
  for(var key in config){
    var value = config[key],
    path = key.split(".");
    if(value !=""){
      if(path[0]=="config"){
        if(result.hasOwnProperty(path[1])){
          if(path.length==2){
            result[path[1]]["value"] = value;
          }else{
            result[path[1]][path[2]] = value;
          }
        }else{
          if(path.length==2){
            result[path[1]] = value;
          }else{
            result[path[1]] = {};
            result[path[1]][path[2]] = value;
          }
        }
      } 
    }
  }
  return(result);
}

function form2config(formSelector) {
    var config = {};
    var inputs = d3.select(formSelector).selectAll("input");
    var selects = d3.select(formSelector).selectAll("select");
    //Iterate through inputs
    inputs.each(function(){
      var input = d3.select(this),
      name = input.attr("name"),
      value = input.property("value");
      config[name] = value;
      });
    //Repeat, ensuring to overwrite duplicate names with checked values
    inputs.each(function(){
        var input = d3.select(this),
        name = input.attr("name"),
        value = input.property("value"),
        type = input.attr("type");
        if (type=="checkbox") {
            var checked = input.property("checked");
            if (checked) {
                config[name] = true;
            }else{
              config[name] = false;
            }
        }else if (type=="radio") {
            var checked = input.property("checked");
            if (checked) {
                config[name] = value;
            }
        }
    });
    
    //Iterate through selects
    selects.each(function(){
      var select = d3.select(this),
      name = select.attr("name"),
      option = select.select("option:checked");
      if (option.size()>0) {
        value = option.property("value");
        config[name] = value;
      }
      });
    
    return(nest_config(config));
}