# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 12:33:06 2024

A program to immitate a variety of daily functions used at an airport for
1P13 Project #1

Luca Iacovelli, Ananyaa Rai, Inaaya Lalani, Anson Liang, Areeb Rahman
Engineering
1P13: Integrated Cornerstone Design Projects
Sam Scott
Fall 2024
"""

import turtle

def passenger_data(txt):
    '''
    Translates a txt file of passenger data to a list of passengers

    Parameters
    ----------
    txt : string
        file name

    Returns
    -------
    passengers : list
        2d list of passengers info

    '''
    file = open(txt)
    
    passengers = []

    ##Loop through each line
    for line in file:
        data = line.split(",")
        passenger = []
        
        ##Loop through each item
        for i in range(len(data)):
            item = data[i].strip()
            
            ##Convert to float reading luggage weight
            if (i == 6):
                item = float(item)
            
            passenger.append(item)
        
        ##Append passenger to main list
        passengers.append(passenger)
    
    file.close()
        
    return passengers

def fleet_data(txt):
    '''
    Translates a txt file of fleet data to a list of planes

    Parameters
    ----------
    txt : string
        file name

    Returns
    -------
    fleet : list
        2d list of fleet info

    '''
    file = open(txt)
    
    fleet = []

    ##Loop through each line
    for line in file:
        data = line.split(",")
        plane = []
        
        ##Loop through each item
        for item in data:
            item = item.strip()
            
            ##Convert to int if reading a number
            if(item.isdigit()):
                item = int(item)
            
            plane.append(item)
        
        ##Append plane to main list
        fleet.append(plane)
    
    file.close()
        
    return fleet

def graphical_Mon46():
    # Creating the screen and initializing the turtle
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 700
    WINDOW_TITLE = "Display Board"
    
    ##Setup window with background color
    turtle.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = turtle.Screen()
    screen.title(WINDOW_TITLE)
    screen.bgcolor("lightblue")
    
    image = "plane.gif"
    screen.addshape(image)

    ##Setup turtle
    t = turtle.Turtle()
    t.shape(image)
    t.hideturtle()
    t.speed(0)

    ##Get data
    passengers = passenger_data("passenger_data_v1.txt")
    fleet = fleet_data("fleet_data.txt")
    
    ##Call each data function
    weight = overweight(passengers, fleet)
    wait = layover(passengers, fleet)
    time = time_delay(passengers, fleet)
    sold = oversold(passengers, fleet, daily_data(passengers, fleet))
    
    t.up()
    t.goto(0, 700/2 - 100)
    t.down()
    t.write("1P13 International Airport", align='center', font=("Arial", 24, "bold"))
    
    ##Starting position for the first display board
    x1, y1 = -SCREEN_WIDTH / 2 + 50, 0
    space_between = 75  ##Space between each display board
    card_size = 200
    
    draw_data = []
    ##Collect all plane data into one 2d list
    for i in range(len(fleet)):
        plane_data = []
        plane_data.append(fleet[i][0])  # Plane Model
        plane_data.append(weight[1][i][1])  # Overweight passengers
        plane_data.append(wait[0][i][1])  # Layover passengers
        plane_data.append(time[i][1])  # Late passengers
        plane_data.append(sold[0][i][1])  # Oversold business
        plane_data.append(sold[1][i][1])  # Oversold economy
        
        draw_data.append(plane_data)
    
    row_counter = 0
    ##Draw each plane card
    for plane in draw_data:  
        if row_counter >= 4:
            row_counter = 0
            y1 -= 220  ##Spacing
            x1 = -SCREEN_WIDTH / 2 + 50
        ##Create card
        t.up()
        t.goto(x1, y1)  
        t.down()
        t.fillcolor("white")
        t.begin_fill()

        ##Drawing the rectangles for the display boards
        t.pensize(2)
        t.pencolor("black")
        for _ in range(2): 
            t.forward(card_size)
            t.left(90)
            t.forward(card_size)
            t.left(90)
        t.end_fill()
        
        ##Writing the data inside the display board
        t.up()
        t.goto(x1 + 10, y1 + 160)
        t.down()
        t.color("darkblue")
        t.write(f"{plane[0]}", font=("Arial", 12, "bold"))
        t.up()
        t.goto(x1 + card_size - 20, y1 + 170)
        t.down()
        t.stamp()

        labels = [
            f"Overweight bags: {plane[1]}",
            f"Layover passengers: {plane[2]}",
            f"Late layover passengers: {plane[3]}",
            f"Oversold business seats: {plane[4]}",
            f"Oversold economy seats: {plane[5]}"
        ]
        
        ##Displaying all data in the card
        y_offset = 140
        for label in labels:
            t.up()
            t.goto(x1 + 10, y1 + y_offset)
            t.down()
            t.color("black")
            t.write(label, font=("Arial", 10, "normal"))
            y_offset -= 20
        
        x1 += card_size + space_between
        row_counter += 1

    t.hideturtle()
    turtle.done()


##Luca
def overweight(passengers, fleet):
    '''
    Counts the number of passengers with overweight luggage on each plane

    Parameters
    ----------
    passengers : list
        list of passengers
    fleet : list
        list of planes

    Returns
    -------
    list
        - a list of passengers who are overweight and by what amount 
        - a list of each plane and their overweight count

    '''
    ##Initialize empty lists
    passenger_weight = []
    fleet_weight = []
    
    for plane in fleet:
        overweight_count = 0
        
        weight_limit = plane[7]
        
        ##Loop through each passenger and compare their weight to the planes maximum weight
        for passenger in passengers:
            weight = passenger[6]
            
            if (plane[4] == passenger[2]):
                ##Append passenger info if overweight
                if (weight > weight_limit):
                    weight_info = [passenger[0], passenger[1], passenger[2], round(weight - weight_limit, 1)]
                    
                    passenger_weight.append(weight_info)
                    ##Track num of overweight passengers
                    overweight_count += 1
        
        fleet_weight.append([plane[0], overweight_count])
    
    return passenger_weight, fleet_weight                
    

##Anson
def time_delay(passenger_data, fleet_data):
    """reports the total number of passengers from all the flights that are going to depart late and layover.
    parameter: passenger_data, fleet_data
    inputs: passenger_data(); fleet_data():
    outputs: produces a 2D list with the plane models and the total number of passengers that will arrive late and have a layover.
    """
    final_delayed_passengers = []

    for plane in fleet_data:
        plane_model = plane[0]  # Plane Number
        plane_gate = plane[4]  # Gate Number
        plane_arrival_status = plane[6]  # Arrival status
        late_passenger_count = 0

        # Check if the plane itself is late
        if plane_arrival_status == "Late":
            for passenger in passenger_data:
                passenger_gate = passenger[2]  # Gate for this passenger's flight
                passenger_arrival_status = passenger[5]  # Arrival status for the passenger
                layover_status = passenger[7]  # Layover status for the passenger

                if passenger_gate == plane_gate and passenger_arrival_status == "Late" and layover_status == "Layover":
                    late_passenger_count += 1

        final_delayed_passengers.append([plane_model, late_passenger_count])

    return final_delayed_passengers

##Ananyaa
def daily_data(passengers,fleet):
    '''
    Counts total number of business and economy seats sold for each plan

    Parameters
    ----------
    passengers : list
        2d list of passengers info

    Returns
    -------
    daily : list
        2d list of total seats sold

    '''
    daily = []
    for plane in fleet:
        gate1 = plane[4] #get gate number
        economy = 0
        business = 0
        for person in passengers:
            gate2 = person[2] #get gate number of person
            if gate1 == gate2: #compare to check if in same flight
                '''check seat type and add to total'''
                seat_type = person[3]
                if seat_type == "E":
                    economy += 1
                elif seat_type == "B":
                    business += 1
       
        daily.append([gate1, business, economy]) #add indivdual gate info to overall list
               
   
    return daily

##Inaaya
def oversold(passenger_data, fleet_data, daily_data):
    '''
    Creates a 2d list of the number of oversold seats in economy and business for each flight

    ***NOTE - passenger_data is not used as fleet_data has the number of each seat type
    and daily_data has the number of sold seats for eahc plane, thus the difference is the
    number of seats oversold
    
    Parameters
    ----------
    passenger_data : 2d list
        List of passengers
    fleet_data : 2d list
        List of plane data
    daily_data : 2d list
        list of seat information for each plane

    Returns
    -------
    oversold_business_seats : 2d list
        list of each plane and the number of oversold busines seats
    oversold_economy_seats : 2d list
        list of each plane and the number of oversold economy seats

    '''
    
     # Initializing empty lists for both oversold business and economy class seats
    oversold_business_seats = []
    oversold_economy_seats = [] 
   
    
    # Finding the plane model and number of availlable business and economy seats in each plane
    for plane in fleet_data:
        model = plane[0]
        available_business_seats = plane[1]
        available_economy_seats = plane[2]
        gate = plane[4]
        
        # Find where the gates are the same in fleet_data and daily_data, and record the number of sold seats for each class in the corresponding plane model
        for seat_info in daily_data:
            if seat_info[0] == gate:
                sold_business_seats = seat_info[1]
                sold_economy_seats = seat_info[2]            
                
                # Calculating how many oversold seats there are
                oversold_business = sold_business_seats - available_business_seats 
                oversold_economy = sold_economy_seats - available_economy_seats 
                
                # If there are oversold seats, append the oversold seats lists, if there are no oversold seats or left over seats, append the list with "0"
                if oversold_business > 0:
                    oversold_business_seats.append([model, oversold_business])
                elif oversold_business <= 0:
                    oversold_business_seats.append([model, 0])
                    
                if oversold_economy > 0:
                    oversold_economy_seats.append([model, oversold_economy])
                elif oversold_economy <= 0:
                    oversold_economy_seats.append([model, 0])
                 
                break 
                 
    return oversold_business_seats, oversold_economy_seats 

##Areeb
def layover(passengers, fleet):
    '''
    Purpose: Tracking number of passengers per plane with layovers while documenting their
    names and gate. 
    Input: List of passenger data and list of fleet data
    Output: 2-D list containing how many passenger with layovers each plane has and another 2-D list 
    containing the first name, last name and gate of each passenger with a layover.
    '''
    plane_layover = [] #contains layover count for each plane
    passenger_layover = [] #contains info on passengers with layovers
    for person_information in passengers: #Goes through each person's info
    
        if person_information[7] == 'Layover': 
            
            temporary_info = [] #Temporary list is intialized to store passenger info
            
            temporary_info.append(person_information[0]) #first name appended to temporary list
            temporary_info.append(person_information[1]) #first letter of last name appended
            temporary_info.append(person_information[2]) #gate appended to temporary list
            passenger_layover.append(temporary_info) #temporary list appended to passenger_layover list
        
        
    for plane_info in fleet: 
        temporary_info = []
        temporary_info.append(plane_info[0]) #plane model appended to temporary list
        temporary_info.append(plane_info[4]) #gate corresponding to plane model appended
        plane_layover.append(temporary_info) #temporary list appended to plane_layover list
    
    
    for layover_info in plane_layover: 
        gate2 = layover_info[1] #gate for each plane is recorded in this variable
        layover_counter = 0 #layover counter initialized
        
        for person_information in passenger_layover: #goes through each passenger with layoer's info
            gate = person_information[2] #gate for each passenger is recorded
            
            if gate in gate2: #Since passenger_layover list only includes passengers with layover each time a certain gate appears in the list, layover counter is added to that specifc plane.
                layover_counter += 1
                
            layover_info[1] = layover_counter #Gate for corresponding plane is replaced by the number of layovers for that plane

    return plane_layover, passenger_layover 


graphical_Mon46()
