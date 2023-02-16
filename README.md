# ME405-Lab3

This repository allows the user to perform step response tests of 2 motors simultaneously. 

First, main.py must be run on the MCU. Then Computer_main.py must be run to get user input and send Kp and and setpoint values to the MCU, which performs the motor control tasks. After the step response test is complete, Computer_main.py will ask the user to type in "plot" to plot the graph of the step response test.
To perform another step response test, stop both programs (main.py and Computer_main.py) and repeat the instructions in this paragraph.

The MCU uses proportional control to make the motors rotate to the setpoint position. As long as the user doesn't input a Kp value that is too high or low, this program is able to accurately rotate the motors and keep them at the set position. However, if the Kp value is too high, the motor will oscillate around its setpoint, and if the Kp value is too low, the motor will not even begin to move. What Kp value is ideal depends on the setpoint, because setpoints that are very close to the initial position will require a higher Kp value to get the motor to begin moving.

The period of the motor control task used in this program is 35 ms. This value was used because it is not excessively fast, while allowing for motor control performance similar to the performance using faster periods. This was tested using a motor connected to a metal flywheel.

## Figure 1: Task Just Fast Enough
This plot shows the step response of a motor attached to a flywheel when then motor control task period was 45 ms. The setpoint was 15000, and the Kp was 10. Making the period smaller than 45 ms did not cause any noticable improvements in the response. However, it is recommended to use a 35 ms motor control task period to provide a safety factor.

## Figure 2: Task Too Slow
This plot shows the step response of a motor attached to a flywheel when the motor contol task period was 60 ms. The setpoint was 15000, and the Kp was 10. Notice how the motor overshoots the setpoint, despite having the same setpoint and Kp as the previous figure. This is because when the period is too slow, the motor keeps moving past the setpoint long after passing it, until the motor speed is updated the next time the motor control task is run. 
