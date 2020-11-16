clc;
clear all;
R=input('Resistance :');
XL=input('Inductive Reactance :');
XC=input('Capacitive Reactance :');
G=input('Conductance :');
length=input('Length of Transmission Line :');
f=input('Frequenc y :');
Z1=  (R+j*XL)*length;
Y1= (G+j*XC)*length;
A = 1;
B = Z1;
C = 0;
D =1;
TM = [ A B; C D ];
Z1
Y1
TM
