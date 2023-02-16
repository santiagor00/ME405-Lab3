"""!
@package docstring
Lab 3 - On schedule

@file Computer_main.py

@brief Takes a values of kp and final position then asks MCU to start running the motors. When done, makes plot.
@details First, main.py must be run on the MCU. Then this program must be run to send Kp and and setpoint values to the MCU, which performs the motor control tasks. After the step response test is complete, this program will ask the user to type in "plot" to plot the graph of the step response test.
"""

from matplotlib import pyplot
import serial

good = [False, False, False, False]

try:
    while True:

        print('enter "plot" in kp to plot the curve(s)')

        kp1 = input("what is the value of kp for motor 1? ")
        if kp1 == "plot" or kp1 == "plot1": raise KeyboardInterrupt
        endpos1 = input("what is the final position for motor 1? ")
        kp2 = input("what is the value of kp for motor 2? ")
        endpos2 = input("what is the final position for motor 2? ")

        

        with serial.Serial("COM7",115200) as file:

            file.write(b"start")
            print("started")
            
            exec(f"file.write(b'{kp1}')")

            file.write(b"\r \n")
            
            exec(f"file.write(b'{endpos1}')")

            file.write(b"\r \n")

            exec(f"file.write(b'{kp2}')")

            file.write(b"\r \n")
            
            exec(f"file.write(b'{endpos2}')")

            file.write(b"\r \n")
            
            waiter = file.in_waiting
            while waiter == 0:
                waiter = file.in_waiting
                #print(waiter)
            

            data = []
            numx1 = []
            numy1 = []
            numx2 = []
            numy2 = []

            for asdf in range(50):
                datastr = file.readline()
                data.append(datastr.decode())

            
            for line in data:
                str = line
                sep = str.split(",")



                try:
                    sep[0] = sep[0].strip()
                    sep[0] = sep[0].strip(" '#Aabcdefghijklmnopqrstuvwxyz ")
                    x = float(sep[0])  
                except ValueError:
                    good[0] = False
                except IndexError:
                    good[0] = False
                else:
                    good[0] = True
                    
                try:
                    sep[1] = sep[1].strip()
                    strip = sep[1].strip(" '#Aabcdefghijklmnopqrstuvwxyz ")
                    y = float(strip)
                except ValueError:
                    good[1] = False
                except IndexError:
                    good[1] = False
                else:
                    good[1] = True

                try:
                    sep[2] = sep[2].strip()
                    strip = sep[2].strip(" '#Aabcdefghijklmnopqrstuvwxyz ")
                    z = float(strip)
                except ValueError:
                    good[2] = False
                except IndexError:
                    good[2] = False
                else:
                    good[2] = True

                try:
                    sep[3] = sep[3].strip()
                    strip = sep[3].strip(" '#Aabcdefghijklmnopqrstuvwxyz ")
                    w = float(strip)
                except ValueError:
                    good[3] = False
                except IndexError:
                    good[3] = False
                else:
                    good[3] = True

                if good == [True,True,True,True]:
                    numx1.append(x)
                    numy1.append(y)
                    numx2.append(z)
                    numy2.append(w)
                elif good == [False,True,True,True]:
                    print(f"bad string {sep[0]}")
                elif good == [True,False,True,True]:
                    print(f"bad string {sep[1]}")
                elif good == [True,True,False,True]:
                    print(f"bad string {sep[2]}")
                else:
                    print(f"2-4 strings bad {sep}")



                    
        #titley = titley.strip()
        pyplot.plot(numx1,numy1)
        pyplot.plot(numx2, numy2)
        pyplot.xlabel("time (ms)")
        pyplot.ylabel("Position")




except KeyboardInterrupt:
    if kp1 == "plot1":
        pyplot.legend(["kp too low","kp too high","kp perfect"])
    print("stopped")
    pyplot.show()
