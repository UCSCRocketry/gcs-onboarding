import eventlet  #networking library for handling concurrent connections and RT communication
from threading import Lock, Event  #threading library for handling concurrent tasks
from flask import Flask, request  #framework for creating server that handles rest api, util for accessing http request data
from flask_cors import CORS  #library for handling cors (cross-origin resource sharing) so front and back can talk
from flask_socketio import SocketIO  #library for handling websockets (RT)
from generate_data import generate  #see generate_data.py for more info
from parse_packet import parse #see parse_packet.py for more info --> TODO: write a parser in this file


api = Flask(__name__) #create flask server
api.config['SECRET_KEY'] = 'secret!' #session cookies, security stuff
CORS(api, resources={r"/*": {"origins": "http://localhost:3000"}})     # allows requests to /api/ pages from origin localhost:3000 (frontend)
socketio = SocketIO(api, async_mode="eventlet", cors_allowed_origins="*", ping_interval=2, always_connect=True) #handles websockets (RT)

# handle threads for RT communication
thread = None
thread_event = Event()
thread_lock = Lock()
thread_update = None

state = {"HIGH_G_ACCEL" : []}  # dict of sensor naem: recent values list from the sensor

queue = []  # queue for data to send to frontend
sequence_id = 0  #sequence id for the packet
connected_users = 0   # number of connected users aka webclients

# generates randomized data from a serialport every 1 ms
def update_data():
    global queue, sequence_id
    while True:
        socketio.sleep(0.01)  #0.01 seconds between each update
        print("updated data!") 
        sequence_id += 1
        packet = generate(sequence_id)  # returns hex-encoded ASCII bytes
        name, seq, data_array = parse(packet)  #TODO: write a parser
        queue.insert(0, [name, seq, data_array])

# sends any data waiting in the queue to the frontend
def send_data(event):
    global thread, queue, state
    count = 0
    try:
        while event.is_set():
            socketio.sleep(0.01)
            while len(queue) > 0:
                count += 1
                print('Sending data...')
                with api.test_request_context('/'):
                    packet = queue.pop()

                    # send all types of data
                    name, seq, data_arr = packet[0], packet[1], packet[2]
                    if name not in state:
                        state[name] = []
                    state[name].extend(data_arr)
                    state[name] = state[name][-5:]
                    print(packet)
                    socketio.emit(f'send_data_{name}',
                                {'label': 'Server generated event',
                                 'name': name,
                                 'num': seq,
                                 'data': data_arr,
                                 'count': count})
    finally:
        event.clear()
        thread = None

# sends state to  frontend
def send_state():
    global state
    for s in state:
        socketio.emit(f'send_data_{s}',
                      {'label': 'Server generated event',
                       'name': s,
                       'num': len(state[s]),
                       'data': state[s]})

#handles new client connections:updates user count, sends current state + ensures background generator/sender tasks are running right
@socketio.on("connect")
def connect_msg():
    global thread, thread_update, connected_users

    connected_users += 1
    print(request.sid)
    print(f'Client is connected! Current users: {connected_users}')

    send_state()

    if thread_update is None:
        thread_update = socketio.start_background_task(update_data)

    with thread_lock:
        if thread is None:
            print("Starting background thread...")
            thread_event.set()
            thread = socketio.start_background_task(send_data, thread_event)
    socketio.emit('connected', {'data': f"id: {request.sid} is connected."})

# stops send_data thread if no users are connected
@socketio.on("disconnect")
def disconnect_msg():
    global thread, connected_users
    connected_users -= 1
    if (not connected_users):
        thread_event.clear()
        with thread_lock:
            if thread is not None:
                thread.join()
                thread = None
    print(f'Client disconnected! Current users: {connected_users}')

# example GET route
@api.route('/api/test')
def testroute():
    global sequence_id
    sequence_id += 1
    packet_hex = generate(sequence_id)  # hex-encoded ASCII bytes
    name, seq, data_array = parse(packet_hex)

    return {
        "packet_hex": packet_hex.decode("ascii"),
        "name": name,
        "sequence_id": seq,
        "data": {
            "x": data_array[0],
            "y": data_array[1],
            "z": data_array[2]
        }

    # Write an example of what this returns? 
    # Note: this format (especially since we are using rest api) is called json

        # {
        #     "packet_hex": " ",
        #     "name": " ",
        #     "sequence_id": " ",
        #     "data": {
        #         "x": ,
        #         "y": ,
        #         "z": 
        #     }
        # }
    }

socketio.run(api, debug=True, port=9999)
