# -*-coding:utf-8-*-
import os
import commands
import string
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


# input
# zip_path: the zip file path; data_path: data to compress
def ZipOperate(zip_path, data_path):
    # zip_path/zip_name
    # find next zip_name based on the zip_path
    cmd = "zip -r %s %s" % (zip_path, data_path)
    os.system(cmd)


# 获取目标路径下，已经保存的文件的最大序列号下一个
# output: {d40001.zip, d40002.zip} => d40003.zp
def GetMaxFileNameFromLocal(local_path, alias):
    files = os.listdir(local_path)
    # files = ['d40001.zip','d40002.zip','d40003.zip']
    machine_file = []
    for ele in files:
        if 'zip' not in ele:
            continue
        cur_num = ele[ele.find('.')-4: ele.find('.')]
        machine_file.append(string.atoi(cur_num))

    if len(machine_file) == 0:
        next_num = 1
    else:
        next_num = max(machine_file) + 1
    next_num_str = '%s%04d.zip' % (alias, next_num)
    return next_num_str


# sys.argv[1]: project path(~:/Test/)
# sys.argv[2]: machine alias(d1,d2)
# sys.argv[3]: whether to clear the data folder
code_path = "%scode/" % (sys.argv[1])
data_path = "%sdata/" % (sys.argv[1])
zip_name = GetMaxFileNameFromLocal(sys.argv[1], sys.argv[2])
ZipOperate("%s%s" % (sys.argv[1], zip_name), data_path)
if sys.argv[3] == 'y':
    # clear the data
    print "Clear the data folder..."
    (status, output) = commands.getstatusoutput("rm -r %s*.txt" % data_path)
else:
    print "The data folder is not clear"
