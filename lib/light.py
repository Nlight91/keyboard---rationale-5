import digitalio
import board
import time

class Led:
    """Led class is used to create luminous sequence with the onboard led
    
    For now, it can only generate a sequence reflecting a number
    
    Usage example :
    >>> led = LED()
    >>> led.set_number(2)
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
        s._led_state = None
        
    def sequence_generator(s, sequence:str=""):
        """sequence is a n length string
         it only accepts two characters :
            - "0" : represent a dot
            - "1" : represent a dash
        yield tuples following this structure :
            - time in milliseconds,
            - state
        the time element states for how long the state should be maintained
        for example, let's admit the following sequence parameter "10", which is one dash(3u on) and one dot(1u on)
        the first tuple will be a space : 7u off (0+7)
        the second tuple will be a dash : 10u on (7+3)
        the third will be a separator   : 11u off(10+1)
        the fourth will be a dot        : 12u on (11+1)
        the fifth will be a separato    : 13u off(12+1)
        """
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
    
    def _sequence_state_at(s, delta:int)->int:
        """-- for internal use --
        returns the led state when said state changes"""
        for tm, state in s.sequence_playing :
            if delta <= tm :
                if state != s._led_state:
                    s._led_state = state
                    return state
                return None
        s.time_sequence_start = time.monotonic()
    
    def set_number(s, number=0):
        """set the sequence playing to the binary morse code representing the number number"""
        s.sequence_playing = tuple(s.sequence_generator(f"{number:0>3b}"))
        s.sequence_step = next(s.sequence_playing)
        s.time_sequence_start = time.monotonic()
        
    def process(s):
        delta_time = time.monotonic() - s.time_sequence_start
        state = s._sequence_state_at(delta_time)
        if state != None : 
            s.led.value = bool(state)
        
        
        
            
    
 