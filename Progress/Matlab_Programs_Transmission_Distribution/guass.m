clear all
clc
y=[  20.0000-50.0000i -10.0000+20.0000i -10.0000+30.0000i
    -10.0000+20.0000i  26.0000-52.0000i -16.0000+32.0000i
    -10.0000+30.0000i -16.0000+32.0000i  26.0000-62.0000i ]
busdata=[ 1 1   0         0   1.05  1.05   0   0    0   0  0
          2 3 -2.566   -1.102   1     1    0   0    0   0  0
          3 3 -1.386   -0.452   1     1    0   0    0   0  0 ]
n=max(busdata(:,1));
type=busdata(:,2);
p=busdata(:,3);
q=busdata(:,4);
v=busdata(:,5);
qmin=busdata(:,6);
qmax=busdata(:,7);
diff=10;
noofiter=1;
vprev=v;
%while(diff>0.00001 || noofiter==1),
for i=2:n
     sumyv=0;
          for k=1:n,
               sumyv=sumyv+y(i,k)*v(k);
          end
if type(i)==2
    for k=1:n,
    q(i)=-imag(conj(v(i))*sumyv);
    end
    Q=q(i)
    if (q(i)>qmax(i) || q(i)<qmin(i)),
                if (q(i)<qmin(i)),
                    q(i)=qmin(i);
                else
                    q(i)=qmax(i);
                end
                type(i)=3;
    end
end
summyv=0;
          for k=1:n,
              if i~=k
               summyv=summyv+y(i,k)*v(k);
              end
          end         
v(i)=(1/y(i,i))*((p(i)-j*q(i))/conj(v(i))-summyv);
if type(i)==2
    deltaindeg=angle(v(i));
   deltainrad=angle(v(i))*(180/pi);
  a=sqrt((1.04.^2)-(imag(v(i)).^2));
  b=imag(v(i));
 v(i)=a+j*b;
end
end
v
noofiter=noofiter+1;      
diff=max(abs(abs(v) - abs(vprev)));    
vprev=v; 
%end 
'Bus voltages'
 V
