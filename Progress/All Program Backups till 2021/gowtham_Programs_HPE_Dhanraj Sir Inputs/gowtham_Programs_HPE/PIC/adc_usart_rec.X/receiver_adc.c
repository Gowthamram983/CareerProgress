/*
 * File:   receiver_adc.c
 * Author: emb1
 *
 * Created on December 11, 2017, 4:58 PM
 */


#include <xc.h>
#include<htc.h>
#define BAUDRATE 9600
#define _XTAL_FREQ 20000000
void cmd(char);
void main(void) {
    int a,b,c,d=0,d1,d2,d3;
    TRISD=0x00;
    TRISE=0x00;
    TRISC6=0;
    TRISC7=0;
    TXSTA=0x04;
    RCSTA=0x90;
    SPBRG=0x81;
    RE0=0;
    cmd(0x38);
    cmd(0x01);
    cmd(0x0C);
    cmd(0x06);
    while(1)
    {
        
    }
    return;
}
void cmd(char s)
{
    PORTD=s;
    RE1=0;
    RE2=0;
    __
}