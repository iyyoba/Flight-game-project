# main for the game

import random
import story
import functions
import mysql.connector

#import from functions import get_airport_info, calculate_distance

conn = mysql.connector.connect(
    host='localhost',
    port=3306,
    collation='utf8mb4_unicode_520_ci',
    database='policegame',
    user='eyobtalew',
    password='',
    autocommit=True
)

storyDialog = input('Do you want to read the background story? (Y/N): ')
if storyDialog == 'Y':
    for line in story.getStory():
        print(line)

print('Are you ready to pursue a criminal?, ')
player = input('Enter your name: ')

# for game over and  win
game_over = False
win = False

# starting money(in Euro) and range(in meters)
money = 1000
player_range = 2000

# for the criminal captured

criminal_captured = False

# for all airports

all_airports = functions.get_airports()

# start airport ident

start_airport = all_airports[0]['ident']

# current airport

current_airport = start_airport

# game id

game_id = functions.create_game(money, player_range, start_airport, player, all_airports)

# game loop

while not game_over:
    airport = functions.get_airport_info(current_airport)

    print(f"You are currently at {airport['name']}.")
    print(f"You have USD{money: .0f} and {player_range:.0f}km of range.")

    input("Press Enter to continue...")
    # if airport has goal ask if the player wants to open
    # check goal type and add or subtract money
    goal = functions.check_goal(game_id, current_airport)
    if goal:
        question = input(
            f"Do you want to open lootbox for {"100$ or " if money > 100 else ""}{"50km range" if player_range > 50 else ""}? M = money, R = range, enter to skip: ")
        #if not question == '' # or question == 'R' or question == 'M':
        if not question == '':
            if question == 'M' and money > 100:
                money -= 100
            elif question == 'R' and player_range > 50:
                player_range -= 50
            else:
                print("Insufficient money!")
            if goal['money'] > 0:
                money += goal['money']
                print(f"Congratulations! You found {goal['name']}. That is worth USD{goal['money']}.")
                print(f"You have now USD{money:.0f}.")
            elif goal['money'] == 0:
                win = True
                print(f"Congratulations! You apprehended the criminal. Now go to start.")
            else:
                money = 0
                print(f"Oh darn it! You just got robbed and lost all your money.")
    # pause
    input("Press Enter to continue...")

    # asking to buy range
    if money > 0:
        question2 = input("Do you want to buy range? You can get 2km of 1USD. Enter amount or press enter: ")
        if not question2 == '':
            question2 = float(question2)
            if question2 > money:
                print(f"You dont have enough money! to buy range.")
            else:
                player_range += question2 * 2
                money -= question2
                print(f"You now have USD {money:.0f} and {player_range:.0f}km  of range.")
        #pause
        input("Press Enter to continue...")

    # if no range, game over
    # show airports in range, if none, game over

    airports = functions.airports_in_range(current_airport, all_airports, player_range)
    print(f"You have {len(airports)} airports in range:")
    if len(airports) == 0:
        print("You have no airports in your range.")
        game_over = True
    else:
        print("Airports:")
        for airport in airports:
            ap_distance = functions.calculate_distance(current_airport, airport['ident'])
            print(f'''{airport['name']}, icao: {airport['ident']}, distance: {ap_distance:.0f}km''')
            # ask for destination
            dest = input("Enter destination airport (Please use a correct icao code): ")
            selected_distance = functions.calculate_distance(current_airport, dest)
            player_range -= selected_distance
            functions.update_location(dest, player_range, money, game_id)
            current_airport = dest
            if player_range < 0:
                game_over = True
        # if diamond is found and player is at the start
        if win and current_airport == start_airport:
            #print(f"You won! You have USD{money:.0f} and {player_range:.0f}km  of range left.")
            game_over = True
    # show game result
    print(f"{'You won!' if win else 'You lost!'}")
    print(f"You have USD{money} money left.")
    print(f"You have {player_range}km of range.")
