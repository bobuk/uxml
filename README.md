# μXML - xml stream parsing in less than 100 lines of code

μXML is oversimlified way to parse large (or slow loading) XML lines with easy way for tag matching and callbacking.
No dependencies (besides python3.4+) and only one class `uxml.Parser` inside the library.

```python
import uxml
p = uxml.Parser(open('test.rss'))
p.find('/rss/channel/item', lambda e: print(e))
p.start()
```

First meaningful line is parser's object creation. The only parameter is file (or any other `io.TextIOWrapper` compatible) object.
`.find` method add new tag matcher for parser. First argument is a pointer to tag which we want to find inside xml stream.
I use nanoxpath notation (i.e. you should show full path to this tags or use `//` as a starting symbol).
Second argument of `find` is a callback which will be invoked if given tag is found and the only argument for this callback is a internal structure of tags and attributes inside this tag. Attributes can be separated from children tags by name, it's always starts with '@' symbol.
If tag is just one internal text - it will be returned as result. If there's more than one children with same name, it will be returned as list of tags. If tag have both internal text and attributes, first will be added to attributes as '#text'.

You can use unlimited number of `find`'s.
Parsing will start with `start` method. Example above will print every item inside given rss file.
Let me show you a little bit more complicated stuff.

```python
res = []
p = uxml.Parser(open('test.rss'))
p.find('//link', lambda x: res.append(x)).find('//description', lambda x: print(x)).start()
```

First off all you can notice what `find` and `start` calls are chainable.
Trailing `/` will convert to any number of previous tags, so this time we will got list of links at `res` variable.


