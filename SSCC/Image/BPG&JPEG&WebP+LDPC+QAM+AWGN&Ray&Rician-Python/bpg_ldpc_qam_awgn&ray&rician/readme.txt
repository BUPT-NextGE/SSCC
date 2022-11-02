！这份代码还需要完善
1.bpg_compress.py用于信源编码，将png文件进行bpg压缩后输出为比特文件；
2.调制，信道，解调：
ldpc_qam_awgn对应AWGN信道
ldpc_qam_rayleigh对应瑞利信道
ldpc_qam_rician对应莱斯信道
3.bpg_decompress.py对解码出的比特进行bpg解压，恢复图像
在信道部分，比特文件不能批量写入或者读出，之后会修改