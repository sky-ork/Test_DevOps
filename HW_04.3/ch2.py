#!/usr/bin/env python3
import socket
import subprocess
import sys
import json
import yaml


# The function returns the URL availability execution code.
def check_url(url):
    return subprocess.run(['curl', '-Is', url],
                          stdout=subprocess.DEVNULL).returncode


# The function returns an array of the dictionary type in the form
# {<URL>: <IP>,....}. Argument: an array of the URL list type.
def get_url_ip(url_dict):
    url_ip = {}
    len_url_dict = len(url_dict)
    for count in range(len_url_dict):
        # Checking the existence of a URL
        if check_url(url_dict[count]) == 0:
            # Checking the availability of an existing URL and
            # and form an array
            r = 0
            while r == 0:
                try:
                    url_ip[str(url_dict[count])] = socket.gethostbyname(str(url_dict[count]))
                    r = 1
                except Exception:
                    r = 0
    return dict(url_ip)


# The function converts an array of the dictionary type to an array
# of the sheet type with elements-arrays of the dictionary type.
# Next, the function writes the array to JSON and YAML files.
def out_service(in_services_dict, file_json, file_yaml):
    services_list = list(in_services_dict.items())
    services_dict = [dict([i]) for i in services_list]
    with open(str(file_json), "w") as js:
        js.write(json.dumps(services_dict, indent=2))
        js.close()
    with open(str(file_yaml), "w") as ym:
        ym.write(yaml.dump(services_dict, indent=2,
                           explicit_start=True,
                           sort_keys=False))
        ym.close()


cnt_ask = 0
print('-' * 40)
while 1 == 1:
    if cnt_ask == 0:
        # We get and output the first result without comparing the IP
        url_ip_dict = get_url_ip(sys.argv)
        for item_key in url_ip_dict.keys():
            result = item_key + " - " + url_ip_dict[item_key]
            print(result)
        url_ip_dict_coll = url_ip_dict
        out_service(url_ip_dict, "ch2_services.json", "ch2_services.yaml")
        cnt_ask = 1
    else:
        # We get and output the result after comparing the IP
        cnt_r = 0
        while cnt_r == 0:
            try:
                url_ip_dict = get_url_ip(sys.argv)
                cnt_r = 1
            except Exception:
                cnt_r = 0
        for item_key in url_ip_dict.keys():
            if url_ip_dict[item_key] == url_ip_dict_coll[item_key]:
                result = item_key + " - " + url_ip_dict[item_key]
                print(result)
            else:
                result = "[ERROR] " + item_key + " IP mismatch: " \
                         + url_ip_dict_coll[item_key] + " --> " \
                         + url_ip_dict[item_key]
                print(result)
                url_ip_dict_coll = url_ip_dict
                out_service(url_ip_dict, "ch2_services.json", "ch2_services.yaml")
    print('-' * 40)
