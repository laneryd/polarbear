# Standard
import json
import os
import shlex
import subprocess
import sys
import urllib.request
from pathlib import Path

# Local
import configparser

HEARTBEAT_SECONDS = 5


class Palette:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    ENDC = "\033[0m"

    def underline(self, msg):
        return f"{self.UNDERLINE}{msg}{self.ENDC}"

    def bold(self, msg):
        return f"{self.BOLD}{msg}{self.ENDC}"

    def green(self, msg):
        return f"{self.OKGREEN}{msg}{self.ENDC}"

    def cyan(self, msg):
        return f"{self.OKCYAN}{msg}{self.ENDC}"

    def blue(self, msg):
        return f"{self.OKBLUE}{msg}{self.ENDC}"


palette = Palette()


def Print(msg):
    return ("Print", msg)


def CreateFile(path, lines):
    return ("CreateFile", (path, lines))


def StartProcess(cmd_line):
    return ("StartProcess", cmd_line)


def SetHeartbeatUrl(url):
    return ("SetHeartbeatUrl", url)


def parse(args, user, read_config):

    if len(args) == 0:
        return [Print("Usage: python3 workon.py <projname>")]

    projname = args[0]
    inifile = f"{projname}.ini"
    cfg = read_config(inifile)

    if "--create" in args:
        args.remove("--create")

        if len(args) == 0:
            return [Print("Create what? --create by itself makes no sense...")]

        if cfg:
            return [Print(f"Cannot create {inifile}: file already exists!")]

        return [
            CreateFile(
                inifile,
                [
                    f"[workon]",
                    f"cmdline=goland '/path/to the/project'",
                    f"server=http://212.47.253.51:8335",
                    f"user={user}",
                ],
            ),
            Print(f"'{inifile}' created."),
            Print(f"Open it with your favorite text editor then type"),
            Print(f"   python3 workon.py {projname}"),
            Print(f"again to begin samkoding!"),
        ]

    if cfg:
        cmdline = cfg["cmdline"]
        url = f'{cfg["server"]}/{cfg["user"]}/workon/{projname}'
        return [
            Print(f"Working on {projname}. Command line: {cmdline}"),
            SetHeartbeatUrl(url),
            StartProcess(shlex.split(cmdline)),
        ]
    else:
        return [
            Print(
                f"Did not find '{inifile}'. Re-run with flag --create to create a default!"
            )
        ]


def run_cmd_line(cmd_line, heartbeat_url):

    process = subprocess.Popen(cmd_line)
    while True:
        http_get(heartbeat_url)
        try:
            process.wait(HEARTBEAT_SECONDS)
            break
        except subprocess.TimeoutExpired:
            pass


def http_get(url):
    with urllib.request.urlopen(url) as response:
        html = response.read()
        state = json.loads(html)
        clear()
        print(palette.blue(palette.underline("** Status **")))
        for (user, proj) in state:
            statusline = (
                palette.bold(user)
                + palette.green(" is working on ")
                + palette.cyan(palette.bold(proj))
            )
            print(statusline)


def clear():
    cmd = "cls" if os.name == "nt" else "clear"
    os.system("clear")


def read_config(path):
    try:
        config = configparser.ConfigParser()
        config.read(path)
        return config["workon"]
    except:
        return None


if __name__ == "__main__":
    effects = parse(args=sys.argv[1:], user="olof", read_config=read_config)
    for effect in effects:
        name, args = effect
        if name == "Print":
            print(args)
        if name == "CreateFile":
            path, lines = args
            Path(path).write_text("\n".join(lines) + "\n")
        if name == "StartProcess":
            run_cmd_line(args, url)
        if name == "SetHeartbeatUrl":
            url = args
            print("Setting heartbeat-url to " + url)