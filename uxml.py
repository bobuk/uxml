import xml.sax
from copy import copy
import re

TEXT = "#text"

def composer(wl,frm = 0):
    res = {}
    last_tag = wl[frm][0]
    skipline = 0
    for num, line in enumerate(wl[frm:], start=frm):
        if skipline and skipline !=num:
            continue
        skipline = 0
        [tag, data] = line
        if tag == last_tag:
            if type(data) == str:
                if data.strip():
                    try:
                        res[TEXT] += data
                    except:
                        res[TEXT] = data
            else:
                res.update(data)
        else:
            if len(tag) > len(last_tag):
                newtag, newres, line = composer(wl, frm=num)
                if newtag in res:
                    if type(res[newtag]) == list:
                        res[newtag].append(newres)
                    else:
                        res[newtag] = [res[newtag], newres]
                else:
                    res[newtag] = newres
                skipline = line
            else:
                if len(res) == 1 and TEXT in res:
                    res = res[TEXT]
                return last_tag[-1], res, num
    return last_tag[-1], res, num

def block_to_dict(wl):
    last_tag, res, num = composer(wl, 0)
    return res

class uXMLParser(xml.sax.ContentHandler):
    def __init__(self, catchers):
        self.path = []
        # self.subs = []
        # self.current = []
        self.catchers = catchers
        super().__init__()

    def startElement(self, name, attrs):
        self.path.append(name)
        self._p = '/' + '/'.join(self.path)
        attrs_w = {'@' + k: v for k,v in attrs.items() if k and v}
        for element in self.catchers:
            if element(self._p):
                element.subs.append(name)
                _r = copy(element.subs)
                if attrs_w:
                    element.current.append([_r, attrs_w])
                    
    def characters(self, content):
        for element in self.catchers:
            if element.current:
                element.current.append([copy(element.subs), content])

    def endElement(self, name):
        if self.path[-1] != name:
            raise Exception('What???')
        self.path.pop()
        self._p = '/' + '/'.join(self.path)
        for element in self.catchers:
            if element.current:
                try:
                    element.subs.pop()
                except:
                    continue # empty tag?
                if not element(self._p):
                    element.callback(block_to_dict(element.current))
                    element.cleanup()

class Catcher:
    def __init__(self, area, cb):
        self._comp = str(area)
        if not callable(area):
            if not hasattr(area, 'match'):
                area = area.replace('//', '.*/') + '.*$'
                area = re.compile(area)
            comp = lambda c: area.match(c)
        else:
            comp = area
        self.comp = comp
        self.callback = cb
        self.cleanup()

    def cleanup(self):
        self.subs = []
        self.current = []

    def __call__(self, arg):
        return self.comp(arg)
    def __repr__(self):
        return f"Catcher {self._comp}"

class Parser:
    def __init__(self, source):
        self.source = source
        self.catchers = []
    
    def find(self, area, cb):
        self.catchers.append(Catcher(area, cb))
        return self
    
    def start(self):
        u_parser = uXMLParser(self.catchers)
        parser = xml.sax.make_parser()
        parser.setContentHandler(u_parser)
        parser.parse(self.source)