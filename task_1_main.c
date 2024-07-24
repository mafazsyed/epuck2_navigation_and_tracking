#include <stdio.h> //Task 1: Exploration
#include <stdlib.h>
#include <string.h>
#include <math.h>

#include "ch.h" // ChibiOS library
#include "hal.h" // Hardware Abstraction Layer library
#include "memory_protection.h" // Memory protection library

 #include <main.h>
 #include "leds.h" // LED control library
 #include "sensors/proximity.h" // Proximity sensor library
 #include "motors.h" // Motor control library
 #include "selector.h"

 #include "epuck1x/uart/e_uart_char.h" //Bluetooth Library
 #include "stdio.h"
 #include "serial_comm.h"

 #define THRESHOLD 250 // ADC value threshold used for determining minimum distance to obstacle
 #define MOTOR_SPEED 600

 // Message bus and synchronization objects
 messagebus_t bus;
 MUTEX_DECL(bus_lock);
 CONDVAR_DECL(bus_condvar);

 int main(void) {
 halInit(); // Initialize the HardwareAbstraction Layer
 chSysInit(); // Initialize ChibiOS
 mpu_init(); // Initialize memory protection unit

 messagebus_init(&bus, &bus_lock, &bus_condvar); // Initialize the message bus
 clear_leds(); // Turn off all LEDs
 proximity_start(0); // Start the proximity sensor
 calibrate_ir(); // Calibrate the infrared sensors
 motors_init(); // Initialize the motors
 char str[100];
 int str_length;
 serial_start();

 while (1) {

 int prox0 = get_calibrated_prox(0); // Prox value for display in serial monitor
 int prox1 = get_calibrated_prox(1);
 int prox2 = get_calibrated_prox(2);
 int prox3 = get_calibrated_prox(3);
 int prox4 = get_calibrated_prox(4);
 int prox5 = get_calibrated_prox(5);
 int prox6 = get_calibrated_prox(6);
 int prox7 = get_calibrated_prox(7);

 str_length = sprintf(str, "Sensor 0: %d\n",prox0); //display value via bluetooth in terminal
 e_send_uart1_char(str, str_length);
 str_length = sprintf(str, "Sensor 1: %d\n",prox1);
 e_send_uart1_char(str, str_length);
 str_length = sprintf(str, "Sensor 2: %d\n",prox2);
 e_send_uart1_char(str, str_length);
 str_length = sprintf(str, "Sensor 3: %d\n",prox3);
 e_send_uart1_char(str, str_length);
 str_length = sprintf(str, "Sensor 4: %d\n",prox4);
 e_send_uart1_char(str, str_length);
 str_length = sprintf(str, "Sensor 5: %d\n",prox5);
 e_send_uart1_char(str, str_length);
 str_length = sprintf(str, "Sensor 6: %d\n",prox6);
 e_send_uart1_char(str, str_length);
 str_length = sprintf(str, "Sensor 7: %d\n",prox7);
 e_send_uart1_char(str, str_length);


 // Read the left and right proximity sensors
 int left_prox = get_calibrated_prox(0) + get_calibrated_prox(1);
 int right_prox = get_calibrated_prox(7) + get_calibrated_prox(6);

 if (left_prox > 175 && right_prox > 175) {

 set_body_led(0); // Turn off Green LED

 //Turn on Red LED
 set_led(LED1, 1);
 set_led(LED3, 1);
 set_led(LED5, 1);
 set_led(LED7, 1);

 // Obstacle on both sides, rotate
 left_motor_set_speed(MOTOR_SPEED);
 right_motor_set_speed(-MOTOR_SPEED);
 // Rotates for 400ms - Around 180 degrees Rotation
 chThdSleepMilliseconds(100);

 prox0 = get_calibrated_prox(0); // Prox value for display in serial monitor
 prox1 = get_calibrated_prox(1);
 prox2 = get_calibrated_prox(2);
 prox3 = get_calibrated_prox(3);
 prox4 = get_calibrated_prox(4);
 prox5 = get_calibrated_prox(5);
 prox6 = get_calibrated_prox(6);
 prox7 = get_calibrated_prox(7);

 str_length = sprintf(str, "Sensor 0: %d\n",prox0); //display value via bluetooth in terminal
 e_send_uart1_char(str, str_length);
 str_length = sprintf(str, "Sensor 1: %d\n",prox1);
 e_send_uart1_char(str, str_length);
 str_length = sprintf(str, "Sensor 2: %d\n",prox2);
 e_send_uart1_char(str, str_length);
 str_length = sprintf(str, "Sensor 3: %d\n",prox3);
 e_send_uart1_char(str, str_length);
 str_length = sprintf(str, "Sensor 4: %d\n",prox4);
 e_send_uart1_char(str, str_length);
 str_length = sprintf(str, "Sensor 5: %d\n",prox5);
 e_send_uart1_char(str, str_length);
 str_length = sprintf(str, "Sensor 6: %d\n",prox6);
 e_send_uart1_char(str, str_length);
 str_length = sprintf(str, "Sensor 7: %d\n",prox7);
 e_send_uart1_char(str, str_length);

 chThdSleepMilliseconds(100);

 prox0 = get_calibrated_prox(0); // Prox value for display in serial monitor
 prox1 = get_calibrated_prox(1);
 prox2 = get_calibrated_prox(2);
 prox3 = get_calibrated_prox(3);
 prox4 = get_calibrated_prox(4);
 prox5 = get_calibrated_prox(5);
 prox6 = get_calibrated_prox(6);
 prox7 = get_calibrated_prox(7);

 str_length = sprintf(str, "Sensor 0: %d\n",prox0); //display value via bluetooth in terminal
 e_send_uart1_char(str, str_length);
 str_length = sprintf(str, "Sensor 1: %d\n",prox1);
 e_send_uart1_char(str, str_length);
 str_length = sprintf(str, "Sensor 2: %d\n",prox2);
 e_send_uart1_char(str, str_length);
 str_length = sprintf(str, "Sensor 3: %d\n",prox3);
 e_send_uart1_char(str, str_length);
 str_length = sprintf(str, "Sensor 4: %d\n",prox4);
 e_send_uart1_char(str, str_length);
 str_length = sprintf(str, "Sensor 5: %d\n",prox5);
 e_send_uart1_char(str, str_length);
 str_length = sprintf(str, "Sensor 6: %d\n",prox6);
 e_send_uart1_char(str, str_length);
 str_length = sprintf(str, "Sensor 7: %d\n",prox7);
 e_send_uart1_char(str, str_length);



 } else if (left_prox > THRESHOLD) {

 set_body_led(0); // Turn off Green LED

 //Turn on Red LED
 set_led(LED1, 1);
 set_led(LED3, 1);
 set_led(LED5, 1);
 set_led(LED7, 1);

 // Obstacle on the left side, turn right
 left_motor_set_speed(-MOTOR_SPEED);
 right_motor_set_speed(MOTOR_SPEED);
 } else if (right_prox > THRESHOLD) {

 set_body_led(0); // Turn off Green LED

 //Turn on Red LED
 set_led(LED1, 1);
 set_led(LED3, 1);
 set_led(LED5, 1);
 set_led(LED7, 1);

 // Obstacle on the right side, turn left
 left_motor_set_speed(MOTOR_SPEED);
 right_motor_set_speed(-MOTOR_SPEED);

 } else {
 // No obstacle, move forward

 //Turn off Red LED
 set_led(LED1, 0);
 set_led(LED3, 0);
 set_led(LED5, 0);
 set_led(LED7, 0);

 set_body_led(1); // Turn on Green LED

 left_motor_set_speed(MOTOR_SPEED); //move forward
 right_motor_set_speed(MOTOR_SPEED);
 }

 // Wait before checking sensors again
 chThdSleepMilliseconds(100);
 }
 }
 #define STACK_CHK_GUARD 0xe2dee396
 uintptr_t __stack_chk_guard = STACK_CHK_GUARD;

 void __stack_chk_fail(void)
 {
 chSysHalt("Stack smashing detected");
 }