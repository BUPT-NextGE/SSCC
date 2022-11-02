"""
img2bit.py
@author Echo
@description 将图片数据集中的每张图片转化为相应的比特流txt

"""

import glob
import os
import numpy as np


def img_bit(input_path, output_path):
    file = open(input_path, 'rb')  # 输入bpg压缩后的文件
    file_context = file.read()  # <class 'bytes'>字节流

    tmp_a = []
    bit_all = ''
    for i in file_context:
        tmp_a.append(i)  # int类型的数据
    tmp_b = np.array(tmp_a, dtype=np.uint8)
    for j in tmp_b:
        k = bin(j).replace('0b', '').rjust(8, '0')
        bit_all = bit_all + k
    with open(output_path, "w", encoding='utf-8') as f:
        f.write(bit_all)
        f.close()


def cut_string(obj, sec):
    """
    切割字符串
    :param obj: 输入字符串
    :param sec: 切割的位数
    :return: 切割后的字符串
    """
    return [obj[i:i + sec] for i in range(0, len(obj), sec)]


def get_bitarray(txt_path):
    """
    获得比特流数组
    :param txt_path: 图片对应比特流存储的txt路径
    :return: 返回比特流数组
    """
    with open(txt_path, 'r') as f:
        f_context = f.read().strip()  # 读取字符串
        k_char = cut_string(f_context, 1)  # 字符串按8切割
        # int(a, 2)表示将二进制的字符串a表示为十进制的int
        k = [int(a, 2) for a in k_char]  # 字符串转换为int类型的数据
        bit_array = np.array(k)
        return bit_array


if __name__ == '__main__':

    input_path = '/Users/serendipity/Downloads/stl_original'
    output_path = '/Users/serendipity/Downloads/stl_original_bit'

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    input_images = glob.glob(os.path.join(input_path, '**/*.png'), recursive=True)
    for img_dir in input_images:
        sub_dir = os.path.basename(os.path.dirname(img_dir))
        test_img_name = img_dir.split('/')[-1].split('.')[0]
        directory = output_path + '/' + sub_dir
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_dir = output_path + '/' + sub_dir + '/' + test_img_name + '.txt'
        img_bit(img_dir, file_dir)
        print('{} done'.format(sub_dir))

    print('done')
