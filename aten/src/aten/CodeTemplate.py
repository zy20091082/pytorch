import re

# match $idenifier or ${identifier}, if the first group matches, then
# this identifier is at the beginning of whitespace on a line and should be treated as
# block subsitution by identing to that depth and replacing

class CodeTemplate(object):
    subtitution = re.compile('(^[^\n\S]*)?\$([^\d\W]\w*|\{,?[^\d\W]\w*\,?})',re.MULTILINE)
    def from_file(filename):
        with open(filename,'r') as f:
            return CodeTemplate(f.read())
    def __init__(self,pattern):
        self.pattern = pattern
    def substitute(self,env={},**kwargs):
        def lookup(v):
             return kwargs[v] if v in kwargs else env[v]
        def indent_lines(indent,v):
            return "".join([indent+l+"\n" for e in v for l in str(e).splitlines()]).rstrip()
        def replace(match):
            indent = match.group(1)
            key = match.group(2)
            comma_before=''
            comma_after=''
            if key[0] == "{":
                key = key[1:-1]
                if key[0] == ",":
                    comma_before = ', '
                    key = key[1:]
                if key[-1] == ',':
                    comma_after = ', '
                    key = key[:-1]
            v = lookup(key)
            if indent is not None and isinstance(v,list):
                return indent_lines(indent,v)
            elif isinstance(v,list):
                middle = ', '.join([str(x) for x in v])
                if len(v) == 0:
                    return middle
                return comma_before+middle+comma_after
            else:
                return (indent or '') + str(v)
        return self.subtitution.sub(replace,self.pattern)

if __name__ == "__main__":
    c = CodeTemplate("""\
    int foo($args) {

        $bar
            $bar
        $a+$b
    }
    int commatest(int a${,stuff})
    int notest(int a${,empty,})
    """)
    print(c.substitute(args=["hi",8],bar=["what",7],a=3,b=4,stuff=["things...","others"],empty=[]))