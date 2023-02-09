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
    tim8 = pyb.Timer (8, prescaler=0, period=0xFFFF)
    tim3 = pyb.Timer (3, freq=20000)
    tim5 = pyb.Timer (5, freq=20000)

    pinC6 = pyb.Pin (pyb.Pin.board.PC6, pyb.Pin.OUT_PP) 
  
    pinC7 = pyb.Pin (pyb.Pin.board.PC7, pyb.Pin.OUT_PP)
      
      
    encreader1 = encoder_reader.EncoderReader(pinC6, pinC7, tim8)
      
    ENA = pyb.Pin (pyb.Pin.board.PA10, pyb.Pin.OUT_OD, pyb.Pin.PULL_UP)
    IN1A = pyb.Pin (pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
    IN2A = pyb.Pin (pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
      
    ENA.high()
      
    mdriver1 = motor_driver.MotorDriver(ENA, IN1A, IN2A, tim3)
    pdriver1 = position_driver.PositionDriver()
      
    p = True

    

    time = array.array("i",300*[0])
    pos1 = array.array("i",300*[0])
    pos2 = array.array("i",300*[0])

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

    timestart = utime.ticks_ms()


def task1_fun(shares):
    """!
    Task which puts things into a share and a queue.
    @param shares A list holding the share and queue used by this task
    """
    # Get references to the share and queue which have been passed to this task
    my_share, my_queue = shares

    counter = 0
    while True:
        my_share.put(counter)
        my_queue.put(counter)
        counter += 1

        yield 0


def task2_fun(shares):
    """!
    Task which takes things out of a queue and share and displays them.
    @param shares A tuple of a share and queue from which this task gets data
    """
    # Get references to the share and queue which have been passed to this task
    the_share, the_queue = shares

    while True:
        # Show everything currently in the queue and the value in the share
        print(f"Share: {the_share.get ()}, Queue: ", end='')
        while q0.any():
            print(f"{the_queue.get ()} ", end='')
        print('')

        yield 0


# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    pinsetup()
    print("Testing ME405 stuff in cotask.py and task_share.py\r\n"
          "Press Ctrl-C to stop and show diagnostics.")

    # Create a share and a queue to test function and diagnostic printouts
    share0 = task_share.Share('h', thread_protect=False, name="Share 0")
    q0 = task_share.Queue('L', 16, thread_protect=False, overwrite=False,
                          name="Queue 0")

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    task1 = cotask.Task(task1_fun, name="Task_1", priority=1, period=400,
                        profile=True, trace=False, shares=(share0, q0))
    task2 = cotask.Task(task2_fun, name="Task_2", priority=2, period=1500,
                        profile=True, trace=False, shares=(share0, q0))
    cotask.task_list.append(task1)
    cotask.task_list.append(task2)

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
    print('\n' + str (cotask.task_list))
    print(task_share.show_all())
    print(task1.get_trace())
    print('')
