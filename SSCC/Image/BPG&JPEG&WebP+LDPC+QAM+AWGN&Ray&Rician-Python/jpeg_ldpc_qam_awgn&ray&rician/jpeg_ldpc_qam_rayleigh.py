"""
@author Echo
@description
对输入数据集图片模拟经过JPEG压缩并进行LDPC信道编码 -> QAM调制 -> AWGN信道 -> QAM解调 -> LDPC信道解码最后恢复出图片的整套流程
"""

import glob
import os
import commpy
import numpy as np
import torch
import math
from PIL import Image
from torchvision.transforms import ToPILImage
from commpy.channelcoding.ldpc import get_ldpc_code_params, ldpc_bp_decode, triang_ldpc_systematic_encode


def pillow_encode(img, output_img_path, fmt='JPEG', quality=10):

    img.save(output_img_path, format=fmt, quality=quality)

    filesize = os.path.getsize(output_img_path)
    bpp = filesize * float(8) / (img.size[0] * img.size[1])

    return bpp


def find_closest_bpp(target, img, dir, fmt='JPEG'):
    lower = 0
    upper = 100
    prev_mid = upper
    for i in range(10):
        mid = (upper - lower) / 2 + lower
        if int(mid) == int(prev_mid):
            break
        bpp = pillow_encode(img, dir, fmt=fmt, quality=int(mid))
        if bpp > target:
            upper = mid - 1
        else:
            lower = mid
    return bpp


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
    directory = output_path + '\\' + os.path.basename(os.path.dirname(img_dir))
    if not os.path.exists(directory):
        os.makedirs(directory)
    img_output_path = directory + '\\' + os.path.basename(img_dir)
    out_stream.tofile(img_output_path)

    try:
        Image.open(img_output_path).convert('RGB')
    except IOError:
        print('Error')
        width = Image.open(img_dir).width
        height = Image.open(img_dir).height
        random_noise(3, width, height).save(img_output_path)


def ldpc_qam_awgn(input_signal, snr=2, qam_order=16):

    binary_arr = input_signal

    """
    LDPC信道编码
    """

    # 赋给message_bits作为信道编码的输入
    message_bits = binary_arr

    # 指定LDPC编码文件
    ldpc_design_file = 'E:\\stl10\\1440.720.txt'

    # 从编码文件中获取编码参数
    param = get_ldpc_code_params(ldpc_design_file)

    # 调用编码函数生成LDPC编码后的消息比特, 输入应为一维数组，输出为二维数组
    ldpc_encoded_bits = triang_ldpc_systematic_encode(message_bits, param)

    """
    QAM调制
    """

    # 记录LDPC编码后的二维数组的尺寸便于后面恢复
    first_dimension_length = ldpc_encoded_bits.shape[0]

    # 将二维转为一维
    bits = ldpc_encoded_bits.reshape(-1)

    # 实例化4QAM模型
    qam_model = commpy.QAMModem(qam_order)

    # 利用实例化的QAM模型对比特流进行调制，输入需要为一维数组
    modulated_bits = qam_model.modulate(bits)

    """
   瑞利信道:复高斯法实现
    """
    # 对调制结果通过莱斯信道（指定SNR）
    N = len(modulated_bits)
    m = np.random.randn(N, 1)
    t = np.random.randn(N, 1)

    complex_mat = 1j * m[1, :]
    complex_mat += t[0, :]
    h=complex_mat/math.sqrt(2)
    s=modulated_bits*h
    r = commpy.awgn(s, snr)
    bits_with_noise=r/h


    """
    QAM解调
    """

    # QAM解调
    demodulated_bits = qam_model.demodulate(bits_with_noise, 'hard')

    print(np.array_equal(bits, demodulated_bits))

    """
    LDPC解码
    """

    # 将一维重新恢复为二维
    ldpc_encoded_bits = demodulated_bits.reshape(first_dimension_length, -1)

    # LDPC解码时需要将1变为-1，将0变为1
    ldpc_encoded_bits[ldpc_encoded_bits == 1] = -1
    ldpc_encoded_bits[ldpc_encoded_bits == 0] = 1

    # 将上面的语句合并
    ldpc_decoded_bits = ldpc_bp_decode(ldpc_encoded_bits.reshape(-1, order='F').astype(float), param, 'MSA', 10)[0][:720].reshape(-1, order='F')[:len(message_bits)]

    print(np.array_equal(ldpc_decoded_bits, message_bits))

    return ldpc_decoded_bits


