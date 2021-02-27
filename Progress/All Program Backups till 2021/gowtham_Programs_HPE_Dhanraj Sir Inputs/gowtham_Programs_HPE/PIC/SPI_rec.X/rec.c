/*
 * File:   rec.c
 * Author: emb1
 *
 * Created on December 6, 2017, 5:50 PM
 */


#include <xc.h>
#include<htc.h>
#define _XTAL_FREQ 20000000
void cmd(char);
void main(void) {
    unsigned char a;
    TRISC=0x18;
    TRISD=0x00;
    TRISE=0;
    SSPSTAT=0x00;
    SSPCON=0x25;
    RE0=0;
    cmd(0x38);
    cmd(0x01);
    cmd(0x0C);
    cmd(0x06);
    cmd(0x80);
    while(1)
    {
        if(a!=0x01)
        { BF=0;
        SSPOV=0;
        while(SSPIF==0)
            a=SSPBUF;
        RE0=1;
        cmd(a);
        __delay_ms(10);
    }
    else
    {
        RE0=0;
        cmd(0x02);
        __delay_ms(10);
        a=10;
    }
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
