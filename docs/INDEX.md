# 文档索引

## 所有文档文件列表

文档位于：`/workspace/docs/` 目录

### 文档文件（共7个）

1. **README.md** - 文档索引和导航
2. **01-快速开始.md** - 安装和配置指南
3. **02-使用指南.md** - 使用流程说明
4. **03-API参考.md** - API接口文档
5. **04-算法设计.md** - 算法设计文档
6. **05-开发指南.md** - 开发规范指南
7. **06-故障排查.md** - 故障排查指南

## 验证文档是否存在

在终端执行以下命令查看文档：

```bash
# 进入docs目录
cd /workspace/docs

# 列出所有文件
ls -la

# 或者查看所有.md文件
ls *.md
```

## 如果找不到文档

1. **检查当前目录**
   ```bash
   pwd
   # 应该显示: /workspace/docs
   ```

2. **列出所有文件（包括隐藏文件）**
   ```bash
   ls -la
   ```

3. **使用find命令查找**
   ```bash
   find /workspace -name "*.md" -type f
   ```

4. **检查文件权限**
   ```bash
   ls -lh /workspace/docs/
   ```

## 文档路径

绝对路径：`/workspace/docs/`

相对路径（从项目根目录）：`docs/`

## 快速访问

- 文档索引：`docs/README.md`
- 快速开始：`docs/01-快速开始.md`
- 使用指南：`docs/02-使用指南.md`
- API参考：`docs/03-API参考.md`
- 算法设计：`docs/04-算法设计.md`
- 开发指南：`docs/05-开发指南.md`
- 故障排查：`docs/06-故障排查.md`
