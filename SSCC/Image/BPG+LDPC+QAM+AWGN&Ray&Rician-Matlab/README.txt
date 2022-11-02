1. 运行bpg-0.9.8-win64文件夹里的bpg_compress.py：得到bpg压缩后的比特，修改文件夹路径名、压缩的质量因子q。
2. 运行LdpcM文件夹里的LDPC_QAM_AWGN.m或LDPC_QAM_rayleigh.m或LDPC_QAM_rician,m：依次经过信道编码、QAM调制、信道、QAM解调、信道解码，得到恢复的比特，修改文件夹路径名，修改block_length、rate、调制阶数、snr等。
3. 运行bpg-0.9.8-win64文件夹里的bpg_decompress.py：得到bpg解压后的图像，修改文件夹路径名。