import digitalio
import board


class Kbd_Matrix:
    """Kbd_Matrix is used to set up your MCU to fit the the physical matrix you
    created. And also to report on the state of keys
    
    usage :
        Kbd_Matrix(inputs, outputs, pullup=True)
        
    arguments :
        inputs []str : list of strings where each string is the name of a pin,
            that will be used as input. That name must match one of the pin
            attributes from the module 'board'.
        
        ouputs []str : same sa inputs, but the pins are set as outputs
        
        pullup  bool : defaults to True. It does set the board pins in pullup or
            pulldown logic. Pullup means that the zero state (key not pressed)
            is 3.3v, and that the one state (key pressed) is 0v. Just pick one
            mode, does not really matter. Most people use pullup"""
    def __init__(s, inputs, outputs, pullup=True):
        s.pullup = pullup
        s.inputs = tuple(s.set_input(name) for name in inputs)  #TO CHECK
        s.outputs = tuple(s.set_output(name) for name in outputs)
        s.rows = s.inputs if len(s.inputs) < len(s.outputs) else s.outputs #assumes that there are less rows than columns
        s.cols = s.inputs if len(s.inputs) > len(s.outputs) else s.outputs
        s.length = len(s.inputs) * len(s.outputs)
        s.old_state = 0
        s._not = 0 if pullup else (1 << s.length) - 1
        
    def set_output(s,pin_name):
        "internal use only"
        pin = digitalio.DigitalInOut(getattr(board,pin_name))
        pin.direction = digitalio.Direction.OUTPUT
        pin.value = s.pullup
        return pin

    def set_input(s,pin_name):
        "internal use only"
        pin = digitalio.DigitalInOut(getattr(board, pin_name))
        pin.direction = digitalio.Direction.INPUT
        pin.pull = getattr( digitalio.Pull, "UP" if s.pullup else "DOWN" )
        return pin

    def bnot(s,num):
        "internal use only"
        return s._not ^ num

    def scan(s):
        """returns the state of physical keys
        NOTE : returned state is automatically converted (if necessary)
        in a pulldown logic"""
        res = 0
        len_row = len(s.cols)
        pullup = s.pullup
        logic = s._index_logic_columns_are_inputs if s.cols is s.inputs else s._index_logic_rows_are_inputs 
        for a, pin_out in enumerate(s.outputs):
            pin_out.value = not pullup
            for b, pin_in in enumerate(s.inputs):
                v = pin_in.value
                if v :
                    res |= v << logic(a,b, len_row)
            pin_out.value = pullup
        return s.bnot(res) if pullup else res

    def get_report(s):
        """ returns 3 lists of indices, repectively:
        newly released keys,
        newly pressed keys,
        previously pressed keys"""
        new_state = s.scan()
        diff = s.old_state ^ new_state
        nre = diff & s.old_state  # nre : N(ewly) RE(leased)
        npr = diff & new_state  # npr : N(ewly) PR(essed)
        ppr = s.bnot(diff) & new_state  # ppr : P(revioulsy) PR(essed)
        nre_idx = []
        npr_idx = []
        ppr_idx = []
        max = ( 1 << s.length ) - 1
        for x in range( s.length ) :
            filt = 1 << x
            if filt & nre :
                nre_idx.append(x)
            elif filt & npr :
                npr_idx.append(x)
            elif filt & ppr:
                ppr_idx.append(x)
            mask = max ^ ( ( 1 << ( x + 1 ) ) - 1 )
            nre, npr, ppr = mask & nre, mask & npr, mask & ppr
            if not any((nre,npr, ppr)):
                break
        s.old_state = new_state
        return nre_idx, npr_idx, ppr_idx

    @staticmethod
    def _index_logic_columns_are_inputs (a, b, len_row) :
        return a * len_row + b

    @staticmethod
    def _index_logic_rows_are_inputs (a, b, len_row) :
        return b * len_row + a