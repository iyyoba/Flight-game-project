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

storyDialog = input('\033[36mDo you want to read the background story? (Y/N):\033[0m ')
if storyDialog == 'Y':
    for line in story.getStory():
        print(line)

print('\033[36mAre you ready to pursue a criminal?\033[0m  ')
player = input('\033[36mEnter your name:\033[0m ')

# for game over and  win
game_over = False
win = False

# starting money(in Euro) and range(in meters)
money = 1000
player_range = 1500

# for the criminal captured

criminal_captured = False

# for all airports

all_airports = functions.get_airports()

# start airport ident

start_airport = all_airports[0]['ident']

# current airport

current_airport = start_airport


#random_or_selected = input("\033[36mDo you want to chose a starting airport or  One will be assigned for you... (Y/N):\033[0m ")
#if  random_or_selected == 'N':
   # start_airport = all_airports[0]['ident']
#else:
  #  print("Enter the icao of your starting airport from the list below: ")
   # for airport in all_airports:
       # print(f'''{airport['name']}, icao: {airport['ident']}''')


game_id = functions.create_game(money, player_range, start_airport, player, all_airports)

# game loop

while not game_over:
    airport = functions.get_airport_info(current_airport)

    print(f"You are currently at {airport['name']}.")
    print(f"You have USD{money: .0f} and {player_range:.0f}km of range.")

    #input("\033[36mPress Enter to continue...\033[0m")
    # if airport has goal ask if the player wants to open
    # check goal type and add or subtract money
    goal = functions.check_goal(game_id, current_airport)
    if goal:
        question = input(
            f"\033[36mDo you want to open lootbox for {"100$ or " if money > 100 else ""}{"50km range" if player_range > 50 else ""}? M = money, R = range, enter to skip:\033[0m ")
        prize_opened = False
        if not question == '':
            if question == 'M' and money >= 100:
                money -= 100
                prize_opened = True
            if question == 'M' and money < 100:
                    print("You don't have enough money! You used your range for the purchase!")
            if question == 'R' and player_range < 50:
                        print("You don't have enough range! You used your money for the purchase!")
            elif question == 'R' and player_range > 50:
                player_range -= 50
                prize_opened = True

            if prize_opened:
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
    input("\033[36mPress Enter to continue...\033[0m")

    # asking to buy range
    if money > 0:
        question2 = input("\033[36mDo you want to buy range? You can get 2km of 1USD. Enter amount or press enter:\033[0m ")
        if not question2 == '':
            question2 = float(question2)
            if question2 > money:
                print(f"You dont have enough money! to buy range.")
            else:
                player_range += question2 * 2
                money -= question2
                print(f"You now have USD {money:.0f} and {player_range:.0f}km  of range.")
        #pause
        input("\033[36mPress Enter to continue...\033[0m")

    # if no range, game over
    # show airports in range, if none, game over

    airports = functions.airports_in_range(current_airport, all_airports, player_range)
    print(f"You have {len(airports)} airports in range:")
    if len(airports) == 0:

        game_over = True
    else:
        print("Airports:")
        for airport in airports:
            ap_distance = functions.calculate_distance(current_airport, airport['ident'])
            print(f'''{airport['name']}, icao: {airport['ident']}, distance: {ap_distance:.0f}km''')
            # ask for destination
        dest = input("\033[36mEnter destination airport (Please use a correct icao code):\033[0m ")
        selected_distance = functions.calculate_distance(current_airport, dest)
        player_range -= selected_distance
        functions.update_location(dest, player_range, money, game_id)
        current_airport = dest
        if player_range < 0:
            game_over = True
        # if superhero_pack is found and player is at the start
        if win and current_airport == start_airport:
            print(f"You won! You have USD{money:.0f} and {player_range:.0f}km  of range left.")
            # ask for destination
            dest = input("Enter destination airport (Please use a correct icao code): ")
            selected_distance = functions.calculate_distance(current_airport, dest)
            player_range -= selected_distance
            functions.update_location(dest, player_range, money, game_id)
            current_airport = dest
            if player_range < 0:

             game_over = True
    # show game result
print(f"{'\033[32mYou won!\033[0m' if win else '\033[31mYou lost!\033[0m'}")
print(f"You have USD{money} money left.")
print(f"You have {player_range: .0f}km of range.")
