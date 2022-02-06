
#State is essentially just a set of global variables which will be accessible through an EHW instance.
class State:
    def __init__(this):
        pass

    def Has(this, name):
        return hasattr(this,name)

    def Set(this, name, value):
        setattr(this, name, value)

    def Get(this, name):
        return getattr(name)