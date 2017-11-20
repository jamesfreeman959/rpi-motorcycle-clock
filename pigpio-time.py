#!/usr/bin/env python

import time

import pigpio

import datetime
now = datetime.datetime.now()
print now.year, now.month, now.day, now.hour, now.minute, now.second

GPIO=17
GPIOMIN=18

square = []
minsquare = []

#                          ON       OFF    MICROS
#square.append(pigpio.pulse(1<<GPIO, 0,       500))
#square.append(pigpio.pulse(0,       1<<GPIO, 500))
#minsquare.append(pigpio.pulse(1<<GPIOMIN, 0,       500))
#minsquare.append(pigpio.pulse(0,       1<<GPIOMIN, 500))

pi = pigpio.pi() # connect to local Pi

pi.set_mode(GPIO, pigpio.OUTPUT)
pi.set_mode(GPIOMIN, pigpio.OUTPUT)

#pi.wave_add_generic(square)
#pi.wave_add_generic(minsquare)

#wid = pi.wave_create()
wid = 1
#if wid >= 0:
#  pi.wave_send_repeat(wid)
#  time.sleep(60)
#  pi.wave_tx_stop()
#  pi.wave_delete(wid)
#
#pi.stop()

if wid >= 0:
  while 1:
    datetime.datetime.now()
    if now.hour > 12:
      twelvehour = now.hour - 12
    else:
      twelvehour = now.hour

    halfperiod = 1000000/(2 * ( twelvehour + ( now.minute/60.0 ) ) * (202/12.0))
    minhalfperiod = (30000 * 63.0) / now.minute
    print("hour: %s, %s" % (twelvehour,halfperiod))
    print("hour: %s, %s" % (now.minute,minhalfperiod))

    square = []
    minsquare = []
    #                          ON       OFF    MICROS
    square.append(pigpio.pulse(1<<GPIO, 0,       halfperiod))
    square.append(pigpio.pulse(0,       1<<GPIO, halfperiod))

    minsquare.append(pigpio.pulse(1<<GPIOMIN, 0,       minhalfperiod))
    minsquare.append(pigpio.pulse(0,       1<<GPIOMIN, minhalfperiod))

    pi.wave_clear()
    
    pi.wave_add_generic(square)
    hourwid = pi.wave_create()

    pi.wave_add_generic(minsquare)
    minwid = pi.wave_create()

    #pi.wave_chain([hourwid, minwid, 255, 0,])
    pi.hardware_PWM(17, 100, 500000)
    #pi.wave_send_repeat(hourwid)
    #pi.wave_send_repeat(minwid)
    time.sleep(1)
