# -*-coding:utf-8-*-
import os
import string
import random
import pexpect
from termcolor import colored
import threading
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


# 获取系统负载信息
# output: 返回15分钟内的平均负载，任务数/总任务数
def load_stat(machine_name):
    machine = "azureuser@%s.cloudapp.net" % machine_name
    rstf = os.popen("ssh %s 'cat /proc/loadavg'" % machine)
    result = rstf.read().split()
    return result[2], result[3]


# 获取系统内存状态信息
# output: xxG, d%
def meminfo(machine_name):
    machine = "azureuser@%s.cloudapp.net" % machine_name
    rstf = os.popen("ssh %s 'cat /proc/meminfo'" % machine)
    result = rstf.read().split('\n')
    # 0->MemTotal, 1->MemFree
    meminfo_total = string.atoi(result[0].split()[1]) / 1024
    meminfo_avail = string.atoi(result[2].split()[1]) / 1024
    usage = 1 - meminfo_avail * 1.0 / meminfo_total
    return '%dM' % meminfo_total, '%d%%' % int(
        string.atof('%.2f' % usage) * 100)


# 获取系统硬盘使用情况
# output: xxxG, d%
def diskinfo(machine_name):
    machine = "azureuser@%s.cloudapp.net" % machine_name
    rstf = os.popen("ssh %s 'df -lh ~/'" % machine)
    result = rstf.read().split('\n')
    value = result[1].split()
    return value[1], value[4]


def getsysinfo_one(ele, result_set):
    loadavg, taskinfo = load_stat(ele)
    mem, memusage = meminfo(ele)
    disk, diskusage = diskinfo(ele)
    value = "%s%s%s%s%s%s%s" % (ele.ljust(16), loadavg.ljust(16),
        taskinfo.ljust(16), mem.ljust(16), memusage.ljust(16), disk.ljust(16),
        diskusage.ljust(16))
    result_set.append(value.center(116))
    return


# 获取系统信息
# 采用多线程算出结果
def getsysinfo(machine_set):
    print_set = []
    title = "  %s%s%s%s%s%s%s  " % ('Machine'.ljust(16), 'Loadavg'.ljust(16),
        'Taskinfo'.ljust(16), 'Memory'.ljust(16), 'MemUsage'.ljust(16),
        'Disk'.ljust(16), 'DiskUsage'.ljust(16))
    split_mark = ('-' * len(title)).center(116, " ")
    print_set.extend([title, split_mark])
    threads = []
    for ele in machine_set:
        threads.append(
            threading.Thread(target=getsysinfo_one, args=(ele, print_set)))

    for t in threads:
        t.setDaemon(True)
        t.start()

    for t in threads:
        t.join()

    print_set.append(split_mark)
    # user interact
    # end_line = "  flag: %d    q(uit)    r(efresh)" % (random.randint(1, 100))
    # print_set.append(end_line)

    print_string = print_set[0]
    for i in range(1, len(print_set)):
        print_string = "%s\n%s" % (print_string, print_set[i])

    return print_string


def gettxtnum_one(ele, result_set, num_dic, cur_dic, path):
    machine = "azureuser@%s.cloudapp.net" % ele
    try:
        rstf = os.popen("ssh %s 'ls -l %s|wc -l'" % (machine, path))
        result = string.atoi(rstf.read()) - 1
        num_dic[ele] = str(result)
        if ele in cur_dic.keys():
            diff = result - string.atoi(cur_dic[ele])
        else:
            diff = result - 0
        value = "%s%s%s" % (ele.ljust(25), str(result).ljust(25),
                            str(diff).ljust(25))
    except Exception:
        value = "%s%s%s" % (ele.ljust(25), "-1".ljust(25), "-1".ljust(25))
        num_dic[ele] = "-1"
    finally:
        result_set.append(value)


# 检查特定机器上的文件夹中的txt数量
# input: ~/xx/xxx, ['fudan-d1', 'fudan-d2']
# cur_dic: key(机器名), val(数量)
# output: 返回需要输出的字符串和新的dic
def gettxtnum(path, machine_set, cur_dic):
    print_set = []
    title = "%s%s%s" % (
        "MachineName".ljust(25), "Number".ljust(25), "Difference".ljust(25))
    split_mark = '-' * len(title)
    print_set.extend([title, split_mark])
    threads = []
    # 记录这次的数量，用于和下一次比较
    num_dic = {}
    for ele in machine_set:
        threads.append(threading.Thread(target=gettxtnum_one, args=(
            ele, print_set, num_dic, cur_dic, path)))

    for t in threads:
        t.setDaemon(True)
        t.start()

    for t in threads:
        t.join()

    # clear the threads list
    # del threads[:]

    print_set.append(split_mark)
    # end_line = "flag: %d    q(uit)    r(efresh)" % (random.randint(1, 100))
    # print_set.append(end_line)

    print_string = print_set[0]
    for i in range(1, len(print_set)):
        print_string = "%s\n%s" % (print_string, print_set[i])

    return print_string, num_dic


# 在特定机器上解压相应文件
# 返回布尔值表示是否解压成功
def unzipfile(path, machine_name):
    machine = "azureuser@%s.cloudapp.net" % machine_name
    try:
        os.popen("ssh %s 'unzip -o %s'" % (machine, path))
        return True
    except Exception:
        return False


# 在特定机器上安装程序
# TODO
def installone(machine_name, pack_name):
    machine = "azureuser@%s.cloudapp.net" % machine_name
    child = pexpect.spawn("ssh %s sudo apt-get install %s" % (
        machine, pack_name))
    rstf = child.expect(["[Y/n]", pexpect.EOF, pexpect.TIMEOUT])
    if rstf == 0:
        print "continue..."
        print child.before
        child.sendline("Y")
        child.expect('$')
        child.expect(pexpect.EOF)
        child.close()
    else:
        print "already installed or failed!!!"
        child.close()


def backrunone(machine_name, py_command):
    machine = "azureuser@%s.cloudapp.net" % machine_name
    try:
        os.popen(
            "ssh %s 'nohup %s >/dev/null 2>&1 &'" % (machine, py_command))
        return True
    except Exception, e:
        print e
        return False


def zipdataone(machine_name, Pro_path, clear_flag):
    machine = "azureuser@%s.cloudapp.net" % machine_name
    try:
        os.popen("ssh %s 'python %scode/ZipData.py %s %s %s'" % (
            machine, Pro_path, Pro_path, machine_name[6:], clear_flag))
        print "%s%s" % (machine_name.ljust(25), "Done")
    except Exception:
        print "Please upload the \'ZipData.py\' into the \'Project/code\' path"


def killone(machine_name, process_name):
    machine = "azureuser@%s.cloudapp.net" % machine_name
    try:
        child = pexpect.spawn("ssh %s" % machine)
        child.expect("$")
        shell_cmd = "ps -ef |grep %s|awk '{print $2}'|xargs kill -9" % (
            process_name)
        child.sendline('/bin/bash', [shell_cmd])
        child.expect("$")
        child.close()
        return True
    except Exception, e:
        print e
        return False


# installone('fudan-d2', 'zip')
# unzipfile("~/Test.zip", "fudan-d1")
# print getsysinfo(['fudan-d1', 'fudan-d2', 'fudan-yuehuang'])
'''
print diskinfo('fudan-yuehuang')
print meminfo('fudan-yuehuang')
print load_stat('fudan-yuehuang')
'''
# killone('fudan-d1', 'Test')
