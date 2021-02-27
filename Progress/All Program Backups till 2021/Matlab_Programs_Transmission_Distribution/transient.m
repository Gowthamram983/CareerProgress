clear all
clc
f=input('Enter frequency')
H=input(' momemt of inertia=')
V=input('Enter generator voltage')
Gx=input('Enter line reactance of generator ')
L2x=input('Enter reactance of transmission line 1')
L3x=input('Enter reactance of transmission line2')
L4x=input('Enter reactance of transmission line3')
Pm=input('Enter input real power')
q=input('Enter input reactive power')
disp('prefault conditions')
I=Pm-1*i*q
X1=Gx+((L2x*L3x)/(L2x+L3x))+L4x
E=V+1*i*X1*I;
Pm1=(abs(E)*V)/X1
del0=asin(Pm/Pm1)
disp('fault condition')
Pm2=0;
disp('post fault condition')
X3=Gx+L2x+L4x
Pm3=(abs(E)*V)/X3
delmax=pi-asin(Pm/Pm3)
a=-del0;
b=-Pm3*cos(delmax)
c=b-delmax
delcri=(acos(a-c)/Pm1)
A1=Pm*(delcri-del0)
A2=((-Pm3*cos(delmax))-delmax)-((-Pm3*cos(delcri))-delcri)
if(A1==A2)
disp('system is stable');
else
disp('system is unstable');
end
%critical clearing time
X1c=Gx+L2x+(L3x/2);
Ec=V+1*i*X1c*I;
Pm1c=(abs(Ec)*V)/X1c
delintial=asin(Pm/Pm1c)
delmaxi=pi-delintial
delmaxideg=delmaxi*180/pi;
delcric=acos(Pm/Pm1c)*(delmaxi-delintial)+cos(delmaxideg);
t=sqrt(2*H*(delcric-delintial)/(pi*f*Pm));
display( ' crtical clearing time= ');
disp(t)


