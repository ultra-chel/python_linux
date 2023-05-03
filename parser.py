import argparse
import re
import json
import os
from collections import defaultdict
from os import listdir
from os.path import join, isfile


def main(file):
    dict_ip = defaultdict(
        lambda: {"GET": 0, "POST": 0, "PUT": 0, "DELETE": 0, "HEAD": 0}
    )

    ips = []

    with open(file) as f:
        idx = 0
        for line in f:
            if idx > 99:
                break

            # 109.169.248.247 - - [12/Dec/2015:18:25:11 +0100] "GET /administrator/ HTTP/1.1" 200 4263
            # "-" "Mozilla/5.0 (Windows NT 6.0; rv:34.0) Gecko/20100101 Firefox/34.0" 7269
            ip_match = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
            if ip_match is not None:
                ip = ip_match.group()
                ips.append(ip)
                method = re.search(r"\] \"(POST|GET|PUT|DELETE|HEAD)", line)
                if method is not None:
                    dict_ip[ip][method.group(1)] += 1
                    idx += 1
    print(ips)
    unique_ips = set(ips)
    print(unique_ips)
    # for ip in unique_ips:
    result = {i: ips.count(i) for i in ips}
    print(result)

    # print(json.dumps(dict_ip, indent=4))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", dest="path", help="Path to logfile")
    args = parser.parse_args()

    log_files = []
    if isfile(args.path):
        log_files.append(args.path)
    else:
        for file in listdir(args.path):
            log_files.append(join(args.path, file))

    for f in log_files:
        print(f'Processing file {f}...')
        main(f)
