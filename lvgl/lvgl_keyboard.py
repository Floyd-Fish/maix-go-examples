# lvgl_keyboard.py - By: Floydfish

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

# Create styles for the keyboard
rel_style = lv.style_t()
pr_style  = lv.style_t()

lv.style_copy(rel_style, lv.style_btn_rel)
rel_style.body.radius = 0
rel_style.body.border.width = 1

lv.style_copy(pr_style, lv.style_btn_pr)
pr_style.body.radius = 0
pr_style.body.border.width = 1

# Create a keyboard and apply the styles
kb = lv.kb(lv.scr_act())
kb.set_cursor_manage(True)
kb.set_style(lv.kb.STYLE.BG, lv.style_transp_tight)
kb.set_style(lv.kb.STYLE.BTN_REL, rel_style)
kb.set_style(lv.kb.STYLE.BTN_PR, pr_style)

# Create a text area. The keyboard will write here
ta = lv.ta(lv.scr_act())
ta.align(None, lv.ALIGN.IN_TOP_MID, 0, 10)
ta.set_text("")

# Assign the text area to the keyboard
kb.set_ta(ta)

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
