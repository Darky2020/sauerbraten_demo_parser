# sauerbraten_demo_parser

<b>Note:</b> this project will not be maintained as it has numerous flaws. A better and more feature complete version will come out some time in the future.<br><br>
A simple sauerbraten demo parser written in python which has the ability to parse demo files as well as raw demo file bytes both compressed using gzip and uncompressed.<br><br>
This documentations assumes that you have the library stored in a folder called "sauerbraten_demo_parser" and a python file in a directory above as such:
- ``main.py``
- ``/sauerbraten_demo_parser``

Basic setup:
```python
from sauerbraten_demo_parser import DemoParser, Packet
from sauerbraten_demo_parser.sauerconsts import *
```

Reading a demo file:
```python
from sauerbraten_demo_parser import DemoParser, Packet
from sauerbraten_demo_parser.sauerconsts import *

parser = DemoParser()
packets = parser.parse("demofile.dmo")
print(packets)
```

Reading a demo from a url:
```python
from sauerbraten_demo_parser import DemoParser, Packet
from sauerbraten_demo_parser.sauerconsts import *
import requests

parser = DemoParser()
raw_demo = requests.get("https://sauerdemos.com/download/1503817.dmo").content
packets = parser.parse_raw(raw_demo, compressed=True) # compressed here means that the demo is gzipped
print(packets)
```

``packets`` will display like this:
```
PacketList([
    Packet(N_WELCOME, timestamp=0, args={}),
    Packet(N_MAPCHANGE, timestamp=0, args={'map': 'haste', 'mode': 17, 'spawnitems': 1}),
    ...
    Packet(N_CLIENT, timestamp=609990, args={'cn': 7, 'length': 2, 'buff': ' n'}),
    Packet(N_CLIENTPING, timestamp=609990, args={'cn': 7, 'ping': 110})
], packets=123196)
```

You can iterate over a ``PacketList`` like you would with a regular list:
```python
packets = parser.parse("demofile.dmo")
for packet in packets:
    print(packet)
```

Each member of a ``PacketList`` is a ``Packet`` object which has these fields:
- ``type``: packet type (such as N_DIED or N_POS), it's an integer. Use the sauerconsts import to simplify working with it.
- ``timestamp``: an integer, number of milliseconds that have passed since the beginning of the game.
- ``args``: a dictionary containing the argumets in a human readable form. Is unique to each packet type.

# Packet filtering
You can filter a ``PacketList`` by type, timestamp, cn and variable.<br>
- By type:
```python
packets = parser.parse("demofile.dmo")
init_clients = (
    packets.where(Packet.type() == N_INITCLIENT)
    .select()
)
print(init_clients)
```

This code will select all the packets of type N_INITCLIENT from the packet list.

- By timestamp:

```python
packets = parser.parse("demofile.dmo")
first_packets = (
    packets.where(Packet.time() == 0)
    .select()
)
print(first_packets)
```

This code will select all the packets that were sent in the very beginning of the demo where everything is initialised.

- By cn (client number):
```python
packets = parser.parse("demofile.dmo")
specific_client_packets = (
    packets.where(Packet.cn() == 3)
    .select()
)
print(specific_client_packets)
```

This code will get all the packets that are related to a player with a client number 3. It will include the packets that were sent by that client and packets that are related to that client (such as N_DAMAGE which has both an actor and a target cns).

- By args:
```python
packets = parser.parse("demofile.dmo")
variable_packets = (
    packets.where(Packet.variable("team") == "evil")
    .select()
)
```

This code will get all the packets that have an argument "team" that is equal to "evil". It will ignore the packets that do not have that argument. Note that it does not work with nested arguments.
<br>
In the examples above we've only used the ``==`` operator but there are more. The full list is:
- ``==``
- ``<``
- ``<=``
- ``>``
- ``>=``
- ``!=``

(Actually there are two more being ``select`` and ``exclude`` but I literally forgot why I even added those 😅)

<br>

