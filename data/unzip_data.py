import os
import zipfile

def check_and_unzip(zip_file_path):

    target_directory =os.path.join( os.getcwd(), 'data')
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    zip_file_name = os.path.basename(zip_file_path)
    zip_file_dir, _ = os.path.splitext(zip_file_name)
    # 检查目标目录是否存在解压后的文件，如果有，则认为已解压
    for filename in os.listdir(target_directory):
        if filename == zip_file_dir:
            print(f"{zip_file_path} 已经解压")
            return True
    # 如果目标目录为空或者没有与 ZIP 文件中不同的文件，则认为未解压
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(target_directory)
        print(f"成功解压文件：{zip_file_path} 到 {target_directory}")
        return True
    except Exception as e:
        print(f"解压文件时出现错误：{e}")
        return False
    

if __name__ == "__main__":
    unzip_file = ['DETRAC-Train-Annotations-XML.zip','Insight-MVT_Annotation_Train.zip']

    for file in unzip_file:
        file = os.path.abspath(file)
        # print(file)
        check_and_unzip(file)

