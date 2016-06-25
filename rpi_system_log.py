#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import os
import socket
import time
import logging.handlers
import psutil

host = socket.gethostname()
path = "/home/pi/RPI-System-Log/logs/rpi_system_data_{}.log".format(host)
LOG_FILENAME = path

# Set up a specific logger with our desired output level
system_logger = logging.getLogger('SystemLogger')
system_logger.setLevel(logging.INFO)


# Add the log message handler to the logger with log rotate
handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=10485760, backupCount=100,)
# create a custom logger
system_logger.addHandler(handler)

while True:
    # Return CPU temperature as a character string
    def get_cpu_temperature():
        res = os.popen('vcgencmd measure_temp').readline()
        return res.replace("temp=", "").replace("'C\n", "")

    # Return RAM information (unit=kb) in a list
    # Index 0: total RAM
    # Index 1: used RAM
    # Index 2: free RAM
    def get_ram_info():
        p = os.popen('free')
        i = 0
        while 1:
            i += 1
            line = p.readline()
            if i == 2:
                return line.split()[1:4]

    # Return % of CPU used by user as a character string
    def get_cpu_use():
        return psutil.cpu_percent(interval=1)

    # Return information about disk space as a list (unit included)
    # Index 0: total disk space
    # Index 1: used disk space
    # Index 2: remaining disk space
    # Index 3: percentage of disk used
    def get_disk_space():
        p = os.popen("df -h /")
        i = 0
        while 1:
            i += 1
            line = p.readline()
            if i == 2:
                return line.split()[1:5]

    def get_timestamp():
        current_time = datetime.datetime.now()
        return current_time.isoformat()

    host = socket.gethostname()
    # CPU information
    cpu_temp = get_cpu_temperature()
    cpu_usage = get_cpu_use()

    # RAM information
    # Output is in kb, here I convert it in Mb for readability
    ram_stats = get_ram_info()
    ram_total = round(int(ram_stats[0]) / 1000, 1)
    ram_used = round(int(ram_stats[1]) / 1000, 1)
    ram_free = round(int(ram_stats[2]) / 1000, 1)

    # Disk information
    disk_stats = get_disk_space()
    disk_total = str(disk_stats[0]).replace("G", "")
    disk_used = str(disk_stats[1]).replace("G", "")
    disk_free = str(disk_stats[2]).replace("G", "")
    disk_perc = str(disk_stats[3]).replace("%", "")

    timestamp = get_timestamp()

    def get_data():

        data_string = "[timestamp={}], [host={}], [cpu_temp={}], [cpu_usage={}]," \
                      " [ram_used={}], [ram_free={}], [disk_total={}]," \
                      " [disk_free={}], [disk_used={}], [disk_perc={}]".format(
                            timestamp,
                            host,
                            cpu_temp,
                            cpu_usage,
                            ram_used,
                            ram_free,
                            disk_total,
                            disk_free,
                            disk_used,
                            disk_perc
        )

        return data_string

    system_logger.info(get_data())
    # print(get_data())
    time.sleep(30)
