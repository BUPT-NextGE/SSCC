#对测试集图像进行bpg压缩，得到压缩后文件，以及压缩后总的比特长度
#q=5：比特长度517774768
#q=10：比特长度409155608
from subprocess import run
import os
import numpy as np

root_dir ='D:\\stl_img\\test'    #测试集图像路径
compress_bpg_root = 'D:\\stl_bpg_compress_q10'   #为bpg压缩后的图像建立文件夹
test_bpg_len = 0

#读取bpg压缩后的文件（字节流）,将其转换为比特流，并存储，返回比特长度
def img_bit(input_path,output_path):
    file = open(input_path, 'rb')   #输入bpg压缩后的文件
    file_context = file.read()  #<class 'bytes'>字节流

    tmp_a = []
    bit_all = ''
    for i in file_context:
        tmp_a.append(i)   #int类型的数据
    tmp_b = np.array(tmp_a,dtype=np.uint8)
    for j in tmp_b:
        k = bin(j).replace('0b','').rjust(8,'0')
        bit_all = bit_all + k
    with open(output_path, "w", encoding='utf-8') as f:
        f.write(bit_all)
        f.close()
    return len(bit_all)

for item in os.listdir(root_dir):
        
        bpg_file = compress_bpg_root + '\\' + item    
        if not os.path.exists(bpg_file):
                os.makedirs(bpg_file)
                
        sub_file = root_dir + '\\' + item
        for pic_name in os.listdir(sub_file):
                file_name = sub_file + '\\' + pic_name   #依次读取item文件夹内的图像
                compress_dir = bpg_file + '\\bpg_' + pic_name.replace('.png','')   #压缩后的图像路径

                #q取值[1,51]，数值越高，压缩率越大，图像质量越差
                #os.system运行时cmd窗口不停闪烁
                #os.system('bpgenc -m 9 -b 8 -q 10 ' + file_name + ' -o ' + compress_dir + '.bpg')
                run('bpgenc -m 9 -b 8 -q 10 ' + file_name + ' -o ' + compress_dir + '.bpg',shell=True)

                #将bpg文件转换为比特流,返回比特流长度
                len_img = img_bit(compress_dir + '.bpg',compress_dir +  '.txt')

                test_bpg_len = test_bpg_len + len_img
                
        print(item + ' done')
        
print(test_bpg_len)

