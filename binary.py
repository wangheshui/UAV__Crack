import cv2
from pathlib import Path

def process_and_save_images(source_dir, dest_dir, threshold=127):
    """
    读取源文件夹中的图片，进行二值化处理后保存到目标文件夹
    
    参数:
        source_dir (str): 源文件夹路径
        dest_dir (str): 目标文件夹路径
        threshold (int): 二值化阈值，默认为127
    """
    source = Path(source_dir)
    destination = Path(dest_dir)
    
    # 确保目标文件夹存在
    destination.mkdir(parents=True, exist_ok=True)
    
    # 支持的图片扩展名集合
    image_exts = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
    
    # 遍历源文件夹中的文件
    for item in source.iterdir():
        if item.is_file() and item.suffix.lower() in image_exts:
            try:
                # 读取图片为灰度图
                img = cv2.imread(str(item), cv2.IMREAD_GRAYSCALE)
                if img is not None:
                    # 应用二值化
                    _, binary_img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
                    
                    # 保存处理后的图片
                    output_path = destination / item.name
                    cv2.imwrite(str(output_path), binary_img)
                    print(f"成功处理并保存: {item.name}")
            except Exception as e:
                print(f"处理图片 {item.name} 时出错: {str(e)}")

# 使用示例
source_folder = "D:/match/test"  # 替换为您的源文件夹路径
destination_folder = "D:/match/test/binary"  # 替换为您的目标文件夹路径
process_and_save_images(source_folder, destination_folder)
