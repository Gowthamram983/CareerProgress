clc
clear all
z=[];
disp('Bus impedance matrix Calculation using building algorithm');
while(1)
    disp(' ')
    disp('1.New node and Reference Node');
    disp('2.New node and Old Node');
    disp('3.Old node and Reference Node');
    disp('4.Old node and Old Node');
    disp('5.Print');
    disp('6.Exit');
    n=input('Enter your choice');
switch(n)
    case 1
        c=input('Enter the impedance value');
        z=c;
    case 2
        c=input('Enter the impedance value');
        d=input('Enter the node to which you want to join');
        y=z;
        z=[z z(:,d);z(d,:) z(d,d)+c];
        i=i+1;
        z;
    case 3
        c=input('Enter the impedance value');
        d=input('Enter the node to which you want to join');
        k=z(d,d)+c;
        z=z-z(:,d)*z(d,:)/k;
        z;
    case 4
        c=input('Enter the impedance value');
        d=input('Enter the node to which you want to join');
        e=input('Enter the node to which you want to join');
        k=z(d,d)+z(e,e)+c-2*z(d,e);
        t=z(:,d)-z(:,e);
        z=z-t*t'/k;
        z;
    case 5
        z;
    case 6
        break;
    otherwise
        disp('Wrong Choice');
 
end
end
