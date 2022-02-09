import threading

#State is essentially just a set of global variables which will be accessible through an EHW instance.
class State:
    def __init__(this):
        this.lock = threading.Lock()

    def Has(this, name):
        ret = False
        with this.lock:
            ret = hasattr(this,name)
        return ret

    def Set(this, name, value):
        with this.lock:
            setattr(this, name, value)

    def Get(this, name):
        ret = False
        with this.lock:
            ret = getattr(name)
        return ret