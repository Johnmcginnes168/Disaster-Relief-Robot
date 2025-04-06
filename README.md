# Disaster Relief Robot (DisasterBot)

## Introduction

The **Disaster Relief Robot (DisasterBot)** is designed for use in disaster recovery scenarios, particularly in environments where it is dangerous for human rescue teams to operate. This project simulates a robot navigating a hotel room after an earthquake, overcoming obstacles, and locating survivors autonomously.

The robot's mission is to search for survivors amidst significant debris in a room (caused by an earthquake) without human intervention. The DisasterBot uses a series of proximity sensors to detect obstacles and survivors, enabling it to navigate through the room safely and retrieve survivors to a safe location.

### Features

- **Autonomous Navigation**: The robot detects obstacles like furniture (mattress, nightstands, bureau) and avoids collisions.
- **Survivor Detection**: Upon detecting a survivor, the robot stops and prints "Survivor Located!" before picking up and safely retrieving the survivor.
- **Sensor Feedback**: The robot uses a combination of proximity sensors to gather real-time data for its environment, updating its internal state based on feedback from these sensors.
- **Simulated Environment**: The robot's actions are simulated in a virtual environment using Python and V-REP (CoppeliaSim), with real-time sensor data driving its movements and decisions.

## Technologies Used

- **Python**: The main programming language used to implement the robot's behavior and logic.
- **V-REP (CoppeliaSim)**: A simulation environment used for robotic simulation, including sensor data collection and control.
- **Simulated Robot**: A virtual robot equipped with a nose sensor for proximity detection and movement control in a dynamic environment.

## Project Overview

### Scenario

The robot is deployed in a simulated hotel room, where an earthquake has caused significant debris. The room contains four obstacles (mattress, two nightstand tables, and a bureau). The robot's task is to search for any survivors and return them safely to the exit, navigating around the obstacles.

### Features and Capabilities

- **Obstacle Avoidance**: The robot uses its proximity sensors to detect obstacles and adjust its movement accordingly.
- **Survivor Detection**: The robot uses a custom sensor to detect survivors ("Person_To_Detect"). When a survivor is located, the robot halts, picks up the survivor, and safely exits the room.
- **Internal State Representation**: The robot keeps track of its environment and the detection status using internal variables, ensuring it can navigate and perform its mission autonomously.

### Sensors Used

- **Nose Sensor**: Detects obstacles (furniture, walls, etc.) and triggers the robot to adjust its movement.
- **Person Detection Sensor**: A custom sensor that identifies a survivor in the environment and triggers the robot to stop and rescue the person.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/disaster-relief-robot.git
```

2. Install Python 3.x if it's not already installed.

3. Install the required Python packages:

```bash
pip install -r requirements.txt
```

4. Download and install V-REP (CoppeliaSim) for simulation. The robot is designed to run in this environment, and you'll need it to run the project.

5. Run the project using the V-REP simulation environment. Follow the instructions in the **V-REP (CoppeliaSim)** documentation to load and run the robot script.

## How It Works

1. **Robot Initialization**: The robot starts with its sensors initialized to detect obstacles and survivors.
2. **Proximity Sensing**: The robot continuously scans the environment using its proximity sensors, adjusting its movement based on sensor data.
3. **Survivor Detection**: When the robot detects a survivor, it halts, prints a message ("Survivor Located!"), and carefully picks up the survivor.
4. **Exit**: After detecting the survivor, the robot exits the room safely, avoiding obstacles along the way.

## Video Demonstration

Watch a demonstration of the DisasterBot in action! The video shows the robot navigating the room, detecting obstacles, and rescuing a survivor.

>
> [Download DisasterBot Demo Video](https://github.com/johnmcginnes168/Disaster-Relief_Robot/raw/main/videos/example.mp4)

## Python Code

The following Python code implements the robot’s behavior using V-REP’s simulation API. The robot uses proximity sensors for obstacle detection and survivor identification.

```python
import math

def sysCall_init():
    sim = require('sim')
    simUI = require('simUI')
    self.num_To_Detect = 0
    self.noseSensor_To_Detect = sim.getObject("/bubbleRob/sensingNose_To_Detect")  
    self.bubbleRobBase = sim.getObject('.')  
    self.leftMotor = sim.getObject("/bubbleRob/leftMotor")  
    self.rightMotor = sim.getObject("/bubbleRob/rightMotor")  
    self.noseSensor = sim.getObject("/bubbleRob/sensingNose")  
    self.minMaxSpeed = [50 * math.pi / 180, 300 * math.pi / 180]  
    self.backUntilTime = -1  
    self.robotCollection = sim.createCollection(0)
    sim.addItemToCollection(self.robotCollection, sim.handle_tree, self.bubbleRobBase, 0)
    self.distanceSegment = sim.addDrawingObject(sim.drawing_lines, 4, 0, -1, 1, [0, 1, 0])
    self.robotTrace = sim.addDrawingObject(sim.drawing_linestrip + sim.drawing_cyclic, 2, 0, -1, 200, [1, 1, 0], None, None, [1, 1, 0])
    self.graph = sim.getObject('/bubbleRob/graph')
    self.distStream = sim.addGraphStream(self.graph, 'bubbleRob clearance', 'm', 0, [1, 0, 0])
    
    # Create the custom UI
    xml = '<ui title="' + sim.getObjectAlias(self.bubbleRobBase, 1) + ' speed" closeable="false" resizeable="false" activate="false">'
    xml = xml + '<hslider minimum="0" maximum="100" on-change="speedChange_callback" id="1"/>'  
    xml = xml + '<label text="" style="* {margin-left: 300px;}"/></ui>'
    self.ui = simUI.create(xml)
    self.speed = (self.minMaxSpeed[0] + self.minMaxSpeed[1]) * 0.5
    simUI.setSliderValue(self.ui, 1, 100 * (self.speed - self.minMaxSpeed[0]) / (self.minMaxSpeed[1] - self.minMaxSpeed[0]))
    
    # Flag to track if the survivor has been detected
    self.survivorDetected = False  
    self.personToDetect = None  
```

## Future Improvements

- **Reinforced Learning**: Implementing machine learning algorithms to help the robot learn and adapt to new environments based on trial and error.
- **Advanced Path Planning**: Using algorithms like A* or Dijkstra’s to optimize the robot's pathfinding.
- **Two-Way Communication**: Equipping the robot with communication capabilities for contact with emergency responders.

