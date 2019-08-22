#!/bin/bash
### BEGIN INIT INFO
# Provides:          smartcan
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start daemon at boot time
# Description:       Enable services provided by daemon.
### END INIT INFO

PIDFILE="/var/run/smartcan.pid"
SMARTCAN_HOME="/home/pi/smartcan"
PYTHON_FILE="${SMARTCAN_HOME}/bin/smartcan.py"
DAEMON="smartcan"
PYTHON=${SMARTCAN_HOME}/venv/bin/python

. /lib/lsb/init-functions

function start() {
    log_daemon_msg "Starting Smartcan..." "smartcan"
    start_daemon ${PYTHON_FILE}
    log_end_msg $?
}

function stop() {
    log_daemon_msg "Stopping Smartcan command" "smartcan"
    killproc -p ${PIDFILE}
    RETVAL=$?
    [[ ${RETVAL} -eq 0 ]] && [[ -e "$PIDFILE" ]] && rm -f ${PIDFILE}
    log_end_msg ${RETVAL}
}

function restart() {
    log_daemon_msg "Restarting Smartcan..." "smartcan"
    $0 stop
    $0 start
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    status)
        status_of_proc -p ${PIDFILE} $DAEMON "smartcan" && exit 0 || exit $?
        ;;
    *)
        echo "Usage: $0 {start|stop|status|restart}"
        ;;
esac

exit 0