Ef=10000;
C=0.000000009;
Zc=400; 
n1=[2*Ef/Zc 0];
d1=[1 1/(Zc*C)]; 
t=0:0.00001:0.0001;
It=step(n1,d1,t); 
plot(t,It,'r');
holdon; 
If=Ef/Zc; 
Ir=It-If; 
plot(t,Ir,'b') 
