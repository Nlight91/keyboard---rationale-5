from scancodes import TRANS
import time

class LayerFunc:
    @property
    def idx(s):
        if s._idx is None :
            s._idx = s.parent.layer_order.index(s.layer_name)
        return s._idx
    def __init__(s, parent, layer_name, exclude_above=True, restore = False):
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
    """
    def __init__(s, size ):
        assert isinstance(size, tuple)
        assert len(size)==2
        s.matrix_size = size
        s.tapped_layer = None
        s.layers = {"default":[]}
        s.layer_order = []
        s.layer_state = {}
        s.restore_point = None
        s.TOGGLE = s._class_dec(TOGGLE)
        s.MOMENTARY = s._class_dec(MOMENTARY)
        s.MOTO = s._class_dec(MOTO)
        s.TAP = s._class_dec(TAP)

    def _class_dec(s, cls):
        """decorator used to insert a Layer isntance reference
        into parameters of [cls].__init__ call"""
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

    def tapped(s):
        return bool(s.tapped_layer)

    def untap(s):
        """turns off any layer activated by a tap modifier"""
        if s.tapped_layer :
            s.layer_state[s.tapped_layer] = False
            s.tapped_layer = None
            return True
        else :
            return False

    def exclude_above(s,idx):
        """turns layers above idx off"""
        for key in s.layer_order[idx+1:]:
            s.layer_state[key] = False

    def exclude_below(s,idx):
        """turns layers below idx off, except default"""
        for key in s.layer_order[1:idx]:
            s.layer_state[key] = False

    def get_key_from_layer(idx,layer_name):
        return s.layers[layer_name][idx]

    def __getitem__(s, pos):
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

class MOTO(LayerFunc):
    def __init__(s, parent, layer_name, exclude_above=True, restore = True, timing=0.12):
        super().__init__(parent, layer_name, exclude_above, restore)
        s.TIMING_MOTO = timing
        s.pressed_at = None
    def beyond_timing(s):
        if s.pressed_at :
            return (time.time() - s.pressed_at) > s.TIMING_MOTO
    def press(s):
        parent = s.parent
        state = parent.layer_state[s.layer_name]
        if not state :
            if s.restore :
                parent.create_restore_point(s.idx)
            if s.exclude_above :
                parent.exclude_above(s.idx)
            s.pressed_at = time.time()
            parent.layer_state[s.layer_name] = True
        else :
            if s.pressed_at :
                s.pressed_at = None
            if s.restore :
                parent.restore()
            parent.layer_state[s.layer_name] = False
    def depress(s):
        parent = s.parent
        if s.pressed_at and s.beyond_timing() :
            if s.restore:
                parent.restore()
            parent.layer_state[s.layer_name] = False
            s.pressed_at = None

class TAP(LayerFunc):
    def __init__(s, parent, layer_name, exclude_above=True, restore = True):
        super().__init__(parent, layer_name, exclude_above, restore)
    def depress(s):
        parent = s.parent
        parent.untap()
        if s.restore :
            parent.create_restore_point(s.idx)
        if s.exclude_above:
            parent.exclude_above(s.idx)
        parent.layer_state[s.layer_name] = True
        parent.tapped_layer = s.layer_name
