"""Base class for all parser classes based on PLY
Most of this class was shamelessly stolen from the examples"""

import os

import dice.third_party.ply.lex as lex
import dice.third_party.ply.yacc as yacc


class PlyParser(object):
    """
    Base class for a lexer/parser that has the rules defined as methods
    """
    tokens = ()
    precedence = ()


    def __init__(self, **kw):
        """Constructs the parser and the lexer"""
        self.debug = kw.get('debug', 2)
        self.names = { }
        try:
            modname = os.path.split(os.path.splitext(__file__)[0])[1] + "_" + self.__class__.__name__
        except:
            modname = "parser"+"_"+self.__class__.__name__
        self.debugfile = modname + ".dbg"
        self.tabmodule = modname + "_" + "parsetab"

        # Build the lexer and parser
        lex.lex(module=self, debug=self.debug)
        yacc.yacc(module=self,
                  debug=self.debug,
                  debugfile=self.debugfile,
                  tabmodule=self.tabmodule,
                  check_recursion=self.debug)
        self.lex=lex
        self.yacc=yacc
        
    def parse(self,content):
        """Do the actual parsing
        @param content: String that is to be parsed
        @return: Result of the parsing"""

        if self.debug:
            debug=10
        else:
            debug=0
            
        return yacc.parse(content,debug=debug)

