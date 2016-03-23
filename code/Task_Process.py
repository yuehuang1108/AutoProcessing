# -*-coding:utf-8-*-
import os
import time
import re
import curses
import pexpect
import random
import string
import threading
from termcolor import cprint, colored
import ChildTask
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


# 以列表形式展示出机器名~~
def display(target_set, column_num):
    print '+------------------' * 5 + '+'
    for i in range(len(target_set)):
        print '| %s' % (target_set[i]),
        print ' ' * (18-3-len(target_set[i])),
        if (i + 1) % column_num == 0:
            print '|'
            print '+------------------' * 5 + '+'
        else:
            continue
    # 补空
    remian_length = len(target_set) % 5
    if remian_length != 0:
        tmp = 5 - remian_length
        print ('|' + ' ' * 18) * tmp + '|'
    print '+------------------' * 5 + '+'


# 配置机器名-添加
# str_input: machine[1:23],machine[35]
def Add_Machine(str_input, machine_set):
    str_data = str_input.split(',')
    for ele in str_data:
        ele = ele.strip('\n')
        ele_str = ele[:ele.find("[")]
        ele_num = []
        if ":" in ele:
            ele_pre = string.atoi(get_string(ele, "[", ":"))
            ele_aft = string.atoi(get_string(ele, ":", "]"))
            ele_num.extend(range(ele_pre, ele_aft+1))
        else:
            if len(ele) == (len(ele_str) + 2):
                machine_set.append(ele_str)
            else:
                # 不为空
                ele_mid = string.atoi(get_string(ele, "[", "]"))
                ele_num.extend(range(ele_mid, ele_mid+1))
        for machine_num in ele_num:
            machine_name = "%s%d" % (ele_str, machine_num)
            if machine_name in machine_set:
                continue
            else:
                machine_set.append(machine_name)

    f = open('../data/Machines.txt', 'w')
    for ele in machine_set:
        f.write('%s\n' % ele)
    f.close()
    print "Add Complete"
    time.sleep(1)
    MachineSet()


# 配置机器名-删除
# str_input: machine[1:23],machine[35]
def Delete_Machine(str_input, machine_set):
    str_data = str_input.split(',')
    for ele in str_data:
        ele = ele.strip('\n')
        ele_str = ele[:ele.find("[")]
        ele_num = []
        if ":" in ele:
            ele_pre = string.atoi(get_string(ele, "[", ":"))
            ele_aft = string.atoi(get_string(ele, ":", "]"))
            ele_num.extend(range(ele_pre, ele_aft+1))
        else:
            if len(ele) == (len(ele_str) + 2):
                machine_set.remove(ele_str)
            else:
                ele_mid = string.atoi(get_string(ele, "[", "]"))
                ele_num.extend(range(ele_mid, ele_mid+1))
        for machine_num in ele_num:
            machine_name = "%s%d" % (ele_str, machine_num)
            if machine_name not in machine_set:
                continue
            else:
                machine_set.remove(machine_name)

    f = open('../data/Machines.txt', 'w')
    for ele in machine_set:
        f.write('%s\n' % ele)
    f.close()
    print "Delete Complete"
    time.sleep(1)
    MachineSet()


# 配置机器名-修改
def Modify_Machine(str_input, machine_set):
    str_data = str_input.split(',')
    old_new_nameset = []
    for i in range(len(str_data)):
        tmp_before = str_data[i][str_data[i].find('(')+1: str_data[i].find(' ')]
        tmp_after = str_data[i][str_data[i].find(' ')+1: str_data[i].find(')')]
        old_new_nameset.append([tmp_before, tmp_after])
    for ele in old_new_nameset:
        if ele[0] in machine_set:
            machine_set.remove(ele[0])
            machine_set.append(ele[1])
        else:
            continue
    f = open('../data/Machines.txt', 'w')
    for ele in machine_set:
        f.write('%s\n' % ele)
    f.close()
    print "Done!"
    time.sleep(1)
    MachineSet()


