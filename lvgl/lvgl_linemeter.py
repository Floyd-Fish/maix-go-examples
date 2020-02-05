# lvgl_linemeter.py - By: Floydfish

import lvgl as lv
import lvgl_helper as lv_h
import lcd
import time
from machine import I2C
from machine import Timer
import touchscreen as ts

Horizonal_res = 320
Vertical_res = 240

# Initialize peripherals
i2c = I2C (I2C.I2C0, freq = 400000, scl = 30, sda = 31)
lcd.init()
ts.init (i2c)
lv.init()

disp_buf1 = lv.disp_buf_t()
buf_size = (Horizonal_res * Vertical_res)//4
buf1_1 = bytearray(buf_size)
lv.disp_buf_init(disp_buf1, buf1_1, None, len(buf1_1) // 4)
disp_drv = lv.disp_drv_t()
lv.disp_drv_init (disp_drv)
disp_drv.buffer = disp_buf1
disp_drv.flush_cb = lv_h.flush
disp_drv.hor_res = Horizonal_res
disp_drv.ver_res = Vertical_res
lv.disp_drv_register(disp_drv)


indev_drv = lv.indev_drv_t()
lv.indev_drv_init (indev_drv)
indev_drv.type = lv.INDEV_TYPE.POINTER
indev_drv.read_cb = lv_h.read
lv.indev_drv_register (indev_drv)

# **********************************
#   Start your codes here.
# **********************************

# Create a style for the line meter
style_lmeter = lv.style_t()
lv.style_copy(style_lmeter, lv.style_pretty_color)
style_lmeter.line.width = 2
style_lmeter.line.color = lv.color_hex(0xc0c0c0)              # Silver
style_lmeter.body.main_color = lv.color_hex(0x91bfed)         # Light blue
style_lmeter.body.grad_color = lv.color_hex(0x04386c)         # Dark blue
style_lmeter.body.padding.left = 16                           # Line length

# Create a line meter
lmeter = lv.lmeter(lv.scr_act())
lmeter.set_range(0, 100)                    # Set the range
lmeter.set_value(80)                        # Set the current value
lmeter.set_scale(240, 31)                   # Set the angle and number of lines
lmeter.set_style(lv.lmeter.STYLE.MAIN, style_lmeter)          # Apply the new style
lmeter.set_size(150, 150)
lmeter.align(None, lv.ALIGN.CENTER, 0, 0)

# **********************************
#   End your codes here.
# **********************************

def on_timer(timer):
    lv.tick_inc(5)

timer = Timer(Timer.TIMER0, Timer.CHANNEL0, mode = Timer.MODE_PERIODIC, period = 5, unit = Timer.UNIT_MS, callback = on_timer, arg = None)

while True :
    tim = time.ticks_ms()
    lv.task_handler()
    while time.ticks_ms() - tim < 5 :
        pass
