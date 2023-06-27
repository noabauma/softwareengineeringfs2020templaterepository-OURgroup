# Health Monitor Device Simulator

## About

This is the script which helps for the development of Health Monitor program. It transmits JSON-like data at specified time intervals and validates receiving data from the input. The state of the program is outputed to a local file (specified in the JSON configuration) along with the history of actuator and sensor values for testing. This way you can produce scenarios of sensor values and see the actuator outputs, in order to verify that the HealthMonitor application works.


## JSON configuration form

```json
{
    "OutputFile": "Path to your output file",
    "HistoryFile": "Path to your history file",
    "HealthMonitorInputPort": "The number that HealthMonitor port listens to",
    "HealthMonitorOutputPort": "The number that HealthMonitor port writes to",
    "HealthMonitorHost": "The server which hosts HealthMonitor. 
                          If it is your pc, it is probably localhost.",
    "SimulatorHost": "The server where the simulator runs. 
                      If it is your pc, it is probably localhost.",
    "Sensors": [
                {"deviceId": "unique device id number", 
                 "deviceDescription": "A description string of the sensor device", 
                 "outputType": "float | int | image", 
                 "range": ["low","high"], 
                 "timeInterval": "number of seconds between transmissions", 
                 "scenario": [{"time": "time between transmission of 
                                        the previous state and this state",
                               "value": "The deterministic value of simulated measurement"},
                              ...
                             ]
                },
                ...
                ],
    "Actuators": [
                 {"deviceId": "unique device id number",
                  "deviceDescription": "Device functionality description",
                  "inputType": "float|int|text",
                  "range": ["low","high"]},
                ...
                ],
    "PatientData": [
                {"modelType": "model to link inputs and outputs",
                 "actuatorIds": ["actuator device deviceId numbers"],
                 "inputSensorIds": ["sensor device deviceId numbers"]},
                ...
                ]
}
```

Sensors is a list of sensor devices run by the simulator. Each entry of this list is the configuration fo a sensor. The values produced (measurements) by the sensor can be random or deterministic. If the scenario is defined then this is the scenario of measurements and the measurements that will be sent to HealthMonitor are the ones described inside this list. Each list entry has 2 values {"time": number, "value": number}. The first ardument is the time to wait after the previous entry was sent the measurement to HealthMonitor in order to send a the one contained by the "value" argument. The second argument is the value to send, if this is not defined then a random value according to the outputType and ranges will be sent. If the scenario is not defined then random measurements in the range `[range[0], range[1]]` of type output type are produced per timeInterval seconds.

Actuators is a list of actuator devices. Their output is provided to HealthMonitor via TCP port `HealthMonitorInputPort`. Each entry of the list describes a device configuration. The device will wait for input in the range `[range[0], range[1]]`. If wrong input provided then the simulator will throw an error.

An example configuration can be found [here](assets/ex.json).

*PatientData* is not used by this tool however it is an idea that can be used by your application to specify the models and the link between sensors and actuators.

## Simulator Transmission Data

The simulation transmits data from each of its sensors in the form:

```
{"deviceId": number, 
 "deviceDescription": The sensor device's description string, 
 "data": the measurement of the sensor}
```

The simulator sensor which sends the data is specified by the "deviceId".

For example for the Sensors defined in the example configuration, a data record transmitted is:

```JSON
{'deviceId': 1, 'deviceDescription': 'Thermometer', 'data': 24.750514222540644}
```

This is transmited in byte string with utf-8 encoding.

## Simulator Receiving Data

The simulator receives data to each of its actuators in the form:

```
{"deviceId": number, 
 "state": number}
```

For example for the actuator defined in the example configuration, a data record received is:

```
{"deviceId":2, "state":0.5}'
```

## Usage

First, a test is needed to verify that this tool is working in your device. 
Open a terminal and type:

```bash
nc -l 8005 # listens to localhost's port 8005
```

Now open a terminal and go to the root folder of this project, next type:

```bash
python3 src/main.py assets/ex.json # launches the simulator
```


Open one more terminal to send data to the simulator, next type:

```bash
echo '{"deviceId":3, "state":0.7}' | netcat localhost 8002 # sends data to localhost port 8002
```

**In order to use it for your project**:

Open a terminal and launch your application:

```bash
./YourHealthMonitorApp pathToYourConfigurationJSONFile
```

When need to close it later, just type `ctrl+C`.


Open another terminal and invoke the simulator:

```bash
python3 src/main.py pathToYourConfigurationJSONFile # launches the simulator with your configuration
```

Open another terminal and view the status file while it changes:

```bash
tail -f state.out
```

Open another terminal and view the history file while it changes:

```bash
tail -f history.out
```

*Hint: The output of this application is the input to HealthMonitor backend and the input of this application is the output of HealthMonitor backend*

## Depedencies Installation

For Linux (installs pip):
```bash
cat .depedencies | xargs apt-get install
pip install -r .pipPackageInstal.txt
```

## Common errors

Common errors that might happen in the execution of the simulator:

`ConnectionRefusedError: [Errno 111] Connection refused :` No application listens to the port defined by "HealthMonitorInputPort".
