clc; 
clear all;
 
warning off; 
a=[.004; .006; .009]; 
b=[5.3; 5.5; 5.8]; 
c=[500; 400; 200]; Pd=800;
delp=10;
 
lambda=input('Enter estimated value of lambda='); 
fprintf('\n')
 
disp(['lambda        P1      P2      P3       delta p    delta lambda']) 
 
iter=0;
 
while abs(delp)>=0.001
    iter=iter+1;
    p=(lambda-b)./(2*a); 
    delp=Pd-sum(p);
 
J=sum(ones(length(a),1)./(2*a)); 
dellambda=delp/J;
disp([lambda,     p(1),   p(2),    p(3),    delp,    dellambda])
lambda=lambda+dellambda;
 
end
lambda
 
ptotalcost=sum(c+b.*p+a.*p.^2)