# 配置机器名
def MachineSet():
    os.system('clear')
    print "=" * 42 + colored(
        "Machine Name", "grey", "on_white") + "=" * 42 + "\n"
    data = open('../data/Machines.txt', 'r')
    content = data.readlines()
    machine_set = []
    for i in range(len(content)):
        machine_set.append(content[i].strip('\n'))
    data.close()
    display(machine_set, 5)
    print "\nTask Name:\n1. Modify\n2. Delete\n3. Add"
    cprint("4. Go Back\n", "magenta")
    task_no0 = raw_input("Please input the task number: ")
    if task_no0 == '4':
        pass
    elif task_no0 == '1':
        text_1 = colored("(s1 t1),(s2 t2),(s3 t3)", "red")
        str_input = raw_input(
            "Please input machine name before and after modified, like " +
            text_1 + ":\n")
        if str_input == "quit!":
            MachineSet()
        else:
            Modify_Machine(str_input, machine_set)
    elif task_no0 == '2':
        text_2 = colored("s[1:3],s[4]", "red")
        str_input = raw_input(
            "Please input machine name that you want to delete, like " +
            text_2 + " :\n")
        if str_input == "quit!":
            MachineSet()
        else:
            Delete_Machine(str_input, machine_set)
    elif task_no0 == '3':
        text_3 = colored("s[1:3],s[4]", "red")
        str_input = raw_input(
            "Please input machine name that you want to add, like " +
            text_3 + " :\n")
        if str_input == "quit!":
            MachineSet()
        else:
            Add_Machine(str_input, machine_set)
    else:
        print("Error!Please input the RIGHT number: ")
        MachineSet()


# 判断当前机器是否已经可以免密码登录
def judge_escaped(machine_name):
    psw = 'abcd1234!'
    machine = 'azureuser@' + machine_name + '.cloudapp.net'
    SSHMachine = pexpect.spawn('ssh %s mkdir -p ~/.ssh' % machine)
    # first login
    if SSHMachine.expect(['(yes/no)', pexpect.EOF, pexpect.TIMEOUT]) == 0:
        SSHMachine.sendline('yes')
    # judge
    if SSHMachine.expect(['password:', pexpect.EOF, pexpect.TIMEOUT]) != 0:
        return True
    SSHMachine.sendline(psw)
    SSHMachine.expect('$')
    SSHMachine.close()
    return False


# 配置一台机器的免密码登录
def set_escaped(machine_name):
    psw = 'abcd1234!'
    machine = 'azureuser@' + machine_name + '.cloudapp.net'
    shell_cmd1 = "cat ~/.ssh/id_rsa.pub | ssh %s 'cat >> ~/.ssh/authorized_keys'" % machine
    child = pexpect.spawn('/bin/zsh', ['-c', shell_cmd1])
    child.expect(['password:', pexpect.EOF, pexpect.TIMEOUT])
    child.sendline(psw)
    child.expect("$")
    child.expect(pexpect.EOF)
    child.close()


# 一次判断设置过程
def EscapePSWone(ele):
    if judge_escaped(ele):
        print '%s\t\t%s\t\t%s' % (ele, colored(
            'YES', "green"), colored('OK', 'green'))
    else:
        set_escaped(ele)
        if judge_escaped(ele):
            print '%s\t\t%s\t\t%s' % (ele, colored(
                'NO', 'red'), colored('OK', 'green'))
        else:
            print '%s\t\t%s\t\t%s' % (ele, colored(
                'NO', 'red'), colored('Error', 'red'))


# 设置免密码登录
def EscapePSW():
    os.system('clear')
    data = open('../data/Machines.txt', 'r')
    content = data.readlines()
    machine_set = []
    for i in range(len(content)):
        machine_set.append(content[i].strip('\n'))
    data.close()
    print "==========" + colored(
        "Check & Set Automatic Login", "grey", "on_white") + "==========\n"
    print 'MachineName\t\tIsEscaped\tResult'
    threads = []
    for ele in machine_set:
        # 把判断、设置过程多线程化
        threads.append(threading.Thread(
            target=EscapePSWone, args=(ele,)))

    for t in threads:
        t.setDaemon(True)
        t.start()

    for t in threads:
        t.join()

    print "\nDone!"
    raw_input("")


# upload file from filepath to targetmachine
def Upload():
    os.system("clear")
    print "=" * 40 + colored("Upload File", "grey", "on_white") + "=" * 40
    data = open('../data/Machines.txt', 'r')
    content = data.readlines()
    machine_set = []
    for i in range(len(content)):
        machine_set.append(content[i].strip('\n'))
    data.close()
    filepath = raw_input(
        "Please input " + colored("the source path", "red") + ": \n")
    print
    targetpath = raw_input("Please input " + colored(
        "the remote relative path", "red") + ": \n")
    print
    if filepath == "quit!" or targetpath == "quit!":
        pass
    else:
        if not os.path.exists(filepath):
            print "Path \'%s\' doesn't exist!Please Check!" % filepath
            time.sleep(2)
            return False
        else:
            for machine in machine_set:
                print "-" * 100
                print machine
                sshpath = "azureuser@%s.cloudapp.net:%s" % (
                    machine, targetpath)
                try:
                    os.system("scp %s %s" % (filepath, sshpath))
                except Exception, e:
                    print e
            print "-" * 100
            print 'All Done, retrun to Main UI after 2 seconds'
            time.sleep(2)


