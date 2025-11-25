from PIL import Image
import os

def get_filename_without_extension(filename):
    """提取文件名（去除扩展名）"""
    return os.path.splitext(filename)[0]

def process_paired_folders(input_dir1, output_dir1, input_dir2, output_dir2, target_size=(512, 512)):
    """
    处理两个输入文件夹中的图像，仅通过文件名（忽略扩展名）匹配对应文件，分别保存到输出文件夹
    
    参数:
        input_dir1: 第一个输入文件夹路径（如原始图像）
        output_dir1: 第一个输出文件夹路径（处理后的原始图像）
        input_dir2: 第二个输入文件夹路径（如标签图像）
        output_dir2: 第二个输出文件夹路径（处理后的标签图像）
        target_size: 目标分辨率，默认为(512, 512)
    """
    # 创建输出目录（如果不存在）
    os.makedirs(output_dir1, exist_ok=True)
    os.makedirs(output_dir2, exist_ok=True)
    
    # 获取两个文件夹中的所有文件，并提取文件名主干（无扩展名）与原始文件名的映射
    # 格式：{文件名主干: 原始文件名}
    files1 = {}
    for f in os.listdir(input_dir1):
        if os.path.isfile(os.path.join(input_dir1, f)):
            name_key = get_filename_without_extension(f)
            files1[name_key] = f  # 用主干作为key，存储原始文件名（含扩展名）
    
    files2 = {}
    for f in os.listdir(input_dir2):
        if os.path.isfile(os.path.join(input_dir2, f)):
            name_key = get_filename_without_extension(f)
            files2[name_key] = f
    
    # 找出文件名主干匹配的文件（忽略扩展名）
    common_keys = set(files1.keys()) & set(files2.keys())
    # 找出仅在一个文件夹中存在的文件名主干
    only_in1 = set(files1.keys()) - set(files2.keys())
    only_in2 = set(files2.keys()) - set(files1.keys())
    
    # 打印警告信息
    if only_in1:
        print(f"警告：第一个文件夹有，第二个文件夹没有的文件名（忽略扩展名）：{only_in1}")
    if only_in2:
        print(f"警告：第二个文件夹有，第一个文件夹没有的文件名（忽略扩展名）：{only_in2}")
    
    # 处理匹配的文件
    print(f"开始处理，共 {len(common_keys)} 对匹配的文件（忽略扩展名）...")
    
    for name_key in common_keys:
        # 获取两个文件夹中对应的原始文件名（含各自的扩展名）
        filename1 = files1[name_key]
        filename2 = files2[name_key]
        
        # 构建输入路径
        path1 = os.path.join(input_dir1, filename1)
        path2 = os.path.join(input_dir2, filename2)
        
        # 构建输出路径（保留原始扩展名）
        out_path1 = os.path.join(output_dir1, filename1)
        out_path2 = os.path.join(output_dir2, filename2)
        
        try:
            # 处理第一个文件夹的图像（用LANCZOS插值保留细节）
            with Image.open(path1) as img1:
                resized1 = img1.resize(target_size, Image.Resampling.LANCZOS)
                resized1.save(out_path1)
            
            # 处理第二个文件夹的图像（标签图用最近邻插值避免像素值失真）
            with Image.open(path2) as img2:
                resized2 = img2.resize(target_size, Image.Resampling.NEAREST)
                resized2.save(out_path2)
            
            print(f"已处理：{filename1}（第一个文件夹）与 {filename2}（第二个文件夹） -> 保存至对应输出目录")
        
        except Exception as e:
            print(f"处理 {name_key} 时出错：{str(e)}")

# --------------------------
# 使用示例
# --------------------------
if __name__ == "__main__":
    # 输入文件夹1（如原始图像）
    input1 = "D:/liefengshibie/unet_crack/datasets/JPEGImages"    # 替换为你的第一个输入文件夹路径
    # 输出文件夹1（处理后的原始图像）
    output1 = "D:/liefengshibie/unet_crack/VOCdevkit/VOC2007/JPEGImages"  # 替换为你的第一个输出文件夹路径
    
    # 输入文件夹2（如标签图像）
    input2 = "D:/liefengshibie/unet_crack/datasets/SegmentationClass"     # 替换为你的第二个输入文件夹路径
    # 输出文件夹2（处理后的标签图像）
    output2 = "D:/liefengshibie/unet_crack/VOCdevkit/VOC2007/SegmentationClass"   # 替换为你的第二个输出文件夹路径
    
    # 调用函数，处理并保持文件对应关系
    process_paired_folders(input1, output1, input2, output2)