import argparse
import re
import os
import json
from collections import defaultdict
from os import listdir
from os.path import join, isfile


def main(file):
    dict_ip = {"TOTAL": 0, "METHOD": {"GET": 0, "POST": 0, "PUT": 0, "DELETE": 0, "HEAD": 0, "OPTIONS": 0}}
    dict_ip_requests = defaultdict(lambda: {"REQUESTS_COUNT": 0})
    list_ip_duration = []

    with open(file) as logfile:

        for line in logfile:
            method = re.search(r"\] \"(POST|GET|PUT|DELETE|HEAD|OPTIONS)", line)
            ip = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line).group()
            duration = int(line.split()[-1])
            date = re.search(r"\[\d.*?\]", line)
            url = re.search(r"\"http.*?\"", line)

            dict_ip["TOTAL"] += 1

            if method is not None:

                dict_ip["METHOD"][method.group(1)] += 1
                dict_ip_requests[ip]["REQUESTS_COUNT"] += 1

                dict_t = {"ip": ip,
                          "date": date.group(0).split(" ")[0].lstrip("["),
                          "method": method.group(1),
                          "url": "-",
                          "duration": duration
                          }

                if url is not None:
                    dict_t["url"] = url.group(0).strip("\"")

                list_ip_duration.append(dict_t)

        top_ips = dict(sorted(dict_ip_requests.items(), key=lambda x: x[1]["REQUESTS_COUNT"], reverse=True)[0:3])
        top_slw_req = sorted(list_ip_duration, key=lambda x: x["duration"], reverse=True)[0:3]

        result = {"top_ips": top_ips,
                  "top_longest": top_slw_req,
                  "total_stat": dict_ip["METHOD"],
                  "total_requests": dict_ip["TOTAL"],
                  }

        with open(f"{file}.json", "w", encoding="utf-8") as f:
            result = json.dumps(result, indent=4)
            f.write(result)
            print(f"\n===== RESULT STATS ON FILE: {file} =====\n {result}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", dest="path", help="Path to logfile")
    args = parser.parse_args()

    log_files = []
    if isfile(args.path):
        log_files.append(args.path)
    elif os.path.isdir(args.path):
        for file in listdir(args.path):
            if file.endswith(".log"):
                log_files.append(join(args.path, file))
    else:
        print("ERROR: Incorrect path to log file or directory")

    for f in log_files:
        print(f'Processing file {f}...')
        main(f)
