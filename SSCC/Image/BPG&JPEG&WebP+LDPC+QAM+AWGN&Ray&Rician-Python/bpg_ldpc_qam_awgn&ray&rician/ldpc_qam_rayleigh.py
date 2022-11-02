"""
@author Echo
@description
LDPC信道编码 -> QAM调制 -> rayleigh信道 -> QAM解调 -> LDPC信道解码
"""

from commpy.channelcoding.ldpc import get_ldpc_code_params, ldpc_bp_decode, triang_ldpc_systematic_encode
import commpy
import numpy as np
import glob
import os
import math
from pathlib import Path

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

def cut_string(obj, sec):
    """
    切割字符串
    :param obj: 输入字符串
    :param sec: 切割的位数
    :return: 切割后的字符串
    """
    return [obj[i:i + sec] for i in range(0, len(obj), sec)]


"""
LDPC信道编码 -> QAM调制 -> rayleigh信道 -> QAM解调 -> LDPC信道解码
"""


def ldpc_qam_rayleigh(input_signal, snr=2, qam_order=16):

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
    h = complex_mat / math.sqrt(2)
    s = modulated_bits * h
    r = commpy.awgn(s, snr)
    bits_with_noise = r / h

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

    # 输入比特txt的目录
    output_txt_path = 'E:\\stl10\\stl_bpg_compress_q10\\test_txt'

    # 输出比特txt的目录
    output_base_path='E:\\stl10\\stl_bpg_compress_q10\\receive_bit'

    # 指定SNR
    snr = 20

    # 指定QAM调制阶数
    qam_order = 16

    input_txts = glob.glob(os.path.join(output_txt_path, '**\\*.txt'), recursive=True)
    total = len(input_txts)
    for txt_dir in input_txts:
        img_bitarray = get_bitarray(txt_dir)
        input_signal = img_bitarray
        output_signal = ldpc_qam_rayleigh(input_signal, snr=snr, qam_order=qam_order)

        bitstring = ''
        for i in output_signal:
            bitstring += str(i)
        output_path = output_base_path
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        file_name = Path(txt_dir).stem + '.txt'
        f = open(output_base_path + '\\' + file_name, 'w')
        f.write(bitstring)

        total = total - 1
        print(total)




