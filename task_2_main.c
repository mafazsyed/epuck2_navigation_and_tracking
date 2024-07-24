// Including Necessary Libraries (Task 2: Object Following)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "ch.h" // ChibiOS library
#include "hal.h" // Hardware Abstraction Layer library
#include "memory_protection.h" // Memory protection library
#include "main.h"
 #include "leds.h" // LED control library
 #include "sensors/proximity.h" // Proximity sensor library
 #include "motors.h" // Motor control library
 #include "selector.h"
 #include "sensors/VL53L0X/VL53L0X.h" //Include distance from sensor

 #define MOTOR_SPEED 700 // Define Motor Speed

 // Message bus and synchronization objects
 messagebus_t bus;
 MUTEX_DECL(bus_lock);
 CONDVAR_DECL(bus_condvar);

 int main(void) {
 halInit();
 chSysInit();
 mpu_init();
 messagebus_init(&bus, &bus_lock, &bus_condvar);

 clear_leds(); // Turn off all LEDs
 proximity_start(0); // Start the proximity sensor
 calibrate_ir(); // Calibrate the infrared sensors
 motors_init(); // Initialize the motors
 VL53L0X_start(); //Start distance sensors

 while (1)
 {
 int detect = 65; //Object detection range
 int prox0 = get_calibrated_prox(0);
 int prox1 = get_calibrated_prox(1);
 int prox2 = get_calibrated_prox(2);
 int prox3 = get_calibrated_prox(3);
 int prox4 = get_calibrated_prox(4);
 int prox5 = get_calibrated_prox(5);
 int prox6 = get_calibrated_prox(6);
 int prox7 = get_calibrated_prox(7);

 // Calculate the distance to objects at front in milimeters
 int distance_to_object_front = VL53L0X_get_dist_mm();

 // Move Epuck Backward if the object is too close
 if (distance_to_object_front < 30)
 {
 set_body_led(0); // Turn off Green LED

 //Turn on Red LED
 set_led(LED1, 1);
 set_led(LED3, 1);
 set_led(LED5, 1);
 set_led(LED7, 1);

 left_motor_set_speed(-700);
 right_motor_set_speed(-700);
 }
 else if (distance_to_object_front < 50)
 // Stop the motors if the object at appropriate distance
 {
 set_body_led(0); // Turn off Green LED

 //Turn on Red LED
 set_led(LED1, 1);
 set_led(LED3, 1);
 set_led(LED5, 1);
 set_led(LED7, 1);

 left_motor_set_speed(0); //stop
 right_motor_set_speed(0);
 }
 else
 {

 //Turn off Red LED
 set_led(LED1, 0);
 set_led(LED3, 0);
 set_led(LED5, 0);
 set_led(LED7, 0);

 set_body_led(1); // Turn on Green LED




 if( prox3 > detect) //for object following
 {
 left_motor_set_speed((MOTOR_SPEED));
 right_motor_set_speed((-MOTOR_SPEED));
 }
 else if( prox4 > detect)
 {
 left_motor_set_speed((-MOTOR_SPEED));
 right_motor_set_speed((MOTOR_SPEED));
 }

 else if( prox2 > detect)
 {
 left_motor_set_speed((MOTOR_SPEED));
 right_motor_set_speed((-MOTOR_SPEED));
 }
 else if( prox5 > detect)
 {
 left_motor_set_speed((-MOTOR_SPEED));
 right_motor_set_speed((MOTOR_SPEED));
 }
 else if( prox1 > detect)
 {
 left_motor_set_speed((MOTOR_SPEED));
 right_motor_set_speed((-MOTOR_SPEED));
 }
 else if( prox6 > detect)
 {
 left_motor_set_speed((-MOTOR_SPEED));
 right_motor_set_speed((MOTOR_SPEED));
 }
 else if( prox0 > detect)
 {
 left_motor_set_speed((MOTOR_SPEED));
 right_motor_set_speed((0*MOTOR_SPEED));
 }

 else if( prox7 > detect)
 {
 left_motor_set_speed((0*MOTOR_SPEED));
 right_motor_set_speed((MOTOR_SPEED));
 }

 else if (distance_to_object_front > 50 && distance_to_object_front < 160 )
 // Start the motors forward if the object at appropriate distance
 {
 left_motor_set_speed((MOTOR_SPEED));
 right_motor_set_speed((MOTOR_SPEED));
 }

 else
 {
 left_motor_set_speed((0*MOTOR_SPEED)); //stop e-puck2 if object not detected
 right_motor_set_speed((0*MOTOR_SPEED));
 }


 }

 // LED blinking for visual feedback

 // set_body_led(1);

 // Wait before checking sensors again
 chThdSleepMilliseconds(50);
 }
 }
 #define STACK_CHK_GUARD 0xe2dee396
 uintptr_t __stack_chk_guard = STACK_CHK_GUARD;

 void __stack_chk_fail(void)
 {
 chSysHalt("Stack smashing detected");
 }