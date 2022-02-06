import os
import logging
import eons as e
from .Exceptions import *
from .HWBase import HWBase

class Device(HWBase):
    def __init__(this, name=e.INVALID_NAME()):
        super(HWBase).__init__(name)

        # See HWBase for docs
        this.RunInThread = True
        this.requiredKWArgs = []
        this.optionalKWArgs = {}

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
