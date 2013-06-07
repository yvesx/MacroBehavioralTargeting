#!/bin/bash
#
# Start/Stop any shell script
#
# chkconfig: 345 95 65
# description: Scalable Computing Worker
# processname: worker.sh
#

# ENVIRONMENT

# Name for the service, used in logging
NAME=posttagger

# Name of the user to be used to execute the service
SCRIPT_USER=download

# In which directory is the shell script that this service will execute
DAEMON_SCRIPTS_DIR=/home/$SCRIPT_USER/post_feature_extract

# How can the script be identified if it appears in a 'ps' command via grep?
#  Examples to use are 'java', 'python' etc.
DAEMON_PROCESS_TYPE=java

set_port() {
    # Construct the command the will cd into the right directory, and invoke the script
    DAEMON_COMMAND="cd $DAEMON_SCRIPTS_DIR; ./runTagger.sh $1"

    # Where to write the log file?
    DAEMON_SVC_LOG_FILE=/tmp/$NAME-$1.log

    # Where to write the process identifier - this is used to track if the service is already running
    PID_FILE=/tmp/$NAME-$1.pid
}

# Load system specific optional arguments
# Create and populate this file with machine specific settings
#if [ -f /etc/sysconfig/$NAME ]; then
    #. /etc/sysconfig/$NAME
#fi

# Is the service already running? If so, capture the process id
getPID() {
    if [ -f $PID_FILE ]; then
        PID=`cat $PID_FILE`
    else
        PID=""
    fi
}

# SERVICE ENTRY POINTS (START/STOP)
start() {
    if [ "${PID}" != "" ]; then
        # Check to see if the /proc dir for this process exists
        if [ -a /proc/${PID} ]; then
            # check to make sure this is likely the running service
            ps aux | grep ${PID} | grep $DAEMON_PROCESS_TYPE >> /dev/null
            # If it is a process of the right type assume that it is daemon and just exit
            if [ "$?" = "0" ]; then
                echo "On " `hostname`", $NAME @ Port $1 is running"
                exit 1
            fi
        fi
    fi
    echo "On " `hostname`", Starting $NAME @ Port $1 ... "   
    /bin/sh -c "$DAEMON_COMMAND > $DAEMON_SVC_LOG_FILE 2>&1" &
    sleep 1
    exit 0
}

stop() {
    echo "On " `hostname`", Stopping $NAME @ Port $1 ... "
    if [ "${PID}" != "" ]; then
        echo -n "killing " $PID
        kill -KILL ${PID}
        for i in {1..30}
        do
            if [ -n "`ps aux | grep $DAEMON_PROCESS_TYPE | grep $NAME `" ]; then
                sleep 1 # Still running, wait a second.
                echo -n .
            else
                # stopped
                rm -f $PID_FILE
                echo
                exit 0
            fi
        done
    else
        echo "On " `hostname`", $NAME @ Port $1 is not running"
        exit 1
    fi
    echo "Failed to stop in 30 seconds."
    kill -KILL ${PID} # Request a thread dump so we can diagnose a hung shutdown
    exit 1
}

restart() {
    echo "On " `hostname`", Stopping $NAME @ Port $1 ... "
    if [ "${PID}" != "" ]; then
        echo -n "killing " $PID
        kill -KILL ${PID}
        for i in {1..30}
        do
            if [ -n "`ps aux | grep $DAEMON_PROCESS_TYPE | grep $NAME `" ]; then
                sleep 1 # Still running, wait a second.
                echo -n .
            else
                # stopped
                rm -f $PID_FILE
                echo
                break
            fi
        done
    fi

    javaPID=`pgrep -f "java -Xbootclasspath/a:./ark-tweet-nlp"`

    if [ "$javaPID" != "" ]
    then
        kill -KILL $javaPID
    fi

    echo "On " `hostname`", Starting $NAME @ Port $1 ... "   
    /bin/sh -c "$DAEMON_COMMAND > $DAEMON_SVC_LOG_FILE 2>&1" &
    sleep 1
    exit 0
}

if [ $2 ]
then
    set_port $2
    getPID
    case "$1" in
        start)
            start $2
            ;;
        stop)
            stop $2
            ;;
        restart)
            restart $2
            ;;
        *)
            echo $"Usage: $0 {start|stop|restart} {port number}"
            exit 1
    esac
else
    echo $"Usage: $0 {start|stop|restart} {port number}"
    exit 1
fi
