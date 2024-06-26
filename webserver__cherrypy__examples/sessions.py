"""
Tutorial - Sessions
Storing session data in CherryPy applications is very easy: cherrypy
provides a dictionary called "session" that represents the session
data for the current user. If you use RAM based sessions, you can store
any kind of object into that dictionary; otherwise, you are limited to
objects that can be pickled.
"""


# SOURCE: https://github.com/cherrypy/cherrypy/blob/master/cherrypy/tutorial/tut07_sessions.py


import cherrypy


class HitCounter:
    _cp_config = {"tools.sessions.on": True}

    @cherrypy.expose
    def index(self):
        # Increase the silly hit counter
        count = cherrypy.session.get("count", 0) + 1

        # Store the new value in the session dictionary
        cherrypy.session["count"] = count

        # And display a silly hit count message!
        return (
            f"""
            During your current session, you've viewed this
            page {count} times! Your life is a patio of fun!
        """
        )


if __name__ == "__main__":
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().
    cherrypy.quickstart(HitCounter())
