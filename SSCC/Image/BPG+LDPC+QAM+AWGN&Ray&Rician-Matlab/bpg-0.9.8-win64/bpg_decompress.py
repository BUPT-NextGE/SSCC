#对解码出的比特进行bpg解压，恢复图像
from subprocess import run
import os
import numpy as np

def cut(obj, sec):
    return [obj[i:i+sec] for i in range(0,len(obj),sec)]

#读取比特字符串，将其转换为字节流，以便bpg解压
def bit_img(input_path,output_path):
    f = open(input_path,'r')
    f_context = f.read().strip()  #读取字符串
    
    k_char_lis = cut(f_context,8)  #字符串按8切割
    k_int = [int(a,2) for a in k_char_lis]  #字符串转换为int类型的数据
    k = np.array(k_int,dtype=np.uint8)

    #利用numpy的tofile将其保存为字节流，后缀为.bpg文件
    k.tofile(output_path)


root_dir ='D:\\stl_bpg_deldpc_12dB'    #解码出的比特文件
decompress_bpg_root = 'D:\\stl_bpg_decompress'   #为bpg解压后的图像建立文件夹

for item in os.listdir(root_dir):
        
        png_file = decompress_bpg_root + '\\' + item    
        if not os.path.exists(png_file):
                os.makedirs(png_file)
                
        sub_file = root_dir + '\\' + item
        for bit_file in os.listdir(sub_file):
                file_name = sub_file + '\\' + bit_file   #依次读取item文件夹内的比特文件
                #print(file_name)
                decompress_dir = png_file + '\\' + bit_file.replace('bpg_','').replace('.txt','')   #解压后的图像路径

                a = bit_img(file_name,decompress_dir + '.bpg')
                
                run('bpgdec -o ' + decompress_dir + '.png' + ' ' + decompress_dir + '.bpg',shell=True)

        print(item + ' done')
