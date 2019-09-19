function [Y] = READ(str)
string1="Encoder";
string2='GRF_F_';
string3='IMU';
text=".txt";
str1=string1+str+text;
str2=string2+str+text;
str3=string3+str+text;
A=importdata(str2);
%B=importdata(str1);
C=importdata(str3);
Y.GRFl=A.data(:,1:4);
Y.GRFr=A.data(:,5:8);
Y.Encr=A.data(:,10)*360/500;
Fi=(A.data(:,11)-8346162)*1.088498166424839e-04;
Fi=rmmissing(Fi);
Fi=Fi/0.22;
[b,a]=butter(2,10/100,'low');
Y.Fi=filtfilt(b,a,Fi);
%Y.T=A.textdata
%Y.encl=B.data(:,1);
Y.IMU=C.data(:,1:3);
end

