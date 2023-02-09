"""!
@file basic_tasks.py
    This file contains a demonstration program that runs some tasks, an
    inter-task shared variable, and a queue. The tasks don't really @b do
    anything; the example just shows how these elements are created and run.

@author JR Ridgely
@date   2021-Dec-15 JRR Created from the remains of previous example
@copyright (c) 2015-2021 by JR Ridgely and released under the GNU
    Public License, Version 2. 
"""

import gc
import pyb
import cotask
import task_share

import utime
import motor_driver
import encoder_reader
import position_driver
import array
from pyb import repl_uart
from pyb import UART


def pinsetup():

    n = 0
    start = "a"
    waiter = 0
    class motor:
        def __init__(self):
            self.kp = 0
            self.endpos = 0
    
    m1 = motor()
    m2 = motor()

    repl_uart(None)

    ser = UART(2,115200)
    while start != "start":
        waiter = ser.any()
        while waiter == 0:
            waiter = ser.any()
        startbyte = ser.read(5)
        
        start = startbyte.decode()

        utime.sleep_ms(5)
    
    m1.kp = ser.readline()
    m1.endpos = ser.readline()
    m2.kp = ser.readline()
    m2.endpos = ser.readline()

    m1.kp = m1.kp.decode()
    m1.endpos = m1.endpos.decode()
    m2.kp = m2.kp.decode()
    m2.endpos = m2.endpos.decode()

    m1.kp = m1.kp.strip()
    m1.endpos = m1.endpos.strip()
    m2.kp = m2.kp.strip()
    m2.endpos = m2.endpos.strip()

    m1.kp = int(m1.kp)
    m1.endpos = int(m1.endpos)
    m2.kp = int(m2.kp)
    m2.endpos = int(m2.endpos)

    return m1,m2