# input:  	local_path(本地存储数据的文件夹路径)
# 			target_path(远端压缩文件所在路径)
# 			filename(文件名)
def OneDownload(local_path, target_path, filename):
    try:
        os.system("scp %s %s" % (target_path, local_path))
    except Exception, e:
        print e
    finally:
        fileset = os.listdir(local_path)
        if filename in fileset:
            return True
        else:
            return False


# 自动化下载
def Download():
    os.system("clear")
    print "=" * 40 + colored("Download File", "grey", "on_white") + "=" * 40
    re_text = colored("remote relative path", "red")
    local_text = colored("local path", "red")
    re_path = raw_input("Please input the " + re_text + ": \n")
    print
    local_path = raw_input(
        "Please input the " + local_text + " to save the data: \n")
    print
    if re_path == "quit!" or local_path == "quit!":
        pass
    else:
        machine_file = GetMaxFileNameFromLocal(local_path)
        for k, d in machine_file.items():
            print "-" * 50
            print "Machine Name: fudan-" + k
            target_name = GetNextFile(k, '%s.zip' % d)
            target_path = "azureuser@fudan-%s.cloudapp.net:%s%s" % (
                k, re_path, target_name)
            while OneDownload(local_path, target_path, target_name):
                target_name = GetNextFile(k, target_name)
                target_path = "azureuser@fudan-%s.cloudapp.net:%s%s" % (
                    k, re_path, target_name)
        print "-" * 50
        print "Done!"
        time.sleep(2)


# 获取目标路径下，已经下载的文件的最大序列号
# output: {'d4': 'd40001', 'd3': 'd30002'}
def GetMaxFileNameFromLocal(local_path):
    files = os.listdir(local_path)
    machine_file = {}
    for ele in files:
        if 'zip' not in ele:
            continue
        cur_num = ele[ele.find('.')-4: ele.find('.')]
        cur_machine = ele[: ele.find('.')-4]
        if cur_machine in machine_file.keys():
            if string.atoi(cur_num) > string.atoi(machine_file[cur_machine][-4:]):
                machine_file[cur_machine] = cur_machine + cur_num
            else:
                continue
        else:
            machine_file[cur_machine] = cur_machine + cur_num
    machine_set, machine_alias = GetMachines()

    for ele in machine_alias:
        if ele not in machine_file.keys():
            tmp_num = '%s%04d' % (ele, 0)
            machine_file[ele] = tmp_num
        else:
            continue

    return machine_file


# input: 'd4', 'd40002.zip'
# output: 'd40003.zip'
def GetNextFile(alias, cur_filename):
    cur_num = cur_filename[len(alias): cur_filename.find('.')]
    next_num = string.atoi(cur_num) + 1
    next_num_str = '%s%04d.zip' % (alias, next_num)
    return next_num_str


# 返回配置文件中的机器名和简称，比如['fudan-d1','fudan-d2'],['d1','d2']
def GetMachines():
    data = open('../data/Machines.txt', 'r')
    content = data.readlines()
    machine_set = []
    for i in range(len(content)):
        machine_set.append(content[i].strip('\n'))
    data.close()

    machine_alias = []
    for ele in machine_set:
        machine_alias.append(ele[6:])

    return machine_set, machine_alias


# 查看机器状态
def GetMachineState():
    os.system('clear')
    print
    MachineSet, _ = GetMachines()
    screen = curses.initscr()
    curses.noecho()
    q = -1
    sysinfo = ChildTask.getsysinfo(MachineSet)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_WHITE)
    while q != ord('q'):
        screen.clear()
        screen.addstr(0, 0, "=" * 52)
        screen.addstr(0, 52, "Machine State", curses.color_pair(1))
        screen.addstr(0, 52 + len("Machine State"), "=" * 52)
        screen.addstr(2, 0, sysinfo)
        enter_num = len(re.findall("\n", sysinfo))
        end_line = "\n  flag: %d    q(uit)    r(efresh)" % (
            random.randint(1, 100))
        screen.addstr(3+enter_num, 0, end_line, curses.color_pair(2))
        screen.refresh()
        q = screen.getch()
        if q == ord('r'):
            sysinfo = ChildTask.getsysinfo(MachineSet)
        time.sleep(0.1)
    curses.endwin()


