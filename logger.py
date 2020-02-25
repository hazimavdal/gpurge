import time

DEBUG_LEVEL = 0
INFO_LEVEL = 1
WARNING_LEVEL = 2
ERROR_LEVEL = 3
FATAL_LEVEL = 4


def level_str(level):
    if level == 0:
        return "DEBUG"
    if level == 1:
        return "INFO"
    if level == 2:
        return "WARN"
    if level == 3:
        return "ERROR"
    if level == 4:
        return "FATAL"


class Logger:
    def __init__(self, verbosity):
        self.lines = []
        self.verbosity = verbosity

    def __log(self, level, msg, *args):
        for i, arg in enumerate(*args):
            msg = msg.replace(f'%{str(i)}', str(arg))

        if level >= self.verbosity:
            print(msg)

        stamp = time.strftime("%Y/%m/%d\t%H:%M:%S")
        self.lines.append(f'<{level_str(level)}>\t{stamp}: {msg}')

    def infof(self, msg, *args):
        self.__log(INFO_LEVEL, msg, args)

    def errorf(self, msg, *args):
        self.__log(ERROR_LEVEL, msg, args)

    def save(self, filename):
        with open(filename, "w+") as f:
            lines = [l + '\n' for l in self.lines]
            f.writelines(lines)
