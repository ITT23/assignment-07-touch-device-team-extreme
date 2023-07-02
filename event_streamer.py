import socket
import json


class EventStreamer:
    def __init__(self, ip: str, width: int, height: int) -> None:
        self.IP = ip
        self.PORT = 5700
        self.width = width
        self.height = height
        self.dippid_data = dict()
        self.events = dict()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    def add_to_stream(self, type: str, x: float, y: float):
        """
        add event for each detected finger to stream
        """
        if type != 'touch' and type != 'hover':
            return
        index = len(self.events)
        current_event = dict()
        current_event['type'] = type
        current_event['x'] = x / self.width
        current_event['y'] = y / self.height
        self.events[index] = current_event
        self.dippid_data['events'] = self.events


    def send_stream(self):
        """
        send data for each detected finger
        """ 
        self.sock.sendto(json.dumps(self.dippid_data).encode(), (self.IP, self.PORT))
        self.events = dict()
        self.dippid_data['events'] = self.events

