#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/danthedeckie/simpleeval/blob/master/README.rst#compound-types
# """
# Compound types (dict, tuple, list, set) in general just work if you pass them in as named objects.
# If you want to allow creation of these, the EvalWithCompoundTypes class works. Just replace any use of
# SimpleEval with that.
# """


# pip install simpleeval
from simpleeval import simple_eval, SimpleEval, EvalWithCompoundTypes


# SimpleEval and simple_eval NOT WORK with compound types
try:
    print(simple_eval("[1, 2, 3, 4]"))
except Exception as e:
    print(e)  # Sorry, List is not available in this evaluator

try:
    my_eval = SimpleEval()
    print(my_eval.eval("[1, 2, 3, 4]"))
except Exception as e:
    print(e)  # Sorry, List is not available in this evaluator

print()

# Compound Types
my_compound_types_eval = EvalWithCompoundTypes()
my_compound_types_eval.functions["len"] = len

# list
print(my_compound_types_eval.eval("[1, 2, 3, 4]"))  # [1, 2, 3, 4]
print(my_compound_types_eval.eval("[1, 2] + [3, 4]"))  # [1, 2, 3, 4]
print(my_compound_types_eval.eval("len([1, 2, 3, 4])"))  # 4
print(my_compound_types_eval.eval("[1, 2, 1, 3, 4].count(1)"))  # 2
print(my_compound_types_eval.eval('list("1234")'))  # ['1', '2', '3', '4']
print()

# dict
print(my_compound_types_eval.eval('{"a": 1, "b": 999}'))  # {'a': 1, 'b': 999}
print(my_compound_types_eval.eval('{"a": 1, "b": 999}["b"]'))  # 999
print(my_compound_types_eval.eval('{"a": 1, "b": 999}.items()')) # dict_items([('a', 1), ('b', 999)])
print(my_compound_types_eval.eval('len({"a": 1, "b": 999})'))  # 2
print(my_compound_types_eval.eval('dict([("a", 1), ("b", 999)])'))  # {'a': 1, 'b': 999}
print()

# tuple
print(my_compound_types_eval.eval("(1, 2, 3, 4)"))  # (1, 2, 3, 4)
print(my_compound_types_eval.eval("(1, 2) + (3, 4)"))  # (1, 2, 3, 4)
print(my_compound_types_eval.eval("1, 2, 3, 4"))  # (1, 2, 3, 4)
print(my_compound_types_eval.eval("len((1, 2, 3, 4))"))  # 4
print(my_compound_types_eval.eval("(1, 2, 1, 3, 4).count(1)"))  # 2
print()

# set
print(my_compound_types_eval.eval("{1, 2, 3, 4}"))  # {1, 2, 3, 4}
print(my_compound_types_eval.eval("{1, 2, 1, 3, 1, 4, 3}"))  # {1, 2, 3, 4}
print(my_compound_types_eval.eval("[1, 2, 1, 3, 1, 4, 3]"))  # [1, 2, 1, 3, 1, 4, 3]
print(my_compound_types_eval.eval("set([1, 2, 1, 3, 1, 4, 3])"))  # {1, 2, 3, 4}
print(my_compound_types_eval.eval("{1, 1, 2}.union({3, 2, 4})"))  # {1, 2, 3, 4}
print(my_compound_types_eval.eval("{1, 1, 2}.intersection({3, 2, 4})"))  # {2}
