function [hR Df]=channel(m,P,d,v)
hL1=zeros(1,m);%���ɴ������
hL2=zeros(1,m);%��Ӱ˥�䣨��߶�˥�䣩
Ps=zeros(1,m);%��߶�˥���Ĺ���
hR=zeros(1,m);%����˥�䣨С�߶�˥�䣩
for j=1:1:m
  hL1(j)=148.1+37.6*log10(d(j));%���ɴ������ģ��
  hL2(j)=normrnd(0,8);%��Ӱ˥�����
%   hL2(j)=8*0.5;%��Ӱ˥�����
  Ps(j)=10^((P(j)-hL1(j)-hL2(j))/10);
  %===�����ŵ�ģ��===%
%   hr=randn(1)+1i*randn(1);
  fc=2*10^9;%�����ز�Ƶ��
  c=3*10^8;%����
  Fs=9600;%����Ƶ��
  Ts=1/Fs;%�������
  v(j)=v(j)/3.6;%�ٶ�ת�� km/hת����m/s
  Fd=fc/c*v(j);%DopplerƵƫ����HzΪ��λ�� ������Fs��ʮ��֮һ
  tau=[0,0.002];%�ྶ��ʱ����sΪ��λ
  pdf=[0,0];%�������ʣ���dBλ��λ
  hr = comm.RayleighChannel(...
    'SampleRate',Fs, ...
    'PathDelays',tau, ...
    'AveragePathGains',pdf, ...
    'MaximumDopplerShift',Fd);
%   %===������������ŵ�����===%
   hR(j)=Ps(j)*(abs(hr(1))^2);%˥�����ʳ����ŵ�ϵ����ƽ����1��ʾ�����źŵ�ƽ
%   hR(j)=Ps(j)*0.5;
end
Df=fc/c*v(j);