
class Logger(object):
    """Python logger utility.

    This logger utility helps output in desired manner in slightly more
    configurable manner than simple print().

    :param args: Dictionary of overides.
    :type args: dictionary
    :example: Logger().log("Hello, world.")
    :example: Logger({"log_level": 5,}).log("Hello, world.")
    """

    def __init__(self, args=None):
        """Init class with defaults.

        Optionally accepts dictionary of default overides.
        :param args: Dictionary of overides.
        :type args: dictionary
        """
        args = args if args is not None else dict()
        defaults = {
            "log_level": 0,
            "min_level": 0,
            "delimiter": " ",
        }
        self.args = self._mergeDicts(defaults, args)

    __init__.__annotations__ = {"args": dict, "return": None}

    def _mergeDicts(self, *dicts):
        """Given multiple dictionaries, merge together in order.
        :param args: Dictionary of overides.
        :type args: dict
        """
        result = {}
        for dictionary in dicts:
            result.update(dictionary)  # merge each dictionary in order
        return result

    _mergeDicts.__annotations__ = {"dicts": dict, "return": dict}

    def log(self, *text, log_level=None, min_level=None, delimiter=None):
        """Log desired output to teminal.

        :param \*text: The desired text to log.
        :param log_level: Current log level/ log level override.
        :param min_level: Minimum required log level to display text.
        :param delimiter: String to place in between positional \*text.
        :type log_level: int
        :type min_level: int
        :type delimiter: str
        :return: None
        :example: Logger({log_level:2}).log("Hello, world.", min_level=0)
        :example: Logger().log("Hello", "world.", delimiter=", ")
        """
        delimiter = str(delimiter) if delimiter is not None else ""
        log_level = log_level if log_level is not None else \
            self.args["log_level"]
        min_level = min_level if min_level is not None else \
            self.args["min_level"]

        if(log_level >= min_level):
            print(delimiter.join(map(str, args)))

    log.__annotations__ = {"*text": tuple, "log_level": int, "min_level": int,
                           "delimiter": str, "return": None}

    def __setitem__(self, key, value):
        """Set a single arg or state by, (key, value)."""
        self.args[key] = value

    __setitem__.__annotations__ = {"key": str, "value": any, "return": None}

    def __getitem__(self, key):
        """Get a single arg or state by, (key, value)."""
        try:
            return self.args[key]
        except KeyError:
            return None  # does not exist is the same as None, gracefull catch

    __getitem__.__annotations__ = {"key": str, "return": any}

    def __delitem__(self, key):
        """Delete a single arg or state by, (key, value)."""
        try:
            del self.args[key]
        except KeyError:
            pass  # job is not done but equivalent outcomes so will not error

    __delitem__.__annotations__ = {"key": str, "return": None}
