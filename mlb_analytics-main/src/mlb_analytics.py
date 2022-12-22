from turtle import left
from numpy import NaN, int64
from numpy import subtract as sub
import numpy as np
import pandas as pd 
from pandas import DataFrame as df
import glob
import math
import matplotlib.pyplot as plt
import itertools
import random
import csv


envrc_loc = glob.glob('~/**/.envrc', recursive = True)
#1)Reroute abs_path
abs_path = '''/mnt/d/Programming/blake_ubuntu_data/conda_development/mlb_analytics/data/Statcast_2017.csv'''

mlb_data = pd.read_csv(abs_path, sep=',', index_col=False, dtype='unicode', na_values=0)

mlb_data.fillna(0, inplace=True)

###Function Utility:  Calculate the mean of given inputs.
def mean_func(input_list):

    return sum(input_list)/len(input_list)

###Function Utility: Calculate sigma of given inputs.
def sum_of_squares(input_list):

    xi_squared_list = [(x-mean_func(input_list))**2 for x in input_list]
    return sum(xi_squared_list)

def sum_of_unsquares(input_list):

    xi_squared_list = [(x-mean_func(input_list)) for x in input_list]
    return sum(xi_squared_list)
    
###Function Utility: Calculate variance of given inputs.
def variance(input_list):

    variance = sum_of_squares(input_list) * (1/(len(input_list)-1))
    return variance

def standard_deviation(input_list):

    data_set = input_list
    count = len(data_set)
    standard_deviation = ((sum_of_squares(data_set))/(count -1))**0.5
    return standard_deviation

###Function Utility: Determine if the pitch was an "inside" or "outside" pitch.
def inside_outside(ball_position, batter_handedness):

    ball_position = float(ball_position)
    if ball_position < 0:

        if batter_handedness == "R":

            pitch = "inside_pitch" 
        elif batter_handedness == "L":

            pitch = "outside_pitch"
        return pitch
            
    if ball_position > 0:

        if batter_handedness == "R":

            pitch = "outside_pitch"
        elif batter_handedness == "L":

            pitch = "inside_pitch"
        return pitch

inside_or_outside = []

for i,s in enumerate(mlb_data["stand"].values):

    inside_or_outside.append(inside_outside(mlb_data['plate_x'][i], mlb_data['stand'][i]))

###Function Utility: Filter all NaN values from sampled dataset.

h_y = [float(y) for y in mlb_data['hc_y'].values]

h_x = [float(x) for x in mlb_data['hc_x'].values]

home_teams = [item for item in mlb_data["home_team"]]

h_coords = list(zip(h_x, h_y))

h_coords_with_teams = list(zip(home_teams, h_coords))

shifts_x = [12,456,12,534,123]

shifts_y = [-324,6,123,6,-43]

shift_x = 12

shift_y = -324

shift_coord = [shift_x,shift_y]

shifts_list = [shifts for shifts in zip(shifts_x,shifts_y)]

shifted_coords_arr = []

coords = [(x,y) for x,y in zip(h_x,h_y)]

converted_coords = []

def convert_to_float(data_list):
    
    for (item1,item2) in data_list:

        x,y = (item1,item2)
        converted_coords.append((float(x),float(y)))

###Function Utility: Find the change in coordinates after being shifted.

def coordinate_reference_shift(converted_coords,shift):

    shifted_coords = converted_coords[0]-shift[0],converted_coords[1]-shift[1]
    return shifted_coords

h_coords_shifted = [coordinate_reference_shift(shift_coord,coord) for coord in h_coords]

for iter,(item1,item2) in enumerate(zip(converted_coords,shifts_list)):

    coordinate_reference_shift(item1,item2)

coords_in = (100,300)

x1_shift = 10

y1_shift = -180

###Function Utility: Find the change in coordinates after being shifted #2.

def coordinate_reference_shift__2(coords_in,x_shift,y_shift):

    coords_out = (coords_in[0] - x_shift , coords_in[1] - y_shift) 
    return (coords_out)

coordinate_reference_shift__2(coords_in, x1_shift,y1_shift)

###Function Utility: Find the angle of a hit ball 

final_distance_coords = [(item1,item2) for item1,item2 in zip(h_x,h_y) if item1 and item2 != 0.0]

# print(len(final_distance_coords))

assigned_final_hit_coords = []

for item1,item2 in zip(mlb_data['home_team'],final_distance_coords):

    if item1 != 0.0 and item2 !=0:

        assigned_final_hit_coords.append((item1,item2))


unpacked_fdc = []

init_plate_coords = [item2 for item1,item2 in enumerate(zip(mlb_data['plate_x'],mlb_data['plate_z']))]

