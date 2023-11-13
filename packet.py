from .sauerconsts import packet_names
from .utils import packet_dict


class Packet(object):
    def __init__(self, type, timestamp, args=[], context={}):
        self.type = type
        self.timestamp = timestamp
        self.raw_args = args
        self.args = packet_dict(self)
        self.context = context

    def __str__(self):
        resp = f"Packet({packet_names[self.type]}, timestamp={self.timestamp}, args={self.args}"

        if self.context:
            resp += f", context={self.context}"

        resp += ")"

        return resp

    def __repr__(self):
        return self.__str__()

    def get(self, arg):
        return self.args.get(arg)

    def __getitem__(self, arg):
        return self.args[arg]

    class type(object):
        def __eq__(self, value):
            return {"query": "type", "action": "==", "value": value}

        def __lt__(self, value):
            return {"query": "type", "action": "<", "value": value}

        def __le__(self, value):
            return {"query": "type", "action": "<=", "value": value}

        def __gt__(self, value):
            return {"query": "type", "action": ">", "value": value}

        def __ge__(self, value):
            return {"query": "type", "action": ">=", "value": value}

        def __ne__(self, value):
            return {"query": "type", "action": "!=", "value": value}

        def select(self, value):
            return {"query": "type", "action": "select", "value": value}

        def exclude(self, value):
            return {"query": "type", "action": "exclude", "value": value}

    class time(object):
        def __eq__(self, value):
            return {"query": "time", "action": "==", "value": value}

        def __lt__(self, value):
            return {"query": "time", "action": "<", "value": value}

        def __le__(self, value):
            return {"query": "time", "action": "<=", "value": value}

        def __gt__(self, value):
            return {"query": "time", "action": ">", "value": value}

        def __ge__(self, value):
            return {"query": "time", "action": ">=", "value": value}

        def __ne__(self, value):
            return {"query": "time", "action": "!=", "value": value}

        def select(self, value):
            return {"query": "time", "action": "select", "value": value}

        def exclude(self, value):
            return {"query": "time", "action": "exclude", "value": value}

    class cn(object):
        def __eq__(self, value):
            return {"query": "cn", "action": "==", "value": value}

        def __lt__(self, value):
            return {"query": "cn", "action": "<", "value": value}

        def __le__(self, value):
            return {"query": "cn", "action": "<=", "value": value}

        def __gt__(self, value):
            return {"query": "cn", "action": ">", "value": value}

        def __ge__(self, value):
            return {"query": "cn", "action": ">=", "value": value}

        def __ne__(self, value):
            return {"query": "cn", "action": "!=", "value": value}

        def select(self, value):
            return {"query": "cn", "action": "select", "value": value}

        def exclude(self, value):
            return {"query": "cn", "action": "exclude", "value": value}

    class variable(object):
        def __init__(self, var):
            self.var = var

        def __eq__(self, value):
            return {
                "query": "variable",
                "variable": self.var,
                "action": "==",
                "value": value,
            }

        def __lt__(self, value):
            return {
                "query": "variable",
                "variable": self.var,
                "action": "<",
                "value": value,
            }

        def __le__(self, value):
            return {
                "query": "variable",
                "variable": self.var,
                "action": "<=",
                "value": value,
            }

        def __gt__(self, value):
            return {
                "query": "variable",
                "variable": self.var,
                "action": ">",
                "value": value,
            }

        def __ge__(self, value):
            return {
                "query": "variable",
                "variable": self.var,
                "action": ">=",
                "value": value,
            }

        def __ne__(self, value):
            return {
                "query": "variable",
                "variable": self.var,
                "action": "!=",
                "value": value,
            }

        def select(self, value):
            return {
                "query": "variable",
                "variable": self.var,
                "action": "select",
                "value": value,
            }

        def exclude(self, value):
            return {
                "query": "variable",
                "variable": self.var,
                "action": "exclude",
                "value": value,
            }


class PacketList(object):
    def __init__(self, packets=[]):
        if type(packets) != list:
            self.packets = list([packets])
        else:
            self.packets = list(packets)

    def __str__(self):
        resp = f"PacketList(["

        num = len(self.packets)

        if num == 1:
            resp += f"\n    {str(self.packets[0])}"
        elif num == 2:
            resp += f"\n    {str(self.packets[0])},\n    {str(self.packets[1])}"
        elif num == 3:
            resp += f"\n    {str(self.packets[0])},\n    {str(self.packets[1])},\n    {str(self.packets[2])}"
        elif num == 4:
            resp += f"\n    {str(self.packets[0])},\n    {str(self.packets[1])},\n    {str(self.packets[2])},\n    {str(self.packets[3])}"
        elif num > 4:
            resp += f"\n    {str(self.packets[0])},\n    {str(self.packets[1])},\n    ...\n    {str(self.packets[-2])},\n    {str(self.packets[-1])}"

        if num > 0:
            resp += "\n"

        resp += f"], packets={num})"

        return resp

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return len(self.packets)

    def __getitem__(self, arg):
        return self.packets[arg]

    def where(self, query={}):
        packet_list_query = PacketListQuery(self)
        packet_list_query.where(query)

        return packet_list_query


class PacketListQuery(object):
    def __init__(self, packet_list):
        self.queries = []
        self.packet_list = packet_list

    def first(self):
        filtered_list = self.select()
        if len(filtered_list) > 0:
            return filtered_list[0]
        else:
            return None

    def last(self):
        filtered_list = self.select()
        if len(filtered_list) > 0:
            return filtered_list[-1]
        else:
            return None

    def where(self, query):
        if query["query"] not in ["type", "time", "cn", "variable"]:
            raise InvalidVariable()

        if query["action"] not in [
            "==",
            ">",
            "<",
            ">=",
            "<=",
            "!=",
            "select",
            "exclude",
        ]:
            raise InvalidAction()

        self.queries.append(query)

        return self

    def select(self):
        packets = []

        def compare(value):
            if query["action"] == "==":
                return value == query["value"]

            elif query["action"] == ">":
                return value > query["value"]

            elif query["action"] == "<":
                return value < query["value"]

            elif query["action"] == ">=":
                return value >= query["value"]

            elif query["action"] == "<=":
                return value <= query["value"]

            elif query["action"] == "!=":
                return value != query["value"]

            elif query["action"] == "select":
                return value in query["value"]

            elif query["action"] == "exclude":
                return value not in query["value"]

        for packet in self.packet_list:
            for query in self.queries:
                if query["query"] == "type":
                    if compare(packet.type):
                        packets.append(packet)

                if query["query"] == "time":
                    if compare(packet.timestamp):
                        packets.append(packet)

                if query["query"] == "cn":
                    # The client num variable has different names in different
                    # packets so we check for all of them
                    if "cn" in packet.args and compare(packet["cn"]):
                        packets.append(packet)

                    elif "mycn" in packet.args and compare(packet["mycn"]):
                        packets.append(packet)

                    elif "tcn" in packet.args and compare(packet["tcn"]):
                        packets.append(packet)

                    elif "acn" in packet.args and compare(packet["acn"]):
                        packets.append(packet)

                    elif "vcn" in packet.args and compare(packet["vcn"]):
                        packets.append(packet)

                if query["query"] == "variable":
                    keys = query["variable"].split(".")
                    variable = packet

                    for key in keys:
                        variable = variable.get(key)

                    if variable is None:
                        continue

                    if compare(variable):
                        packets.append(packet)

        return PacketList(packets)
