jpeg_ldpc_qam_rayleigh.py和jpeg_ldpc_qam_rician.py是JPEG+LDPC+16/64 QAM+Rayleigh/Rician通信模型的python代码。
jpeg_ldpc_qam_rayleigh.py使用瑞利信道，在258-279行设置输入、输出文件路径，调整目标BPP，指定信噪比SNR，指定QAM调制阶数。
jpeg_ldpc_qam_rician.py使用莱斯信道，在256-281行设置输入、输出文件路径，调整目标BPP，指定信噪比SNR，指定QAM调制阶数，设置莱斯信道K因子。

环境配置：
python 3.2 or above
numpy 1.10 or above
scipy 0.15 or above
matplotlib 1.4 or above
nose 1.3 or above
sympy 1.7 or above
