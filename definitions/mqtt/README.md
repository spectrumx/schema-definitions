
# MEP Internal Communication Schema
This defines how the local services on the MEP's Jetson will interact with each other.  
Services should adhere to the following requirements:
- Establish a `service_name` which should be snake_case (lower-case with underscores).
- Built as a Docker container, using a slim base container and minimizing container size wherever possible.
- Connect to local MQTT broker and create a top-level topic matching the service name.
    - MQTT broker: localhost
    - Port: 1883
- Subscribe to `[service_name]/command` for incoming commands. 
- Publish status updates (JSON) to `[service_name]/status`, with a `state` key matching either `online`/`offline` and an epoch timestamp with the last update.  Additional key/values as needed. 
    - Example:
    - {"state": "online" / "disabled" / "offline", "timestamp": 123456789, "additional": "info" }
    - Use Last Will and Testament to mark the state `offline` when exiting.
    - The `disabled` state is to show the algorithm is still online and able to receive commands, but is disabled.  
- Send an announcement (JSON) to `announce/[service_name]` with human-readable information about this service.  See [Announcement format](/#announcement) below.

<a id="announcement"></a>
### Announcement format
```
{
  // required fields
  "title": "Human readable name",
  "description": "Human readable description of the algorithm",
  "author": "Name <email>",
  "source": "URL from where this came from (Docker, Github)",
  "output":  
      // Where output is being sent, either MQTT topic or location on disk.  
      // Use `null` if no output is expected.  
      // Multiple outputs can be specificed via JSON with name/location
      // Examples:
      // null                                       - no output
      // "/data/new_ringbuffer"                     - location on disk
      // "fft/output"                               - MQTT topic
      // {"1024": "fft/1024", "8192": "fft/8192"}   - multiple MQTT outputs

  // optional fields
  "version": "0.1",
  "type": ['algorithm','hardware','service'],       - choose one
  "time_started": "epoch timestamp",
}
```


## Current High-level Services & Hardware
- `icarus/` - Icarus - connect to sensing platform via MQTT, receive commands and distribute locally, coordinate Jetson activities
- `docker/` - Manage docker containers, pull updates, etc
- `rfsoc/` - RFSoC control channel - change freq, gain, etc
- `afe/` - AFE control channel
- `fft/` - Algorithm for automatically creating spectrogram data
- `filter/` - Algorithm for filtering data



### Icarus
```
{ # Ring buffer control
  "task_name": "tasks.rf.digitalrf.ringbuffer_start",
  "arguments": { // to be determined }
}
```
or
```
{ # Upload data to SDS
  "task_name": "tasks.archive.sds_upload",
  "arguments": { // to be determined }
}
```


### Algorithms
Processing algorithms will read incoming data from `/data/ringbuffer`, perform whatever is necessary and send their output to match the `announce` packet above: possibly to an MQTT topic, a file on disk, or a new ring buffer.  

Code snippet:
```
import paho.mqtt.client as mqtt
import time
import json

service_name = "fft"
disabled = False

# MQTT Functions
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        send_status(client)

def on_message(self, client, userdata, msg):
  global disabled
  payload = json.loads(msg.payload)
  if payload['task_name'] == "disable":
    disabled = True
  if payload['task_name'] == "status":
    send_status()

def send_status(client):
  global service_name
  client.publish(service_name + "/status", {"state": "online", "timestamp": time.time()})


client = mqtt.Client(service_name)
client.on_message = on_message
client.on_connect = on_connect
client.connect("localhost", 1883)
client.will_set(service_name + "/status", payload={"state":"offline"}, qos=1, retain=True)
client.loop_start()


while True:
  if !disabled:
    #Do processing

    # Send data to SDS archive
    #client.publish("icarus/command", {"task_name": "tasks.archive.sds_upload", "arguments": {"source":"/data/path", "destination":"SDS_name"} })


```


