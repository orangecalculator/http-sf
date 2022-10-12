
# HTTP Structured Field Values in Python

[![Actions Status](https://github.com/mnot/http_sfv/workflows/CI/badge.svg)](https://github.com/mnot/http_sfv/actions)

This is a [Python 3](https://python.org/) library implementing parsing and serialisation of [HTTP Structured Fields](https://httpwg.org/http-extensions/draft-ietf-httpbis-header-structure.html).

The library's initial purpose is to prove the algorithms in the specification; as a result, it is not at all optimised. It tracks the specification closely, but since it is not yet an RFC, may change at any time.

_Currently, this implements draft 19 of the specification._

## Python API

Textual HTTP headers can be parsed by calling `parse_text`; the return value is a data structure that represents the field value.

~~~ python
>>> from http_sfv import parse_text, ser_text
>>> parse_text(b"foo; a=1, bar; b=2", tltype="dictionary")
{'foo': (True, {'a': 1}), 'bar': (True, {'b': 2})}
~~~

Note that `.parse()` takes a bytes-like object as the first argument. If you want to parse a string, please `.encode()` it first.

Because the library needs to know which kind of field it is, you need to hint this when calling `parse_text`. There are two ways to do this:

1. Using `tltype`, whose value should be one of 'dictionary', 'list', or 'item'.
2. Using `name` to indicate a field name that has a registered type, per [the retrofit draft](https://httpwg.org/http-extensions/draft-ietf-httpbis-retrofit.html).

Note that if you use `name`, a `KeyError` will be raised if the type associated with the name isn't known.

Dictionaries are represented as Python dictionaries; Lists are represented as Python lists, and Items are represented using the following Python types:

* Integers: `int`
* Decimals: `float`
* Strings: `str`
* Tokens: `http_sfv.Token` // a `UserString`
* Byte Sequences: `bytes`
* Booleans: `bool`

Inner Lists are represented as lists as well.

Structured Types that can have parameters (including Dictionary and List members as well as singular Items and Inner Lists) are represented as a tuple of `(value, parameters)` where parameters is a dictionary.

So, a single item that's a Token with one parameter whose value is an integer will be represented like this:

~~~ python
>>> parse_text(b"foo; a=1", tltype="item")
(Token("foo"), {'a': 1})
~~~

Note that even if there aren't parameters, a tuple will still be returned, as in soem items on this List:

~~~ python
>>> parse_text(b"a, b; q=5, c", tltype="list")
[(Token("a"), {}), (Token("b"), {'q': 5}), (Token("c"), {})]
~~~

To serialise that data structure back to a textual Structured Field, use `ser_text`:

~~~ python
>>> field = parse_text(b"a, b; q=5, c", tltype="list")
>>> ser_text(field)
'a, b;q=5, c'
~~~

When using `ser_text`, if an Item or Inner List doesn't have parameters, they can be omitted; for example:

~~~ python
>>> structure = [5, 6, (7, {"with": "param"})]
>>> ser_text(structure)
'5, 6, 7;with="param"'
~~~

However, `parse_text` will always produce tuples for Items and Inner Lists, even when there are no parameters:

~~~ python
>>> parse_text(bytes(ser_text(structure), encoding='ascii'), tltype='list')
[(5, {}), (6, {}), (7, {'with': 'param'})]
~~~

Note that `ser_text` produces a string, not a bytes-like object.


## Command Line Use

You can validate and examine the data model of a field value by calling the library on the command line, using `-d`, `-l` and `-i` to denote dictionaries, lists or items respectively; e.g.,

~~~ example
> python3 -m http_sfv -i "foo;bar=baz"
[
    {
        "__type": "token",
        "value": "foo"
    },
    {
        "bar": {
            "__type": "token",
            "value": "baz"
        }
    }
]
~~~

or:

~~~ example
> python3 -m http_sfv -i "foo;&bar=baz"
FAIL: Key does not begin with lcalpha or * at: &bar=baz
~~~

Note that if successful, the output is in the JSON format used by the [test suite](https://github.com/httpwg/structured-header-tests/).
