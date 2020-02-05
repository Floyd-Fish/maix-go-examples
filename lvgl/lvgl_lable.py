# lvgl_lable.py - By: Floydfish

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

label1 = lv.label(lv.scr_act())
label1.set_long_mode(lv.label.LONG.BREAK)     # Break the long lines
label1.set_recolor(True)                      # Enable re-coloring by commands in the text
label1.set_align(lv.label.ALIGN.CENTER)       # Center aligned lines
label1.set_text("#000080 Re-color# #0000ff words# #6666ff of a# label " +
                "and  wrap long text automatically.")
label1.set_width(150)
label1.align(None, lv.ALIGN.CENTER, 0, -30)

label2 = lv.label(lv.scr_act())
label2.set_long_mode(lv.label.LONG.SROLL_CIRC)     # Circular scroll
label2.set_width(150)
label2.set_text("It is a circularly scrolling text. ")
label2.align(None, lv.ALIGN.CENTER, 0, 30)
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
