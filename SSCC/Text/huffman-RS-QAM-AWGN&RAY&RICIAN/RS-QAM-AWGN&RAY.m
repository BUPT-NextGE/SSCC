%RS(5,13) - 16QAM - awgn/ray�ŵ� - ��� - �ŵ�����
n = 13;  %RS�ŵ����� - �볤
k = 5;   %RS�ŵ����� - ��Ϣλ����
m = 4;
q = 16;   %���ƽ���
snr = 0;  %�����
err = 0;
%��txt�ж�ȡ��������  txt���һ��Ϊ��
in_path = 'D:/src_en/huffman.txt';  %����Ķ�������
out_path = 'F:/tra-de-0dB/rs_huffman_new.txt';  %����Ķ�������
f_in = fopen(in_path);
f_out = fopen(out_path , 'w');
%����ļ�������feof()���ط�0ֵ�����򷵻�0
while feof(f_in) ~=1
    str_in = fgetl(f_in);  %fgetl��ȡʱ�ų����з�, char
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
    len = length(x0);  %x0������Ķ������룬len�����볤��
    len1 = length(x1);  %x1��Ϊ�˱��벹ȫ��Ķ������룬len1�ǲ�ȫ��ĳ���
    y = rs_en(x1,n,k,m);  %RS���룬������������
    z = mo_chan_de(y,q,snr);  %����-awgn/ray�ŵ�-��������������
    de_in = reshape(z,n,length(z)/n).';
    de_out = rs_de(de_in,n,k,m);  %RS���룬*k
    de_T = reshape(de_out.',numel(de_out),1);  %������
    bin_T = q2bi(de_T);  %0-15ת2���ƣ���������
    bin_out = bin_T(:,(len1-len+1:len1));  %ȡ��Чλ
    [number_of_errors,bit_error_rate] = biterr(x0,bin_out);
    err = err + number_of_errors;
    disp(number_of_errors)
    str_out = '';
    for a = 1:len
        str_out = [str_out,num2str(bin_out(a))];
    end
    fprintf(f_out,'%s\n',str_out);
end
fclose(f_in);
fclose(f_out);
disp(err)

function r = q2bi(x)
    %x����������������
    r = [];
    for j = 1:length(x)
        a = x(j);
        c = [];
        for h = 1:4
            b = floor(a/2^(4-h));
            c = [c,b];
            a = a - b*2^(4-h);
        end
        r = [r,c];  %������
    end  
end
function y = rs_en(x,n,k,m)
    %x��������0��1��n�����ֳ��ȣ�k����Ϣ�볤�ȣ�һ������m=4 bit
    msg = bi2de(reshape(x,m,length(x)/m).','left-msb');  %������ת0-15��������4bitΪ1������
    msg_T = reshape(msg,k,length(msg)/k).';
    msg_gf = gf(msg_T,m);
    en = rsenc(msg_gf,n,k);
    y = reshape((double(en.x)).',length(msg)/k*n,1);  %������
end
function b = ray_chan(a,snr)
    N = length(a);
    m=randn(N,1);
    t=randn(N,1);
    h=(m+1i*t)/sqrt(2);
    s=a.*h;%��������˥���ŵ�
    r = awgn(s,snr,'measured'); % �Ӹ�˹���� ����
    b = r./h;  %�ŵ����Ƴ�h
end
function p = mo_chan_de(x,q,snr)
    y = qammod(x,q);   %������0-15��������ӳ�䵽����
    yn = awgn(y,snr,'measured');   % AWGN�ŵ�
    %yn = ray_chan(y,snr);    % ����˥���ŵ�
    p = qamdemod(yn,q);  %������Ϊʮ��������
end
function de_out = rs_de(x,n,k,m)
    a = gf(x,m);
    o = rsdec(a,n,k);
    de_out = double(o.x);
end
