# See https://stackoverflow.com/questions/16202548/measuring-the-time-to-load-a-page-python

url = "file:///home/jeanc/jupyterbook-venv/HeatHack-Data/_build/html/index.html"

import time

import urllib.request 

def time_it(func):
    def wrapper(*arg,**kw):
        t1 = time.time()
        res = func(*arg,**kw)
        t2 = time.time()
        return round((t2-t1),3),res,func
    return wrapper

@time_it
def perf_measure(url=""):
    # is this right?
    stream = urllib.request.urlopen(url)
    stream.close()
    pass


elapsed, result, f = time_it(perf_measure)(url)
print(elapsed, result, f)