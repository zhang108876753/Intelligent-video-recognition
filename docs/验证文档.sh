#!/bin/bash
# 文档验证脚本

echo "=========================================="
echo "文档验证脚本"
echo "=========================================="
echo ""

echo "1. 当前目录:"
pwd
echo ""

echo "2. docs目录下的所有文件:"
ls -la
echo ""

echo "3. 所有.md文档文件:"
ls -1 *.md 2>/dev/null || echo "未找到.md文件"
echo ""

echo "4. 文件详细信息:"
for file in *.md; do
    if [ -f "$file" ]; then
        echo "  - $file ($(wc -l < "$file") 行, $(du -h "$file" | cut -f1))"
    fi
done
echo ""

echo "5. 文档内容预览 (README.md前5行):"
head -5 README.md 2>/dev/null || echo "无法读取README.md"
echo ""

echo "=========================================="
echo "验证完成"
echo "=========================================="
