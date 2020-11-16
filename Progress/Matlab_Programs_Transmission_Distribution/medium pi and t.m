clc;
clear all;
R=input('Resistance :');
XL=input('Inductive Reactance :');
XC=input('Capacitive Reactance :');
G=input('Conductance :');
length=input('Length of Transmission Line :');
f=input('Frequenc y :' );
Z1= (R+j*XL)*length;
Y1= (G+j*XC)*length;
m=menu('ENTER THE TYPE OF NETWORK','NOMINAL T', 'NOMINAL PI ');
switch m
case {1}
A = 1+(Z1*Y1/2);
B=Z1*(1+(Z1*Y1/4));
C=Y1;
D=A;
otherwise
A = 1+(Z1*Y1/2);
B=Z1;
C=Y1*(1+(Z1*Y1/4));
D=A;
end
TM = [ A B; C D ];
Z1
Y1
TM
