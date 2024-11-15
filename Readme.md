# OxygenSensor Tango Device Server

This Tango Device Server (`OxygenSensor`) is designed to interface with an oxygen sensor  [Gravity: Electrochemical Oxygen / O2 Sensor (0-25%Vol, I2C)](https://www.dfrobot.com/product-2052.html), which communicates via an ESP32 microcontroller over a serial (UART) connection. The ESP32 acts as a bridge between the sensor and the Tango Device Server, enabling the acquisition of oxygen concentration data. 

## Features
- **Real-time oxygen concentration monitoring**: Provides live updates on oxygen levels measured in percentage (%).
- **Automatic reconnection**: Attempts to reconnect to the ESP32 if the serial connection is lost.
- **Configurable serial communication**: Supports different serial ports and baud rates, adjustable via Tango device properties.

## Installation

### Prerequisites
Ensure that you have the following installed on your system:
- **Python 3**
- **PySerial**: For serial communication with the ESP32


## Configuration

### Device Properties
When registering the `OxygenSensor` Tango Device Server, configure the following device properties:

| Property   | Data Type | Default Value   | Description                                             |
|------------|-----------|-----------------|---------------------------------------------------------|
| Port       | String    | `/dev/ttyUSB0`  | Serial port to which the ESP32 is connected.            |
| BaudRate   | Integer   | 115200          | Baud rate for the serial communication with ESP32.      |

### Example Configuration via Jive
1. Open **Jive** (Tango's configuration tool).
2. Create a new device for the `OxygenSensor` class.
3. Set the **Device Properties**:
- `Port`: Set to the appropriate serial port (e.g., `/dev/ttyUSB0` or `/dev/ttyS0` on Linux).
- `BaudRate`: Set according to your ESP32’s configuration (default is 115200).

### Running the Server
To start the Tango Device Server, use the following command:
```
python OxygenSensor.py <instance name>
```

## Structure
oxygen_sensor/
├── __init__.py
├── __main__.py
└── oxygen_sensor.py


## Usage

### Available Attributes
The `OxygenSensor` Tango Device Server provides the following attributes:

- **O2 Concentration (`o2_concentration`)**:
  - Type: `float`
  - Access: Read-only
  - Description: Measured oxygen concentration in percentage (%).
  - Example: `20.90` (represents 20.9% oxygen level)


## Author
Simon Gaebel 

## Additional Resources

- Tango Controls Documentation: [https://tango-controls.readthedocs.io/](https://tango-controls.readthedocs.io/)
- DFROBOT Oxygen Sensor Documentation: [DFROBOT Sensor Manual](https://wiki.dfrobot.com/Gravity_I2C_Oxygen_Sensor_SKU_SEN0322)