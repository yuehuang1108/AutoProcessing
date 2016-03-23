# -*-coding:utf-8-*-
import Task_Process
import os
from termcolor import colored, cprint
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def PrintMainUI():
    text = colored("Task List", "grey", "on_white")
    print ">" * 10 + text + "<" * 10
    print "\n1. Settings"
    print "2. Data Management"
    print "3. Machine Control"
    cprint("4. Quit\n", "magenta")


def PrintSettings():
    text = colored("Settings", "grey", "on_white")
    print ">" * 10 + text + "<" * 10
    print "\n1. Machine Setting"
    print "2. Auto Login Setting"
    cprint("3. Go Back\n", "magenta")
    flag = raw_input("Please Input the Number: ")
    return flag


def OperateSettings(flag):
    if flag == '1':
        Task_Process.MachineSet()
        # Back to settings page
        Task('1')
    elif flag == '2':
        Task_Process.EscapePSW()
        Task('1')
    elif flag == '3':
        MainUI()
    else:
        error_msg = raw_input("Error!Please input the RIGHT number: ")
        OperateSettings(error_msg)


def PrintData():
    text = colored("Data Management", "grey", "on_white")
    print ">" * 10 + text + "<" * 10
    print "\n1. Upload"
    print "2. Download"
    print "3. Decompress"
    print "4. Compress"
    cprint("5. Go Back\n", "magenta")
    flag = raw_input("Please Input the Number: ")
    return flag


def OperateData(flag):
    if flag == '1':
        Task_Process.Upload()
        # back to Data page
        Task('2')
    elif flag == '2':
        Task_Process.Download()
        Task('2')
    elif flag == '3':
        Task_Process.Unzip()
        Task('2')
    elif flag == '4':
        Task_Process.Zip()
        Task('2')
    elif flag == '5':
        MainUI()
    else:
        error_msg = raw_input("Error!Please input the RIGHT number: ")
        OperateData(error_msg)


def PrintView():
    text = colored("View Machines", "grey", "on_white")
    print ">" * 10 + text + "<" * 10
    print "\n1. View Machine State"
    print "2. View Data Number"
    print "3. Run Crawler"
    print "4. Kill Process"
    cprint("5. Go Back\n", "magenta")
    flag = raw_input("Please Input the Number: ")
    return flag


def OperateView(flag):
    if flag == '1':
        Task_Process.GetMachineState()
        Task('3')
    elif flag == '2':
        Task_Process.GetTxtNum()
        Task('3')
    elif flag == '3':
        Task_Process.BackRun()
        Task('3')
    elif flag == '5':
        MainUI()
    else:
        error_msg = raw_input("Error!Please input the RIGHT number: ")
        OperateView(error_msg)


def Task(task_no):
    # 退出登录
    if task_no == '4':
        flag = raw_input("Are You Sure To Quit?(Y/N): ")
        if flag in ['Y', 'y']:
            print "bye"
        elif flag in ['N', 'n']:
            MainUI()
        else:
            print 'Invalid Input!'
            Task(task_no)
    # Settings
    elif task_no == '1':
        os.system('clear')
        OperateSettings(PrintSettings())
    # Data
    elif task_no == '2':
        os.system('clear')
        OperateData(PrintData())
    elif task_no == '3':
        os.system('clear')
        OperateView(PrintView())
    else:
        error_msg = raw_input("Error!Please input the RIGHT number: ")
        Task(error_msg)


def MainUI():
    os.system('clear')
    # TODO(print the title)
    PrintMainUI()
    task_no = raw_input("Please input the number: ")
    Task(task_no)


if __name__ == '__main__':
    MainUI()
