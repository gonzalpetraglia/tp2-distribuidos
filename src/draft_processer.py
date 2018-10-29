
context = zmq.Context()
socket = context.socket(zmq.SUB)
# We can connect to several endpoints if we desire, and receive from all.
socket.connect('tcp://{}:{}'.format('127.0.0.1', 2000))

socket.setsockopt_string(zmq.SUBSCRIBE, '')