unpacked_ipc = []

for iter, items in enumerate(zip(final_distance_coords,init_plate_coords)):

    finals,inits = items
    a=float(finals[0])
    b=float(finals[1])
    c=float(inits[0])
    d=float(inits[1])

    if a and b and c and d != 0.0:

        unpacked_fdc.append((a,b))
        unpacked_ipc.append((c,d))

# def thetas(a_tuple):

#     adj,opp = a_tuple
#     hyp = (adj**2+opp**2)**0.5
#     theta = math.degrees(math.acos(adj/hyp))
#     return theta

# def get_thetas(a_tuple):

#     x,y = a_tuple
#     angle_calculations=(thetas((x,y)))
#     return angle_calculations

# calculated_theta_array = [get_thetas(coords) for team,coords in assigned_final_hit_coords]


###**********************************************************************
##Function Utility: Find the distance of a hit ball

def get_distance(tuple_1,tuple_2):
        
        dx1,dy1 = tuple_1
        dx2,dy2 = tuple_2
        dxi = dx2 - dx1
        dyi = dy2 - dy1
        dz = (dxi**2 + dyi**2)**0.5
        return dz
        
park_leftfield_rightfield = [

    ("BAL",(333,318),(7,703),(1879,742),(965,1658)),
    ("BOS",(310,302),(5,771),(1711,779),(864,1625)),
    ("TB",(315,322),(23,755),(1825,731),(912,1641)),
    ("NYY",(318,314),(6,726),(1738,737),(878,1595)),
    ("TOR",(328,328),(14,671),(1852,670),(932,1591)),
    ("PHI",(329,330),(2,684),(1820,690),(915,1593)),
    ("MIA",(344,335),(15,661),(1928,687),(985,1633)),
    ("ATL", (334, 325),(10,663),(1896,703),(973,1631)),
    ("NYM",(335,330),(15,721),(2005,745),(1019,1729)),
    ("WSH",(337,335),(16,688),(1933,680),(972,1641)),
    ("CHC",(355,353),(9,617),(2064,629),(1044,1655)),
    ("CIN",(328,325),(10,684),(1844,663),(918,1589)),
    ("MIL",(344,345),(12,604),(1963,591),(983,1571)),
    ("PIT",(325,320),(5,694),(1876,704),(948,1633)),
    ("STL",(336,335),(15,662),(1970,660),(993,1638)),
    ("CWS",(330,334),(17,686),(1919,681),(968,1634)),
    ("CLE",(339,328),(27,682),(1986,699),(1017,1669)),
    ("DET",(345,330),(8,769),(1888,794),(962,1720)),
    ("KC",(330,330),(19,728),(1812,731),(920,1624)),
    ("MIN",(339,328),(28,681),(1987,701),(1017,1671)),
    ("HOU",(315,326),(17,918),(1922,874),(952,1848)),
    ("OAK",(330,330),(15,596),(1693,596),(855,1434)),
    ("LAA",(347,350),(8,681),(1929,697),(977,1648)),
    ("SEA",(331,326),(5,688),(1866,702),(943,1624) ),
    ("TEX",(329,326),(13,764),(1974,812),(1021,1767)),
    ("COL",(347,350),(28,729),(2088,720),(1055,1753)),
    ("LAD",(330,330),(10,655),(1829,643),(915,1557)),
    ("ARI",(330,334),(3,641),(1762,649),(887,1523)),
    ("SD",(334,322),(5,588),(1787,641),(922,1505)),
    ("SF",(339,309),(28,650),(1923,747),(1034,1649))

]

def normalize(*args):

    a,b,c1 = args 
    c2 = (a**2 + b**2)**0.5
    c = c1/c2
    return c

normalization_factors = []

assigned_normalization_factors = {}

for item in park_leftfield_rightfield:

    park_name, coords_ft, coords_px1, coords_px2, coords_homeplate = item
    a,b = coords_ft
    distance_px = get_distance(coords_px1,coords_px2)
    normalized = normalize(a,b,distance_px)
    normalization_factors.append(normalized)

    for i in range(len(normalization_factors)):

        assigned_normalization_factors[park_name] = normalized

unconverted_distance_array = [get_distance(item1,item2) for item1,item2 in zip(unpacked_fdc,unpacked_ipc)]

home_teams = [str(name) for name in mlb_data["home_team"][0:35500].values if name != 0]

converted_home_teams  = [item for iter,item in enumerate(home_teams) if item not in home_teams[:iter]]

