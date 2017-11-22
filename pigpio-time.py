#!/usr/bin/env python

import time

import pigpio

import datetime

import sys

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

lasthour = 0
lastminute = 0

if wid >= 0:
  while 1:
    now = datetime.datetime.now()
    if now.hour > 12:
      twelvehour = now.hour - 12
    elif now.hour == 0:
      # Prevent divide by zero errors - this is a 12 hour dial so "0" is actually 12am
      twelvehour = 12
    else:
      twelvehour = now.hour

    if(now.hour==lasthour and now.minute==lastminute):
      # No update required if no change - let the pulse trains continue
      sys.stdout.write('.')
    else:
      lasthour = now.hour
      lastminute = now.minute

      halfperiod = 1000000/(2 * ( twelvehour + ( now.minute/60.0 ) ) * (202/12.0))
      if now.minute > 0:
        minhalfperiod = (30000 * 63.0) / now.minute
      else:  
        minhalfperiod = 0
      print("hour: %s, half period in us: %s" % (twelvehour,halfperiod))
      print("minute: %s, half-period in us: %s" % (now.minute,minhalfperiod))

      square = []
      minsquare = []
      # Duration of pulse train in us (1000000us = 1s)
      duration = 10000000

      pi.wave_clear()

      # Build up 1s worth of pulses for the hour - do a simple integer division - this is
      # accurate enough for our use case
      for i in xrange(int(duration/(2*halfperiod))):
        #                          ON       OFF    MICROS
        square.append(pigpio.pulse(1<<GPIO, 0,       halfperiod))
        square.append(pigpio.pulse(0,       1<<GPIO, halfperiod))

      pi.wave_add_generic(square)

      if(minhalfperiod>0):
        # Now build up 1s worth of pulses for the minute readout as above
        for i in xrange(int( duration / ( 2 * minhalfperiod ) ) ):
          minsquare.append(pigpio.pulse(1<<GPIOMIN, 0,       minhalfperiod))
          minsquare.append(pigpio.pulse(0,       1<<GPIOMIN, minhalfperiod))
      else:
        # Minutes == 0 should mean a DC output (i.e. no ON pulse)  
        for i in xrange(int(duration/(2*halfperiod))):
          minsquare.append(pigpio.pulse(0,       1<<GPIOMIN, minhalfperiod*2))
    
      pi.wave_add_generic(minsquare)
  
      wid = pi.wave_create()

      pi.wave_send_repeat(wid)
      #pi.wave_send_repeat(minwid)

    time.sleep(1)
