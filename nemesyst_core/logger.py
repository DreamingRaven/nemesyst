
class Logger(object):

    def __init__(self, args=None):
        args = args if args is not None else dict()
        defaults = {
            "debug": True,
            "delimiter": " ",
        }
        self.args = self._mergeDicts(defaults, args)

    def _mergeDicts(self, *dicts):
        """Given multiple dictionaries, merge together in order."""
        result = {}
        for dictionary in dicts:
            result.update(dictionary)  # merge each dictionary in order
        return result

    def log(self, *printables, debug=None, delimiter=None):
        delimiter = str(delimiter) if delimiter is not None else ""
        if(debug):
            print(delimiter.join(map(str, printables)))
