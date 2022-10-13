import eons

# For validating args
class ArgumentNotProvided(Exception, metaclass=eons.ActualType): pass

# For initialization
class InitializationError(Exception, metaclass=eons.ActualType): pass

# All Device errors
class DevicesError(Exception, metaclass=eons.ActualType): pass

# Exception used for miscellaneous Device errors.
class OtherBuildError(DevicesError, metaclass=eons.ActualType): pass

# All Routine errors
class RoutineError(Exception, metaclass=eons.ActualType): pass

# Exception used for miscellaneous Routine errors.
class OtherRoutineError(RoutineError, metaclass=eons.ActualType): pass
