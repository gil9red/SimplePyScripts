from sly import Lexer, Parser
import pprint


class JSONLexer(Lexer):
    tokens = {"FLOAT", "INTEGER", "STRING"}

    literals = {'{', '}', '[', ']', ',', ':'}
    ignore = " \t\n"

    @_(r"\".*?\"")
    def STRING(self, t):
        t.value = t.value.strip("\"")
        return t

    @_(r"\d+\.\d*")
    def FLOAT(self, t):
        t.value = float(t.value)
        return t

    @_(r"\d+")
    def INTEGER(self, t):
        t.value = int(t.value)
        return t


class JSONParser(Parser):
    tokens = JSONLexer.tokens
    start = "json"

    @_('object',
       'array')
    def json(self, p):
        return p[0]

    @_('"{" members "}"')
    def object(self, p):
        return {key: value for key, value in p.members}

    @_('pair')
    def members(self, p):
        return [p.pair]

    @_('pair "," members')
    def members(self, p):
        return [p.pair] + p.members

    @_('STRING ":" value')
    def pair(self, p):
        return p.STRING, p.value

    @_('"[" elements "]"')
    def array(self, p):
        return p.elements

    @_('value')
    def elements(self, p):
        return [p.value]

    @_('value "," elements')
    def elements(self, p):
        return [p.value] + p.elements

    @_('STRING',
       'INTEGER',
       'FLOAT',
       'object',
       'array')
    def value(self, p):
        return p[0]

    def error(self, p):
        raise ValueError("Parsing error at token %s" % str(p))


if __name__ == "__main__":
    lexer = JSONLexer()
    parser = JSONParser()
    json_text = """
        {"menu": {
          "id": "file",
          "value": "File",
          "popup": {
            "menuitem": [
              {"value": "New", "onclick": "CreateNewDoc()"},
              {"value": "Open", "onclick": "OpenDoc()"},
              {"value": "Close", "onclick": "CloseDoc()"}
            ],
            "delay" : 1.5
          }
        }}
    """
    result = parser.parse(lexer.tokenize(json_text))
    pprint.pprint(result)
