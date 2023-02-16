# ME405-Lab3

This repository allows the user to perform step response tests of 2 motors simultaneously. 

First, main.py must be run on the MCU. Then Computer_main.py must be run to get user input and send Kp and and setpoint values to the MCU, which performs the motor control tasks. After the step response test is complete, Computer_main.py will ask the user to type in "plot" to plot the graph of the step response test.

The MCU uses proportional control to make the motors rotate to the setpoint position. As long as the user doesn't input a Kp value that is too high or low, this program is able to accurately rotate the motors and keep them at the set position. However, if the Kp value is too high, the motor will oscillate around its setpoint, and if the Kp value is too low, the motor will not even begin to move. What Kp value is ideal depends on the setpoint, because setpoints that are very close to the initial position will require a higher Kp value to get the motor to begin moving.

## Figure 1:
