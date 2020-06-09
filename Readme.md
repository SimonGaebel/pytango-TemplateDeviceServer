# Template for a Tango Device Server
This is a template for a (PyTango) Tango Device Server (TDS) that helps you register and write your own TangoDS. Just clone the contents and alter them as you like. This is of course no sufficient replacement of the full Pytango (https://pytango.readthedocs.io/en/stable/) or Tango (https://tango-controls.readthedocs.io/en/latest/) Documentation.

## Registering a Tango DS
To test the server while you are editing it, it is useful to register the server before you are actually done coding. This can be done through Jive or even more easily through a python prompt:

<pre>
<code>>>> import tango
>>> my_device = tango.DbDevInfo()
>>> my_device.server = "MyTangoDS/sys"
>>> my_device._class = "MyTangoDS"
>>> my_device.name = "sys/tango_device_template/1"

>>> db = tango.Database()
>>> db.add_device(my_device)</code>
</pre>

Now your <em>server</em> "MyTangoDS" will be registered under the <em>domain</em> "sys", the <em>family</em> "tango_device_template" and the <em>member</em> "1". The server is conventionally named after the Tango Class inside the server.

## Starting the TDS
To use the server you must start it inside a terminal. This is easily done by executing the TDS through python with the following parameters: <em>domain</em> "sys" and (optionally) your <em>debugging level</em> (v4: debug, v1:error).

<pre>
<code>$python3 ~/TangoDeviceServer.py sys -v4</code>
</pre>

You can edit your TDS without a problem while it is running. Changes must be saved and the TDS must be restarted for the changes to be applied in the server.

## Testing the TDS
Test your server, again, either through Jive or a python prompt. The latter is done as follows:

<pre>
<code>>>> from tango import DeviceProxy
>>> my_device = DeviceProxy("sys/tango_device_template/1")
>>> my_device.state()
>>> my_device.temperature
>>> my_device.temperature = 10
>>> my_device.Turn_Off()
</pre>

In the code example above, a device is being instatiated with the TangoDS. Afterwards the current state is requested, the temperature is requested and set and the device state set to off.
