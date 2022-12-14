%RS(5,13) - 16QAM - rician信道 - 解调 - 信道解码
n = 13;  %RS信道编码 - 码长
k = 5;   %RS信道编码 - 信息位长度
m = 4;
q = 16;   %调制阶数
snr = 12;  %信噪比
err = 0; %误码个数
lines=0; %文本行数
BER=0; %误比特率
K=50;%莱斯信道因子,K越大，直射分量功率占比越大
%从txt中读取二进制码  txt最后一行为空
in_path = 'E:/work1huffman/huffman_test1.txt';  %输入的二进制码
out_path = 'E:/work1huffman/huffman_test1_rician.txt';  %输出的二进制码
f_in = fopen(in_path);
f_out = fopen(out_path , 'w');
%如果文件结束，feof()返回非0值，否则返回0
while feof(f_in) ~=1
    str_in = fgetl(f_in);  %fgetl读取时排除换行符, char
    len = length(str_in);
    x0 = [];
    for i=1:len
        x0 = [x0,str2num(str_in(i))];
    end
    p = mod(len,m*k);
    if p > 0
        b = zeros(1,m*k-p);
        x1 = [b,x0];
    else
        x1 = x0;
    end
    len = length(x0);  %x0是输入的二进制码，len是输入长度
    len1 = length(x1);  %x1是为了编码补全后的二进制码，len1是补全后的长度
    y = rs_en(x1,n,k,m);  %RS编码，编码后的列向量
    z = mo_chan_de(y,q,snr,K);  %调制-awgn/ray信道-解调输出，列向量
    de_in = reshape(z,n,length(z)/n).';
    de_out = rs_de(de_in,n,k,m);  %RS解码，*k
    de_T = reshape(de_out.',numel(de_out),1);  %列向量
    bin_T = q2bi(de_T);  %0-15转2进制，得行向量
    bin_out = bin_T(:,(len1-len+1:len1));  %取有效位
    [number_of_errors,bit_error_rate] = biterr(x0,bin_out);
    err = err + number_of_errors;
    lines=lines+1;
    BER=bit_error_rate+BER;
    disp(number_of_errors)
    str_out = '';
    for a = 1:len
        str_out = [str_out,num2str(bin_out(a))];
    end
    fprintf(f_out,'%s\n',str_out);
end
fclose(f_in);
fclose(f_out);
disp(err) %显示误比特数
BER=BER/lines;
disp(['误比特率：',num2str(BER)]) %显示误码率
function r = q2bi(x)
    %x是行向量或列向量
    r = [];
    for j = 1:length(x)
        a = x(j);
        c = [];
        for h = 1:4
            b = floor(a/2^(4-h));
            c = [c,b];
            a = a - b*2^(4-h);
        end
        r = [r,c];  %行向量
    end  
end
function y = rs_en(x,n,k,m)
    %x是行向量0，1；n是码字长度，k是信息码长度，一个符号m=4 bit
    msg = bi2de(reshape(x,m,length(x)/m).','left-msb');  %二进制转0-15的整数，4bit为1个符号
    msg_T = reshape(msg,k,length(msg)/k).';
    msg_gf = gf(msg_T,m);
    en = rsenc(msg_gf,n,k);
    y = reshape((double(en.x)).',length(msg)/k*n,1);  %列向量
end

function b = rician_chan(a,snr,K)
    N = length(a);
    f=randn(N,1);
    t=randn(N,1);
    h=sqrt(K/(K+1)) + sqrt(1/(K+1))*(f+1i*t)/sqrt(2);   %复高斯法实现瑞利信道，再转化成莱斯信道，sqrt(K/(K+1))代表直射分量
    s=a.*h;                                             %经过莱斯衰落信道
    r = awgn(s,snr,'measured');                         % 加高斯噪声 复数
    b = r./h;                                           %信道估计出h
end

function p = mo_chan_de(x,q,snr,K)

    y = qammod(x,q);   %输入是0-15的整数，映射到复数
    yn = rician_chan(y,snr,K);    % 莱斯衰落信道
    p = qamdemod(yn,q);  %解调结果为十进制整数
end
function de_out = rs_de(x,n,k,m)
    a = gf(x,m);
    o = rsdec(a,n,k);
    de_out = double(o.x);
end
