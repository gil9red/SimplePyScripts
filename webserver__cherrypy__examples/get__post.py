"""
Tutorial - Passing variables
This tutorial shows you how to pass GET/POST variables to methods.
"""


# SOURCE: https://github.com/cherrypy/cherrypy/blob/master/cherrypy/tutorial/tut03_get_and_post.py


import cherrypy


class WelcomePage:
    @cherrypy.expose
    def index(self) -> str:
        # Ask for the user's name.
        return """
            <p>GET:<p>
            <form action="greet_user" method="GET">
                What is your name?
                <input type="text" name="name" />
                <input type="submit" />
            </form>
            
            <br>
            <p>POST:<p>
            <form action="greet_user" method="POST">
                What is your name?
                <input type="text" name="name" />
                <input type="submit" />
            </form>
        """

    @cherrypy.expose
    def greet_user(self, name=None) -> str:
        # CherryPy passes all GET and POST variables as method parameters.
        # It doesn't make a difference where the variables come from, how
        # large their contents are, and so on.
        #
        # You can define default parameter values as usual. In this
        # example, the "name" parameter defaults to None so we can check
        # if a name was actually specified.

        if name:
            # Greet the user!
            return "Hey %s, what's up?" % name
        else:
            if name is None:
                # No name was specified
                return 'Please enter your name <a href="./">here</a>.'
            else:
                return 'No, really, enter your name <a href="./">here</a>.'


if __name__ == "__main__":
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().
    cherrypy.quickstart(WelcomePage())
