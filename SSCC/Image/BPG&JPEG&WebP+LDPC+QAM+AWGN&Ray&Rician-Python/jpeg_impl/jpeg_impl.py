"""
jpeg_impl.py
@author Echo
@description 对图片进行JPEG压缩

"""


import glob
import os
from PIL import Image


def pillow_encode(img, output_img_path, fmt='JPEG', quality=10):

    img.save(output_img_path, format=fmt, quality=quality)

    filesize = os.path.getsize(output_img_path)
    bpp = filesize * float(8) / (img.size[0] * img.size[1])

    return bpp


def find_closest_bpp(target, img, dir, fmt='JPEG'):
    lower = 0
    upper = 100
    prev_mid = upper
    for i in range(10):
        mid = (upper - lower) / 2 + lower
        if int(mid) == int(prev_mid):
            break
        bpp = pillow_encode(img, dir, fmt=fmt, quality=int(mid))
        if bpp > target:
            upper = mid - 1
        else:
            lower = mid
    return bpp


if __name__ == '__main__':

    # 输入图片数据集根父路径
    input_base_path = '/Users/serendipity/Downloads/stl_original'

    # 输入的图片格式(后缀名，区分大小写)
    input_fmt = 'png'

    # 输出图片数据集根父路径
    output_base_path = '/Users/serendipity/Downloads/stl_original_2'

    # 目标BPP
    target_bpp = 0.9

    input_images = glob.glob(os.path.join(input_base_path, '**/*.' + input_fmt), recursive=True)
    total_bpp = 0
    for img_dir in input_images:
        # 加上类别目录
        output_path = output_base_path + '/' + img_dir.split('/')[-2]
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        # 输出图片路径(指定到文件名)
        output_img_path = output_path + '/' + img_dir.split('/')[-1].split('.')[0] + '.JPEG'
        img = Image.open(img_dir)
        img = img.convert("RGB")
        bpp_per_img = find_closest_bpp(target_bpp, img, output_img_path, fmt='JPEG')
        total_bpp += bpp_per_img
        print(bpp_per_img)

    avg_bpp = total_bpp / len(input_images)
    print('平均bpp: {}'.format(avg_bpp))
