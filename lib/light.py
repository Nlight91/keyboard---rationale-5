import digitalio
import board
import time

class Led:
    """Led class is used to create luminous sequence with the onboard led
    
    For now, it can only generate a sequence reflecting a number
    
    Usage example :
    >>> led = LED()
    >>> led.layer_index(2)
    >>> while 1:
    ...     led.process()
    ...     time.sleep(0.002)
    """
    def __init__(s, dot_time:int=166 ):
        s.led = digitalio.DigitalInOut(board.LED)
        s.led.direction = digitalio.Direction.OUTPUT
        s.time_sequence_start = None
        s.run_func = None
        s.dot_time = 166 #ms
        s.dash_time = s.dot_time * 3
        s.sequence_playing = None
        s.sequence_step = None
        
    def sequence_generator(s, sequence:str=""):
        """sequence is a n length string
         it only accepts two characters :
            - "0" : represent a dot
            - "1" : represent a dash
        tm = tm + s.dot_time * 7
        yield ( tm, 0 )
        for c in sequence :
            if c == "0" :
                tm += s.dot_time
                yield (tm, 1)
                tm += s.dot_time
                yield (tm, 0)
            elif c == "1" :
                tm += s.dash_time
                yield (tm, 1)
                tm += s.dot_time
                yield (tm, 0)
    
    def sequence_state_at(s, delta):
        for tm, state in s.sequence_playing :
            if delta <= tm :
                return state
        s.time_sequence_start = time.monotonic()
    
    def set_number(s, index=0):
        s.sequence_playing = tuple(s.sequence_generator(f"{index:0>3b}"))
        s.sequence_step = next(s.sequence_playing)
        s.time_sequence_start = time.monotonic()
        
    def process(s):
        delta_time = time.monotonic() - s.time_sequence_start
        s.led.value = bool(s.sequence_state_at(delta_time))
        
        
        
            
    
 