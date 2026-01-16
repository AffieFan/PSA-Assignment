import time
import board
import digitalio


# --- PIN SETTING ---

purple_chain_pin = board.GP18   #red+blue series chain
green_pin = board.GP11          #green LED
button_pin = board.GP21        # button to GND


# --- Outputs ---
purple_chain = digitalio.DigitalInOut(purple_chain_pin)
purple_chain.direction = digitalio.Direction.OUTPUT


green = digitalio.DigitalInOut(green_pin)
green.direction = digitalio.Direction.OUTPUT


# --- Button input with pull-up ---
button = digitalio.DigitalInOut(button_pin)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP  # not pressed = True, pressed = False


mode = 0  # 0=OFF, 1=purple chain ON, 2=green ON


def set_mode(m):
   if m == 0:
       purple_chain.value = False
       green.value = False
   elif m == 1:
       purple_chain.value = True
       green.value = False
   elif m == 2:
       purple_chain.value = False
       green.value = True


set_mode(mode)


# --- debounce + press detection ---
last_state = button.value
last_time = time.monotonic()


while True:
   now = time.monotonic()
   state = button.value


   # debounce window (0.06 s)
   if state != last_state and (now - last_time) > 0.06:
       last_time = now
       last_state = state


       # pressed (goes False because pull-up)
       if state == False:
           mode = (mode + 1) % 3
           set_mode(mode)


   time.sleep(0.005)