def get_coords_in_feet(team):

    for item in park_leftfield_rightfield:

        name,tuple1,tuple2,tuple3,tuple4 = item
        if team == name and tuple1 != None:

            return tuple1
      
coords_by_team = [get_coords_in_feet(item) if item != "None" else item.pop() for item in converted_home_teams]

normalized_factors_only = list(assigned_normalization_factors.values())

for item1,item2 in zip(normalized_factors_only,park_leftfield_rightfield):

     name,tuple1,tuple2,tuple3,tuple4 = item2
     x1,y1 = tuple2
     x2,y2 = tuple3
     leftfield_to_rightfield_in_feet = (x2-x1)/item1

homeplate_array = []

for item in park_leftfield_rightfield:

    name,tuple1,tuple2,tuple3,tuple4 = item
    homeplate_array.append(tuple4)

team_by_homeplates = [(team ,plate_coords) for team , plate_coords in zip(converted_home_teams,homeplate_array)]

homeplate_array = []

hometeam_with_homeplate = []

#CORRESPONDING TEAMS WITH HOMEPLATE COORDINATES
assigned_homeplate_coords = []

#CORRESPONDING TEAMS WITH HIT COORDINATES

for item in park_leftfield_rightfield:

    name,tuple1,tuple2,tuple3,tuple4 = item
    homeplate_array.append(tuple4)
    hometeam_with_homeplate.append((name,tuple4))

for item in hometeam_with_homeplate:

    team,coords = item
    for name in mlb_data['home_team']:

        if team == name:

            assigned_homeplate_coords.append((name,coords))

final_hit_distance_in_feet = []

for (item1,item2) in zip(assigned_homeplate_coords,assigned_final_hit_coords):

    name1,homeplate_coords = item1
    name2,final_hit_coords = item2
    if name1==name2:

        test_distance = get_distance(homeplate_coords,final_hit_coords)
        for key,value in assigned_normalization_factors.items():

            if key == name1:

                test_distance = test_distance/value
                final_hit_distance_in_feet.append(test_distance)


                assigned_homeplate_coords = list(set(assigned_homeplate_coords))

ha_list = []
assigned_ha_distance = []
assigned_ha_in_feet = []

coords_distance_in_feet = []
assigned_coords_distance = []
assigned_coords_distance_in_feet = []


for hp,hc in zip(assigned_homeplate_coords,assigned_final_hit_coords):
    hp_name,hp_coords = hp
    hc_name,hc_coords = hc
    hp_x,hp_y = hp_coords
    hc_x,hc_y = hc_coords

    for item in assigned_final_hit_coords:

        if item[0] == hp_name:
            h_adj = ((item[0]),(item[1][0],hp_y))
            ha_list.append(h_adj)
            assigned_ha_distance.append((item[0],get_distance(h_adj[1],hp_coords)))
            assigned_coords_distance.append((item[0],get_distance(item[1],hp_coords)))
            

ha_list = sorted(ha_list)

for ha_item,cd_item in zip(assigned_ha_distance,assigned_coords_distance):
    for nf_item in assigned_normalization_factors.items():

        if ha_item[0] == nf_item[0]:
            if cd_item[0] == nf_item[0]:
                distance_in_feet = cd_item[1]/nf_item[1]
                adj = ha_item[1]/nf_item[1]
                coords_distance_in_feet.append(distance_in_feet)
                assigned_coords_distance_in_feet.append((cd_item[0],nf_item[0],distance_in_feet))
                assigned_ha_in_feet.append((ha_item[0],nf_item[0],adj))
                # adj_test.append((item1[0],item2[0],item1[1],item2[1]))

def thetas(a_tuple):

    adj,hyp = a_tuple
    theta = math.degrees(math.acos(adj/hyp))
    return theta

def get_thetas(a_tuple):

    x,y = a_tuple
    angle_calculations=(thetas((x,y)))
    return angle_calculations

calculated_theta_array = [(get_thetas((ha_distance[2],cd_distance[2]))) for ha_distance,cd_distance in zip(assigned_ha_in_feet,assigned_coords_distance_in_feet) if ha_distance[0] == cd_distance[0]]


calculated_theta_array = sorted(calculated_theta_array)

xpoints = np.array(calculated_theta_array)
ypoints = np.array(coords_distance_in_feet)

plt.title("Distance a baseball is hit based on angle")
plt.xlabel("Angle")
plt.ylabel("Distance in feet")

plt.plot(xpoints, ypoints)
plt.show()

