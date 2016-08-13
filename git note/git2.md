

##`git status`查看工作区的状态,文件是否修改、删除、或者新建


	$ git status
	# On branch master
	# Changes not staged for commit:
	#   (use "git add <file>..." to update what will be committed)
	#   (use "git checkout -- <file>..." to discard changes in working directory)
	#
	#    modified:   readme.txt
	#
	no changes added to commit (use "git add" and/or "git commit -a")

`Changes not staged for commit`表示修改的文件还没有加入缓存区，即还没有用`git commit`提交。下面是已经`git commit`之后的`git status`输出信息：

	$ git status
	# On branch master
	# Changes to be committed:
	#   (use "git reset HEAD <file>..." to unstage)
	#
	#       modified:   readme.txt
	#

##`git diff`查看修改内容

	$ git diff readme.txt
	diff --git a/readme.txt b/readme.txt
	index 46d49bf..9247db6 100644
	--- a/readme.txt
	+++ b/readme.txt
	@@ -1,2 +1,2 @@
	-Git is a version control system.
	+Git is a distributed version control system.
	 Git is free software.

##`git log`查看`git commit`记录

	$ git log
	commit 3628164fb26d48395383f8f31179f24e0882e1e0
	Author: Michael Liao <askxuefeng@gmail.com>
	Date:   Tue Aug 20 15:11:49 2013 +0800

	    append GPL

	commit ea34578d5496d7dd233c827ed32a8cd576c5ee85
	Author: Michael Liao <askxuefeng@gmail.com>
	Date:   Tue Aug 20 14:53:12 2013 +0800

	    add distributed

	commit cb926e7ea50ad11b8f9e909c05226233bf755030
	Author: Michael Liao <askxuefeng@gmail.com>
	Date:   Mon Aug 19 17:51:55 2013 +0800

	    wrote a readme file

记录太多的时候可以用

	$ git log --pretty=oneline
	3628164fb26d48395383f8f31179f24e0882e1e0 append GPL
	ea34578d5496d7dd233c827ed32a8cd576c5ee85 add distributed
	cb926e7ea50ad11b8f9e909c05226233bf755030 wrote a readme file

输出的结果中第一列为`commit id`

或者用 `--oneline` 选项来查看历史记录的紧凑简洁的版本。

	$ git log --oneline
	8d585ea Merge branch 'fix_readme'
	3cbb6aa fixed readme title differently
	3ac015d fixed readme title
	558151a Merge branch 'change_class'
	b7ae93b added from ruby
	3467b0a changed the class name
	17f4acf first commit

我们还可以用它的十分有帮助的` --graph` 选项，查看历史中什么时候出现了分支、合并。以下为相同的命令，开启了拓扑图选项：

	$ git log --oneline --graph
	*   8d585ea Merge branch 'fix_readme'
	|\
	| * 3ac015d fixed readme title
	* | 3cbb6aa fixed readme title differently
	|/
	*   558151a Merge branch 'change_class'
	|\
	| * 3467b0a changed the class name
	* | b7ae93b added from ruby
	|/
	* 17f4acf first commit


现在我们可以更清楚明了地看到何时工作分叉、又何时归并。 这对查看发生了什么、应用了什么改变很有帮助，并且极大地帮助你管理你的分支。

如果你要查看`erlang`分支的日志记录，可以使用`git log --oneline erlang`

	$ git log --oneline erlang
	1834130 added haskell
	ab5ab4c added erlang
	8d585ea Merge branch 'fix_readme'
	3cbb6aa fixed readme title differently
	3ac015d fixed readme title
	558151a Merge branch 'change_class'
	b7ae93b added from ruby
	3467b0a changed the class name
	17f4acf first commit

##`git reset`版本回退

回退到上一个版本

	$ git reset --hard HEAD^

回退到上上个版本

	$ git reset --hard HEAD^^

回退到上100次个版本

	$ git reset --hard HEAD~100

回退到某个`commit id = 3628164fb26d`的版本

	git reset --hard 3628164fb26d

##要回退到未来版本，用`git reflog`查看未来和过去的版本

在从未来回退到之前一个版本后，用`git log` 查看不到未来的版本，这时可以用`git reflog`,输出的结果中第一列为`commit id`

	$ git reflog
	ea34578 HEAD@{0}: reset: moving to HEAD^
	3628164 HEAD@{1}: commit: append GPL
	ea34578 HEAD@{2}: commit: add distributed
	cb926e7 HEAD@{3}: commit (initial): wrote a readme file

##`git checkout`撤销修改

1、文件还没有`git commit`，想撤销修改。使用` git checkout -- <file>`撤销修改

2、文件已经`git commit`，想撤销修改。使用`git reset --hard HEAD^`使工作区的文件回退到上次commit的版本，即工作区的内容重新设置到和缓存区一样，然后再` git checkout -- <file>`撤销修改

##分支的创建、切换和合并

###查看当前分支：`git branch`

没有参数时，`git branch` 会列出你在本地的分支。你所在的分支的行首会有个星号作标记。 如果你开启了彩色模式，当前分支会用绿色显示。

	$ git branch
	* master

###创建分支：`git branch <name>`

	$ git branch testing
	$ git branch
	* master
	  testing

###切换分支：`git checkout <name>`

###创建新分支，并立即切换到它：`git checkout -b <name>`

###合并某分支到当前分支：`git merge <name>`

现在，我们切换回master：

	$ git checkout master
	Switched to branch 'master'

