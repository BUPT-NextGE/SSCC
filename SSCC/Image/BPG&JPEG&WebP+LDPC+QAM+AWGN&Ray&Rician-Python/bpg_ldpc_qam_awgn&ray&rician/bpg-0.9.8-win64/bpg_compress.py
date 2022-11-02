#对测试集图像进行bpg压缩，得到压缩后文件，以及压缩后总的比特长度
#q=5：比特长度517774768
#q=10：比特长度409155608
from subprocess import run
import os
import numpy as np
import shutil

root_dir ='E:\\stl10\\image_test'    #测试集图像路径
compress_bpg_root = 'E:\\stl10\\1compare\\BPG\\test'   #为bpg压缩后的图像建立文件夹
test_bpg_len = 0


def split_file(src, dst1, dst2):
    '''
    function: 将文件中不同后缀的文件分开到不同文件夹
    example: 区分txt和bpg
    src:str(filefolder)
    dst:str(filefolder)
    '''


    txt = []
    bpg = []
    for f in os.listdir(src):
        if f.endswith('.txt'):
            txt.append(f)
        elif f.endswith('.bpg'):
            bpg.append(f)
    # 创建目标文件夹
    if not os.path.isdir(dst1):
        os.mkdir(dst1)
    if not os.path.isdir(dst2):
        os.mkdir(dst2)
    # 拷贝文件到目标文件夹
    for j in txt:
        _txt = os.path.join(src, j)
        shutil.copy(_txt, dst1)
    for p in bpg:
        _bpg = os.path.join(src, p)
        shutil.copy(_bpg, dst2)

#读取bpg压缩后的文件（字节流）,将其转换为比特流，并存储，返回比特长度
def img_bit(input_path,output_path):
    file = open(input_path, 'rb')   #输入bpg压缩前的文件
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
                compress_dir = bpg_file + '\\' + pic_name.replace('.png','')   #压缩后的图像路径

                #q取值[1,51]，数值越高，压缩率越大，图像质量越差
                #os.system运行时cmd窗口不停闪烁
                #os.system('bpgenc -m 9 -b 8 -q 10 ' + file_name + ' -o ' + compress_dir + '.bpg')
                run('bpgenc -m 9 -b 8 -q 10 ' + file_name + ' -o ' + compress_dir + '.bpg',shell=True)

                #将bpg文件转换为比特流,返回比特流长度
                len_img = img_bit(compress_dir + '.bpg',compress_dir +  '.txt')

                test_bpg_len = test_bpg_len + len_img
                
        print(item + ' done')
        print(test_bpg_len)

#将bpg文件和txt文件分到两个文件夹中
        src = os.path.join(compress_bpg_root,'1')
        dst1 = os.path.join(compress_bpg_root, 'txt_file')
        dst2 = os.path.join(compress_bpg_root, 'bpg_file')
        split_file(src, dst1, dst2);



