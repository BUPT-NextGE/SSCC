1. 运行huffman_en：对英文文本进行huffman编码，每个字母对应一个码字。使用时修改读、写文件路径。
2. 运行RS-QAM-AWGN&RAY或运行RS-QAM-RICIAN：对huffman编码后的比特进行RS信道编码、16QAM调制，经过AWGN或瑞利衰落信道或莱斯信道，然后解调、信道解码。使用时修改读、写文件路径，可修改RS参数n、k，信噪比snr等。
3. 运行huffman_de：按照huffman编码的码字，对信道解码后的比特进行huffman解码。使用时修改读、写文件路径。