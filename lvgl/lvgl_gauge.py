# lvgl_gauge.py - By: Floydfish

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
lcd.clear(0xFFFF)
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

# Create a style
style = lv.style_t()
lv.style_copy(style, lv.style_pretty_color)
style.body.main_color = lv.color_hex3(0x666)     # Line color at the beginning
style.body.grad_color =  lv.color_hex3(0x666)    # Line color at the end
style.body.padding.left = 10                     # Scale line length
style.body.padding.inner = 8                     # Scale label padding
style.body.border.color = lv.color_hex3(0x333)   # Needle middle circle color
style.line.width = 3
style.text.color = lv.color_hex3(0x333)
style.line.color = lv.color_hex3(0xF00)          # Line color after the critical value

# Describe the color for the needles
needle_colors = [
    lv.color_make(0x00, 0x00, 0xFF),
    lv.color_make(0xFF, 0xA5, 0x00),
    lv.color_make(0x80, 0x00, 0x80)
]

# Create a gauge
gauge1 = lv.gauge(lv.scr_act())
gauge1.set_style(lv.gauge.STYLE.MAIN, style)
gauge1.set_needle_count(len(needle_colors), needle_colors)
gauge1.set_size(150, 150)
gauge1.align(None, lv.ALIGN.CENTER, 0, 20)

# Set the values
gauge1.set_value(0, 10)
gauge1.set_value(1, 20)
gauge1.set_value(2, 30)

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
