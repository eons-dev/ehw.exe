import os
import logging
import eons as e
import threading
from subprocess import Popen, PIPE, STDOUT
from .Exceptions import *

class HWBase(e.UserFunctor):
    def __init__(this, name=e.INVALID_NAME(), state=None):
        super(e.UserFunctor).__init__(name)

        # See State.py
        this.state = state

        # If you would like to loop Run() in a separate thread, set this to true, otherwise, set to false
        this.RunInThread = True

        # For required args, simply list what is needed. They will be provided as member variables or *this will not be run.
        this.requiredKWArgs = []

        # For optional args, supply the arg name as well as a default value.
        this.optionalKWArgs = {}

    # Set the state of this.
    def UseState(this, state):
        this.state = state

    # Do stuff!
    # Override this or die.
    def Run(this):
        pass

    # Hook for any pre-run configuration.
    # RETURN whether or not to continue running.
    def Initialize(this):
        return True

    # Hook for any post-run configuration.
    # RETURN whether or not Cleanup was successful.
    def Cleanup(this):
        return True

    # Will try to get a value for the given varName from:
    #    first: this
    #    second: the state
    #    third: the environment
    # RETURNS the value of the given variable or None.
    def FetchVar(this, varName, prepend=""):
        logging.debug(f"{prepend}{this.name} looking to fetch {varName}...")

        if (hasattr(this, varName)):
            logging.debug(f"...{this.name} got {varName} from myself!")
            return getattr(this, varName)

        if (this.state.Has(varName)):
            stateVar = this.state.Get(varName)
            if (stateVar is not None):
                logging.debug(f"...{this.name} got {varName} from state")
                return stateVar

        envVar = os.getenv(varName)
        if (envVar is not None):
            logging.debug(f"...{this.name} got {varName} from environment")
            return envVar

        return None


    # Override of eons.UserFunctor method. See that class for details.
    def ValidateArgs(this):
        for rkw in this.requiredKWArgs:
            if (hasattr(this, rkw)):
                continue

            fetched = this.FetchVar(rkw)
            if (fetched is not None):
                setattr(this, rkw, fetched)
                continue

            # Nope. Failed.
            errStr = f"{rkw} required but not found."
            logging.error(errStr)
            raise ArgumentNotProvided(errStr)

        for okw, default in this.optionalKWArgs.items():
            if (hasattr(this, okw)):
                continue

            fetched = this.FetchVar(okw)
            if (fetched is not None):
                setattr(this, okw, fetched)
                continue

            logging.debug(f"Failed to fetch {okw}. Using default value: {default}")
            setattr(this, okw, default)

    # Override of eons.Functor method. See that class for details
    def UserFunction(this, ehw):

        this.UseState(ehw.state)
        this.ValidateArgs()

        if (not this.Initialize()):
            errStr = f"Failed to initialize {this.name}"
            raise InitializationError(errStr)

        if (not this.Cleanup()):
            logging.error(f"Failed to clean up {this.name}")

    # Run whatever.
    # DANGEROUS!!!!!
    # TODO: check return value and raise exceptions?
    # per https://stackoverflow.com/questions/803265/getting-realtime-output-using-subprocess
    def RunCommand(this, command):
        p = Popen(command, stdout=PIPE, stderr=STDOUT, shell=True)
        while True:
            line = p.stdout.readline()
            if (not line):
                break
            print(line.decode('utf8')[:-1])  # [:-1] to strip excessive new lines.

