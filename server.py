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

    result = "Error: Review could not be saved."

    if message:
        if message.lower() == 'q':
            context.destroy()
            break
        else:
            review = message.split('\n')
            title = review[1]
            artist = review[2]

            with open(REVIEWS, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(review)

            result = f"Review added for {title} by {artist}."

        socket.send_string(result)