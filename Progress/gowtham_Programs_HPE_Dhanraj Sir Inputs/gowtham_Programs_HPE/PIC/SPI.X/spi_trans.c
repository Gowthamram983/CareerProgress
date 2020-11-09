/*
 * File:   spi_trans.c
 * Author: emb1
 *
 * Created on December 6, 2017, 5:39 PM
 */


#include <xc.h>
#include <htc.h>
#define _XTAL_FREQ 20000000
void cmd(char);
void main(void) {
    unsigned char a[8]="Gowtham";
    TRISC=0x10;
    TRISD=0x00;
    TRISE=0;
    
    RC3=0;
    RC5=0;
    SSPSTAT=0x80;
    SSPCON=0x20;
    
    RE0=0;
    cmd(0x38);
    cmd(0x01);
    cmd(0x0C);
    cmd(0x06);
    while(1)
    {
        cmd(0x80);
        for(int i=0 ;i<8;i++)
        {
            WCOL=0;
            SSPBUF=a[i];
            RE1=1;
            cmd(a[i]);
            while(SSPIF==0);
            __delay_ms(10);
            SSPIF=0;
        }
        WCOL=0;
        SSPBUF=0x01;
        while(SSPIF==0);
        __delay_ms(20);
        SSPIF=0;
        }
    return;
}
void cmd(char a)
{
    PORTD=a;
    RE1=0;
    RE2=1;
    __delay_ms(10);
    RE2=0;
}