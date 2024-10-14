"""
get_data：
- 解析获取xml内容
    def _xml2dict
    使用 xmltodict 将 xml 数据导入为 dict 进行解析

- 在image上显示 bbox 效果
    步骤：
        获取 img
        将 bbox 逐个画在 img 上
        显示结果
    目的：检测坐标和 img 的统一
"""

import os
import cv2
import xmltodict
import numpy as np
from pybaseutils import file_utils, image_utils

PATH = r'C:\Users\xuezi\Downloads\UA-DETRAC train\data'
XML_DIRNAME = 'DETRAC-Train-Annotations-XML'
DTAT_DIRNAME = 'Insight-MVT_Annotation_Train'

def xml2dict(mvi_name:str):

    anno_path = os.path.join(PATH, XML_DIRNAME)
    data_path = os.path.join(PATH, DTAT_DIRNAME)

    xml_file = os.path.join(anno_path, mvi_name + ".xml")
    # xml_file = os.path.abspath(xml_file)
    # print(xml_file)
    with open(xml_file, encoding='utf-8') as fd:
        content = xmltodict.parse(fd.read())

    data_mvi_path = os.path.join(data_path, mvi_name)

    content = content['sequence']

    ret = {}
    ret['weather'] = content['sequence_attribute']['@sence_weather']

    ignore_list = []
    for bbox in content['ignored_region']['box']:
        # left, top, width, height
        ignore_list.append([float(i) for i in bbox.values()])
    # ret['ignored_region'] = np.array(ignore_list)
    ret['ignored_region'] = ignore_list

    frame_list = []  # num, bbox: np.array, labels
    for frame in content['frame']:
        frame_info = dict()
        frame_info['frame_id'] = int(frame['@num'])

        img_name = f"img{frame_info['frame_id']:05}.jpg"
        frame_info['frame_path'] = os.path.join(data_mvi_path, img_name)

        labels = []
        bboxes = []
        
        if isinstance(frame['target_list']['target'], dict):
            frame['target_list']['target'] = [frame['target_list']['target']]
        for tgt in frame['target_list']['target']:
            bboxes.append([float(i) for i in tgt['box'].values()])
            labels.append(tgt['attribute']['@vehicle_type'])
        # bboxes = np.array(bboxes)

        frame_info.update({'bboxes': bboxes,'labels': labels})
        frame_list.append(frame_info)

    ret['frames'] = frame_list

    return ret


def img_show(mvi_dict: dict, frame_id:int =0,is_anno:bool =True):
    """
    使用 xml2dict() 获取 dict 展示样本
    - 读取 img
    - 获取 bbox 信息
    - 画图
    - imshow
    """
    curr_frame = mvi_dict['frames'][frame_id]
    img_path = curr_frame['frame_path']
    image = cv2.imread(img_path)

    bboxes = curr_frame['bboxes']
    bboxes = image_utils.rects2bboxes(bboxes)
    # rects2bboxes 计算过程：
    # x1, y1, w, h = rect
    # x2 = x1 + w
    # y2 = y1 + h
    labels = curr_frame['labels']

    image = image_utils.draw_image_bboxes_text(image, bboxes, labels,
                                                color=(255, 0, 0), thickness=2, fontScale=1.0)
    cv2.imshow("img_show", image)
    cv2.waitKey(0)

    return
        

if __name__ == "__main__":
    sample = "MVI_20011"
    ret = xml2dict(mvi_name=sample)
    print(ret.keys())
    img_show(ret)