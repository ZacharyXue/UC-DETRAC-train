"""
将原始数据 annotation 中的 xml 转换为 json 文件， evaluation-service中使用 
具体转换为：
    mvi_{mvi_name}.xml: 视频的 xml 文件
    --> annotations/mvi_{mvi_name}_{frame_id}.json
    --> images/mvi_{mvi_name}_{frame_id}.jpg

步骤：
    1. 遍历获取所有 mvi ，共计 200 张，计算每个 mvi 提取 imgs 数
    2. 使用 xml2dict 对应 mvi 的 dict ，以等差数列读取对应 frame
        a. 遍历所有 mvi
        b. 获取frame num，遍历指定 frame
    3. 按照规则存储 frame 的 img 和 label 信息
        a. 生成需保存 json dict
        b. 保存 img 和 dict 到指定路径
"""
import os
import cv2
import json
from tqdm import tqdm
from data import xml2dict


def get_all_mvi(data_path:str, samples_num:int = 200):

    mvi_list = os.listdir(data_path)
    pic_num_each_mvi = samples_num // len(mvi_list)

    log_str = f"共有视频 {len(mvi_list)} 个, 每个视频选取图片 {pic_num_each_mvi} 张"
    print(log_str)

    return mvi_list, pic_num_each_mvi, log_str


def annotation_generate(labels:dict, frame_id:int):
    """
    根据传入的 xml 信息和frame_id信息 ，生成 evaluation-service 指定格式

    具体的目标格式为：
    - markResult
		- features ：list
			其中每个 elem 包括：
			- properties 
                - content 
                    - label：str/list，list情况只使用第一个 str
			- geometry 
                - coordinates：[ :4]，返回值为 bbox 的四个点，每个点为（x, y）
    
    return: dict

    notes:
        - 需要保存 ignore region 用于后期删除 prediction 中对应区域的 bounding boxes
        - TODO 后续需要在 evaluation-service 中检查/添加 ignore region 的设定
        - TODO 图片环境的标签不确定是否需要添加
    """
    def elem_create(label, bbox):
        """
        因为目标dict中嵌套过多，通过函数形式实现复用
        params:
            bbox: @left, @top, @width, @height
        """
        content = {'label': label}
        properties = {'content': content}

        coordinates = [
            [bbox[0], bbox[1]],
            [bbox[0] + bbox[2], bbox[1]],
            [bbox[0], bbox[1] + bbox[3]],
            [bbox[0] + bbox[2], bbox[1] + bbox[3]],
        ] 
    
        return {'properties': properties, 'coordinates': coordinates}

    features = []
    frame_info = labels['frames'][frame_id]
    for i, label in enumerate(frame_info['labels']):
        bbox = frame_info['bboxes'][i]
        features.append(elem_create(label, bbox))

    ret = dict()
    ret['markResult'] = {'features': features}

    return ret
    

def data_save(img, label, mvi_name:str, frame_id:int,save_path="new_data"):
    """
    保存文件：
        annotations/{mvi_name}_{frame_id}.json
        images/{mvi_name}_{frame_id}.jpg
    """
    # 创建路径
    label_path = os.path.join(save_path, "annotations")
    data_path = os.path.join(save_path, "data")
    for dir_name in [save_path, label_path, data_path]:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
    
    # 设置文件名
    name = f"{mvi_name}_{frame_id:05}"
    
    # 保存 label
    json_name = name + '.json'
    json_file_path = os.path.join(label_path, json_name)
    with open(json_file_path, 'w') as json_file:
        json.dump(label, json_file)

    # 保存 img
    img_name = name + '.jpg'
    img_file_path = os.path.join(data_path, img_name)
    cv2.imwrite(img_file_path, img)


def frame_index_get(num_all_frames, num_frames):
    step = num_all_frames // num_frames
    ret = list(range(1, num_all_frames, step))

    if len(ret) < num_frames:
        ret.append(num_all_frames - 1)
    return ret


if __name__ == "__main__":
    raw_data_path = 'data\Insight-MVT_Annotation_Train'
    mvi_list, num_frames, _ = get_all_mvi(raw_data_path)

    for mvi_name in tqdm(mvi_list):
        mvi_dict = xml2dict(mvi_name)
        num_all_frames = len(mvi_dict['frames'])

        frame_ids = frame_index_get(num_all_frames, num_frames)
        for frame_id in frame_ids:
            label = annotation_generate(mvi_dict, frame_id)

            img_path = mvi_dict['frames'][frame_id]['frame_path']
            img = cv2.imread(img_path)

            data_save(img, label, mvi_name, frame_id)
