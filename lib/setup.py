"""setup.py
that module shall read a given json file and create a <Matrix> instance along with a <Layers> instance"""
import json
from .matrix import Kbd_Matrix
from .layers import Layers

def setup(json_string:str)->tuple[Kbd_Matrix,Layers]:
    config = json.loads(json_string)

    matrix = Kbd_Matrix(**config["matrix"])

    layers = Layers(matrix.length)
    switches:dict = config["switches"]
    for switch_name, args in switches.items() :
        layers.add_switch(args["type"], switch_name, args["arguments"])
    layers.set_default_layer(config["default_layer"]["layout"])
    for layer in config["layers"]:
        if layer["name"][0]=="_" : continue
        layers.add_layer(layer["name"], layer["layout"])
    return matrix, layers
        
    
    