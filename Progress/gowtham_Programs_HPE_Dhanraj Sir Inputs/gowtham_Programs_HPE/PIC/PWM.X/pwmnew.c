/*
 * File:   pwmnew.c
 * Author: emb1
 *
 * Created on December 4, 2017, 4:54 PM
 */
#pragma config FOSC = HS        // Oscillator Selection bits (HS oscillator)
#pragma config WDTE = OFF       // Watchdog Timer Enable bit (WDT disabled)
#pragma config PWRTE = OFF      // Power-up Timer Enable bit (PWRT disabled)
#pragma config BOREN = ON       // Brown-out Reset Enable bit (BOR enabled)
#pragma config LVP = OFF        // Low-Voltage (Single-Supply) In-Circuit Serial Programming Enable bit (RB3 is digital I/O, HV on MCLR must be used for programming)
#pragma config CPD = OFF        // Data EEPROM Memory Code Protection bit (Data EEPROM code protection off)
#pragma config WRT = OFF        // Flash Program Memory Write Enable bits (Write protection off; all program memory may be written to by EECON control)
#pragma config CP = OFF         // Flash Program Memory Code Protection bit (Code protection off)

// #pragma config statements should precede project file includes.
// Use project enums instead of #define for ON and OFF.

#include <xc.h>
#include<htc.h>
#define _XTAL_FREQ 20000000

void main(void) {
    TRISB=0x03;
    TRISC2=0;
    RC2=0;
    CCP1CON=0x0C;
    CCPR1L=0x00;
    CCPR1H=0x00;
    T2CON=0x04;
    PR2=255;
    TMR2=0;
    
    while(1){
        if(RB0==1)
        {
            CCPR1L=0xFE;
        }
        else if (RB1==1)
        {
            CCPR1L=0x0F;
        }
    }
    return;
}
