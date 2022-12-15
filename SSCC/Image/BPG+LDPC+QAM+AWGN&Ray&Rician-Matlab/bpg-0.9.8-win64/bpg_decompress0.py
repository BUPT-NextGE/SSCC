#对解码出的比特进行bpg解压，恢复图像
from subprocess import run
import os
import numpy as np
import shutil
import cv2 as cv
import math



def psnr(img1, img2):
    mse = np.mean((img1 / 255.0 - img2 / 255.0) ** 2)
    if mse < 1e-10:
        return 100
    psnr = 20 * math.log10(1 / math.sqrt(mse))
    return psnr

def cut(obj, sec):
    return [obj[i:i+sec] for i in range(0,len(obj),sec)]


def split_file(src, dst1, dst2):
    '''
    function: 将文件中不同后缀的文件分开到不同文件夹
    example: 区分txt和bpg
    src:str(filefolder)
    dst:str(filefolder)
    '''


    bpg = []
    jpg = []
    for f in os.listdir(src):
        if f.endswith('.bpg'):
            bpg.append(f)
        elif f.endswith('.jpg'):
            jpg.append(f)
    # 创建目标文件夹
    if not os.path.isdir(dst1):
        os.mkdir(dst1)
    if not os.path.isdir(dst2):
        os.mkdir(dst2)
    # 拷贝文件到目标文件夹
    for j in bpg:
        _bpg = os.path.join(src, j)
        shutil.copy(_bpg, dst1)
    for p in jpg:
        _jpg = os.path.join(src, p)
        shutil.copy(_jpg, dst2)

#读取比特字符串，将其转换为字节流，以便bpg解压
def bit_img(input_path,output_path):
    f = open(input_path,'r')
    f_context = f.read().strip()  #读取字符串
    # f_length = len(f_context)
    # ###output_signal的前218个bit存入字符串head
    # g = open("E:\\stl10\\1BPG_rayleigh\\bpg_head.txt", "r")  # 设置文件对象
    # header = g.read()  # 将txt文件的所有内容读入到字符串str中
    # g.close()  # 将文件关闭
    # b = open("E:\\stl10\\1BPG_rayleigh\\bpg_tail.txt", "r")  # 设置文件对象
    # tail = b.read()  # 将txt文件的所有内容读入到字符串str中
    # b.close()  # 将文件关闭
    #
    # ###
    # f_context = header[:175] + f_context[176:f_context-16] + tail[:]  # 将bitstring前214个bit和后16个用head中的bit替换

    k_char_lis = cut(f_context,8)  #字符串按8切割
    k_int = [int(a,2) for a in k_char_lis]  #字符串转换为int类型的数据
    k = np.array(k_int,dtype=np.uint8)

    #利用numpy的tofile将其保存为字节流，后缀为.bpg文件
    k.tofile(output_path)

snr = 3;
root_dir ='E:\\stl10\\1BPG_protection\\16QAM0.5rate\\1CIFAR_out_txt\\1CIFAR_out_txt3dB'
decompress_bpg_root = 'E:\\stl10\\1BPG_protection\\1CIFAR_q50_out_'+ str(snr) + 'dB'
#root_dir ='E:\\stl10\\1BPG\protection\\1CIFAR_out_txt\\4QAM_out_txt' + str(snr) + 'dB'    #解码出的比特文件id
#decompress_bpg_root = 'E:\\stl10\\1BPG_protection\\symbol_out_decode\\4QAM_out_txt' + str(snr) + 'dB'   #为bpg解压后的图像建立文件夹

for item in os.listdir(root_dir):

        jpg_file = decompress_bpg_root + '\\' + item
        if not os.path.exists(jpg_file):
                os.makedirs(jpg_file)

        sub_file = root_dir + '\\' + item
        for bit_file in os.listdir(sub_file):
                file_name = sub_file + '\\' + bit_file   #依次读取item文件夹内的比特文件
                #print(file_name)
                decompress_dir = jpg_file + '\\' + bit_file.replace('bpg_','').replace('.txt','')   #解压后的图像路径

                a = bit_img(file_name,decompress_dir + '.bpg')
                run('bpgdec -o' + decompress_dir + '.jpg' + ' ' + decompress_dir + '.bpg',shell=True)

        print(item + ' done')

src = os.path.join(decompress_bpg_root, '1')
bpg = []
for f in os.listdir(src):
    if f.endswith('.bpg'):
        bpg.append(f)

for j in bpg:
    _bpg = os.path.join(src, j)
    os.remove(_bpg)

out_path = decompress_bpg_root + "\\jpg_file"
path = "E:\\stl10\\lab_data\\test1\\1"  #源文件
path_list = os.listdir(out_path)
result = 0
count = 0
#path_list.sort() #对读取的路径进行排序
for filename in path_list:
    filename1 = os.path.join(path, filename);
    filename2 = os.path.join(out_path,filename);
    img1=cv.imread(filename1);
    img2=cv.imread(filename2);
    count = count+1;
    result = result + psnr(img1,img2);

result = result/count;
print("result:", result)
