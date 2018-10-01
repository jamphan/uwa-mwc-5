/*******************************************************************************
 * Copyright (c) 2015 Matthijs Kooijman
 *
 * Permission is hereby granted, free of charge, to anyone
 * obtaining a copy of this document and accompanying files,
 * to do whatever they want with them without any restriction,
 * including, but not limited to, copying, modification and redistribution.
 * NO WARRANTY OF ANY KIND IS PROVIDED.
 *
 * This example transmits data on hardcoded channel and receives data
 * when not transmitting. Running this sketch on two nodes should allow
 * them to communicate.
 * Source: https://github.com/dragino/Lora/tree/master/Lora%20Shield/Examples/lmic-raw-915
 * Tutorial http://wiki.dragino.com/index.php?title=Lora_Shield Example4 -- LMIC-RAW-915
 * Note changes are required to be made in the lmic library as explained in the Tutorial
 *******************************************************************************/

#include <lmic.h>
#include <hal/hal.h>
#include <SPI.h>

#if !defined(DISABLE_INVERT_IQ_ON_RX)
#error This example requires DISABLE_INVERT_IQ_ON_RX to be set. Update \
       config.h in the lmic library to set it.
#endif

// Set to 1 if the mote is connected to a RPi base station
// in which case it will send a Serial frame to the base station
// which will be sent to the central server
#define SERIAL_PUSH_TO_LISTENER 1

// Specify the sensor id
const char *SENSOR_ID = "Lora1";

/* TODO
4.Edit the "main.cpp" to "Set center frequency" on your Raspberry Pi.
change
uint32_t freq = 868100000; //in Mhz! (868.1)
to
uint32_t freq = 915000000; //in Mhz! (915.0)
*/

// How often to send a packet. Note that this sketch bypasses the normal
// LMIC duty cycle limiting, so when you change anything in this sketch
// (payload length, frequency, spreading factor), be sure to check if
// this interval should not also be increased.
// See this spreadsheet for an easy airtime and duty cycle calculator:
// https://docs.google.com/spreadsheets/d/1voGAtQAjC1qBmaVuP1ApNKs1ekgUjavHuVQIXyYSvNc 
#define TX_INTERVAL 4000 

// Pin mapping
const lmic_pinmap lmic_pins = {
    .nss = 10,
    .rxtx = LMIC_UNUSED_PIN,
    .rst = 9,
    .dio = {2, 6, 7},
};


// These callbacks are only used in over-the-air activation, so they are
// left empty here (we cannot leave them out completely unless
// DISABLE_JOIN is set in config.h, otherwise the linker will complain).
void os_getArtEui (u1_t* buf) { }
void os_getDevEui (u1_t* buf) { }
void os_getDevKey (u1_t* buf) { }

void onEvent (ev_t ev) {
}

osjob_t txjob;
osjob_t timeoutjob;
static void tx_func (osjob_t* job);

// Transmit the given string and call the given function afterwards
void tx(const char *str, osjobcb_t func) {
  os_radio(RADIO_RST); // Stop RX first
  delay(1); // Wait a bit, without this os_radio below asserts, apparently because the state hasn't changed yet
  LMIC.dataLen = 0;
  while (*str)
    LMIC.frame[LMIC.dataLen++] = *str++;
  LMIC.osjob.func = func;
  os_radio(RADIO_TX);
  Serial.println("TX");
}

// Enable rx mode and call func when a packet is received
void rx(osjobcb_t func) {
  LMIC.osjob.func = func;
  LMIC.rxtime = os_getTime(); // RX _now_
  // Enable "continuous" RX (e.g. without a timeout, still stops after
  // receiving a packet)
  os_radio(RADIO_RXON);
  Serial.println("RX");
}

static void rxtimeout_func(osjob_t *job) {
  digitalWrite(LED_BUILTIN, LOW); // off
}

