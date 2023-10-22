#!/usr/bin/python3
"""
A flask app that renders a template.
"""
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.route("/states", strict_slashes=False)
@app.route("/states/<state_id>", strict_slashes=False)
def states_with_id(state_id=None):
    """
    Returns all states if no id is passed,
    else it returns all cities under the state
    with the specific id passed.
    """
    states = storage.all(State)
    if state_id is not None:
        state_id = f"State.{state_id}"

    return render_template(
        '9-states.html',
        states=states,
        state_id=state_id 
    )


@app.teardown_appcontext
def teardown_func(exception):
    """Handles storage.close()"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
