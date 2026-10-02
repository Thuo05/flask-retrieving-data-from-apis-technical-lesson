from flask import Flask, jsonify, request

app = Flask(__name__)


# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}


# In-memory list simulates a database
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]


# POST /events - Create a new event
@app.route("/events", methods=["POST"])
def create_event():
    # Get JSON data sent by the client
    data = request.get_json()

    # Make sure the request contains JSON
    if not data:
        return jsonify({"error": "Request body must contain JSON data"}), 400

    # Get the title from the JSON body
    title = data.get("title")

    # Validate that a title was provided
    if not title:
        return jsonify({"error": "Event title is required"}), 400

    # Generate a new ID based on the existing events
    new_id = max(event.id for event in events) + 1 if events else 1

    # Create and store the new event
    new_event = Event(new_id, title)
    events.append(new_event)

    # Return the created event with 201 Created
    return jsonify(new_event.to_dict()), 201


# PATCH /events/<id> - Update an event title
@app.route("/events/<int:id>", methods=["PATCH"])
def update_event(id):
    # Find the event with the requested ID
    event = next((event for event in events if event.id == id), None)

    # Return 404 if the event does not exist
    if event is None:
        return jsonify({"error": "Event not found"}), 404

    # Get JSON data from the request
    data = request.get_json()

    # Make sure JSON data was provided
    if not data:
        return jsonify({"error": "Request body must contain JSON data"}), 400

    # Get the new title
    title = data.get("title")

    # Validate the new title
    if not title:
        return jsonify({"error": "Event title is required"}), 400

    # Update the event title
    event.title = title

    # Return the updated event
    return jsonify(event.to_dict()), 200


# DELETE /events/<id> - Remove an event
@app.route("/events/<int:id>", methods=["DELETE"])
def delete_event(id):
    # Find the event with the requested ID
    event = next((event for event in events if event.id == id), None)

    # Return 404 if the event does not exist
    if event is None:
        return jsonify({"error": "Event not found"}), 404

    # Remove the event from the in-memory list
    events.remove(event)

    # Return a confirmation message
    return jsonify({"message": "Event deleted successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True)