准备合并dev分支，请注意--no-ff参数，表示禁用Fast forward：

	$ git merge --no-ff -m "merge with no-ff" dev
	Merge made by the 'recursive' strategy.
	 readme.txt |    1 +
	 1 file changed, 1 insertion(+)

因为本次合并要创建一个新的commit，所以加上-m参数，把commit描述写进去。

合并后，我们用git log看看分支历史：

	$ git log --graph --pretty=oneline --abbrev-commit
	*   7825a50 merge with no-ff
	|\
	| * 6224937 add merge
	|/
	*   59bc1cb conflict fixed
	...

通常，合并分支时，Git会用Fast forward模式，在这种模式下，删除分支后，会丢掉分支信息。

如果要强制禁用Fast forward模式，使用`git merge --no-ff -m "<修改记录>" <分支名>`，Git就会在merge时生成一个新的commit，这样，从分支历史上就可以看出分支信息。

###删除分支：`git branch -d <name>`

###删除远程分支：`git push origin :<要删除的远程分支名字>`

##远程操作

###删除远程主机： `git remote rm <主机名>`

###远程主机的改名： `git remote rename <原主机名> <新主机名>`

###查看当前的远程库：`git remote`

要查看当前配置有哪些远程仓库，可以用 `git remote` 命令，它会列出每个远程库的简短名字。在克隆完某个项目后，至少可以看到一个名为 `origin` 的远程库，Git 默认使用这个名字来标识你所克隆的原始仓库：

	$ git clone git://github.com/schacon/ticgit.git
	Cloning into 'ticgit'...
	remote: Reusing existing pack: 1857, done.
	remote: Total 1857 (delta 0), reused 0 (delta 0)
	Receiving objects: 100% (1857/1857), 374.35 KiB | 193.00 KiB/s, done.
	Resolving deltas: 100% (772/772), done.
	Checking connectivity... done.
	$ cd ticgit
	$ git remote
	origin

也可以加上 `-v` 选项（译注：此为 --verbose 的简写，取首字母，中文意思为冗长的），显示对应的克隆地址：

	$ git remote -v
	origin  git://github.com/schacon/ticgit.git (fetch)
	origin  git://github.com/schacon/ticgit.git (push)

如果有多个远程仓库，此命令将全部列出。比如在我的 Grit 项目中，可以看到：

	$ cd grit
	$ git remote -v
	bakkdoor  git://github.com/bakkdoor/grit.git
	cho45     git://github.com/cho45/grit.git
	defunkt   git://github.com/defunkt/grit.git

###查看该主机的详细信息：`git remote show <主机名>`

	$ git remote show origin
	* remote origin
	  URL: git://github.com/schacon/ticgit.git
	  Remote branch merged with 'git pull' while on branch master
	    master
	  Tracked remote branches
	    master
	    ticgit

除了对应的克隆地址外，它还给出了许多额外的信息。它友善地告诉你如果是在 master 分支，就可以用 git pull 命令抓取数据合并到本地。另外还列出了所有处于跟踪状态中的远端分支。
###添加远程主机： `git remote add <shortname> <url>`

将 [url] 以 [shortname] 的别名添加为本地的远端仓库。

	$ git remote
	origin
	$ git remote add pb git://github.com/paulboone/ticgit.git
	$ git remote -v
	origin  git://github.com/schacon/ticgit.git
	pb  git://github.com/paulboone/ticgit.git

###从远端仓库提取数据并尝试合并到当前分支：`git fetch <remote-name>`
现在可以用字符串 `pb` 指代对应的仓库地址了。比如说，要抓取所有 Paul 有的所有更新，但本地仓库没有的信息，可以运行 `git fetch pb`：

	$ git fetch pb
	remote: Counting objects: 58, done.
	remote: Compressing objects: 100% (41/41), done.
	remote: Total 44 (delta 24), reused 1 (delta 0)
	Unpacking objects: 100% (44/44), done.
	From git://github.com/paulboone/ticgit
	 * [new branch]      master     -> pb/master
	 * [new branch]      ticgit     -> pb/ticgit

默认情况下，`git fetch`取回所有分支（branch）的更新。如果只想取回特定分支的更新，可以指定分支名。

    $ git fetch <远程主机名> <分支名>

比如，取回origin主机的master分支。

    $ git fetch origin master

所取回的更新，在本地主机上要用"远程主机名/分支名"的形式读取。比如`origin`主机的`master`，就要用`origin/master`读取。
`git branch`命令的`-r`选项，可以用来查看远程分支，`-a`选项查看所有分支。

	$ git branch -r
	origin/master

	$ git branch -a
	* master
	  remotes/origin/master

上面命令表示，本地主机的当前分支是`master`，远程分支是`origin/master`。

###为远程分支创建新分支`git checkout -b <new-branch-name> <remote-branch-name>`

取回远程主机的更新以后，可以在它的基础上，使用`git checkout`命令创建一个新的分支。

	$ git checkout -b newBrach origin/master

###合并远程分支`git merge <remote-name> <branch-name>`

上面命令表示，在`origin/master`的基础上，创建一个新分支。
此外，也可以使用`git merge`命令或者`git rebase`命令，在本地分支上合并远程分支。

	$ git merge origin/master
	# 或者
	$ git rebase origin/master
上面命令表示在当前分支上，合并`origin/master`。

###推送数据到远程仓库`git push <remote-name> <branch-name>`

如果要将你的 [branch] 分支推送成为 [alias] 远端上的 [branch] 分支

如果要把本地的 `master` 分支推送到 `origin` 服务器上（再次说明下，克隆操作会自动使用默认的 master 和 origin 名字），可以运行下面的命令：

	$ git push origin master

