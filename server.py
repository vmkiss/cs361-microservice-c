import os
import zmq
import csv
import time

# Create CSV file if it doesn't exist yet
HEADERS = ["Title", "Artist", "Rating", "Review"]
REVIEWS = "reviews.csv"

if not os.path.exists(REVIEWS):
    with open(REVIEWS, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(HEADERS)

# Establish socket connection
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://localhost:5555")

while True:
    message = socket.recv_string()
    time.sleep(1)

    if message:
        if message.lower() == 'q':
            context.destroy()
            break
        else:
            data_rows = message.split('\n')

    socket.send_string("reply")