if __name__ == "__main__":

    # 输入图片数据集根父路径
    input_base_path = 'E:\\stl10\\image_test'

    # 输入的图片格式(后缀名，区分大小写)
    input_fmt = 'png'

    # 输出JPEG图片数据集根父路径（未进行LDPC+QAM+AWGN）
    output_base_path = 'E:\\stl10\\stl_jpeg'

    # 图片对应字节比特流txt的目录
    output_txt_path = 'E:\\stl10\\stl_jpeg_bit'

    # 输出通过了信道传输的JPEG图片数据集根父路径（经过了LDPC+QAM+AWGN）
    channelcoded_output_base_path = 'E:\\stl10\\stl_jpeg_with_ldpc_qam_rayleigh'

    # 目标BPP
    target_bpp = 0.9

    # 指定SNR
    snr = 20

    # 指定QAM调制阶数
    qam_order = 16

    """
    完成整套JPEG压缩
    """
    input_images = glob.glob(os.path.join(input_base_path, '**\\*.' + input_fmt), recursive=True)
    total_bpp = 0
    for img_dir in input_images:
        # 加上类别目录
        output_path = output_base_path + '\\' + img_dir.split('\\')[-2]
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        # 输出图片路径(指定到文件名)
        output_img_path = output_path + '\\' + img_dir.split('\\')[-1].split('.')[0] + '.JPEG'
        img = Image.open(img_dir)
        img = img.convert("RGB")
        bpp_per_img = find_closest_bpp(target_bpp, img, output_img_path, fmt='JPEG')
        total_bpp += bpp_per_img
        print(bpp_per_img)

    avg_bpp = total_bpp / len(input_images)
    print('平均bpp: {}'.format(avg_bpp))

    """
    对JPEG压缩后的图片读取字节流，并转换为比特流，存入txt
    """
    if not os.path.exists(output_txt_path):
        os.makedirs(output_txt_path)

    input_images = glob.glob(os.path.join(output_base_path, '**\\*.JPEG'), recursive=True)
    for img_dir in input_images:
        sub_dir = os.path.basename(os.path.dirname(img_dir))
        test_img_name = img_dir.split('\\')[-1].split('.')[0]
        directory = output_txt_path + '\\' + sub_dir
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_dir = output_txt_path + '\\' + sub_dir + '\\' + test_img_name + '.txt'
        img_bit(img_dir, file_dir)
        print('{} done'.format(sub_dir))

    print('done')

    """
    读取对应txt得到比特流数组，并进行LDPC+QAM+AWGN，最后恢复，得到经过JPEG压缩并且通过了LDPC+QAM+AWGN的图片
    """
    input_txts = glob.glob(os.path.join(output_txt_path, '**\\*.txt'), recursive=True)

    total = len(input_txts)
    for txt_dir in input_txts:
        img_bitarray = get_bitarray(txt_dir)
        input_signal = img_bitarray
        output_signal = ldpc_qam_awgn(input_signal, snr=snr, qam_order=qam_order)
        bitstring = ''
        for i in output_signal:
            bitstring += str(i)
        output_path = channelcoded_output_base_path
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        # 需要找到txt对应原图
        base_dir = output_base_path
        img_dir = base_dir + '\\' + txt_dir.split('\\')[-2] + '\\' + txt_dir.split('\\')[-1].split('.')[0] + '.JPEG'
        bit_to_img(bitstring, img_dir, output_path=output_path)
        total = total - 1
        print(total)
