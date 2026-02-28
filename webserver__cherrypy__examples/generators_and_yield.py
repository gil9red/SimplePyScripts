"""
Bonus Tutorial: Using generators to return result bodies
Instead of returning a complete result string, you can use the yield
statement to return one result part after another. This may be convenient
in situations where using a template package like CherryPy or Cheetah
would be overkill, and messy string concatenation too uncool. ;-)
"""


# SOURCE: https://github.com/cherrypy/cherrypy/blob/master/cherrypy/tutorial/tut08_generators_and_yield.py


import cherrypy


class GeneratorDemo:
    def header(self) -> str:
        return "<html><body><h2>Generators rule!</h2>"

    def footer(self) -> str:
        return "</body></html>"

    @cherrypy.expose
    def index(self):
        # Let's make up a list of users for presentation purposes
        users = ["Remi", "Carlos", "Hendrik", "Lorenzo Lamas"]

        # Every yield line adds one part to the total result body.
        yield self.header()
        yield "<h3>List of users:</h3>"

        for user in users:
            yield "%s<br/>" % user

        yield self.footer()


if __name__ == "__main__":
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().
    cherrypy.quickstart(GeneratorDemo())
