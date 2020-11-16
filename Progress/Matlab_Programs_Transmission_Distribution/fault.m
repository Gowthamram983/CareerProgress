clear all;
clc;
clc                     
z=[ 0.1075 0.172 .068 0.0424
    0.172 0.13 0.108 0.068 
    0.068 0.108 0.13 0.082 
    0.0424 0.13 0.082 0.1075];
 
for i=1:4
    i
v(i,1)=input('Enter prefault bus voltage')
end
r=input('Enter fault bus')
Zf=input('Enter fault impedance');
for i=1:4
vn(i)=v(i)-z(i,r)*v(r)/z(r,r);
end
disp('Post fault voltage are')
vn
disp('Fault current If =');
If=v(i)/z(r,r)+Zf

