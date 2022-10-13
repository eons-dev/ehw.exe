import os
import logging
import eons
import threading
from subprocess import Popen, PIPE, STDOUT
from threading import Thread
from .Exceptions import *

class HWBase(eons.StandardFunctor):
    def __init__(this, name=eons.INVALID_NAME(), state=None):
        super().__init__(name)

        # See State.py
        this.state = state

        # For optional args, supply the arg name as well as a default value.
        this.optionalKWArgs['shouldRunInThread'] = True

        this.fetchFrom = [
            'this',
            'args',
            'precursor',
            'state'
            'environment',
        ]

    # Set the state of this.
    def UseState(this, state):
        this.state = state

    # Do stuff!
    # Override this or die.
    def Run(this):
        pass

    # Hook for any pre-run configuration.
    # RETURN whether or not to continue running.
    def InitializeHardware(this):
        return True

    # Hook for any post-run configuration.
    # RETURN whether or not Cleanup was successful.
    def Cleanup(this):
        return True

    def ParseInitialArgs(this):
        super().ParseInitialArgs()
        this.UseState(this.executor.state)

    # Override of eons.Functor method. See that class for details
    def Function(this):        

        if (not this.InitializeHardware()):
            errStr = f"Failed to initialize {this.name}"
            raise InitializationError(errStr)

        if (this.shouldRunInThread):
            thread = Thread(target=this.Run).start()
            thread.join()
        else:
            this.Run()

        if (not this.Cleanup()):
            logging.error(f"Failed to clean up {this.name}")


    def fetch_location_state(this, varName, default, fetchFrom):
        if (not this.state.Has(varName)):
            return default, False
        stateVar = this.state.Get(varName)
        if (stateVar is not None):
            logging.debug(f"...{this.name} got {varName} from state")
            return stateVar, True
        return default, False
