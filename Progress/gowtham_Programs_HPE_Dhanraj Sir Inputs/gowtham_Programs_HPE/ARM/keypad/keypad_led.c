#include<lpc214x.h>
void scancol();
void scanrow();
int col=0,row=0;
void delay()
{
	int i,j;
	for(i=0;i<1000;i++)
	for(j=0;j<100;j++);
}
int main()
{
	unsigned int a[4][4]={0x00000000,0x00010000,0x00020000,0x00030000,0x00040000,0x00050000,0x00060000,0x00070000,0x00080000,0x00090000,0x000A0000,0x000B0000,
	0x000C0000,0x000D0000,0x000E0000,0x000F0000};
	PINSEL1=0;
	PINSEL0=0;
	IODIR1=0x00FF0000;//port1
	
		while(1)
		{
			IODIR0=0x000000F0;//port0
			IO0PIN=0;
			while(IOPIN0==0x0000000F);
			scanrow();
			IODIR0=0x0000000F;//dir port0
			IOPIN0=0;//pinval port0
			while(IOPIN0==0x000000F0);
			scancol();
			
			IOPIN0=0;
			delay();
			IOPIN1=a[row][col];
			delay();
		}
return 0;
}

void scanrow()
{
	switch(IOPIN0)
	{
		//int row;
		case 0x00000007:
		row=0;
		break;
		case 0x0000000B:
		row=1;
		break;
		case 0x0000000D:
		row=2;
		break;
		case 0x0000000E:
		row=3;
		break;
	}
}
void scancol()
{
	switch(IOPIN0)
	{
		//int col;
		case 0x00000070:
			col=0;
		break;
		case 0x000000B0:
			col=1;
		break;
		case 0x000000D0:
			col=2;
		break;
		case 0x000000E0:
			col=3;
		break;
		
	}
}