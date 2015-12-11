#!/usr/bin/python
# coding: utf-8

import os
import re
import time
import psutil
from datetime import datetime

os.environ['DJANGO_SETTINGS_MODULE'] = 'jumpserver.settings'

import django
#django.setup()
from jlog.models import Log


def log_hanler(id):
    log = Log.objects.get(id=id)
    pattern = re.compile(r'([\[.*@.*\][\$#].*)|(.*mysql>.*)')
    if log:
        filename = log.log_path
        if os.path.isfile(filename):
            f_his = filename + '.his'
            f1 = open(filename)
            f2 = open(f_his, 'a')
            lines = f1.readlines()
            for line in lines[7:]:
                match = pattern.match(line)
                if match:
                    newline = re.sub('\[[A-Z]', '', line)
                    f2.write(newline)
            f1.close()
            f2.close()
            log.log_finished = True
            log.save()


def set_finish(id):
    log = Log.objects.filter(id=id)
    if log:
        log.update(is_finished=1, end_time=datetime.now())


def kill_pid(pid):
    try:
        os.kill(pid, 9)
    except OSError:
        pass


def get_pids():
    pids1, pids2 = [], []
    pids1_obj = Log.objects.filter(is_finished=0)
    pids2_obj = Log.objects.filter(is_finished=1, log_finished=0)
    for pid_obj in pids1_obj:
        pids1.append((pid_obj.id, pid_obj.pid, pid_obj.log_path, pid_obj.is_finished, pid_obj.log_finished, pid_obj.start_time))
    for pid_obj in pids2_obj:
        pids2.append(pid_obj.id)

    return pids1, pids2


def run():
    pids1, pids2 = get_pids()
    for pid_id in pids2:
        log_hanler(pid_id)

    for pid_id, pid, log_path, is_finished, log_finished, start_time in pids1:
        try:
            file_time = int(os.stat(log_path).st_ctime)
            now_time = int(time.time())
            if now_time - file_time > 10800:
                if psutil.pid_exists(pid):
                    kill_pid(pid)
                set_finish(pid_id)
                log_hanler(pid_id)
            if not psutil.pid_exists(pid):
                set_finish(pid_id)
                log_hanler(pid_id)
        except OSError:
            pass

#function erorcheck is added by Lin to resolve CPU filled issue 2015.08.24

def errorcheck():
    f=os.popen("ps auxr | grep -v auxr|sed -n 2p")
    a=f.read().strip()
    f.close()
    pid=0
    try:
        if a is not None:
            b=a.split(" ")
            if b[-1]=='/opt/jumpserver/connect.py' and b[-2]=='python' and b[-8]=='R' and int(b[-3].split(':')[0])>100:
                for i,j in enumerate(b):
                    if i==0 or j=='':
                        continue
                    else:
                        pid=int(j)
                        break
                kill_pid(pid)
    except :
        pass

if __name__ == '__main__':
    while True:
        run()
        time.sleep(5)
        errorcheck()
