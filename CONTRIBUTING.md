## 协作流程
克隆仓库
- git clone git@github.com:T-X-G/rsod-web-platform.git
- cd rsod-web-platform
1. 同步主分支  确保本地的 main 分支是最新的
   - git checkout main
   - git pull origin main
2. 创建功能分支
   - git checkout -b feature/功能描述
   - 示例：- feature/single-detection
          - feature/history-page
          - fix/api-error
3. 本地开发与提交
   - git add .
   - git commit -m "feat(detection): 实现图片上传组件"
4. 推送分支到远程
   - git push origin feature/功能描述
5. 发起 Pull Request (PR)
6. 代码审查与修改
7. 合并 Pull Request
8. 更新本地仓库
   - 合并后，其他成员在开始新任务前需要同步最新的 main 分支：
     - git checkout main
     - git pull origin main
   - 同时删除本地已合并的功能分支（可选）：
     - git branch -d feature/功能描述
9. 处理合并冲突
   - 你的功能分支落后于 main，且 main 上有与你冲突的修改。
     - git checkout feature/你的分支名
     - git pull origin main
     - git add .
     - git commit -m "merge: 解决与 main 的冲突"
     - git push origin feature/你的分支名
## 常用命令
- 查看当前状态	git status
- 查看本地分支	git branch
- 查看所有分支（含远程）	git branch -a
- 切换分支	git checkout <分支名>
- 创建并切换分支	git checkout -b <新分支名>
- 拉取最新代码	git pull origin <分支名>
- 推送分支	git push origin <分支名>
- 删除本地分支	git branch -d <分支名>
- 删除远程分支	git push origin --delete <分支名>
- 查看提交历史（图形化）	git log --oneline --graph
- 暂存当前修改	git stash
- 恢复暂存	git stash pop
