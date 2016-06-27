#!/usr/bin/env python3
import os
from flask import Flask, request, render_template, send_from_directory

script_dir = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__)

class AttrDict(dict):
    def __init__(self, d):
        if not isinstance(d, dict):
            d = {a:getattr(d,a) for a in dir(d)}

        super(AttrDict, self).__init__(d)
        self.__dict__ = self

def check(text):
    import base64, operator, itertools, zlib
    R = ('eJw1i0sKwzAMRHuULmXwpRTbYIM/QlZoEubwdVoyi4H3mHm9UccnKXaR1bVMQ2PB0Ihp'
         'iqsIuFbMfUMY3bj0iZYsjxiWXxdNktjWmPU+hrwmqG2AJWLrAWoZx3khklH3QkqVGg1/'
         'OOe80bbUjYFOR0zztn++Hv7lCwJAPlc=')
    A = zlib.decompress(base64.b64decode(R)).decode().split('|')
    D = dict(itertools.chain(*(zip(A[i+15], operator.attrgetter(*A[3*i+3:3*i+6])(x))
        for i,x in enumerate((AttrDict(__builtins__), AttrDict(__builtins__), operator, itertools)))))
    try: return not eval(A[20], D, dict(zip(A[19], A[:3]), s=text))
    except: return False

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        if check(request.form['data']):
            return render_template('index.html', showflag=True)
        else:
            return render_template('index.html', incorrect=True)
    else:
        return render_template('index.html')

@app.route('/app.py')
def get_source():
    return send_from_directory(script_dir, 'app.py')

if __name__ == "__main__":
    app.run(debug=True, port=5001)
