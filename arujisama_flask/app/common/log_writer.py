import datetime
import os
from pathlib import Path


def write_log(log="", ip="not known", id="", func="not known", memo=""):
    current_time = datetime.datetime.now()

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    directory = os.path.join(BASE_DIR, 'log')
    if not (os.path.isdir(directory)):
        Path(directory).mkdir(parents=True, exist_ok=True)

    target_file = os.path.join(directory,"{0}.log".format(current_time.strftime("%Y-%m-%d")))
    timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

    log_message = "{0}) {1}\nip) {2}\nid) {3}\nfunc) {4}\nmemo) {5}\n\n".format(timestamp, log, ip, id, func, memo)

    try:
        with open(target_file, mode="a", encoding="utf-8") as fp:
            fp.write(log_message)

    except FileNotFoundError as e:
        with open(target_file, mode="w", encoding="utf-8") as fp:
            fp.write(log_message)
