# RepRap Ltd Upgrades to the Petoi Bittle Walking Robot

The [Petoi Bittle Robot Dog](https://www.petoi.com/pages/bittle-open-source-bionic-robot-dog) is a servo driven quadruped robot with an Arduino controller. But it also allows you to turn the Arduino inside it off and instead plug in a Raspberry Pi. This allows much more sophisticated control with essentially no space limitations on the size of the software driving the robot.

![RRL Petoi Bittle](https://github.com/RepRapLtd/Walking-robots/blob/main/Petoi/Pix/dog-in-progress.jpg)

Here is the experimental modified robot on it's development stand. Yes - we know the wires need to be tidied...

We have plugged in a WiFi Raspberry Pi Zero and connected up a small PCB of our own. As you can see we have also replaced the lower legs and the robot's original head with 3D printed ones.

The enhancements that we are in the process of making are:

1. Hall effect foot sensors, so the robot knows when its feet touch down.
2. Gold contacts on the feet, so the robot can find a charging mat and recharge itself automatically.
3. A small OLED display to convey information. On boot, this gives the robot's IP address.
4. The Pi's camera mounted on the head.
5. A LIDAR rangefinder, also on the head.

All these (except the camera) works using the Pi/Petoi's I2C interface.

This is very much work-in-progress, so the mechanical, electronic and software design WILL all change. But if you want to see what we have so far, the main items are:

1. Electronics/RRLInterface/ - the Kicad design for our custom PCB
2. Mechanics/Head Camera and Lidar Mount.FCStd - the FreeCAD design for the neck/head
3. Mechanics/Forearm/v3/ - the lower leg design with the Hall sensor
4. Software/TeachableMachine/ - AI vision to find the charging mat (see [Teachable Machine here](https://teachablemachine.withgoogle.com/))
5. Software/Pi/ - the Python control software for everything non-AI