You can also combine those queries:
```python
packets = parser.parse("demofile.dmo")
shotgun_shots = (
    packet_list.where(Packet.type() == N_SHOTFX)
    .select()
    .where(Packet.variable("gunselect") == GUN_SG)
    .select()
    .where(Packet.cn() == 1)
    .select()
)
print(shotgun_shots)
```

This query will find all the shots performed with shotgun by a client with cn 1

Finally you can get the first or the last packet in a query by replacing ``.select()`` with ``.first()`` or ``.last()``. This helps the performance a little when you know that there should be only one result. If there are no packets left it will return ``None``.

# Examples

Getting the map, mode and players in a demo:
```python
from sauerbraten_demo_parser import DemoParser, Packet
from sauerbraten_demo_parser.sauerconsts import *
import requests

parser = DemoParser()

demo = requests.get("https://sauerdemos.com/download/1503817.dmo").content
packet_list = parser.parse_raw(demo)

# Note the use of first() here as we know there is only one N_MAPCHANGE packet
mm_info = packet_list.where(Packet.type() == N_MAPCHANGE).first()
mode = mode_to_str[mm_info.args["mode"]]
map = mm_info.args["map"]

# Make sure that time timestamp is 0 meaning that we only
# include the clients that were initially on the server
player_packets = (
    packet_list.where(Packet.type() == N_INITCLIENT)
    .select()
    .where(Packet.time() == 0)
    .select()
)

players = []

for player in player_packets:
    players.append(
        {
            "cn": player["cn"],
            "name": player["name"],
            "team": player["team"],
        }
    )

print(f"Map: {map}, Mode: {mode}")
print(players)
```
<br>


Getting a list of death spots of a player with cn 1:
```python
from sauerbraten_demo_parser import DemoParser, Packet
from sauerbraten_demo_parser.sauerconsts import *
import requests

parser = DemoParser()

demo = requests.get("https://sauerdemos.com/download/1503817.dmo").content

packet_list = parser.parse_raw(demo)
cn = 1

pos_packets = (
    packet_list.where(Packet.type() == N_POS)
    .select()
    .where(Packet.cn() == cn)
    .select()
)

# vcn stands for victim cn aka the client who died and not the client who fragged
died_packets = (
    packet_list.where(Packet.type() == N_DIED)
    .select()
    .where(Packet.variable("vcn") == cn)
    .select()
)

died_pos = []

for died in died_packets:
    # We get the last position packet of our client before the died packet
    death_spot = pos_packets.where(Packet.time() <= died.timestamp).last()

    died_pos.append(death_spot)

print(died_pos)
```

Note that we pre-parse N_POS packets and N_DIED packets instead of doing that inside the loop. Doing so would tank the performace so beware.

<br>

Getting all the 120 rocket hits:
```python
from sauerbraten_demo_parser import DemoParser, Packet
from sauerbraten_demo_parser.sauerconsts import *
import requests

parser = DemoParser()

demo = requests.get("https://sauerdemos.com/download/1503817.dmo").content

packet_list = parser.parse_raw(demo)

# Note that the shot/explosion information and the damage information are in separate packets
gun_hits = packet_list.where(Packet.type() == N_DAMAGE).select()
rocket_explosions = (
    packet_list.where(Packet.type() == N_EXPLODEFX)
    .select()
    .where(Packet.variable("gun") == GUN_RL)
    .select()
)

rockets_120 = []

for explosion in rocket_explosions:
    # Find a hit that has the same timestamp and cn
    current_hit = (
        gun_hits.where(Packet.time() == explosion.timestamp)
        .select()
        .where(Packet.cn() == explosion.args["cn"])
        .last()
    )

    # If no hit we skip the loop
    if not current_hit:
        continue

    # Skip if the damage isn't 120
    if current_hit.args["damage"] != 120:
        continue

    rockets_120.append(current_hit)

print(rockets_120)
```

# What next?
To use this tool effectively you need to know how the sauer net protocol works. A good starting point would be looking at the ``sauerconsts.py`` which contains all the network packets (starting with N_) and then trying to get all the packets of one specific type and printing them out to see what information they contain.
<br>
<br>
As for the project I'd like to rewrite it in C or Rust eventually to improve performance as well as adding more helper functions and features.
