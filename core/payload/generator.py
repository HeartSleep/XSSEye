import json
from pathlib import Path

from rjsmin import jsmin


class Generator:
    def __init__(self, scripts):
        self.script_prepend = ''
        for script_file in scripts:
            self.script_prepend += Path('payload/' + script_file).read_text(encoding='utf-8')
        self.script_prepend += '\r\n'
        self.script_prepend = jsmin(self.script_prepend)

    def generate(self, options):
        script = '(function(options) {var context = {options: options};'
        script += self.script_prepend
        script += '\r\n'
        script += jsmin(Path('payload/main.js').read_text(encoding='utf-8'))
        script += '})(%s)' % (json.dumps(options))

        return script
