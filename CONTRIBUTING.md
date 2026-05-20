## 协作流程

1. 确保在 `dev` 分支：`git checkout dev && git pull`
2. 创建功能分支：`git checkout -b feature/你的任务名`
3. 提交代码：`git add . && git commit -m "[模块] 说明"`
4. 推送分支：`git push origin feature/你的任务名`
5. 在 GitHub 发起 Pull Request 到 `dev` 分支
6. 至少一位成员批准后合并
7. 删除远程和本地功能分支（可选）

## 常用命令

- 查看分支：`git branch -a`
- 切换分支：`git checkout <分支名>`
- 拉取最新：`git pull origin dev`
- 删除本地分支：`git branch -d <分支名>`
- 删除远程分支：`git push origin --delete <分支名>`
