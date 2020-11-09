#include<lpc214x.h>
void delay()
{
	int i,j;
	for (i=0;i<1000;i++)
		for(j=0;j<1000;j++);
}
int main()
{
	int a;
	unsigned int val[10]={0x0000003F,0x00000006,0x0000005B,0x0000004F,0x00000066,0x0000006D,0x0000007D,0x00000007,0x0000007F,0x0000006F};
	PINSEL0=0x00000000;
	IODIR0=0x000000FF;
	IOCLR0=0x000000FF;
	while(1)
	{
		for(a=0;a<10;a++)
		{
			IOPIN0=val[a];
			delay();
		}
	}
	return 0;
}
