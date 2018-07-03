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
    def __init__(self, flt, callback):
        self.finder = flt
        self.callback = callback
        self.path = []
        self.current = []
        self.subs = []
        super().__init__()

    def startElement(self, name, attrs):
        self.path.append(name)
        self._p = '/' + '/'.join(self.path)
        if self.finder(self._p):
            self.subs.append(name)
            _r = copy(self.subs)
            attrs_w = {'@' + k: v for k,v in attrs.items() if k and v}
            if attrs_w:
                self.current.append([_r, attrs_w])
                    
    def characters(self, content):
        if not self.current: return
        self.current.append([copy(self.subs), content])

    def endElement(self, name):
        if self.path[-1] != name:
            raise Exception('What???')
        self.path.pop()
        self._p = '/' + '/'.join(self.path)
        if self.current:
            try:
                self.subs.pop()
            except:
                return # empty tag?
            if not self.finder(self._p):
                self.callback(block_to_dict(self.current))
                self.current = []
                self.subs = []

class Parser:
    def __init__(self, source):
        self.source = source

    def find(self, area, cb):
        if not callable(area):
            if not hasattr(area, 'match'):
                area = area.replace('//', '.*/') + '.*$'
                area = re.compile(area)
            comp = lambda c: area.match(c)
        else:
            comp = area
        self.comp = comp
        self.callback = cb
        return self
    
    def start(self):
        u_parser = uXMLParser(self.comp, self.callback)
        parser = xml.sax.make_parser()
        parser.setContentHandler(u_parser)
        parser.parse(self.source)