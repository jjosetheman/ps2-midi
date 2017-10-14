// serkey.c
// Read from PS/2 keyboard, write to TTL serial

// Based on keyboard.c
//   for NerdKits with ATmega168
//   hevans@nerdkits.com


//#define F_CPU 14745600

#include <stdio.h>

#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/pgmspace.h>
#include <inttypes.h>

#include <util/delay.h>

#include "softuart.h"
#include "instruments.h"
#include "notemap.h"

//Keyboard pin out
//Green - pin 5 - clock
//Yellow - pin 3 - GND
//White - pin 1 - data
//Red - pin 4 - VCC

//PIN configuration
//PB1 (PCINT1) -  CLK
//PB0           -  DATA

volatile uint8_t kbd_data;
volatile uint8_t char_waiting;
volatile uint8_t up_event, down_event;
volatile uint8_t next_extended, next_otherextended, up_extended, down_extended;
volatile uint8_t key_state[256];
uint8_t started;
uint8_t bit_count;
uint8_t shift;
uint8_t caps_lock;
uint8_t extended;
uint8_t release;

ISR(PCINT0_vect){

  //make sure clock line is low, if not ignore this transition
  if(PINB & (1<<PB1)){
    return;
  }

  //if we have not started, check for start bit on DATA line
  if(!started){
    if ( (PINB & (1<<PB0)) == 0 ) {
      started = 1;
      bit_count = 0;
      kbd_data = 0;
      //printf_P(PSTR("%d"),started);
      return;
    }
  } else if(bit_count < 8) { //we started, read in the new bit
    //put a 1 in the right place of kdb_data if PC2 is high, leave
    //a 0 otherwise
    if(PINB & (1<<PB0)){
      kbd_data |= (1<<bit_count);
    }
    bit_count++;
    return;
  } else if(bit_count == 8){ //pairty bit
    //not implemented
    bit_count++;
    return;
  } else {  //stop bit
    //should check to make sure DATA line is high, what to do if not?
    started = 0;
    bit_count = 0;
  }

  if(kbd_data == 0xF0){ //release code
    release = 1;
    kbd_data = 0;
    return;
  } else if (kbd_data == 0xE0) { //extended code
    next_extended = 1;
    return;
  } else if (kbd_data == 0xE1) { //the other extended code (pause/break)
    next_otherextended = 1;
    return;
/*  } else if ((kbd_data == 0x12) || (kbd_data == 0x59)) { //handle shift key
    if(release == 0){
      shift = 1;
    } else {
      shift = 0;
      release = 0;
    }
    return;*/
  } else { //not a special character
    if(release){ //we were in release mode - exit release mode
      release = 0;
      if (next_otherextended == 1) {
	// it's the damn pause/break key. Attempt to ignore this miserable spawn of satan.   
      } else {
          up_event = kbd_data;
          up_extended = next_extended;
      }
      next_extended = 0;
      next_otherextended = 0;
      key_state[kbd_data] = 0;
    } else { 
      if (next_otherextended == 1) {
   	  // it's the damn pause/break key. Attempt to ignore this miserable spawn of satan.
      } else if (key_state[kbd_data] == 1) {
          // ignore down events if key repeat is occurring 
      } else {
          down_event = kbd_data;
          down_extended = next_extended;
      }
      next_otherextended = 0;
      next_extended = 0;
      char_waiting = 1;
      key_state[kbd_data] = 1;
    }
  }

}

char map_note(uint8_t data, uint8_t extended){
  if (extended) {
      return pgm_read_byte(&(ext_notemap[data]));
  } else {
      return pgm_read_byte(&(notemap[data]));
  }
}

char map_channel(uint8_t data, uint8_t extended){
  if (extended) {
      return pgm_read_byte(&(ext_chanmap[data]));
  } else {
      return pgm_read_byte(&(chanmap[data]));
  }
}

uint8_t read_char(){
  while(!char_waiting){
     //wait for a character
  }
  char_waiting = 0;
  return kbd_data;
}

void init_keyboard()
{
  uint8_t i;

  for (i=0; i<255; i++) {
    key_state[i] = 0;
  }

  started = 0;
  kbd_data = 0;
  bit_count = 0;
  next_extended = 0;
  next_otherextended = 0;
  down_event = 0;
  up_event = 0;

  //make PB1 input pin
  //DDRB &= ~(1<<PB1);
  //turn on pullup resistor
  PORTB |= (1<<PB1);

  //Enable PIN Change Interrupt 1 - This enables interrupts on pins
  GIMSK |= (1<<PCIE);

  //Set the mask on Pin change interrupt 1 so that only PCINT1 (PB1) triggers
  //the interrupt.
  PCMSK |= (1<<PCINT1);
}

void led_init()
{
  // make pb5 an output
  DDRB |= (1<<PB5);
}

void led_on()
{
  PORTB |= (1<<PB5);
}

void led_off()
{
  PORTB &= ~(1<<PB5);
}

int main() {
  int i;

  init_keyboard();

  uartInit();

  led_init();

  //enable interrupts
  sei();

  char chan, note;

  up_event = 0;
  down_event = 0;

  // setup the channels

  for (i=0; i<CHANNEL_COUNT; i++) {
    uartSend(0xC0 + CHANNEL_OFFSET + i);
    uartSend(pgm_read_byte(&(insmap[i]))-1);
  }

  while(1) {
    if (up_event != 0) {
        led_off();
        chan = map_channel(up_event, up_extended);
        note = map_note(up_event, up_extended);
        if (note != 0) {
            uartSend(0x80 + CHANNEL_OFFSET + chan);
            uartSend(note);
            uartSend(0x40);
        }
        up_event = 0;
    }
    if (down_event != 0) {
      led_on();
      chan = map_channel(down_event, down_extended);
      note = map_note(down_event, down_extended);
      if (note != 0) {
	uartSend(0x90 + CHANNEL_OFFSET + chan);
	uartSend(note);
	uartSend(0x40);
      }
      down_event = 0;
    }
  }

  return 0;
}
