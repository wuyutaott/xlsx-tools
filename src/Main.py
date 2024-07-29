import os
import sys
import stat
import errno
import shutil
import glob


def lastPath(curAbsPath):
    return os.path.abspath(os.path.join(curAbsPath, ".."))


def delPath(path):
    if os.path.exists(path):
        shutil.rmtree(path, onerror=handle_remove_read_only)


def handle_remove_read_only(func, path, exc):
    excvalue = exc[1]
    if func in (os.rmdir, os.remove, os.unlink) and excvalue.errno == errno.EACCES:
        os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777
        func(path)
    else:
        raise


def nextPath(curAbsPath, next):
    return os.path.abspath(os.path.join(curAbsPath, next))


def gitClone(repo, branch, name, path):
    """
    :param repo: 配置表仓库地址
    :param branch: 所在分支
    :param name: 克隆下来的本地目录
    :param path: 在哪个文件夹下操作
    """
    repoPath = os.path.join(path, name)
    if os.path.exists(repoPath) == False:
        os.chdir(path)
        os.system("git clone " + repo + " " + name)
        print("git clone ok")
        
    os.chdir(repoPath)
    print("git checkout " + branch)
    os.system("git checkout " + branch)
    print("checkout ok")
    os.system("git pull --rebase")
    print("pull ok")


# 当前脚本执行所在的目录
CurPath = os.path.abspath(os.path.join(sys.argv[0], ".."))
print("当前路径", CurPath)

# 更新仓库
repo = "git@github.com:jfcwrlight/DasinoClient-Table.git"
branch = "main"
srcDirName = "tables"
path = CurPath
gitClone(repo, branch, srcDirName, path)

# # 删除所有.ts文件
# pattern = CurPath + "\*.ts"
# for ts in glob.glob(pattern, recursive = True):
#     os.remove(ts)

# 删除输出目录
ourDirPath = os.path.join(path, srcDirName, "out")
delPath(ourDirPath)

# 切换到工具脚本目录
os.chdir(CurPath)
srcDirPath = os.path.join(CurPath, srcDirName)
os.system("python3 ExcelTo.py -t " + srcDirPath + " -o " + ourDirPath + " --ts")

print("-----------------打表完成-------------------") 
