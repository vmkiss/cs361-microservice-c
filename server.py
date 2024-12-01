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

    result = ''

    if message:
        if message.lower() == 'q':
            context.destroy()
            break
        else:
            data = message.split('\n')
            if data[0] == "create":
                result = "Error: Review could not be saved."
                title = data[1]
                artist = data[2]
                row = data[1:]

                with open(REVIEWS, "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(row)
                result = f"Review added for {title} by {artist}."

            if data[0] == "search":
                result = "Error: Review could not be found."
                with open(REVIEWS, "r", newline="") as f:
                    review_reader = csv.DictReader(f)
                    reviews = list(review_reader)
                    for review in reviews:
                        if review['Title'] == data[1]:
                            result = f"REVIEW OF {review['Title'].upper()} BY {review['Artist'].upper()}:\n"
                            result += "RATING: " + review['Rating'] + "\n" + "REVIEW DETAILS: " + review['Review'] + "\n"

        socket.send_string(result)