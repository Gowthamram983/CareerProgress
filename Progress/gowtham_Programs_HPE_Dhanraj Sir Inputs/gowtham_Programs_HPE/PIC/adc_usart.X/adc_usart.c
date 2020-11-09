/*
 * File:   adc_usart.c
 * Author: emb1
 *
 * Created on December 6, 2017, 5:09 PM
 */

// CONFIG
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
#define BAUDRATE 9600
#define _XTAL_FREQ 20000000

//void cmd(char);
void transmit(char);
void main(void) {
    int d=0,d0,d1,d2,d3,a,b,c;
    TRISA0=1;
    TRISD=0;
    TRISC6=0;
    TRISE=0;
    RC6=0;
    TXSTA=0x24;
    SPBRG=0x81;
    TXEN=1;
    SPEN=1;
    
    PORTB=0x00;
    PORTC=0x00;
    ADCON0=0xC5;
    ADCON1=0x82;
    __delay_ms(100);
   // RE0=0;
     //       cmd(0x38);
       //     cmd(0x01);
         //   cmd(0x0C);
           // cmd(0x06);
            while(1)
            {
                GO_nDONE=1;
                while(GO_nDONE==1);
                a=ADRESL;
                b=ADRESH;
                b=b*256;
                c=a+b;
                
                d3=c/1000;
                c=c%1000;
                d2=c/100;
                c=c%100;
                d1=c/10;
                d0=c%10;
                
                d3=d3+48;
                d2=d2+48;
                d1=d1+48;
                d0=d0+48;
      //          RE0=0;
    //            cmd(0x80);
                
              /*  RE0=1;
                cmd(d3);
                cmd(d2);
                cmd(d1);
                cmd(d0);
                */
                transmit(d3);
                transmit(d2);
                transmit(d1);
                transmit(d0);
                
            }
    return;
}
/*void cmd(char s)
{
    PORTD=s;
    RE1=0;
    RE2=1;
    __delay_ms(10);
    RE2=0;
}*/
void transmit(char a)
{
    while(TXIF==0);
        TXREG=a;
        TXIF=0;
}