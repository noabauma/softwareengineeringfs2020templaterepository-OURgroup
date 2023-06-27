# This is the code of the Actuator device which receives the desired state from HealthMonitor
import sys
import json
import socketserver
import threading

possibleInputTypes = {"float", "int", "text"}
# text is std::string in C++ and a string in python

class ActuatorDevice:
    def __init__(self, deviceId, deviceDescription, inputType, range=[], initialState=0):
        """ This is an actuator device. The state of this device is 
            determined by the output of HealthMonitor. In order to send a new value
            the HealthMonitor's output should contain a dictionary (JSON object) like this:
            {"deviceId": number, "state": number}
            deviceId provides the deviceId argument.
            state provides a number which sets the actuator state. This number should 
            be inside the range (low, high) limits. If not an error message is sent back to
            HealthMonitor.
            Before receiving any output the state is set to intialState.
               
        Arguments:
            deviceId {int} -- It is the unique id of the sensor as device.
                              It has to be different than any other device.
            deviceDescription {string} -- A string like "nurseAlarm" which describes the device functionality.
            inputType {string} -- inputType can be any out of possibleInputTypes.
            range {array} -- A 2 number array [low,high] defining the range of the sensors output.

        Keyword Arguments:
            initialState {number} -- The implied actuator's state before there is any input from HealthMonitor.
        """
        self.deviceId= deviceId
        self.deviceDescription = deviceDescription
        self.inputType = inputType
        if(not (inputType in possibleInputTypes)):
            raise("inputType {} is not any out of {}".format(inputType, str(possibleInputTypes)))
        self.range = range
        self.received = ""
        self.state = initialState

    def receive(self, dictInput):
        """ This simulates the receiving of an input. If the state is not in the range
            defined in the configuration then an error is produced.
        
        Arguments:
            dictInput {dictionary} -- Dicitionary of the type:
                                      {"deviceId": number, "state": number}
        
        Returns:
            dictionary -- Dictionary from getRawStatus() 
                          with an "error" boolean argument added and if that is true, 
                          a "desiredState" argument is also added.
        """
        self.received = dictInput
        state = dictInput["state"]
        if(self.inputType == "text" or (self.range[0] <= self.state and self.state <= self.range[1])):
            self.state = state 
            d = self.getRawStatus()
            d["error"] = False
        else:
            d = self.getRawStatus()
            d["error"] = True
            d["desiredState"] = state
        return d
    
    def getStatus(self):
        """
        Returns:
            string -- "actuatorDevice:[" dictionary returned by getRawStatus() "]"
        """
        return "actuatorDevice:[{}]".format(str(self.getRawStatus()))

    def getRawStatus(self):
        """
        Returns:
            dictionary -- A dictionary containing the device id, 
                          the device description and the last desired state received.
        """
        return {"deviceId": self.deviceId, 
                "deviceDescription": self.deviceDescription, 
                "data": self.state}

