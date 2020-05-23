# Git 分支大全

## 一、本地分支





## 二、远程分支

假设当前分支为master，需要创建的分支是my-test

    git checkout -b my-test  //在当前分支下创建my-test的本地分支分支
    git push origin my-test  //将my-test分支推送到远程
    git branch --set-upstream-to=origin/my-test //将本地分支my-test关联到远程分支my-test上   
    git branch -a //查看远程分支 

此时远程分支my-test已经创建好了，并且本地的分支已经关联到远程分支上
本地push代码以后会push到关联的远程分支上。