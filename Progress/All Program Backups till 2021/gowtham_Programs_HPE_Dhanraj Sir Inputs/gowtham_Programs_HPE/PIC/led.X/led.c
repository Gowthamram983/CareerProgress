/*
 * File:   led.c
 * Author: emb1
 *
 * Created on December 9, 2017, 11:15 AM
 */


#include <xc.h>
#include <htc.h>
#define _XTAL_FREQ 20000000

void main(void) {
    TRISB=0X00; //OUTPUT
    PORTB=0X00; //CLEAR
    while(1)
    {
        PORTB=0XFF;
        __delay_ms(500);
        PORTB=0X00;
        __delay_ms(500);
    }
    return;
}
