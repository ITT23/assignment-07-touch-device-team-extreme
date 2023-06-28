from DIPPID import SensorUDP

'''
this file is for testing event_streamer.py
'''

PORT = 5700
sensor = SensorUDP(PORT)


def handle_callback(data):
    for finger_id, value in data.items():
        type = value['type']
        x = value['x']
        y = value['y']
        print(finger_id, type, x, y)

sensor.register_callback('events', handle_callback)