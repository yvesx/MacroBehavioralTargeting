#!/home/download/python2.7/bin/python2.7
import time
import conf

config = conf.config()


def write_log(string, level):
    if level == 1:
        levelmsg = "Critical"
        log_filepath = config.log_critical
    elif level == 2:
        levelmsg = "Message"
        log_filepath = config.log_message
    elif level == 3:
        levelmsg = "Debug"
        log_filepath = config.log_debug

    timestr = time.strftime('%Y-%m-%d %X', time.localtime(time.time()))
    error_msg = "[%s] [%s] %s" % (timestr, levelmsg, string)

    if config.debug:
        print error_msg

    try:
        logfile = open(log_filepath, "a")
        logfile.write(error_msg.__str__() + '\n')
        logfile.close()

    except Exception:
        pass
