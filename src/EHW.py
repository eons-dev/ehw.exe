import os
import logging
import eons as e
import jsonpickle

from .Exceptions import *
from .State import State

class EHW(e.Executor):

    def __init__(this):
        super().__init__(name="eons hardware", descriptionStr="Modular framework for controlling hardware devices.")

        this.RegisterDirectory("ehw")

        this.state = State()

    #Override of eons.Executor method. See that class for details
    def RegisterAllClasses(this):
        super().RegisterAllClasses()

    #Override of eons.Executor method. See that class for details
    def AddArgs(this):
        super().AddArgs()
        this.argparser.add_argument('-c', '--config', type = str, metavar = 'config.json', help = 'configuration file.', default = None, dest = 'config')
        this.argparser.add_argument('-d','--device', type = str, action='append', nargs='*', metavar = 'status_led', help = 'enables use of the specified device and assumes the device is properly connected.', dest = 'devices')
        this.argparser.add_argument('-r','--routines', type = str, action='append', nargs='*', metavar = 'blink_led', help = 'will execute the given routine.', dest = 'routines')


    #Override of eons.Executor method. See that class for details
    def ParseArgs(this):
        super().ParseArgs()

        # These are only sets while being populated. They will become lists at the end of this method.
        this.devices = set()
        this.routines = set()

        if (os.path.isfile(this.args.config)):
            config = jsonpickle.decode(open(this.args.config, 'r').read())
            for key in config:
                if (key == "devices"):
                    [this.devices.add(d) for d in config[key]]
                elif (key == "routines"):
                    [this.routines.add(r) for r in config[key]]
                else:
                    this.state.Set(key, config[key])

        if (this.args.devices is not None):
            [[this.devices.add(str(d)) for d in l] for l in this.args.devices]
        this.devices = list(this.devices)

        if (this.args.routines is not None):
            [[this.routines.add(str(r)) for r in l] for l in this.args.routines]
        this.routines = list(this.routines)

        for arg, val in this.extraArgs.items():
            this.state.Set(arg, val)

    #Override of eons.Executor method. See that class for details
    def UserFunction(this, **kwargs):
        super().UserFunction(**kwargs)
        for d in this.devices:
            this.StartHW(d, "dev")
        for r in this.routines:
            this.StartHW(r, "routine")

    #Run some HWBase.
    def StartHW(this, hwName, type):
        hw = this.GetRegistered(hwName, type)
        logging.debug(f"Starting {hw}")
        hw(ehw=this)