def motor1(shares1):
    """!
    Task which puts things into a share and a queue.
    @param shares A list holding the share and queue used by this task
    """
    # Get references to the share and queue which have been passed to this task
    qtim1, qpos1, skp1, sendpos1, fin = shares1

    tim8 = pyb.Timer (8, prescaler=0, period=0xFFFF)
    tim3 = pyb.Timer (3, freq=20000)

    pinC6 = pyb.Pin (pyb.Pin.board.PC6, pyb.Pin.OUT_PP) 
    pinC7 = pyb.Pin (pyb.Pin.board.PC7, pyb.Pin.OUT_PP)
      
    encreader1 = encoder_reader.EncoderReader(pinC6, pinC7, tim8)
      
    ENA = pyb.Pin (pyb.Pin.board.PA10, pyb.Pin.OUT_OD, pyb.Pin.PULL_UP)
    IN1A = pyb.Pin (pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
    IN2A = pyb.Pin (pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
      
    ENA.high()
      
    mdriver1 = motor_driver.MotorDriver(ENA, IN1A, IN2A, tim3)

    pdriver = position_driver.PositionDriver()

    pdriver.run(encreader1.read(),sendpos1.get() ,skp1.get())

    timestart = utime.ticks_ms()

    n=0

    while True:
        posnow = encreader1.read()
        level = pdriver.run(posnow)
        mdriver1.set_duty_cycle(level)
        timenow = utime.ticks_ms()
        if n != 300:
            qtim1.put(utime.ticks_diff(timenow,timestart))
            qpos1.put(posnow)
            n += 1
        else:
            fin.put(fin.get()+1)

        yield 0


def motor2(shares2):
    """!
    Task which takes things out of a queue and share and displays them.
    @param shares A tuple of a share and queue from which this task gets data
    """
    # Get references to the share and queue which have been passed to this task
    qtim2, qpos2, skp2, sendpos2, fin = shares2

    tim4 = pyb.Timer (4, prescaler=0, period=0xFFFF)
    tim5 = pyb.Timer (5, freq=20000)

    pinB6 = pyb.Pin (pyb.Pin.board.pB6, pyb.pin.OUT_PP)
    pinB7 = pyb.Pin (pyb.Pin.board.pB7, pyb.pin.OUT_PP)

    encreader2 = encoder_reader.EncoderReader(pinB6, pinB7, tim4)

    ENB = pyb.Pin (pyb.Pin.board.PC1, pyb.Pin.OUT_OD, pyb.Pin.PULL_UP)
    IN1B = pyb.Pin (pyb.Pin.board.PA0, pyb.Pin.OUT_PP)
    IN2B = pyb.Pin (pyb.Pin.board.PA1, pyb.Pin.OUT_PP)
    
    ENB.high()

    mdriver2 = motor_driver.MotorDriver(ENB, IN1B, IN2B, tim5)

    pdriver = position_driver.PositionDriver()

    pdriver.run(encreader2.read(),sendpos2.get() ,skp2.get())

    timestart = utime.ticks_ms()

    n=0

    while True:
        posnow = encreader2.read()
        level = pdriver.run(posnow)
        mdriver2.set_duty_cycle(level)
        timenow = utime.ticks_ms()
        if n != 300:
            qtim2.put(utime.ticks_diff(timenow,timestart))
            qpos2.put(posnow)
            n += 1
        else:
            fin.put(fin.get()+1)

        yield 0

def serprint(shares):
    qtim1, qpos1, qtim2, qpos2 = shares

    ser.write(f"{time[i]},{pos[i]}\r \n")

    yield 0


# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    m1,m2 = pinsetup()
    print("Testing ME405 stuff in cotask.py and task_share.py\r\n"
          "Press Ctrl-C to stop and show diagnostics.")

    # Create a share and a queue to test function and diagnostic printouts
    """share0 = task_share.Share('h', thread_protect=False, name="Share 0")
    q0 = task_share.Queue('L', 16, thread_protect=False, overwrite=False, name="Queue 0")
    """
    qtim1 = task_share.Queue('i',16,thread_protect=False,overwrite=False,name="time1")
    qpos1 = task_share.Queue('i',16,thread_protect=False,overwrite=False,name="position1")
    qtim2 = task_share.Queue('i',16,thread_protect=False,overwrite=False,name="time2")
    qpos2 = task_share.Queue('i',16,thread_protect=False,overwrite=False,name="position2")

    skp1 = task_share.share("i", thread_protect=False, name="shared_kp1")
    sendpos1 = task_share.share("i",thread_protect=False, name="shared_endpos1")
    skp2 = task_share.share("i", thread_protect=False, name="shared_kp2")
    sendpos2 = task_share.share("i",thread_protect=False, name="shared_endpos2")
    fin = task_share.share("i", thread_protect=False, name="finished")

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    """task1 = cotask.Task(task1_fun, name="Task_1", priority=1, period=400, profile=True, trace=False, shares=(share0, q0))
    task2 = cotask.Task(task2_fun, name="Task_2", priority=2, period=1500, profile=True, trace=False, shares=(share0, q0))
    cotask.task_list.append(task1)
    cotask.task_list.append(task2)
    """

    skp1.put(m1.kp)
    sendpos1.put(m2.endpos)
    skp2.put(m2.kp)
    sendpos2.put(m2.endpos)
    fin.put(0)

    mot1 = cotask.Task(motor1, name = "motor_1", priority=1, period=15, profile=True, trace=False, shares=(qtim1,qpos1,skp1,sendpos1,fin))
    mot2 = cotask.Task(motor2, name = "motor_2", priority=1, period=15, profile=True, trace=False, shares=(qtim2,qpos2,skp2,sendpos2,fin))
    arr = cotask.Task(serprint, name = "serial_print", priority=2, period=15, profile=True, trace=False, shares=(qtim1,qpos1,qtim2,qpos2,fin))

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect()

    # Run the scheduler with the chosen scheduling algorithm. Quit if ^C pressed
    while True:
        try:
            cotask.task_list.pri_sched()
        except KeyboardInterrupt:
            break

    # Print a table of task data and a table of shared information data
    """print('\n' + str (cotask.task_list))
    print(task_share.show_all())
    print(task1.get_trace())
    print('')
    """
