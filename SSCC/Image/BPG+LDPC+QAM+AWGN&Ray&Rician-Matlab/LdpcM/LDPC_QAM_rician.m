% LDPC+QAM+Rician channel
clear;

max_decode_iterations = 40;
ldpc_code = LDPCCode(0, 0);
min_sum = 1;
block_length = 1944; % Should be one of 648, 1296, and 1944
rate = 2/3; % Should be one of 1/2, 2/3, 3/4, 5/6
info_length = block_length * rate; %信息位长度
lis = [648*rate,1296*rate,1944*rate]; 

M = 16;         %调制阶数，16QAM、64QAM
snr = 13;       %信噪比
sym_all = 0;
num_err = 0;
%莱斯信道K因子在129行，莱斯信道的定义中，修改参数

in_root_dir = 'E:/stl10/stl_bpg_compress_q10';   %要进行LDPC编码的比特文件
out_root_dir = ['E:/stl10/stl_bpg_deldpc_rician_',num2str(snr),'dB'];   %经过信道编码、调制、awgn、解调、信道解码后的比特文件
mkdir(out_root_dir);

subdir  = dir(in_root_dir);     %根文件夹下的子文件合集
for i = 3 : length(subdir)
    subdirpath = fullfile(in_root_dir, subdir(i).name, '*.txt' );
    txt_list = dir(subdirpath);              % 该子文件夹下找后缀为txt的文件集合

    new_subdir = fullfile(out_root_dir, subdir(i).name);
    mkdir(new_subdir);    %新建解码后的子文件夹
    
    for j = 1 : length(txt_list)
        in_path = fullfile(in_root_dir, subdir(i).name, txt_list(j).name);
        out_path = fullfile(new_subdir,txt_list(j).name);
        [img_bit,len_bit] = get_bit(in_path);  %压缩后生成的比特img_bit及其长度len_bit
        num_block = fix(len_bit/info_length);
        remain_len = mod(len_bit,info_length);
        remain_bit = img_bit(len_bit-remain_len+1:len_bit,1);
        decoded = [];
        num_bit_error = 0;
        for n = 1:num_block
            info_bit = img_bit((n-1)*info_length+1:n*info_length,1);
            decoded_bits = ldpc_qam(ldpc_code,info_bit,block_length, rate,max_decode_iterations,min_sum,M,snr);
            decoded = [decoded;decoded_bits];
            num_bit_error = num_bit_error + biterr(info_bit,decoded_bits);
        end
        if remain_len == 0
            sym_len = (num_block*block_length)/log2(M);  %生成的星座点符号数量
        elseif remain_len <= lis(1)
            a = zeros(lis(1)-remain_len,1);
            new_remain = [remain_bit;a];
            decoded_bits = ldpc_qam(ldpc_code,new_remain,648, rate,max_decode_iterations,min_sum,M,snr);
            sym_len = (num_block*block_length + 648)/log2(M);  %生成的星座点符号数量
        elseif remain_len <= lis(2)
            a = zeros(lis(2)-remain_len,1);
            new_remain = [remain_bit;a];
            decoded_bits = ldpc_qam(ldpc_code,new_remain,1296, rate,max_decode_iterations,min_sum,M,snr);
            sym_len = (num_block*block_length + 1296)/log2(M);  %生成的星座点符号数量
        else
            a = zeros(lis(3)-remain_len,1);
            new_remain = [remain_bit;a];
            decoded_bits = ldpc_qam(ldpc_code,new_remain,1944, rate,max_decode_iterations,min_sum,M,snr);
            sym_len = (num_block*block_length + 1944)/log2(M);  %生成的星座点符号数量
        end
        if remain_len ~= 0
            new_decoded = decoded_bits(1:remain_len,1);
            decoded = [decoded;new_decoded];
            num_bit_error = num_bit_error + biterr(remain_bit,new_decoded);
        end
        
        write_txt(decoded,out_path);
       
        num_err = num_err + num_bit_error;
        sym_all = sym_all + sym_len;
    end
    disp([subdir(i).name,' done'])
end

