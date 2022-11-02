"""
ldpc_qam_awgn.py
@author Echo
@description
LDPC信道编码 -> QAM调制 -> AWGN信道 -> QAM解调 -> LDPC信道解码
"""

from commpy.channelcoding.ldpc import get_ldpc_code_params, ldpc_bp_decode, triang_ldpc_systematic_encode
import commpy
import numpy as np

"""
LDPC信道编码 -> QAM调制 -> AWGN信道 -> QAM解调 -> LDPC信道解码
"""


def ldpc_qam_awgn(input_signal, snr=2, qam_order=16):

    binary_arr = input_signal

    """
    LDPC信道编码
    """

    # 赋给message_bits作为信道编码的输入
    message_bits = binary_arr

    # 指定LDPC编码文件
    ldpc_design_file = '/Users/serendipity/Documents/Applications/PyCharm/PyCharmProjects/PostGraduate/ImageCompression/ImageCompressionUtils/CommPy/commpy/channelcoding/designs/ldpc/wimax/1440.720.txt'

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
    AWGN信道
    """

    # 对调制结果通过AWGN信道（指定SNR）
    bits_with_noise = commpy.awgn(modulated_bits, snr)

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
    input_signal = np.random.choice((0, 1), 10000)

    output_signal = ldpc_qam_awgn(input_signal, snr=20, qam_order=16)
