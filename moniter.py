import os,signal
import time
 
def get_now_time():
    # 获取当前的本地时间
    now_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    return now_time
 
def kill(pid):
    print('pid',pid)
    # pgid=os.getpgid(pid)
    # print(pgid)
    # a = os.killpg(pgid,signal.SIGKILL)
    a = os.kill(pid,signal.SIGKILL)
    print('已杀死pid为%s的进程,　返回值是:%s' % (pid, a))
 
def kill_target(target):
    cmd_run="ps aux | grep {}".format(target)
    out=os.popen(cmd_run).read()
    for line in out.splitlines():
        print(line)
        if '另外判断杀死进行所在的路径' in line:
            pid = int(line.split()[1])
            kill(pid)
# 建议在运行命令后面加上&符号，似乎是以另一个线程跑
os.system('python ./run.py') 
       
while True:
    # 关闭
    if some_condition:
        print('暂停')
        kill_target('woringThread.py')
    # 打开
    if some_else_condition:
        os.system('python ./woringThread.py')

