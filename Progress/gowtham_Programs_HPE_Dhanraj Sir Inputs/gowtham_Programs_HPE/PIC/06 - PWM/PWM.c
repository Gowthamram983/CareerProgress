#include<lpc214x.h>

void delay(void);
unsigned int i;

int main()
{
	PINSEL1=0x00000400;			// P0.21-PWM5 Pin of PORT0 as PWM

	/*Configure the PLL block and set the CCLK and PCLK at 60 MHz */
	PLL0CON = 0x01;
	PLL0CFG = 0x24;
	PLL0FEED = 0xAA;
	PLL0FEED = 0x55;
	while(!(PLL0STAT & 0x00000400));
	PLL0CON = 0x03;
	PLL0FEED = 0xAA;
	PLL0FEED = 0x55;
	VPBDIV = 0x01;
	
	/* Setup and initialize the PWM block */
	PWMPCR = 0x00;						// Single Edge PWM Mode
	PWMPR = 60000-1; 					// Resolution of PWM is set at 1 mS
	PWMMR0 = 10; 							// Period of PWM is 10 mS
	PWMMR5 = 1; 							// Pulse width of PWM5 is 1 mS
	PWMMCR = (1<<1); 					// PWMTC is reset on match with PWMMR0
	PWMLER = (1<<5)| (1<<0);	// Update Match Registers PWMMR0 and PWMMR5
	PWMPCR = (1<<13); 				// Enable PWM5 output
	PWMTCR = (1<<1); 					// Reset PWM TC and PWM PR
	PWMTCR = (1<<0)| (1<<3);	// Enable PWM Timer Counters and PWM Mode
	while (1)
	{
		for(i=1;i<11;i++)
		{
			PWMMR5 = i;
			PWMLER = (1<<5); //Update Latch Enable bit for PWMMR5
			delay();
		}
		for(i=10;i>=1;i--)
		{
			PWMMR5 = i;
			PWMLER = (1<<5); //Update Latch Enable bit for PWMMR5
			delay();
		}
	}
	//return 0;
}

void delay(void)
{
	unsigned int j,k;
	for(j=0;j<100;j++)
	{
		for(k=0;k<5000;k++);
	}
}
