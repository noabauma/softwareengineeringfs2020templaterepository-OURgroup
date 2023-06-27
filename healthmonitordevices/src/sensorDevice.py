# This is the code of the sensor device which reads data of the patient and sends data to the HealthMonitor
import random
import numpy as np
import sys
import json
from repeatedTimer import RepeatedTimer
import socket
import threading
from time import sleep
random.seed(100)

possibleOutputTypes = ["float", "int", "image"] # possible output types that sensor can produce


class sensorDevice:
    allDevicesSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connected = False
    def __init__(self, hostToSendData, portToSendData, id, deviceDescription,
                 outputType, range, statusFile, historyFile, timeInterval=10000, scenario=None):
        """ This class defines a sensor device. A sensor device sends artificial measurements to HealthMonitor
            via TCP. It can sent both random or guided (via a scenario) measurements.
        
        Arguments:
            hostToSendData {string} -- It is the host of HealthMonitor application. 
                                       This is the host the sensor's data will be sent 
            portToSendData {int} -- It is the port which the HealthMonitor application listens to.
            id {integer} -- It is the unique id of the sensor as device. 
                            It has to be different than any other device.
            deviceDescription {string} -- A string like "Thermometer" which describes the device functionality.
            outputType {string} -- OutputType can be any out of  possibleOutputTypes
            range {list} -- A 2 number array defining the range of the sensors output.
                             In case outputType == "image" then the two numbers define 
                             width and height respectively.
            statusFile {string} -- file path of status file, where the status of all the devices 
                                   (both sensors and actuators) is reported.
            historyFile {string} -- file path of history file, where the changes of all the devices
                                    (throughout thes simulator execution) are saved.
        Keyword Arguments:
            timeInterval {int} -- if no scenario is defined then this is the time 
                                  interval between two measurements. (default: {10000})
            scenario {list of dictionaries} -- If this is defined then this is the scenario of measurements and the measurements 
                                               that will be sent to HealthMonitor are the ones described inside this list. 
                                               Each list entry has 2 values {"time": number, "value": number}. 
                                               The first ardument is the time to wait after the previous entry was sent the measurement 
                                               to HealthMonitor in order to send a the one contained by the "value" argument.
                                               The second argument is the value to send, if this is not defined then a random value
                                               according to the outputType will be sent. (default: {None})
        
        Returns:
            sensorDevice -- A sensor device configured to send data to hostToSendData:portToSendData 
                            either by following a scenario or randomly in specified time intervals.
        """
        self.id = id
        self.deviceDescription = deviceDescription
        self.statusFilePath = statusFile
        self.historyFilePath = historyFile
        self.outputType = outputType
        self.range = range
        self.scenario = scenario
        self.scenarioIdx = 0
        if( (not (outputType in possibleOutputTypes)) and scenario == None):
            raise("Output type:{} is not any out of {}".format(outputType, str(possibleOutputTypes)))

        self.timeInterval = timeInterval
        self.lastData = None
        self.hostToSendData = hostToSendData
        self.portToSendData = portToSendData
        
        while(not(sensorDevice.connected)): # keep trying until there is a connection
            sleep(1)
            print("trying to connect to socket")
            if(sensorDevice.allDevicesSocket.connect_ex(
                (socket.gethostbyname(self.hostToSendData), self.portToSendData)) == 0):
                sensorDevice.connected = True
        
        if(scenario != None):
            self.rt = RepeatedTimer(scenario[0]["time"], self.sendData)
        else:
            self.rt = RepeatedTimer(self.timeInterval, self.sendData)

    def produceRandomData(self):
        """
        Returns:
            various -- returns random data with type according to the type provided
                       if type == float: returns a random float number
                       if type == int : returns an integer number
                       if type == image : returns a 3D array (H,W,3) with random pixel values
        """        
        if(self.outputType == 'float'):
            return self.randFuncFloat(self.range) # range small, big
        elif(self.outputType == 'int'):
            return self.randFuncInt(self.range) # range small, big
        elif(self.outputType == 'image'):
            return self.randFuncImage(self.range) # range = W X H of image
        else:
            raise("Not such input type:{}".format(outputType))

    def produceData(self):
        """
        Returns:
            various -- deterministic data in case there is scenario random data if there is not.
        """
        if(self.scenario != None):
            return self.getOutputFromScenario()
        else:
            return self.produceRandomData()

    def sendData(self):
        """This sends data to HealthMonitor. 
           The data sent are the same as the output of getStatus().
           Encoding is utf-8
        """
        # random data generation

        self.lastData = self.produceData()
        # return data as JSON string
        d = self.getRawStatus()
        s = str(d)
        # send data to HealthMonitor
        sensorDevice.allDevicesSocket.send(bytes(s, encoding='utf-8'))
        # edit history
        self.updateHistoryFile(s)
        # edit status
        self.updateStatusFile(d)

    def updateHistoryFile(self, textSent):
        """ This updates history file, reporting the device's new measurement. 
            It appends the information at the end of the file.
                    
        Arguments:
            textSent {string} -- Text to append to the history file.        
        """
        with open(self.historyFilePath, "a") as f:
            f.writelines(textSent)

    def updateStatusFile(self, dat):
        """ This updates the status file (which is a JSON file), 
            by updating the JSON structure and altering only the value of this device.
        
        Arguments:
            dat {dictionary} -- dat contains the values produced by getRawStatus().
        """
        oldStatus = {}
        with open(self.statusFilePath, "r+") as f:
            if(f.readlines(10) == []): # if file does not have content
               oldStatus = {"Actuators":[], "Sensors":[]}
            else:
                f.seek(0)
                oldStatus = json.load(f)
            f.seek(0)
            f.truncate(0)
            f.seek(0)
            r = range(len(oldStatus["Sensors"]))
            sensors = oldStatus["Sensors"]
            I = [i for i in r if sensors[i]["deviceId"] == self.id]
            if(I == []):
                oldStatus["Sensors"].append(dat)
            else:
                idx = I[0]
                oldStatus["Sensors"][idx] = dat
            json.dump(oldStatus, f)

    def getStatus(self):
        """
        Returns:
            string -- "sensorDeviceEvent:[ dictionary returned by getRawStatus() ]"
        """
        return "sensorDeviceEvent:[{}]".format(str(self.getRawStatus()))

    def getRawStatus(self):
        """
        Returns:
            dictionary -- A dictionary containing the id , the device description and the last measurement.
        """
        return {"deviceId": self.id,
                "deviceDescription": self.deviceDescription,
                "data": self.lastData}

    def getOutputFromScenario(self):
        """ This follows the scenario and produces measurements by this scenario. 
            The state of the scenario is determined by self.scenarioIdx which shows 
            which value has to be sent next. If the argument "value" is missing from an
            entry then the value sent is a random number according to the outputType defined.
        
        Returns:
            various -- The value produced by the last scenario entry.
        """
        if("value" in self.scenario[self.scenarioIdx]):
            val = self.scenario[self.scenarioIdx]["value"]
        else:
            val = self.produceRandomData()
        if(self.scenarioIdx != len(self.scenario)-1):
            self.scenarioIdx += 1
            self.rt.stop()
            self.rt.interval = self.scenario[self.scenarioIdx]["time"]
            self.rt.start()
        return val

    def randFuncInt(self, range):
        """
        Arguments:
            range {list} -- list/array or tuple of 2 integers [low,high].
        
        Returns:
            int -- random integer in the interval [low, high].
        """
        return random.randint(range[0], range[1])

    def randFuncFloat(self, range):
        """
        Arguments:
            range {list} -- list/array or tuple of 2 floats [low,high].
        
        Returns:
            float -- random float number in the interval [low, high].
        """
        return random.random() * (range[1] - range[0]) + range[0]

    def randFuncImage(self, range):
        """
        Arguments:
            range {list} -- list/array or tuple of 2 integers [Image Width, Image Height]
        
        Returns:
            list -- random image array with size [Image Height, Image Width, 3] 
                    and integer values in the interval [0,255].
        """
        return np.random.randint(0, 255, size=(range[1],range[0],3)).tolist()



