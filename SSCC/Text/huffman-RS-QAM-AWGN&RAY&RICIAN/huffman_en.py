import string
import collections
from huffman import codebook as hcode


#huffman
f = open('D:/src/test_src.txt','r',encoding='utf-8')  #要传输的文本
char_count = collections.Counter()
for line in f:
    char_count.update(line[:-1]) #去掉换行符   
f.close()
huffman_code = hcode(char_count.items())  #huffman编码平均码长固定
#{'l': '000', 'o': '01', 'v': '1111', 'e': '001', ' ': '10', '.': '110', 'k': '1110'}

code_huffman = dict((value,key) for key,value in huffman_code.items())
#{'000': 'l', '01': 'o', '1111': 'v', '001': 'e', '10': ' ', '110': '.', '1110': 'k'}


f_src = open('D:/src/test_src.txt','r',encoding='utf-8')  #从英文文本中读、写都用utf-8
f_huffman = open('D:/src_en/huffman.txt','w')
for l in f_src:
    sentence = l[:-1]
    huffman_en = ''.join(huffman_code.get(x,huffman_code[' ']) for x in sentence)
    f_huffman.write(huffman_en + '\n')
    
f_src.close()
f_huffman.close()
