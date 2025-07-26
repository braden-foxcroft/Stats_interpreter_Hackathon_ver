



# tokens:
"""
( ) + - // *
integers
strings (with '_' allowed)
"""

# Sample lines:
"""
select str from expr [where expr]
set str = expr
discard expr

if expr
    code

if expr
    code
else
    code

if expr
    code
elif expr
    code
elif expr
    code
else
    code

for str in expr
    code

for str from expr
    code

pass
fail
done
good
bad

"""

# Expr:
"""
binary operators:
or
and
,
to
+ -
* //
()

unary operators:
not
-

"""


def compile(file):
    return None # Tree

