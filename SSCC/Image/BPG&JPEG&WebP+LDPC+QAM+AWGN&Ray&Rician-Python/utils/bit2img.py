"""
bit2img.py
@author Echo
@date 2022-05-13 13:51
@description 单独将txt中的比特流恢复成图片，若恢复的图片不能打开，则转为相应尺寸的噪声图

"""

import glob
import os

import numpy as np
from torchvision.transforms import ToPILImage
import torch
from PIL import Image


def img_to_bit(input_path, output_path):
    """
    将输入路径下的所有图片转为二进制比特流，并保存为txt
    :param input_path: 输入图片路径
    :param output_path: 输出txt路径
    :return: None
    """
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
    with open(output_path, 'w', encoding='utf-8') as f:
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


def get_bitstring(input_path):
    """
    获得比特流
    :param input_path: 图片对应比特流存储的txt路径
    :return: 返回比特流字符串
    """
    with open(input_path, 'r') as f:
        f_context = f.read().strip()  # 读取字符串
        k_char = cut_string(f_context, 1)  # 字符串按8切割
        # int(a, 2)表示将二进制的字符串a表示为十进制的int
        k = [int(a, 2) for a in k_char]  # 字符串转换为int类型的数据
        bit_array = np.array(k)

        bitstring = ''
        for i in bit_array:
            bitstring += str(i)
        return bitstring


def random_noise(nc, width, height):
    """Generator a random noise image from tensor.

    If nc is 1, the Grayscale image will be created.
    If nc is 3, the RGB image will be generated.

    Args:
        nc (int): (1 or 3) number of channels.
        width (int): width of output image.
        height (int): height of output image.
    Returns:
        PIL Image.
    """
    img = torch.rand(nc, width, height)
    img = ToPILImage()(img)
    return img


def bit_to_img(string, img_dir, output_path):
    """
    将比特流字符串重新转换为图片，若转换后的图片无法打开则将之变为一副对应尺寸的随机噪声图
    :param img_dir: 输入图片路径
    :param string: 图片比特流字符串
    :param output_path: 输出图片文件夹路径
    :return: None
    """
    split_char = cut_string(string, 8)  # 字符串按8切割
    # int(a, 2)表示将二进制的字符串a表示为十进制的int
    int_8 = [int(a, 2) for a in split_char]  # 字符串转换为int类型的数据
    out_stream = np.array(int_8, dtype=np.uint8)
    # print(out_stream)
    # print(out_stream.size)
    directory = output_path + '/' + os.path.basename(os.path.dirname(img_dir))
    if not os.path.exists(directory):
        os.makedirs(directory)
    img_output_path = directory + '/' + os.path.basename(img_dir)
    out_stream.tofile(img_output_path)

    try:
        Image.open(img_output_path).convert('RGB')
    except IOError:
        print('Error')
        width = Image.open(img_dir).width
        height = Image.open(img_dir).height
        random_noise(3, width, height).save(img_output_path)


if __name__ == '__main__':

    input_txts = glob.glob(os.path.join('/Users/serendipity/Downloads/stl_original_bit', '**/*.txt'), recursive=True)

    total = len(input_txts)
    for txt_dir in input_txts:
        img_bitstring = get_bitstring(txt_dir)
        output_path = '/Users/serendipity/Downloads/WebP/voc_webp_0.25_bit_ldpc_snr_11dB_2img'
        # 需要找到txt对应原图
        base_dir = '/Users/serendipity/Downloads/WebP/voc_webp_0.25'
        img_dir = base_dir + '/' + txt_dir.split('/')[-2] + '/' + txt_dir.split('/')[-1].split('.')[0] + '.webp'
        bit_to_img(img_bitstring, img_dir, output_path=output_path)
        total = total - 1
        print(total)
