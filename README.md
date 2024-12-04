# IIIF图像展示系统

这是一个基于IIIF和Mirador的图像展示系统。

## 使用方法

1. 添加新图像
   - 将图像文件（支持PNG、JPG、JPEG格式）放入 `images` 文件夹

2. 生成manifest
   - 确保已安装Python依赖：
     ```bash
     pip install Pillow
     ```
   - 运行生成脚本：
     ```bash
     python scripts/generate_manifest.py
     ```

3. 提交更改
   ```bash
   git add .
   git commit -m "Add new images"
   git push origin main
   ```

4. 查看结果
   - 访问 https://oushiei120.github.io/web/index.html
   - 等待几分钟让GitHub Pages更新

## 文件结构
- `images/`: 存放图像文件
- `iiif/manifests/`: 存放生成的manifest.json
- `web/`: 存放网页文件
- `scripts/`: 存放自动化脚本

## 注意事项
- 图像文件名支持中文，系统会自动进行URL编码
- 图像会按文件名字母顺序排序
- 支持PNG和JPG/JPEG格式的图像
