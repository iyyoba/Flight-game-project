import random
from geopy import distance

import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    port=3306,
    collation = 'utf8mb4_unicode_520_ci',
    database='policegame',
    user='eyobtalew',
    password='',
    autocommit=True
)



# for selection of airports
def get_airports():
    sql = '''SELECT iso_country, ident, name, type, latitude_deg, longitude_deg 
    FROM airport 
    WHERE continent = 'EU'
    AND type='large_airport'
    ORDER by RAND()
    LIMIT 30;'''

    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

    # To get all the goals

def get_goals():
    sql = "SELECT * FROM goal;"
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

# creating new game

def create_game(start_money, p_range, cur_airport, p_name, a_ports):
    sql = "INSERT INTO game (money, player_range, location, screen_name) VALUES (%s, %s, %s, %s);"
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, (start_money, p_range, cur_airport, p_name))
    g_id = cursor.lastrowid

    #add goals / mystery boxes

    goals = get_goals()
    goal_list = []
    for goal in goals:
        for i in range(0, goal['probability'], 1):
            goal_list.append(goal['id'])

    g_ports = a_ports[1:].copy()
    random.shuffle(g_ports)

    for i, goal_id in enumerate(goal_list):
        sql =  "INSERT INTO locations (game, airport, goal) VALUES (%s, %s, %s);"
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, (g_id, g_ports[i]['ident'], goal_id))
    return g_id

# get airport info
def get_airport_info(icao):
    sql = f'''SELECT iso_country, ident, name, latitude_deg, longitude_deg
                FROM airport
                WHERE ident = %s'''
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, (icao,))
    result = cursor.fetchone()
    cursor.close()
    return result

def check_goal(g_id, cur_airport):
    sql = f'''SELECT locations.id, goal, goal.id as goal_id, name, money 
    FROM locations 
    JOIN goal ON goal.id = locations.goal 
    WHERE game = %s 
    AND airport = %s'''
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, (g_id, cur_airport))
    result = cursor.fetchone()
    if result is None:
        return False
    return result


# calculate distance between two airports
def calculate_distance(current, target):
    start = get_airport_info(current)
    end = get_airport_info(target)
    return distance.distance((start['latitude_deg'], start['longitude_deg']),
                             (end['latitude_deg'], end['longitude_deg'])).km
# get airports in range
def airports_in_range(icao, a_locations, p_range):
    in_range = []
    for a_location in a_locations:
        dist = calculate_distance(icao, a_location['ident'])
        if dist <= p_range and not dist == 0:
            in_range.append(a_location)
    return in_range

# update location
def update_location(icao, p_range, u_money, g_id):
    sql = f'''UPDATE game SET location = %s, player_range = %s, money = %s WHERE id = %s'''
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, (icao, p_range, u_money, g_id))

#airports = get_airports()
#create_game(1000, 3000, 'UTOI', 'Frank', airports)







    