class AllActuatorSimulator(socketserver.StreamRequestHandler):
    """ Class that handles all simulated actuators communication with HealthMonitor. """
    statusFile = "" # static file path of status file 
    historyFile = "" # static file path of history file
    actuatorsList = [] # static list of actuators
    def addActuator(self, newActuatorDevice):
        """This adds an actuator to the static list of actuators actuatorList.
        
        Arguments:
            newActuatorDevice {ActuatorDevice} -- actuator device to add.
        """
        if(AllActuatorSimulator.actuatorsList == None):
            AllActuatorSimulator.actuatorsList = [newActuatorDevice]
        else:
            AllActuatorSimulator.actuatorsList.append(newActuatorDevice)
    def setStatusFile(self, statusFile):
        """ Sets status file path for this simulator instance """
        self.statusFile = statusFile

    def setHistoryFile(self, historyFile):
        """ Sets history file path for this simulator instance """
        self.historyFile = historyFile
    
    @staticmethod
    def initStatusFile():
        """ initializes the actuators records inside the status file"""
        with open(AllActuatorSimulator.statusFile, "r+") as f:
            if(f.readlines(10) == []): # if file does not have content
               oldStatus = {"Actuators":[], "Sensors":[]}
            else:
               f.seek(0)
               oldStatus = json.load(f)
            f.seek(0)
            f.truncate(0)
            f.seek(0)
            for actuator in AllActuatorSimulator.actuatorsList:
                oldStatus["Actuators"].append(actuator.getRawStatus())
            json.dump(oldStatus, f)
    
    def updateStatusFile(self, idx, append=False):
        """ This updates the status file (which is a JSON file), 
            by updating the JSON structure and altering only the value of this device.
        
        Arguments:
            idx {int} -- index of actuator in the actuatorsList which has changed. 
            append {boolean} -- If true then the data are appended.
        """
        with open(self.statusFile, "r+") as f:
            if(f.readlines(10) == []): # if file does not have content
                oldStatus = {"Actuators":[], "Sensors":[]}
                for actuator in AllActuatorSimulator.actuatorsList:
                    oldStatus["Actuators"].append(actuator.getRawStatus())
            else: # update just idx
                f.seek(0)
                oldStatus = json.load(f)
                if(append):
                    oldStatus["Actuators"].append(AllActuatorSimulator.actuatorsList[idx].getRawStatus())
                else:
                    oldStatus["Actuators"][idx] = AllActuatorSimulator.actuatorsList[idx].getRawStatus()
            f.seek(0)
            f.truncate(0)
            f.seek(0)
            json.dump(oldStatus, f)

    def updateHistoryFile(self, textReceived):
        """ This updates history file, reporting the device's new measurement. 
            It appends the information at the end of the file.
        
        Arguments:
            textReceived {string} -- Text to append to the history file.
        """
        with open(self.historyFile, "a") as f:
            f.writelines("Received:" + textReceived)

    def handle(self):
        """ This reads the data comming from HealthMonitor via socket and updates the
            specified actuator determined by deviceId. 
            If an error occurs because the state is not inside range an error is 
            returned to HealthMonitor containing an error flag and the desiredState 
            sent by the HealthMonitor.
            and the device does not change its status.
            The status and history file are also updated.
            In case no deviceId is specified, a simulator error occurs.
        """
        self.data = self.rfile.readline().strip()
        s = str(self.data, encoding='utf-8')
        print(s)
        deviceData = json.loads(s)
        if not("deviceId" in deviceData):
            raise("No deviceId in incoming data: {}".format(self.data))
        acIndex = [i for i in range(len(AllActuatorSimulator.actuatorsList)) 
                   if AllActuatorSimulator.actuatorsList[i].deviceId == deviceData["deviceId"]]
        idx = acIndex[0]
        errorStatus = AllActuatorSimulator.actuatorsList[idx].receive(deviceData)
        # update history and status file 
        self.updateHistoryFile(s)
        self.updateStatusFile(idx)
        if(errorStatus["error"] == True):
            self.wfile.writelines(str(errorStatus))


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """ This is just a wrapper for calling socketServer.ThreadMixin """
    pass


def getActuatorsServer(actuatorsList, host, port, statusFilePath, historyFilePath):
    """ This creates the server and its corresponding thread for simulating the actuator devices.
    
    Arguments:
        actuatorsList {list} -- list of ActuatorDevice holding the actuators
        host {string} -- It is the host of this simulator application. Typically localhost.
        port {int} -- It is the port this simulator application listens to.
        statusFilePath {string} -- file path of status file, where the status of all the devices 
                                   (both sensors and actuators) is reported.
        historyFilePath {string} -- file path of history file, where the changes of all the devices
                                    (throughout thes simulator execution) are saved.
    
    Returns:
        socketserver.ThreadedTCPServer -- The actuators server.
        threading.Thread -- Thread which handles actuators simulation.
    """
    AllActuatorSimulator.statusFile = statusFilePath
    AllActuatorSimulator.historyFile = historyFilePath
    AllActuatorSimulator.actuatorsList = actuatorsList
    AllActuatorSimulator.initStatusFile()
    actuatorsServer = ThreadedTCPServer((host,port), AllActuatorSimulator)
    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    actuatorsServerThread = threading.Thread(target=actuatorsServer.serve_forever)
    # Exit the server thread when the main thread terminates
    actuatorsServerThread.daemon = True

    return actuatorsServer, actuatorsServerThread

def createActuators(settings):
    """ This creates a list of actuators given their configuration settings.
    
    Arguments:
        settings {list} -- list (JSON array) where each entry is a dictionary containing 
                           the arguments: "deviceId", "deviceDescription", "inputType", "range", 
                           "initialState". For description of each of these see ActuatorDevice.
    
    Returns:
        list -- list of ActuatorDevice objects.
    """
    actuators = []
    for entry in settings:
        actuators.append(
            ActuatorDevice(entry["deviceId"], entry["deviceDescription"], 
                           entry["inputType"], entry["range"]
        ))
    return actuators

def createActuatorsServer(actuatorSettings, simulatorHost, simulatorPort, statusFilePath, historyFilePath):
    """ This creates the actuators, the actuatorsServer 
        and the thread which runs the actuators simulation.
    
    Arguments:
        actuatorSettings {array} -- (JSON array) list of actuator configurations, for more info see ActuatorDevice.
        simulatorHost {string} -- It is the host of this simulator application. Typically localhost.
        simulatorPort {int} -- It is the port this simulator application listens to. 
                               It should be the same as the output port of the HealthMonitor.
        statusFilePath {string} -- The status file path.
        historyFilePath {string} -- The history file path.

    Returns:
        socketserver.ThreadedTCPServer -- The actuators server.
        threading.Thread -- Thread which handles actuators simulation.
    """
    actuators = createActuators(actuatorSettings)
    return getActuatorsServer(actuators,
                              simulatorHost,
                              simulatorPort,
                              statusFilePath,
                              historyFilePath)