# @Author: GeorgeRaven <raven>
# @Date:   2020-02-22T00:09:49+00:00
# @Last modified by:   raven
# @Last modified time: 2020-02-28T12:40:32+00:00
# @License: please see LICENSE file in project root

import logging
import datetime


class Logger(object):
    """Python logger utility.

    This logger utility helps output in desired manner in slightly more
    configurable manner than simple print().

    40-DEBUG: Detailed information, typically of interest only when diagnosing
    problems.

    30-INFO: Confirmation that things are working as expected.

    20-WARNING: An indication that something unexpected happened, or indicative
    of some problem in the near future (e.g. ‘disk space low’). The software
    is still working as expected.

    10-ERROR: Due to a more serious problem, the software has not been able to
    perform some function.

    0-CRITICAL: A serious error, indicating that the program itself may be
    unable to continue running.

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
            "log_level": 30,                # setting default log level to INFO
            "log_min_level": 40,            # setting default minim to DEBUG
            "log_delimiter": " ",           # default to act just like print
            "log_file": "nemesyst.log",     # default log file to use
            "log_filemode": "w",            # append to file not overwrite
            "log_format": "%(asctime)s %(levelname)s:%(message)s",
            "log_date_format": "%Y-%m-%dT%H:%M:%S",
            "log_debug": 40,
            "log_info": 30,
            "log_warning": 20,
            "log_error": 10,
            "log_critical": 0,
        }
        self.args = self._mergeDicts(defaults, args)
        logging.basicConfig(filename=self.args["log_file"],
                            filemode=self.args["log_filemode"],
                            level=50-self.args["log_level"],
                            format=self.args["log_format"],
                            datefmt=self.args["log_date_format"])
        logging.info("logger is now online")

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

    def __call__(self, *text, log_min_level=None, log_delimiter=None):
        """Magic function used for drop-in-replacement of print from object"""
        # # logging usage of compatibility function
        # self.log("compatibility function usage",
        #          log_min_level=self.args["log_debug"])
        # redirecting compatibility function
        self.log(*text, log_min_level=log_min_level,
                 log_delimiter=log_delimiter)

    def log(self, *text, log_min_level=None,
            log_delimiter=None):
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
        log_delimiter = str(log_delimiter) if log_delimiter is not None else \
            self.args["log_delimiter"]
        log_min_level = log_min_level if log_min_level is not None else \
            self.args["log_min_level"]
        message = log_delimiter.join(map(str, text))

        if(log_min_level < self.args["log_error"]):
            logging.critical(message)
        elif(log_min_level < self.args["log_warning"]) and \
                (log_min_level >= self.args["log_error"]):
            logging.error(message)
        elif(log_min_level < self.args["log_info"]) and \
                (log_min_level >= self.args["log_warning"]):
            logging.warning(message)
        elif(log_min_level < self.args["log_debug"]) and \
                (log_min_level >= self.args["log_info"]):
            logging.info(message)
        elif(log_min_level >= self.args["log_debug"]):
            logging.debug(message)

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


def _logger_unit_test():

    pylog = Logger({
        "log_file": "log_test.log",
        "log_filemode": "w",  # overwrite previous log
        # "log_level": 20,
        "log_format": "%(levelname)s:%(message)s",
        "log_level": 9000,
        "log_min_level": 30,
    })
    # checking magic (__call__) function
    pylog("log", "compatibility", log_delimiter="-",
          log_min_level=0)
    # checking normal usage
    pylog.log("log", log_delimiter="-", log_min_level=40)
    pylog("log", "append", log_delimiter="-", log_min_level=10)
    pylog = Logger({
        "log_file": "./log_test.log",
        "log_filemode": "a",  # append to previous log
        "log_level": 0,
        "log_min_level": 20,
        "log_delimiter": "-",
    })
    # checking python logging still behaves  the same, and ignores all
    # subsequent instances of itself which means if we create a second Logger
    # it will act exactly like the first, and most options will be ignored.
    pylog("second-pylog", "ignore")  # note delim still used from second logger

    with open('./log_test.log', 'r') as content_file:
        content = content_file.read()

    # expected = "INFO:logger is now online\nCRITICAL:log-compatibility\nCRITICAL:log\nCRITICAL:log-append\nINFO:logger is now online\nINFO:second-pylog-ignore"
    # expected = expected.splitlines()
    content = content.splitlines()
    expected = ['INFO:logger is now online',
                'CRITICAL:log-compatibility',
                'DEBUG:log',
                'ERROR:log-append',
                'INFO:logger is now online',
                'WARNING:second-pylog-ignore']
    if(content == expected):
        pylog("success")
    else:
        raise ArithmeticError("Unit test failed, outputs not the same")


if(__name__ == "__main__"):
    _logger_unit_test()