# print(calculated_theta_array[9000:90050])
# print(len(ha_list))
# print(ha_list[4200:4340])
# print(assigned_ha_distance[:5])
# print(len(assigned_ha_distance))
# print(len(ha_in_feet))
# print(ha_in_feet[:5])
# print(adj_test[:5])
# print(assigned_normalization_factors.items())
# print(len(assigned_coords_distance))
# print(assigned_coords_distance[:5])
# print(len(assigned_coords_distance_in_feet))
# print(assigned_coords_distance_in_feet[:5])


##Function Utility: Find location of a pitched ball relative to batter (in feet)

def get_pitch_location_relative_to_hitter(ball_coords, handedness):

    distance_batter = 3.21 #Distance from batters box to home plate
    if handedness == "R":

        ball_position = distance_batter + ball_coords
    elif handedness == "L":

        ball_position = distance_batter - ball_coords
    return str(ball_position)

origin_coords = [(items) for iter, items in enumerate(zip(mlb_data['plate_x'][0:2500], mlb_data['stand'][0:2500]))]

hitter_distance_from_plate = []

for iter,items in enumerate(origin_coords):

    distance,count = items
    if float(distance) > 0 and count != 0:

        if distance or count != None:

            hitter_distance_from_plate.append(get_pitch_location_relative_to_hitter(float(distance),count))
    else:

        continue

standard_deviation_distance = standard_deviation(coords_distance_in_feet[:2500])

standard_deviation_theta = standard_deviation(calculated_theta_array[:2500])

ss_x = sum_of_squares(coords_distance_in_feet[:2500])

ss_y = sum_of_squares(calculated_theta_array[:2500])

def combined(*args):

    x_arr,y_arr = args
    x_list = []
    y_list = []
    x_mean = mean_func(x_arr)
    y_mean = mean_func(y_arr)
    for x,y in zip(x_arr,y_arr):

        x_diff = x - x_mean
        x_list.append(x_diff)
        y_diff = y - y_mean
        y_list.append(y_diff)
    return x_list,y_list

def products(combined_arrs):

    x_list,y_list = combined_arrs
    product = []
    for x,y in zip(x_list,y_list):

        product.append(x*y) 
    return sum(product)
combined_products = products(combined(coords_distance_in_feet,calculated_theta_array))

def correlate(*args):

    combined_products, ss_x, ss_y = args
    r_correlation = combined_products/ ((ss_x)*(ss_y))**0.5 * 100
    return r_correlation
print("PRODUCTS: "+str(combined_products))
print("R: " + str(correlate(combined_products, ss_x, ss_y)) + " % Correlation")

#FIND DISTANCE FROM HOME-PLATE AND (HC_X,HC_Y)

# #  (Baltimore Orioles) ///////////////////TEAM
# "Oriole Park": "", ///////////////////////PARK
# #  (Boston Red Sox)
# "Fenway Park":"",
# #  (Tampa Bay Rays)
# "Tropicana Field":"",
# #  (New York Yankees)
# "Yankee Stadium":"",
# #  (Toronto Blue Jays)
# "Rogers Centre":"",
# #  (Philadelphia Phillies)
# "Citizens Bank Park":"",
# #  (Miami Marlins)
# "Marlins Park":"",
# #  (Atlanta Braves)
# "SunTrust Park":"4.04788717266179",
# #  (New York Mets)
# "Citi Field":"",
# #  (Washington Nationals)
# "Nationals Park":"",
# #  (Chicago Cubs)
# "Wrigley Field":"",
# #  (Cincinnati Reds)
# "Great American Ball Park":"",
# #  (Milwaukee Brewers)
# "Miller Park":"",
# #  (Pittsburgh Pirates)
# "PNC Park":"",
# #  (St. Louis Cardinals)
# "Busch Stadium":"",
# #  (Chicago White Sox)
# "Guaranteed Rate Field":"",
# #  (Cleveland Indians)
# "Progressive Field":"",
# #  (Detroit Tigers)
# "Comerica Park":"",
# #  (Kansas City Royals)
# "Kauffman Stadium":"",
# #  (Minnesota Twins)
# "Target Field":"",
# #  (Houston Astros)
# "Minute Maid Park":"",
# #  (Oakland Athletics)
# "Oakland Alameda County Coliseum":"",
# #  (Los Angeles Angels)
# "Angel Stadium of Anaheim":"",
# #  (Seattle Mariners)
# "Safeco Field":"",
# #  (Texas Rangers)
# "Globe Life Park in Arlington":"",
# #  (Colorado Rockies)
# "Coors Field":"",
# #  (Los Angeles Dodgers)
# "Dodger Stadium":"",
# #  (Arizona Diamondbacks)
# "Chase Field":"",
# #  (San Diego Padres)
# "Petco Park":"",
# #  (San Francisco Giants)
# "AT&T Park":""
