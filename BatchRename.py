import os
import sys
from pathlib import Path

def rename(path):
    i = 0
    '该文件夹下所有的文件（包括文件夹）'
    FileList = os.listdir(path)
    '遍历所有文件'
    for files in FileList:
        '原来的文件路径'
        oldDirPath = os.path.join(path, files)
        if oldDirPath.endswith(".git"):
            continue
        if oldDirPath.endswith(".vscode"):
            continue
        if oldDirPath.endswith(".vs"):
            continue
        newDirpath = oldDirPath.replace(" ", "")
        os.rename(oldDirPath, newDirpath)
        '如果是文件夹则递归调用'
        if os.path.isdir(newDirpath):
            rename(newDirpath)

_pth = Path.cwd();
path = "" + os.path.realpath(_pth) + "\\";
rename(path)