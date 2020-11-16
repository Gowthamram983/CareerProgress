Ef=10000; 
C=0.000000009; 
Zc=400; 
n1=[2*Ef/(Zc*C)]; 
d1=[1 1/(Zc*C)];
t=0:0.00001:0.0001;
Et=step(n1,d1,t); 
plot(t,Et,'r'); 
Er=Et-Ef; 
holdon; 
plot(t,Er,'b') 
