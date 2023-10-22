#!/usr/bin/python3
"""
A flask app that renders a template.
"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.user import User


app = Flask(__name__)


@app.route("/hbnb", strict_slashes=False)
def hbnb_filters():
    """
    Displays states and amenities filters.
    As well as places.
    """
    states = storage.all(State).values()
    amenities = storage.all(Amenity).values()
    places = storage.all(Place).values()
    users = storage.all(User).values()

    return render_template(
        '100-hbnb.html',
        states=states,
        amenities=amenities,
        places=places,
        users=users
    )


@app.teardown_appcontext
def teardown_func(exception):
    """Handles storage.close()"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