static void rx_func (osjob_t* job) {
  // Blink once to confirm reception and then keep the led on
  digitalWrite(LED_BUILTIN, LOW); // off
  delay(10);
  digitalWrite(LED_BUILTIN, HIGH); // on

  // Timeout RX (i.e. update led status) after 3 periods without RX
  os_setTimedCallback(&timeoutjob, os_getTime() + ms2osticks(3*TX_INTERVAL), rxtimeout_func);

  // Reschedule TX so that it should not collide with the other side's
  // next TX
  os_setTimedCallback(&txjob, os_getTime() + ms2osticks(TX_INTERVAL/2), tx_func);

  Serial.print("Got ");
  Serial.print(LMIC.dataLen);
  Serial.println(" bytes");
  Serial.write(LMIC.frame, LMIC.dataLen);
  Serial.println();
  Serial.print("DR=");
  Serial.println(LMIC.datarate); //see region specs eg 2=SF7, 3=SF9
  Serial.print("txpow=");
  Serial.println(LMIC.txpow); //dbM
  Serial.print("rssi=");
  Serial.println(LMIC.rssi);  //dbM ?
  Serial.print("snr=");
  Serial.println(LMIC.snr);
  Serial.println();

  push_to_listener(LMIC.frame, LMIC.rssi);

  // Restart RX
  rx(rx_func);
}

/* Pushes the information to the Listener (RPi) in the correct format
 * F:<SENSOR_ID>,<SENSOR_DATA>,<RSSI>\n
 *
 */
static void push_to_listener(unsigned char *sensor_payload, int rssi)
{

  if (SERIAL_PUSH_TO_LISTENER)
  {
    Serial.print("F:");           // Serial frame header
    Serial.print(SENSOR_ID);
    Serial.print(",");
    Serial.print(sensor_payload); // Sensor data
    Serial.print(",");
    Serial.print(rssi);
    Serial.println("");           // Serial frame terminator
  }

}

static void txdone_func (osjob_t* job) {
  rx(rx_func);
}

// log text to USART and toggle LED
static void tx_func (osjob_t* job) {
  // say hello
  char msg[10]="F:01,50";
  sprintf(msg, "msg:%d", LMIC.rssi);
  tx(msg, txdone_func);
  // reschedule job every TX_INTERVAL (plus a bit of random to prevent
  // systematic collisions), unless packets are received, then rx_func
  // will reschedule at half this time.
  os_setTimedCallback(job, os_getTime() + ms2osticks(TX_INTERVAL + random(500)), tx_func);
}

// application entry point
void setup() {
  Serial.begin(9600); //115200);
  Serial.println("Starting");
  #ifdef VCC_ENABLE
  // For Pinoccio Scout boards
  pinMode(VCC_ENABLE, OUTPUT);
  digitalWrite(VCC_ENABLE, HIGH);

  Serial.println(LMIC.freq); //from http://wiki.dragino.com/index.php?title=Lora_Shield
  
  delay(1000);
  #endif

  pinMode(LED_BUILTIN, OUTPUT);

  // initialize runtime env
  os_init();

  // Set up these settings once, and use them for both TX and RX

  //see also void LMIC_setDrTxpow (dr_t dr, s1_t txpow)
  
  // Use a frequency in the g3 which allows 10% duty cycling.
  // TODO select different frequencies
  LMIC.freq = 915525000;

  // Set data rate and transmit power (note: txpow seems to be ignored by the library)
  // for loraWAN  LMIC_setDrTxpow(DR_SF7,14);
    
  // Maximum TX power use 27;
  //TODO cycle through different txpowers
  LMIC.txpow = 2; //2 to 15
  // Use a medium spread factor. This can be increased up to SF12 for
  // better range, but then the interval should be (significantly)
  // lowered to comply with duty cycle limits as well.
  LMIC.datarate = DR_SF7; //was DR_SF9;  //other choices eg DR_SF7 lowest energy w BW125
  // This sets CR 4/5, BW125 (except for DR_SF7B, which uses BW250)
  LMIC.rps = updr2rps(LMIC.datarate);

  Serial.println("Started");
  Serial.flush();

  // setup initial job
  os_setCallback(&txjob, tx_func);
}

void loop() {
  // execute scheduled jobs and events
  os_runloop_once();
}
