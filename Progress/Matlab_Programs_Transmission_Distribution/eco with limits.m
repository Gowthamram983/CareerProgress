clear all;
clc;
n=input('Enter the number of units:');
pd=input('Enter the load demand:');
for i=1:n
    i
    a(i)=input('Enter the coefficient of pgi^2:');
    b(i)=input('Enter the coefficient of pgi:');
    c(i)=input('Enter the constant coefficient :');
    pgmax(i)=input('Enter the maximum generating limit:');
    pgmin(i)=input('Enter the minimum generating limit:');
end
x=0;y=0;
for i=1:n
    x=x+(b(i)/(2*a(i)));
    y=y+(1/(2*a(i)));
end
lambda=(pd+x)/y
for i=1:n
    pg(i)=(lambda-b(i))/(2*a(i));
end
pg
for i=1:n
    if(pg(i)<pgmin(i))
        k=i;
        pg(i)=pgmin(i);
    else if(pg(i)>pgmax(i))
            k=i;
            pg(i)=pgmax(i);
        end
    end
end
pdnew=pd-pg(k)
x1=0;y1=0;
for i=1:n
    if(i~=k)
        x1=x1+(b(i)/(2*a(i)));
        y1=y1+(1/(2*a(i)));
    end
end
lambdanew=(pdnew+x1)/y1
for i=1:n
    
    if(i~=k)
        pg(i)=(lambdanew-b(i))/(2*a(i));
    end
end
disp('The economic dispatch values:');
pg
cost=0;
costtotal=0;
% for i=1:n
%        cost(i)=c(i)+b(i)*pg(i)+a(i)*pg(i)^2
%        costtotal=costtotal+cost(i)
% end
     ptotalcost=sum(c+b.*pg+a.*pg.^2)
 
