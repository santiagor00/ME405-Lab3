"""!
@package docstring
Lab 2 - Out of Control

@file Computer_main.py

@brief Takes a value of kp and final position then starts running the motor. When done, makes plots.
@details Runs in a loop to repeat the process of starting the motor with potentially different kp and end position, and sends this over com4. Once all loops are complete, it prints a single plot with all runs separated.
"""

from matplotlib import pyplot
import serial

good = [False, False, False]

try:
    while True:

        print('enter "plot" in kp to plot the curve(s)')

        kp1 = input("what is the value of kp for motor 1? ")
        if kp1 == "plot" or kp1 == "plot1": raise KeyboardInterrupt
        endpos1 = input("what is the final position for motor 1? ")
        kp2 = input("what is the value of kp for motor 2? ")
        endpos2 = input("what is the final position for motor 1? ")

        

        with serial.Serial("COM4",115200) as file:

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
            

            data = []
            numx = []
            numy = []
            numz = []

            for asdf in range(300):
                datastr = file.readline()
                data.append(datastr.decode())
            
            for line in data:
                str = line
                sep = str.split(",")

                try:
                    sep[0] = sep[0].strip()
                    sep[0] = sep[0].strip(" #Aabcdefghijklmnopqrstuvwxyz ")
                    x = float(sep[0])  
                except ValueError:
                    good[0] = False
                except IndexError:
                    good[0] = False
                else:
                    good[0] = True
                    
                try:
                    sep[1] = sep[1].strip()
                    strip = sep[1].strip(" #Aabcdefghijklmnopqrstuvwxyz ")
                    y = float(strip)
                except ValueError:
                    good[1] = False
                except IndexError:
                    good[1] = False
                else:
                    good[1] = True

                try:
                    sep[2] = sep[2].strip()
                    strip = sep[2].strip(" #Aabcdefghijklmnopqrstuvwxyz ")
                    z = float(strip)
                except ValueError:
                    good[2] = False
                except IndexError:
                    good[2] = False
                else:
                    good[2] = True

                if good == [True,True,True]:
                    numx.append(x)
                    numy.append(y)
                    numz.append(z)
                elif good == [False,True,True]:
                    print(f"bad string {sep[0]}")
                elif good == [True,False,True]:
                    print(f"bad string {sep[1]}")
                elif good == [True,True,False]:
                    print(f"bad string {sep[2]}")
                else:
                    print(f"2-3 strings bad {sep}")

                    
        #titley = titley.strip()
        pyplot.plot(numx,numy)
        pyplot.xlabel("time (ms)")
        pyplot.ylabel("Position")

except KeyboardInterrupt:
    if kp1 == "plot1":
        pyplot.legend(["kp too low","kp too high","kp perfect"])
    print("stopped")
    pyplot.show()
