import string
import collections
from huffman import codebook as hcode


def huffman_de(x,code_huffman):
	a = ''
	lis = []
	for i in x:
		a = a+i
		if a in code_huffman.keys():
			lis.append(code_huffman[a])
			a = ''
	sen = ''.join(lis)
	return sen


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


f_en = open('F:/tra-de-15dB/rs_huffman_ray_new_13.txt','r')
f_de = open('F:/tra-sen-15dB/rs_huffman_ray_new_13.txt','w',encoding='utf-8')
for line in f_en:
	x = line[:-1]
	sen = huffman_de(x,code_huffman)
	f_de.write(sen+'\n')
f_en.close()
f_de.close()


