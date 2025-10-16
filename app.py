from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title
    
    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    # Get the JSON data from the request
    data = request.get_json()
    
    # Check if title is provided
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400
    
    # Create a new event with a new ID
    new_id = len(events) + 1
    new_event = Event(new_id, data["title"])
    events.append(new_event)
    
    return jsonify(new_event.to_dict()), 201

# Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    # Get the JSON data from the request
    data = request.get_json()
    
    # Find the event with the matching ID
    for event in events:
        if event.id == event_id:
            # Update the title if provided
            if "title" in data:
                event.title = data["title"]
                return jsonify(event.to_dict()), 200
            else:
                return jsonify({"error": "Title is required"}), 400
    
    # If event not found
    return jsonify({"error": "Event not found"}), 404

# Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):

    # Find and remove the event with the matching ID
    for i, event in enumerate(events):
        if event.id == event_id:
            events.pop(i)
            return "", 204
    
    # If event not found
    return jsonify({"error": "Event not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)