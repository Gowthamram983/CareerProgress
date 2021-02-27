clear all
clc
ydata= [1   1   2   1/(0.1+j*0.3)       j*0.02
        2   2   3   1/(0.15+j*0.5)      j*0.0125
        3   3   1   1/(0.2+j*0.6)       j*0.028]; % transmission line data
elements = max(ydata(:,1));
buses=max(max(ydata(:,2)),max(ydata(:,3)));
ybus=zeros(buses,buses);
% Diagonal elements
    for i=1:buses,
          for m=1:elements,
                  if (ydata(m,2)==i) || (ydata(m,3)==i);
                      ybus(i,i)=ybus(i,i)+ydata(m,4)+ydata(m,5);
                  end
          end
    end
% Off diagonal elements    
    for i=1:elements,
        m=ydata(i,2);
        n=ydata(i,3);
        ybus(m,n)=-1*ydata(i,4);
        ybus(n,m)=ybus(m,n);
    end
    ybus
