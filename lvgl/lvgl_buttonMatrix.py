# lvgl_buttonMatrix.py - By: Floydfish

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

def event_handler(obj, event):
    if event == lv.EVENT.VALUE_CHANGED:
        txt = obj.get_active_btn_text()
        print("%s was pressed" % txt)

btnm_map = ["1", "2", "3", "4", "5", "\n",
            "6", "7", "8", "9", "0", "\n",
            "Action1", "Action2", ""]

btnm1 = lv.btnm(lv.scr_act())
btnm1.set_map(btnm_map)
btnm1.set_btn_width(10, 2)        # Make "Action1" twice as wide as "Action2"
btnm1.align(None, lv.ALIGN.CENTER, 0, 0)
btnm1.set_event_cb(event_handler)

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
