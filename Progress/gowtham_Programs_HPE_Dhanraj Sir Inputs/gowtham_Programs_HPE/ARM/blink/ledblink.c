#include<lpc214x.h>
void delay()
{
int i,j;
	for( i=0;i<1000;i++)
		for( j=0;j<1000;j++);
}
int main()
{
	//int i;
	PINSEL0=0;
	IODIR0=0x00000001;
	IOCLR0=0x00000001;
	while(1)
	{
		IOSET0=0x00000001;
		delay();
		IOCLR0=0x00000001;
		delay();
	}
	return 0;
}
