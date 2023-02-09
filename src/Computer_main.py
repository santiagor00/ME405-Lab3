"""!
@package docstring
Lab 2 - Out of Control

@file Computer_main.py

@brief Takes a value of kp and final position then starts running the motor. When done, makes plots.
@details Runs in a loop to repeat the process of starting the motor with potentially different kp and end position, and sends this over com4. Once all loops are complete, it prints a single plot with all runs separated.
"""

from matplotlib import pyplot
import serial

good = [False, False]

try:
    while True:

        print('enter "plot" in kp to plot the curve(s)')

        kp = input("what is the value of kp? ")
        if kp == "plot" or kp == "plot1": raise KeyboardInterrupt
        endpos = input("what is the final position? ")

        

        with serial.Serial("COM4",115200) as file:

            file.write(b"start")
            print("started")
            
            exec(f"file.write(b'{kp}')")

            file.write(b"\r \n")
            
            exec(f"file.write(b'{endpos}')")

            file.write(b"\r \n")
            
            waiter = file.in_waiting
            while waiter == 0:
                waiter = file.in_waiting
            

            data = []
            numx = []
            numy = []

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

                if good == [True,True]:
                    numx.append(x)
                    numy.append(y)
                elif good == [False,True]:
                    print(f"bad string {sep[0]}")
                elif good == [True,False]:
                    print(f"bad string {sep[1]}")
                else:
                    print(f"both strings bad {sep}")

                    
        #titley = titley.strip()
        pyplot.plot(numx,numy)
        pyplot.xlabel("time (ms)")
        pyplot.ylabel("Position")

except KeyboardInterrupt:
    if kp == "plot1":
        pyplot.legend(["kp too low","kp too high","kp perfect"])
    print("stopped")
    pyplot.show()
