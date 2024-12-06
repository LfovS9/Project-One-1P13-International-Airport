"""
A program to active and control a set of mechanisms designed to transfer
luggage between different locations

Luca Iacovelli, Ananyaa Rai, Inaaya Lalani, Anson Liang, Areeb Rahman
Engineering
1P13: Integrated Cornerstone Design Projects
Sam Scott
Fall 2024
"""

ip_address =  "localhost"
project_identifier = 'P3A'
#--------------------------------------------------------------------------------
import sys
sys.path.append('../')
from Common.hardware_project_library import *
from Common.standalone_actuator_lib import *
from Common.barcode_checker import *
bot = qbot()
hardware = True
arm = qarm(project_identifier,ip_address,hardware)
table = servo_table(ip_address,None,hardware)
scanner = barcode_checker()

#--------------------------------------------------------------------------------
# STUDENT CODE BEGINS
#---------------------------------------------------------------------------------


import time

def pick_up():
    '''
    Move arm to pickup position and grip suitcase

    Returns
    -------
    None.

    '''
    arm.move_arm(0.0,-0.446,0.217)
    time.sleep(1)
    arm.control_gripper(45)

def reject():
    '''
    Move arm to reject postion and release suitcase

    Returns
    -------
    None.

    '''
    arm.move_arm(0.0,0.483,0.217)
    time.sleep(1)
    arm.control_gripper(-45)

def drop_off():
    '''
    Move arm to drop off position and release suitcase

    Returns
    -------
    None.

    '''
    arm.move_arm(0.431,-0.166,0.407)
    time.sleep(1)
    arm.control_gripper(-45)

def scan():
    '''
    Scan barcode

    Returns
    -------
    value : boolean
        true if suitcase should be rejected

    '''
    value = scanner.barcode_check()
    
    return value == "Rejection Bin"

def deploy():
    '''
    Spin the rotary actuator to deploy the transfer mechanism

    Returns
    -------
    None.

    '''
    bot.activate_stepper_motor()
    time.sleep(2)
    bot.rotate_stepper_cw(3)

def retract():
    '''
    Spin the rotary actuator to retract the transfer mechanism

    Returns
    -------
    None.

    '''
    bot.activate_stepper_motor()
    time.sleep(2)
    bot.rotate_stepper_ccw(3)

##Initialize and deploy mechanisms
loop =True
deploy()
arm.home()

while loop:
    ##Scan bag and move it to pickup location
    bag = scan()
    table.rotate_table_angle(180)
    time.sleep(1)

    ##Pick up bag
    pick_up()
    time.sleep(1)
    
    ##Select drop off location
    if bag:
        reject()
    else:
        drop_off()


    ##Home arm after dropping off
    arm.home()
    
    ##Check if program should continue
    cont = input("Continue? (Y/N)")
    if (cont.upper() == "N"):
        ##Retract mechanism and end loop
        loop = False
        retract()
        arm.terminate()
    else:
        ##Rotate table for next run
        table.rotate_table_angle(90)

#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------


    

    

