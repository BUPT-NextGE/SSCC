# README

# jpeg_ldpc_qam_awgn.py

> 对输入数据集图片模拟经过 JPEG 压缩并进行 LDPC 信道编码 -> QAM 调制 -> AWGN 信道 -> QAM 解调 -> LDPC 信道解码最后恢复出图片的整套流程
> 

![Untitled](README%2037cc77f8851f4f6b81f584787bad9abd/Untitled.png)

1. 输入图片数据集根父路径
2. 输入的图片格式(后缀名，区分大小写)
3. 输出 JPEG 图片数据集根父路径（未进行 LDPC + QAM + AWGN）
4. 图片对应字节比特流 txt 的目录
5. 输出通过了信道传输的 JPEG 图片数据集根父路径（经过了 LDPC + QAM + AWGN）
6. 指定目标 BPP、SNR、QAM 调制阶数

---

# webp_ldpc_qam_awgn.py

> 对输入数据集图片模拟经过 WebP 压缩并进行 LDPC 信道编码 -> QAM 调制 -> AWGN 信道 -> QAM 解调 -> LDPC 信道解码最后恢复出图片的整套流程
> 

![Untitled](README%2037cc77f8851f4f6b81f584787bad9abd/Untitled%201.png)

1. 输入图片数据集根父路径
2. 输入的图片格式(后缀名，区分大小写)
3. 输出 JPEG 图片数据集根父路径（未进行 LDPC + QAM + AWGN）
4. 图片对应字节比特流 txt 的目录
5. 输出通过了信道传输的 JPEG 图片数据集根父路径（经过了 LDPC + QAM + AWGN）
6. 指定目标 BPP、SNR、QAM 调制阶数

---

# ldpc_qam_awgn.py

> 单独实现了 LDPC信道编码 -> QAM调制 -> AWGN信道 -> QAM解调 -> LDPC信道解码
> 

![Untitled](README%2037cc77f8851f4f6b81f584787bad9abd/Untitled%202.png)

1. 修改输入
2. 指定信噪比和调制阶数

---

# webp_impl.py

> 实现了对图片进行指定 BPP 的 WebP 压缩
> 

![Untitled](README%2037cc77f8851f4f6b81f584787bad9abd/Untitled%203.png)

1. 输入图片数据集根父路径
2. 指定输入的图片格式（即后缀名，区分大小写）
3. 指定输出图片数据集根父路径
4. 指定目标 BPP

---

# jpeg_impl.py

> 实现了对图片进行指定 BPP 的 JPEG 压缩
> 

![Untitled](README%2037cc77f8851f4f6b81f584787bad9abd/Untitled%203.png)

1. 输入图片数据集根父路径
2. 指定输入的图片格式（即后缀名，区分大小写）
3. 指定输出图片数据集根父路径
4. 指定目标 BPP