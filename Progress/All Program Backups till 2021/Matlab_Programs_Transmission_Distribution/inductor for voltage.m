Ef=10000;
L=0.004; 
Zc=400; 
n1=[2*Ef 0];
d1=[1 Zc/L]; 
t=0:0.00001:0.0001; 
Et=step(n1,d1,t); 
plot(t,Et,'r'); 
Er=Et-Ef; 
hold on; 
plot(t,Er,'b')
