#include<lpc214x.h>
void delay(int ss)
{
	unsigned int i,j;
	for(i=0;i<ss;i++)
		for(j=0;j<1000;j++);
}
void dat(char q)									//1.16=RS 1.17=RW 1.18=EN
{
	IO1PIN=0x00050000;
	IO0PIN=q;
	delay(1);
	IO1PIN=0x00010000;
}
void cmd(char s)
{
	IO1PIN=0x00040000;
	IO0PIN=s;
	delay(1);
	IO1PIN=0x00000000;
}
int main()
{
	int b;
	char a[9]=" gowtham";
	PINSEL0=0;
	PINSEL2=0;
	IODIR0=0X000000FF;
	IODIR1=0X00070000;
	IOPIN0=0;
	IOPIN1=0;
	delay(2);
	cmd(0x00000038);
	cmd(0x0000000E);
	cmd(0x00000001);
	cmd(0x00000006);
	cmd(0x00000080);
	while(1)
	{
		for(b=0;b<9;b++)
		{
			dat(a[b]);
			delay(100);
		}
		cmd(0x00000001);
	}
	return 0;
}
