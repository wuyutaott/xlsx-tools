import os
import sys
import stat
import errno
import shutil
import glob


def lastPath(curAbsPath):
    return os.path.abspath(os.path.join(curAbsPath, ".."))


def delPath(path):
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


# 当前脚本执行所在的目录
CurPath = os.path.abspath(os.path.join(sys.argv[0], ".."))
print("CurPath", CurPath)

# 删除所有.ts文件
pattern = CurPath + "\*.ts"
for ts in glob.glob(pattern, recursive = True):
    os.remove(ts)

# 切换到工具脚本目录
os.chdir(CurPath)
os.system("python3 ExcelTo.py -t " + CurPath + " -o " + CurPath + " --ts")

print("-----------------打表完成-------------------") 
