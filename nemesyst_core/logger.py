
class Logger(object):
    """Python logger utility.

    This logger utility helps output in desired manner in slightly more
    configurable manner than simple print().

    :param args: Dictionary of overides.
    :type args: dictionary
    :example: Logger().log("Hello, world.")
    :example: Logger({"debug": True,}).log("Hello, world.")
    """

    def __init__(self, args=None):
        """Init class with defaults.

        Optionally accepts dictionary of default overides.
        :param args: Dictionary of overides.
        :type args: dictionary
        """
        args = args if args is not None else dict()
        defaults = {
            "debug": True,
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

    def log(self, *printables, debug=None, delimiter=None):
        """Log desired output to teminal."""
        delimiter = str(delimiter) if delimiter is not None else ""
        debug = debug if debug is not None else self.args["debug"]
        if(debug):
            print(delimiter.join(map(str, printables)))
