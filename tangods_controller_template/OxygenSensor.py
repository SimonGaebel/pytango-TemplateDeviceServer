#!/usr/bin/env python3

import serial
import time
from tango import AttrWriteType, DispLevel, DevState
from tango.server import Device, attribute, device_property

class OxygenSensor(Device):
    # Device Properties
    Port = device_property(dtype="str", default_value="/dev/ttyUSB0")
    BaudRate = device_property(dtype="int", default_value=115200)

    # Attributes
    o2_concentration = attribute(
        label="O2 Concentration",
        dtype="float",
        format="%6.2f",
        display_level=DispLevel.OPERATOR,
        access=AttrWriteType.READ,
        doc="Measured oxygen concentration in %",
    )

    def init_device(self):
        """Initialize the device and establish a serial connection."""
        Device.init_device(self)
        self.set_state(DevState.INIT)
        self._last_o2_value = 0.0
        self._last_update = time.time()
        self._retry_attempts = 3  # Number of retry attempts
        self.connect_to_sensor()

    def connect_to_sensor(self):
        """Try to establish a serial connection with retries."""
        for attempt in range(self._retry_attempts):
            try:
                self.serial_conn = serial.Serial(
                    port=self.Port, baudrate=self.BaudRate, timeout=1
                )
                if self.serial_conn.is_open:
                    self.set_state(DevState.ON)
                    self.info_stream(f"Connected to sensor on {self.Port}")
                    return
            except serial.SerialException as e:
                self.warn_stream(f"Connection attempt {attempt + 1} failed: {e}")
                time.sleep(2)  # Wait before retrying
        self.set_state(DevState.FAULT)
        self.error_stream("Failed to connect to the sensor after retries")

    def always_executed_hook(self):
        """Check the serial connection status before each operation."""
        if not self.serial_conn.is_open:
            self.set_state(DevState.FAULT)
            self.error_stream("Serial connection lost")
            self.connect_to_sensor()

    def read_o2_concentration(self):
        """Read the oxygen concentration from the sensor."""
        if self.get_state() != DevState.ON:
            self.error_stream("Device not ready")
            return self._last_o2_value

        try:
            self.serial_conn.write(b"O2_data\n")
            self.serial_conn.flush()
            response = self.serial_conn.readline().decode().strip()

            if response:
                self._last_o2_value = float(response)
                self._last_update = time.time()
                self.debug_stream(f"Received O2 value: {self._last_o2_value:.2f}%")
            else:
                self.warn_stream("No data received from sensor")

        except serial.SerialTimeoutException:
            self.error_stream("Serial timeout error")
            self.set_state(DevState.FAULT)
        except ValueError:
            self.error_stream("Received invalid data")
        except Exception as e:
            self.error_stream(f"Error reading data: {e}")
            self.set_state(DevState.FAULT)

        return self._last_o2_value

    def delete_device(self):
        """Cleanup serial connection on device deletion."""
        if hasattr(self, "serial_conn") and self.serial_conn.is_open:
            self.serial_conn.close()
            self.info_stream("Serial connection closed")

if __name__ == "__main__":
    OxygenSensor.run_server()