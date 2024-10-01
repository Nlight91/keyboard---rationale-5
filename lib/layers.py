"""This module implement the concept of layers.
Just as layers in Photoshop, a layer with a higher index takes precedence over
layers with a lower index. For example the layer at index 0 (default layer)
will always get covered by other layers.
"""
from scancodes import TRANS
import time

class LayerFunc:
    """LayerFunc subclasses of this class are the proper layers"""
    @property
    def idx(s):
        if s._idx is None :
            s._idx = s.parent.layer_order.index(s.layer_name)
        return s._idx
    def __init__(s, parent, layer_name:str, exclude_above=True, restore = False):
        """LayerFunc.__init__(parent, layer_name, exclude_above, retore)

        parent : <Layer> Layer instance
        layer_name : <str> layer name
        exclude_above : <bool> defaults to True
            if this flag is on, layers above this one get deactivated
        retore : <bool> defaults to False
            flag telling if layer configuration above this layer idx should be
            save/restored
        """
        s.parent = parent
        s.layer_name = layer_name
        s.exclude_above = exclude_above
        s.restore = restore
        s._idx = None
    def __call__(s) : pass
    def press(s):
        return None
    def depress(s):
        return None

class Layers :
    """Layer Manager

    this class is intended to handle and manage several layers of keymapping.
    This is the layer manager if you will.

    NOTES :
        s.layers:{ name:str : [key_value, ...]}
            s.layers actually holds the mappings associated to a layer name
        
        s.layer_order:[name:str, ...]
            s.layer_order tells us the order of the layers, order is set by order of creation
        
        s.layer_state:{ name:str : bool, ... }
            s.layer_state tells us the activation state of each layer
    """
    def __init__(s, size ):
        assert isinstance(size, tuple)
        assert len(size)==2
        s.matrix_size = size
        s.layers = {"default":[]}
        s.layer_order = []
        s.layer_state = {}
        s.restore_point = None
        s.TOGGLE = s._class_dec(TOGGLE)
        s.MOMENTARY = s._class_dec(MOMENTARY)

    def _class_dec(s, cls):
        """decorator used to set the current instance as the parent parameter of cls.
        cls must be a subclass of LayerFunc"""
        def w(*a, **kw):
            return cls(s, *a, **kw)
        return w

    def set_default_layer(s, args):
        assert len(args) == s.matrix_size[0]*s.matrix_size[1]
        s.layers["default"] = args

    def add_layer(s,layer_name, args):
        assert isinstance(layer_name, str)
        assert layer_name != "default"
        assert len(args) == s.matrix_size[0]*s.matrix_size[1]
        s.layers[layer_name] = args
        if layer_name not in s.layer_order :
            s.layer_order.append(layer_name)
            s.layer_state[layer_name] = False

    def create_restore_point(s, idx):
        """saves layer state above the layer_order[idx]"""
        idx += 1
        ls = s.layer_state
        if not s.restore_point :
            s.restore_point = idx, tuple([ls[name] for name in s.layer_order[idx:]])
        else :
            rpi, rpd = s.restore_point
            rpd = [False]*(len(s.layer_order)-idx-len(rpd)) + list(rpd)
            nrpd = (ls[name] for name in s.layer_order[idx:])
            s.restore_point = idx, tuple([(new or old) for new, old in zip(nrpd,rpd)])

    def restore(s):
        rp = s.restore_point
        if not rp :
            return None
        ls = s.layer_state
        lo = s.layer_order
        for name, state in zip(lo[rp[0]:], rp[1]) :
            ls[name] = state
        s.restore_point = None

    def exclude_above(s,idx):
        """turns layers above idx off"""
        for key in s.layer_order[idx+1:]:
            s.layer_state[key] = False

    def exclude_below(s,idx):
        """turns layers below idx off, except default"""
        for key in s.layer_order[1:idx]:
            s.layer_state[key] = False

    def get_key_from_layer(s, idx,layer_name):
        return s.layers[layer_name][idx]

    def get_topmost_active_layer_index(s):
        for i,name in list(enumerate(s.layer_order))[::-1]:
            if s.layer_state[name] :
                return i+1
        return 0

    def __getitem__(s, pos:int|tuple):
        """what does __getitem__ does in this context ?
        returns a key value, whether it is a <str>, an <int>, a <LayerFunc> or None
        """
        if type(pos) is not int:
            assert isinstance(pos, tuple)
            assert len(pos) == 2
            c,r = pos
            assert 0 <= r < s.matrix_size[0]
            assert 0 <= c < s.matrix_size[1]
            idx = s.matrix_size[0] * r + c
        else :
            idx = pos
        layer_state = s.layer_state
        trans = TRANS
        for layer_name in s.layer_order[::-1]:
            if layer_state[layer_name]:
                k = s.layers[layer_name][idx]
                if k is trans:
                    continue
                elif k is None:
                    return None
                return k
        else :
            return s.layers["default"][idx]

class TOGGLE(LayerFunc):
    """TOGGLE is a key function that as the name suggest turns on or off a
    layer"""
    def __init__(s, parent, layer_name, exclude_above=True, restore = False):
        super().__init__(parent, layer_name, exclude_above, restore)
    def press(s):
        parent = s.parent
        state = parent.layer_state[s.layer_name]
        if s.restore :
            if not state :
                parent.create_restore_point(s.idx)
            else :
                parent.restore()
        if s.exclude_above and not state:
            parent.exclude_above(s.idx)
        parent.layer_state[s.layer_name] = not(parent.layer_state[s.layer_name])

class MOMENTARY(LayerFunc):
    """MOMENTARY is a key function that switches to a given layer as long as the
    key is pressed, and then turns if off as soon as it is released"""
    def __init__(s, parent, layer_name, exclude_above=True, restore = True):
        super().__init__(parent, layer_name, exclude_above, restore)
    def press(s):
        parent = s.parent
        if s.restore :
            parent.create_restore_point(s.idx)
        if s.exclude_above :
            parent.exclude_above(s.idx)
        parent.layer_state[s.layer_name] = True
    def depress(s, time_pressed=None):
        parent = s.parent
        if s.restore:
            parent.restore()
        parent.layer_state[s.layer_name] = False