# 查看程序运行结果，查看指定文件夹下的txt数目
def GetTxtNum():
    # os.system("clear")
    remote_path = raw_input("Please input the " + colored(
        "remote relative data path", "red") + ": \n")
    if remote_path == "quit!":
        pass
    else:
        machine_set, _ = GetMachines()
        title, num_dic = ChildTask.gettxtnum(remote_path, machine_set, {})
        screen = curses.initscr()
        curses.noecho()
        q = -1
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_WHITE)
        while q != ord('q'):
            screen.clear()
            screen.addstr(0, 0, "=" * 28)
            screen.addstr(0, 28, "View Package Number", curses.color_pair(1))
            screen.addstr(0, 28 + len("View Package Number"), "=" * 28)
            screen.addstr(2, 0, title)
            enter_num = len(re.findall("\n", title))
            end_line = "\n  flag: %d    q(uit)    r(efresh)" % (
                random.randint(1, 100))
            screen.addstr(3+enter_num, 0, end_line, curses.color_pair(2))
            screen.refresh()
            q = screen.getch()
            if q == ord('r'):
                title, num_dic = ChildTask.gettxtnum(
                    remote_path, machine_set, num_dic)
            time.sleep(0.1)
        curses.endwin()


# 解压文件
def Unzip():
    os.system("clear")
    print "=" * 40 + colored("Decompress File", "grey", "on_white") + "=" * 40
    zip_path = raw_input("Please input " + colored(
        "the remote relative ZIP path", "red") + ": \n")
    machine_set, _ = GetMachines()
    print
    if zip_path == "quit!":
        pass
    else:
        for ele in machine_set:
            print ele.ljust(20),
            if ChildTask.unzipfile(zip_path, ele):
                print "Unzip Done!"
            else:
                print "Error!"
            time.sleep(2)


# 将运行完的数据压缩
# input: project path, alias, y/n


def Zip():
    os.system("clear")
    print "=" * 40 + colored("Compress File", "grey", "on_white") + "=" * 40
    Pro_path = raw_input("Please input " + colored(
        "the remote relative project path", "red") + ": \n")
    print
    clear_flag = raw_input("Do you want to " + colored(
        "clear the data folder", "red") + " after compression(Y/N): \n")
    print
    if Pro_path == "quit!" or clear_flag == "quit!":
        pass
    else:
        machine_set, _ = GetMachines()
        threads = []
        print "%s%s" % ("MachineName".ljust(25), "Result")
        for ele in machine_set:
            # 多线程处理
            threads.append(threading.Thread(
                target=ChildTask.zipdataone, args=(
                    ele, Pro_path, clear_flag)))

        for t in threads:
            t.setDaemon(True)
            t.start()

        for t in threads:
            t.join()

        print "\nAll Done, Return Back after 2 Seconds!"
        time.sleep(2)


# 在后台运行python文件
def BackRun():
    py_command = raw_input("Please input the " + colored(
        "command to run the crawler", "red") + " : \n")
    if py_command == "quit!":
        pass
    else:
        os.system("clear")
        machine_set, _ = GetMachines()
        print "=" * 19 + colored(
            "Run Crawler", "grey", "on_white") + "=" * 19
        print
        print "Machine Name".ljust(25),
        print "Result"
        print "-" * 50
        for ele in machine_set:
            print ele.ljust(25),
            if ChildTask.backrunone(ele, py_command):
                print colored("Running", "green")
            else:
                print colored("Something Wrong", "red")
        print "\nDone"
        raw_input("")


# 杀死目标机器中的进程
def KillProcess():
    process_name = raw_input("Please input the " + colored(
        "remote process name", "red") + " : \n")
    if process_name == "quit!":
        pass
    else:
        os.system("clear")
        machine_set, _ = GetMachines()
        print "=" * 19 + colored(
            "Kill Process", "grey", "on_white") + "=" * 19
        print
        print "Machine Name".ljust(25),
        print "Result"
        print "-" * 50
        for ele in machine_set:
            print ele.ljust(25),


def get_string(line, pre, pos):
    i = line.find(pre)
    j = line.find(pos, i+len(pre))
    return (line[i+len(pre): j])


# 安装系统库文件
'''
def Install():
    pack_name = raw_input("Please input the package name: ")
    machine_set, _ = GetMachines()
    for ele in machine_set:
        installOne(ele)
'''
# GetMachineState()
# EscapePSW()
# Upload('../data/hyTest.zip', ['fudan-d4'], '~/')
# Download()
# BackRun()
# GetTxtNum()
# print get_string(sys.argv[1], sys.argv[2], sys.argv[3])
# print GetMaxFileNameFromLocal("/Users/huangyue/Documents/workspace/TestData/")
