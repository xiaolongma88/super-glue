from PIL import Image
import os

# 指定包含TIF文件的文件夹路径
directory = 'E://Ideaproject//SuperGluePretrainedNetwork-master//assets//buildings'
uploads = 'E://Ideaproject//SuperGluePretrainedNetwork-master//images'
# 遍历文件夹中的所有文件
for filename in os.listdir(directory):
    if filename.lower().endswith(".tif"):
        # 拼接完整的文件路径
        tif_path = os.path.join(directory, filename)
        # 打开TIF文件
        with Image.open(tif_path) as img:
            # 定义PNG文件的名称和路径
            png_path = os.path.join(uploads, filename[:-4] + '.png')
            # 将图片保存为PNG格式
            img.save(png_path, 'PNG')
            print(f'Converted {filename} to PNG format')
