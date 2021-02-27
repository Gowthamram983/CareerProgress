/*
 * File:   LCD_4-bit.c
 * Author: Dhanaraj
 *
 * Created on May 3, 2017, 4:19 PM
 */


#include <xc.h>
#include <htc.h>
#define _XTAL_FREQ 20000000

void lcd_data(char s) {
    RC1 = 0;
    RC2 = 1;
    PORTB = (s & 0xF0); //Send higher nibble
    __delay_ms(10);
    RC2 = 0;
    __delay_ms(20);
    RC1 = 0;
    RC2 = 1;
    PORTB = ((s << 4) & 0xF0); //Send Lower nibble
    __delay_ms(10);
    RC2 = 0;
    __delay_ms(20);
}

void main(void) {
    unsigned char msg[20] = "COIMBATORE";
    TRISB = 0X00;
    TRISC = 0X00;
    PORTB = 0X00;
    PORTC = 0X00;
    __delay_ms(100);

    RC0 = 0;
    lcd_data(0x02);
    lcd_data(0x28);
    lcd_data(0x0E);
    lcd_data(0X01);
    lcd_data(0x06);
    lcd_data(0X80);
    while (1) {
        for (int i = 0; i < 10; i++) {
            RC0 = 1;
            lcd_data(msg[i]);
        }
        RC0 = 0;
        lcd_data(0x02);
    }
    return;
}
