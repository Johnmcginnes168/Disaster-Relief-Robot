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
    self.robotTrace = sim.addDrawingObject(sim.drawing_linestrip + sim.drawing_cyclic, 2, 0, -1, 200, [1, 1, 0], None,
                                           None, [1, 1, 0])
    self.graph = sim.getObject('/bubbleRob/graph')
    self.distStream = sim.addGraphStream(self.graph, 'bubbleRob clearance', 'm', 0, [1, 0, 0])

    # Create the custom UI
    xml = '<ui title="' + sim.getObjectAlias(self.bubbleRobBase,
                                             1) + ' speed" closeable="false" resizeable="false" activate="false">'
    xml = xml + '<hslider minimum="0" maximum="100" on-change="speedChange_callback" id="1"/>'
    xml = xml + '<label text="" style="* {margin-left: 300px;}"/></ui>'
    self.ui = simUI.create(xml)
    self.speed = (self.minMaxSpeed[0] + self.minMaxSpeed[1]) * 0.5
    simUI.setSliderValue(self.ui, 1,
                         100 * (self.speed - self.minMaxSpeed[0]) / (self.minMaxSpeed[1] - self.minMaxSpeed[0]))

    # Flag to track if the survivor has been detected
    self.survivorDetected = False
    self.personToDetect = None


def sysCall_actuation():
    result, *_ = sim.readProximitySensor(self.noseSensor)
    if result > 0:
        self.backUntilTime = sim.getSimulationTime() + 4
    if self.backUntilTime < sim.getSimulationTime():

        sim.setJointTargetVelocity(self.leftMotor, self.speed)
        sim.setJointTargetVelocity(self.rightMotor, self.speed)
    else:
        sim.setJointTargetVelocity(self.leftMotor, -self.speed / 2)
        sim.setJointTargetVelocity(self.rightMotor, -self.speed / 8)

    result_To_Detect, distance, detectedPoint, detectedObjectHandle, _ = sim.readProximitySensor(
        self.noseSensor_To_Detect)
    if result_To_Detect > 0:
        if detectedObjectHandle:
            if sim.getObjectAlias(detectedObjectHandle) == 'Person_To_Detect':
                self.num_To_Detect = self.num_To_Detect + 1
                if not self.survivorDetected:
                    print("Survivor located!")
                    self.survivorDetected = True
                    printing
                sim.setObjectColor(self.noseSensor_To_Detect, 0, sim.colorcomponent_ambient_diffuse, [0, 1, 0])
                # Stop the robot when the person is detected
                sim.setJointTargetVelocity(self.leftMotor, 0)
                sim.setJointTargetVelocity(self.rightMotor, 0)

                self.personToDetect = detectedObjectHandle

    else:
        sim.setObjectColor(self.noseSensor_To_Detect, 0, sim.colorcomponent_ambient_diffuse, [0, 0, 1])

    if self.personToDetect:
        robot_position = sim.getObjectPosition(self.bubbleRobBase, -1)
        # Move the detected person to follow the robot
        follow_position = [robot_position[0], robot_position[1], robot_position[2] + 0.5]
        sim.setObjectPosition(self.personToDetect, -1, follow_position)


def sysCall_sensing():
    result, distData, *_ = sim.checkDistance(self.robotCollection, sim.handle_all)
    if result > 0:
        sim.addDrawingObjectItem(self.distanceSegment, None)
        sim.addDrawingObjectItem(self.distanceSegment, distData)
        sim.setGraphStreamValue(self.graph, self.distStream, distData[6])
    p = sim.getObjectPosition(self.bubbleRobBase)
    sim.addDrawingObjectItem(self.robotTrace, p)


def speedChange_callback(ui, id, newVal):
    self.speed = self.minMaxSpeed[0] + (self.minMaxSpeed[1] - self.minMaxSpeed[0]) * newVal / 100


def sysCall_cleanup():
    simUI.destroy(self.ui)
