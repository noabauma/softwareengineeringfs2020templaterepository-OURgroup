from actuatorDevice import createActuatorsServer
from sensorDevice import createSensorDevices, closeSensorSocket
import json
import sys
from time import sleep


def createDumpStatusFile(filePath, numSensors, numActuators):
    """ Creates an empty status file specified by filePath.
    
    Arguments:
        filePath {string} -- status file path.
        numSensors {int } -- >0 number of Sensors in the simulation.
        numActuators {int } -- >0 number of Actuators in the simulation.
    """    
    statusString = {"Sensors": [{"deviceId": i, "data": None} for i in range(numSensors)],
                    "Actuators": [{"deviceId": i, "state" : None} for i in range(numActuators)]}
    with open(filePath, "w") as f:
        json.dump(statusString, f)

def main(confSettingsFilePath):
    """ This reads the configuration settings JSON file and creates sensors, actuators
    with the settings provided in the configuration file. All sensors run in separate threads,
    but all actuators are handled by one thread. The main thread goes in an endless loop. 
    In case there is an error it stops and closes all communication with HealthMonitor.
    
    Arguments:
        confSettingsFilePath {string} -- path to JSON file with the configuration settings.
    """
    confSettings = {}

    with open(confSettingsFilePath, "r") as f:
        confSettings = json.load(f)

    createDumpStatusFile(confSettings["OutputFile"],
                         len(confSettings["Sensors"]),
                         len(confSettings["Actuators"]))

    sensorDevices = createSensorDevices(confSettings["Sensors"],
                                        confSettings["HealthMonitorHost"],
                                        confSettings["HealthMonitorInputPort"],
                                        confSettings["OutputFile"],
                                        confSettings["HistoryFile"])

    actuatorsServer, actuatorsServerThread  = createActuatorsServer(confSettings["Actuators"],
                                                                    confSettings["SimulatorHost"],
                                                                    confSettings["HealthMonitorOutputPort"],
                                                                    confSettings["OutputFile"], 
                                                                    confSettings["HistoryFile"])
    actuatorsServerThread.start()
    try:
        while(True):
            sleep(1)
    except:
        print("Exception occured closing Server")
        with open(confSettings["HistoryFile"], "a") as f:
            f.writelines("Exception occured closing Server")
    finally:
        actuatorsServer.shutdown()
        closeSensorSocket()
        for sensor in sensorDevices:
            sensor.rt.stop()


if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print("No json file provided")
        sys.exit(0)
    main(sys.argv[1])