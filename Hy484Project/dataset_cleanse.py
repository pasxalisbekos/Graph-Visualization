import csv

path = 'globalterrorismdb_0718dist.txt'

#################################################################################
#function  make_cities_csv:                                                     #
#   Params: a)dict_cities (dictionary)                                          #
#           b)year (str)                                                        #
#                                                                               #
#This function is used to create the csv file that contains the city names      #
#and corresponding ids.The year param is used only for the declaration of the   #
#file name.                                                                     #
#                                                                               #
#################################################################################
def make_cities_csv(dict_cities,year,location):
    rows = []

    rows.append(["City_Name","City_id","Lon","Lat"])    
    for i in dict_cities:
        rows.append([   str(i),dict_cities[i], location[i][0], location[i][1]    ])


    with open('./Attacks/'+year+'_Cities.csv','w+') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC, delimiter=';')
        writer.writerows(rows)
        file.close()

#################################################################################
#function  make_cities_csv:                                                     #
#   Params: a)attacks (dictionary)                                              #
#           b)year (str)                                                        #
#                                                                               #
#This function is used to create the csv file that contains information about   #
#the event id of the attack, the city id of the city the attack occured and the #
#group name that claimed the attack.The year param is used only for the         #
#declaration of the file name.                                                  #
#                                                                               #
#################################################################################
def make_attacks_csv(attacks,year,cities):
    rows = []

    rows.append(["eventid","city_id","tgroup"])    
    for i in attacks:
        gname = attacks[i][1]
        city_name = attacks[i][0]
        city_id = cities[city_name]    
        rows.append([str(i),city_id,gname])
    
    with open('./Attacks/'+year+'_Attacks.csv','w+') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC, delimiter=';')
        writer.writerows(rows)
        file.close()

#################################################################################
#function make_connection_by_city:                                              #
#   Params :a)attacks(dictionary)                                               #
#           b)year(str)                                                         #
#           c)dict_cities(dictionaries)                                         #
#                                                                               #
#This function creates a csv file that has the matches of the attack id and the #
#city id (in which the attack took place).The year param is used only for the   #
#declaration of the file name.                                                  #
#                                                                               #
#################################################################################
def make_connection_by_city(attacks,year,dict_cities):
    edge_id = 50000
    rows = []
    rows.append(['city_attack_id','from_attack','to_city'])
    for i in attacks:
        city_name = attacks[i][0]
        city_id = dict_cities[city_name]
        rows.append([str(edge_id),str(i),str(city_id)])
        edge_id += 1

    with open('./Attacks/'+year+'City_Attacks_Connection.csv','w+') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC, delimiter=';')
        writer.writerows(rows)
        file.close()

#################################################################################
#function make_connection_by_group:                                             #
#   Params: a)dict_groups (dictionary)                                          #
#           b)year (str)                                                        #
#                                                                               #
#This function creates the csv file that shows  the connection between the      #
#attacks based on the group that claimed them.The year param is used only for   #
#the declaration of the file name.                                              #
#                                                                               #
#################################################################################
def make_connection_by_group(dict_tgroups,year):
    group_id = 100000
    rows = []

    rows.append(['group_id','from_attack','to_attack'])
    
    for i in dict_tgroups:
        if len(dict_tgroups[i]) >= 2 :    
            sublist = []
            print(str(i)+'->'+str(dict_tgroups[i]))
            for k in range(len(dict_tgroups[i])-1):
                for z in range(k,len(dict_tgroups[i])):
                    if k != z:
                        print(str(dict_tgroups[i][k])+'    ->      '+str(dict_tgroups[i][z]))
                        rows.append([str(group_id),str(dict_tgroups[i][k]-1),str(dict_tgroups[i][z]-1)])
                        group_id += 1 



    with open('./Attacks/'+year+'Attack_Attack_Connection.csv','w+') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC, delimiter=';')
        writer.writerows(rows)
        file.close()

#################################################################################
#function read_per_year():                                                      #
#   Params: a)year(str)                                                         #
#                                                                               #
#This function takes a csv file converted to .txt as it is and analysizes its   #
#containtes based on the specified year.The creates 4 seperate csv files that   #   
#hold the information needed to represent cities and attacks(events) as nodes   #
#and connection between attacks and attack-city as edges.                       #
#                                                                               #
#################################################################################
def read_per_year(year):
    dict_year = {}
    dict_cities = dict()
    dict_tgroups = dict()
    attacks = dict()
    locations =dict()
    counter_city = 1
    counter_events = 10000
    with open(path,encoding = "ISO-8859-1") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if str(row['iyear']) == year and row['gname'] != 'Unknown' and row['gname'] != 'Gunmen':
                if str(row['success']) == '1' : 
                    if row['eventid'] and ('Europe' in row['region_txt'] or 'America' in row['region_txt']):
                        '''
                            1)Creating the csv file for the city nodes.
                            A city node is specified by:
                                i)A unique identifier (int)
                                ii)A name (string)
                        '''
                        city = row['city']
                        if city not in dict_cities.keys():
                            dict_cities[city] = counter_city
                            locations[city] = tuple()
                            locations[city] = (row['longitude'],row['latitude'])
                            counter_city+=1
                            
                        if counter_events not in attacks.keys():
                            attacks[counter_events] = tuple()
                            attacks[counter_events] = (row['city'],row['gname'])
                            counter_events+=1

                        gname = row['gname']
                        if gname not in dict_tgroups.keys():
                            dict_tgroups[gname] = list()
                            dict_tgroups[gname].append(counter_events)
                        else:
                            dict_tgroups[gname].append(counter_events)
                        
        make_cities_csv(dict_cities,year,locations)            
        make_attacks_csv(attacks,year,dict_cities)
        make_connection_by_city(attacks,year,dict_cities)
        make_connection_by_group(dict_tgroups,year)
        csv_file.close()

if __name__ == "__main__":
    read_per_year(str(2001))
