import os
import logging
import eons
import jsonpickle

from .Exceptions import *
from .State import State

class EHW(eons.Executor):

    def __init__(this):
        super().__init__(name="eons hardware", descriptionStr="Modular framework for controlling hardware devices.")

        this.defaultPrefix = "hw"

        this.state = State()

        this.requiredKWArgs.append('routines')

    #Override of eons.Executor method. See that class for details
    def Function(this):
        super().Function()
        for r in this.routines:
            this.StartRoutine(r)

    #Run some Routine.
    def StartRoutine(this, routine, *args, **kwargs):
        return this.Execute(routine, *args, **kwargs)