def createSensorDevices(sensorSettings, hostToSendData, portToSendData, statusFilePath, historyFilePath):
    """ This creates the sensor devices used by this simulation given the configuration settings as a JSON object.

    Arguments:
        sensorSettings {JSON obj} -- configuration settings for creating the simulation's sensor devices.
        hostToSendData {string} -- It is the host of HealthMonitor application.
                                    This is the host the sensor's data will be sent
        portToSendData {int} -- It is the port which the HealthMonitor application listens to.
        statusFilePath {string} -- file path of status file, where the status of all the devices 
                                   (both sensors and actuators) is reported.
        historyFilePath {string} -- file path of history file, where the changes of all the devices
                                    (throughout thes simulator execution) are saved.
    
    Returns:
        list -- list of sensor devices.
    """
    sensorDevices = []
    for entry in sensorSettings:
        cD = None
        if("scenario" in entry):
            cD = sensorDevice(
                hostToSendData, portToSendData,
                entry["deviceId"], entry["deviceDescription"], 
                entry["outputType"], entry["range"],
                statusFilePath, historyFilePath, entry["timeInterval"],
                entry["scenario"])
        else:
            cD = sensorDevice(
                hostToSendData, portToSendData,
                entry["deviceId"], entry["deviceDescription"], 
                entry["outputType"], entry["range"],
                statusFilePath, historyFilePath, entry["timeInterval"])
 
        sensorDevices.append(cD)

    return sensorDevices

def closeSensorSocket():
    sensorDevice.allDevicesSocket.close()