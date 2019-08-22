#!/home/pi/smartcan/venv/bin/python
import argparse
import sys
import daemon
from daemon import pidfile

sys.path.insert(1, '/home/pi/smartcan/')

import embedded


def run():
    embedded_runtime = embedded.runtime()
    while True:
        embedded_runtime.run()


def start_daemon(pidf):
    with daemon.DaemonContext(
        working_directory='/home/pi/smartcan',
        umask=0o002,
        pidfile=pidfile.TimeoutPIDLockFile(pidf),
    ) as context:
        run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Smartcan daemong")
    parser.add_argument('-p', '--pid-file', default='/var/run/smartcan.pid')

    args = parser.parse_args()

    start_daemon(pidf=args.pid_file)

