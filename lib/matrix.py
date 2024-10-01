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
    def __init__(s, inputs, outputs, pullup=True, less_rows_than_columns=True):
        s.pullup = pullup
        s.inputs = tuple(s.set_input(name) for name in inputs)  #TO CHECK
        s.outputs = tuple(s.set_output(name) for name in outputs)
        lin = len(s.inputs)
        lout = len(s.outputs)
        if less_rows_than_columns:
            s.rows = s.inputs  if lin <= lout else s.outputs
            s.cols = s.outputs if lin <= lout else s.inputs
        elif not less_rows_than_columns :
            s.rows = s.inputs  if lin > lout else s.outputs
            s.cols = s.outputs if lin > lout else s.inputs
        s.length = len(s.inputs) * len(s.outputs)
        s.old_state = 0
        s._full_mask = (1 << s.length) - 1
        
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

    def _ones_complement(s,num):
        """internal use only
        one's complement reverse each bit of a number"""
        return s._full_mask ^ num

    def scan(s)->int:
        NOTE : returned state is automatically converted (if necessary)
        in a pulldown logic"""
        res = 0
        len_row = len(s.cols) # length of each row
        pullup = s.pullup
        col_is_input = s.cols is s.inputs
        for a, pin_out in enumerate(s.outputs):
            pin_out.value = not pullup
            for b, pin_in in enumerate(s.inputs):
                v = pin_in.value
                if v :
                    res |= v << s._grid_to_flat_index(a,b, len_row, col_is_input)
            pin_out.value = pullup
        return s._ones_complement(res) if pullup else res

    def get_report(s)->tuple[list,list,list]:
        """ returns 3 lists of indices, repectively:
        newly released keys,
        newly pressed keys,
        previously pressed keys
        
        indices in the lists are the indices of the key pressed in a mapping
        (whichever one)"""
        new_state = s.scan()
        diff = s.old_state ^ new_state
        nre = diff & s.old_state  # nre : N(ewly) RE(leased)
        npr = diff & new_state  # npr : N(ewly) PR(essed)
        spr = s.old_state & new_state  # spr : S(till) PR(essed)
        all_states = new_state | s.old_state
        nre_idx = []
        npr_idx = []
        spr_idx = []
        max = s._full_mask
        for x in range( s.length ) :
            filt = 1 << x
            if filt & nre :
                nre_idx.append(x)
            elif filt & npr :
                npr_idx.append(x)
            elif filt & spr:
                spr_idx.append(x)
            mask = max ^ ( ( filt << 1 ) - 1 )
            if not (all_states & mask) :
                # no keys left
                break
        s.old_state = new_state
        return nre_idx, npr_idx, spr_idx
    
    @staticmethod
    def _grid_to_flat_index(out_index:int, in_index:int, len_row:int, col_is_input:bool)->int:
        """convert grid coordinates into flat array coordinates"""
        if col_is_input : row, col = out_index, in_index
        else : row, col = in_index, out_index
        return row * len_row + col