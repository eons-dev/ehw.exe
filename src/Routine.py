import os
import logging
import eons
from .Exceptions import *
from .HWBase import HWBase

class Routine(HWBase):
    def __init__(this, name=eons.INVALID_NAME()):
        super(HWBase).__init__(name)

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
