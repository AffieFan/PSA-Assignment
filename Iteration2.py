import time
import board
import digitalio


# --- PINS (edit these if needed) ---
RED_PIN = board.GP16
BLUE_PIN = board.GP17
THIRD_LED_PIN = board.GP11     # white or green LED
BUTTON_PIN = board.GP21


# --- LEDs ---
red = digitalio.DigitalInOut(RED_PIN)
red.direction = digitalio.Direction.OUTPUT


blue = digitalio.DigitalInOut(BLUE_PIN)
blue.direction = digitalio.Direction.OUTPUT


third = digitalio.DigitalInOut(THIRD_LED_PIN)
third.direction = digitalio.Direction.OUTPUT


# --- Button (to GND) with pull-up ---
btn = digitalio.DigitalInOut(BUTTON_PIN)
btn.direction = digitalio.Direction.INPUT
btn.pull = digitalio.Pull.UP  # not pressed=True, pressed=False


# Modes:
# 0 = OFF
# 1 = PURPLE (red+blue)
# 2 = THIRD LED (white/green)
mode = 0


def set_mode(m):
   if m == 0:          # OFF
       red.value = False
       blue.value = False
       third.value = False
   elif m == 1:        # PURPLE
       red.value = True
       blue.value = True
       third.value = False
   elif m == 2:        # WHITE/GREEN
       red.value = True
       blue.value = True
       third.value = True


set_mode(mode)


# --- debounce + press detection ---
last_state = btn.value
last_time = time.monotonic()
DEBOUNCE_S = 0.06


while True:
   now = time.monotonic()
   state = btn.value


   if state != last_state and (now - last_time) > DEBOUNCE_S:
       last_time = now
       last_state = state


       # pressed event (goes False)
       if state == False:
           mode = (mode + 1) % 3
           set_mode(mode)


   time.sleep(0.005)
