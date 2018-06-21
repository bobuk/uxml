import xml.etree.ElementTree as ET
import re

def element_to_dict(element, clean=False):
    '''Convert xml element to pythonic structures like dict or string.
    params: clean (False by default) if set - return only attribs and children of this element
    '''
    tag = element.tag
    text = [element.text.strip() if element.text else "", ]

    d = {"@"+a:v for a,v in element.attrib.items()}

    for kid in element:
        text.append(kid.tail.strip() if kid.tail else "")
        ch = element_to_dict(kid)
        if kid.tag in d:
            c = d[kid.tag]
            if isinstance(c, list):
                c.append(ch[kid.tag])
            else:
                d[kid.tag] = [c, ch[kid.tag]]
        else:
            d[kid.tag] = ch[kid.tag]

    text = [t for t in text if t]
    text = text[0] if len(text) == 1 else '\n'.join(text)
    if d:
        if text:
            d["#text"] = text
    else:
        d = text
    return d if clean else {tag: d}

class Parser:
    def __init__(self, source):
        self.source = source
        self.comp = []

    def find(self, area, cb, clean=True):
        if not callable(area):
            if not hasattr(area, 'match'):
                area = area.replace('//', '.*/') + '$'
                area = re.compile(area)
            comp = lambda c, e: area.match(c)
        else:
            comp = area
        opts = {'clean': clean}
        self.comp.append(
            (comp, cb, opts, )
        )
        return self
    
    def start(self, cleanup = True):
        parser = ET.XMLPullParser(events=('start', 'end'))
        position = []
        for chunk in self.source.read():
            parser.feed(chunk)
            for action, element in parser.read_events():
                if action == 'start':
                    position.append(element.tag)
                elif action == 'end':
                    if element.tag == position[-1]:
                        pos = '/' + '/'.join(position)
                        for comp, callback, opts in self.comp:
                            if comp(pos, element):
                                res = callback(element_to_dict(element, clean=opts['clean']))
                                if cleanup:
                                    # this is very nasty, beware
                                    element.clear()
                        position.pop()
                    else:
                        raise Exception(f'What a heck? {element}')

