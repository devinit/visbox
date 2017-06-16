def clean_value(value):
    if value is None or value == "None" or value == "":
        return None
    try:
        valueFloat = float(value)
        return valueFloat
    except ValueError:
        return value

def nest_config(config):
    result = {}
    for key, value in config.iteritems():
        path = key.split(".")
        #Special case for arrays
        if path[-1]=="colors":
            value = value.split(",")
        else:
            value = clean_value(value)
        if value is not None:
            if path[0]=="config":
                if path[1] in result:
                    if(len(path)==2):
                        result[path[1]]["value"] = value
                    #Either 2 or 3
                    else:
                        result[path[1]][path[2]] = value
                else:
                    if(len(path)==2):
                        result[path[1]] = value
                    #Either 2 or 3
                    else:
                        result[path[1]] = {}
                        result[path[1]][path[2]] = value
    return result