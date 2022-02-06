# For validating args
class ArgumentNotProvided(Exception): pass

# For initialization
class InitializationError(Exception): pass

# All Device errors
class DevicesError(Exception): pass

# Exception used for miscellaneous Device errors.
class OtherBuildError(DevicesError): pass

# All Routine errors
class RoutineError(Exception): pass

# Exception used for miscellaneous Routine errors.
class OtherRoutineError(RoutineError): pass