disp(['误比特数：',num2str(num_err)])
disp(sym_all)


%从txt文件中读取0、1字符串,得到列向量及其长度
function [imgbits,len_bits] = get_bit(f_path)
    f_context = fopen(f_path);
    str = fgetl(f_context);
    len_bits = length(str);
    imgbits = zeros(len_bits,1);
    for i=1:length(str)
        imgbits(i,1) = str2num(str(i));
    end
    fclose(f_context);
end

%对读取出的列向量进行ldpc编码、qam调制、awgn信道、qam解调、ldpc解码，返回解码数据
function decoded_bits = ldpc_qam(ldpc_code,info_bits,block_length, rate,max_decode_iterations,min_sum,M,snr)
    ldpc_code.load_wifi_ldpc(block_length, rate);
    coded_bits = ldpc_code.encode_bits(info_bits);  %info_bits列向量，coded_bits列向量
    x = qammod(coded_bits,M,'InputType','bit','UnitAveragePower',true);
    noiseVar = 1./(10.^(snr/10));

%定义莱斯信道
    function g_t = rician_channel(a,snr) 

    N=4*M+2;      %N根据M计算
    l=length(a);  %符号个数
    n = 1:M;

    Ts = (0.5*10^-3)/l;     %符号时间可以设置
    t0 = 0;
    l=1:l;
    t=(t0+l(1)*Ts):Ts:(t0+l(length(l))*Ts);

    fd=20;      %最大多普勒频移。
    %fd,Ts可以设置，二者与信道衰落类型的联系：
    %最大多普勒频移fd越大，相干时间越小，能容忍的符号时间越短，越容易产生符号间干扰，信号越容易发生快速变化，
    % 若相干时间小于符号时间Ts，这时候的信道就属于快衰落信道（快时变）；反之，则属于慢衰落信道（慢时变）
    omega_d = 2*pi*fd;
    omega_n = omega_d*cos(2*pi*n/N);
    alpha = 0;
    beta_n = n*pi/M;


    %Jakes's Model
    for i=1:length(t)
        gI_t(i) = sum(2*cos(beta_n).*cos((omega_n)*t(i)))+sqrt(2)*cos(omega_d*t(i))*cos(alpha);
        gQ_t(i) = sum(2*sin(beta_n).*cos((omega_n)*t(i)))+sqrt(2)*cos(omega_d*t(i))*sin(alpha);
    end

    %Rayleigh distribution  瑞利分布
    gI_t = gI_t/sqrt(2*sum(gI_t.^2));
    gQ_t = gQ_t/sqrt(2*sum(gQ_t.^2));
    g_t_Rayleigh = (gI_t+1i*gQ_t)*sqrt(length(l)); 

    % Rician fading 莱斯衰落信道
    KdB = 20;       %dB形式的莱斯信道因子
    A = 10^(-KdB/20);                   %A=sqrt(K),K=10lgKdB
    gain = 1/(sqrt(1+10^(-KdB/10)));    %信号乘以这个增益，可以能量归一化
    g_t_Rician = (1+g_t_Rayleigh*A)*gain;
    h=(g_t_Rician/sqrt(sum(abs(g_t_Rician).^2))*sqrt(length(l)));
    s = h.*a;
    r = awgn(s,snr,'measured');     %加高斯噪声，复数
    g_t = r./h;                     %信道估计出h; 
end

    y=rician_channel(x,snr); %信号通过莱斯信道


    llr = qamdemod(y,M,'OutputType','llr','UnitAveragePower',true,'NoiseVariance',noiseVar);
    [decoded_codeword, ~] = ldpc_code.decode_llr(llr, max_decode_iterations, min_sum);
    decoded_bits = double(decoded_codeword(1:ldpc_code.K,1));  %列向量
end

%将列向量写入txt文件
function write_txt(decoded,f_path)
    f_out = fopen(f_path , 'w');
    str_out = '';
    for i = 1:length(decoded)
        str_out = [str_out,num2str(decoded(i,1))];
    end
    fprintf(f_out,'%s\n',str_out);
    fclose(f_out);
end


