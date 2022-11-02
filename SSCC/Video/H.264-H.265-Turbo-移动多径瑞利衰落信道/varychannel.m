function [hR Df]=channel(m,P,d,v)
hL1=zeros(1,m);%自由传播损耗
hL2=zeros(1,m);%阴影衰落（大尺度衰落）
Ps=zeros(1,m);%大尺度衰落后的功率
hR=zeros(1,m);%瑞利衰落（小尺度衰落）
for j=1:1:m
  hL1(j)=148.1+37.6*log10(d(j));%自由传播损耗模型
  hL2(j)=normrnd(0,8);%阴影衰落损耗
%   hL2(j)=8*0.5;%阴影衰落损耗
  Ps(j)=10^((P(j)-hL1(j)-hL2(j))/10);
  %===瑞利信道模型===%
%   hr=randn(1)+1i*randn(1);
  fc=2*10^9;%中心载波频率
  c=3*10^8;%光速
  Fs=9600;%采样频率
  Ts=1/Fs;%采样间隔
  v(j)=v(j)/3.6;%速度转换 km/h转换成m/s
  Fd=fc/c*v(j);%Doppler频偏，以Hz为单位， 不超过Fs的十分之一
  tau=[0,0.002];%多径延时，以s为单位
  pdf=[0,0];%各径功率，以dB位单位
  hr = comm.RayleighChannel(...
    'SampleRate',Fs, ...
    'PathDelays',tau, ...
    'AveragePathGains',pdf, ...
    'MaximumDopplerShift',Fd);
%   %===计算个车辆的信道增益===%
   hR(j)=Ps(j)*(abs(hr(1))^2);%衰减功率乘以信道系数的平方，1表示传输信号电平
%   hR(j)=Ps(j)*0.5;
end
Df=fc/c*v(j);