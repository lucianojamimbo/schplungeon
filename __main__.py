
#imports:
import os
import json
import random
import time
import sys
#base player stats and stuff
locID = 1
playerhp = 20
playerac = 15
playeratkbonus = 5
playerxp = 0
playerlv = 1

#delay times
short_dly = 1
med_dly = 3
long_dly = 5


#define some other variables:
movecommands = ["n", "e", "s", "w"]
commands = ["n", "e", "s", "w", "kill"]

#entity related variables:
entIDlist = [0]
entitylocationlist = [0]
entstat = [["null", 1]]

#load up world data:
#load up the different types of entities:
with open(os.getcwd()+("\\data\\entitytypes.json"), "r") as temp:
    entitytypes = json.load(temp)
    temp.close()
#load up the area data list
with open(os.getcwd()+("\\data\\areadata.json"), "r") as temp:
    area_data = json.load(temp)
    temp.close()


#functions:
def xp(entID):
    global playerxp
    global playerlv
    global playerhp
    global playeratkbonus
    playerxp += entstat[entID][4]
    if playerxp >= 30 * playerlv:
        playerlv += 1
        playerhp += (playerlv * 5)
        playeratkbonus += 1
        print("\n"*2)
        print("-------------------------------------------------------------")
        print("You are now level", playerlv, "!")
        print("You HP is now", playerhp)
        print("Your Attack Bonus is now", playeratkbonus)
        print("Your AC has not changed.")
        print("-------------------------------------------------------------")
        print("\n"*2)
        playerxp = 0

def battle(turn, enemID):
    global entstat
    global playerhp
    while True:
        if turn == "player":
            print("you are attacking", entstat[enemID][0])
            print("your HP:", playerhp)
            print("<add choosing weapon here once extra weapons are added to the game>")
            roll=random.randint(1,20)
            roll+=playeratkbonus
            if roll > entstat[enemID][2]:
                print("hit!")
                damroll = random.randint(1,8)
                entstat[enemID][1] -= damroll
                print(entstat[enemID])
            else:
                print("you missed!")
            if entstat[enemID][1] < 1:
                xp(enemID)
                print("The foe is dead.")
                entity.delete(enemID)
                time.sleep(short_dly)
                return
            turn = "entity"
        time.sleep(med_dly)
        if turn == "entity":
            print(entstat[enemID][0], "is attacking you!")
            roll=random.randint(1,20)
            roll+=entstat[enemID][3]
            if roll > playerac:
                print("you were hit!")
                damroll = random.randint(1,8)
                playerhp -= damroll
            if playerhp < 1:
                print("you died!")
                game.over()
                return
            turn = "player"

#define all the classes
###################################################################################################################################
class entity():
    
    def spawn(loc, entitytype):
        global entIDlist
        global entitylocationlist
        global entstat
        global entitytypes
        entIDlist.append(len(entIDlist))
        entitylocationlist.append(loc)
        entstat.append(entitytypes[entitytype])
    
    def delete(IDtoberemoved):
        global entIDlist
        global entitylocationlist
        global entstat
        newidlist = []
        for item in entIDlist[:IDtoberemoved]:
            newidlist.append(item)
        for item in entIDlist[IDtoberemoved:]:
            newidlist.append(item-1)
        entIDlist = newidlist[:]
        del entIDlist[IDtoberemoved]
        del entitylocationlist[IDtoberemoved]
        del entstat[IDtoberemoved]
        
        
    def entityturn(): #all entities take a turn
        None
###################################################################################################################################
class game():
    global locID
    global commands
    global movecommands
    def turn(): #the players turn
        global locID
        entitiesinarea = []
        entitiesinareanames = []
        IDofentitiesinarea = ([i for i,loc in enumerate(entitylocationlist) if loc == locID])#ID of entities in current area
        for i in IDofentitiesinarea:
            entitiesinarea.append(entstat[i])
        for i in entitiesinarea:
            entitiesinareanames.append(i[0])
        isplayerinputvalid = False
        while isplayerinputvalid != True:
            player_input = input(">")
            print("\n"*2)
            if len(player_input) != 0:
                if player_input not in area_data[locID][4]: #check if player_input is a movement cmd
                    if player_input in movecommands:
                        print("you cannot go in this direction")
                else:
                    isplayerinputvalid = True
                    locID = (area_data[locID][3][area_data[locID][4].index(player_input)]) #update players location
                if len(player_input) > 1:
                    if player_input.split()[0] == "kill":#if player uses kill command:
                        if player_input.split()[1] not in entitiesinareanames: #see if specified entity is present
                            print("entity not found")
                        else:
                            isplayerinputvalid = True
                            idofentitybeingattacked = IDofentitiesinarea[entitiesinareanames.index(player_input.split()[1])]
                            battle("player", idofentitybeingattacked)
                            
                if player_input == "endgame":
                    print("Goodbye, you acheived Level", playerlv, "!")
                    time.sleep(med_dly)
                    print("Exiting..")
                    time.sleep(med_dly)
                    sys.exit()
                if player_input == "exitnow" or player_input == "quitnow":
                    sys.exit()
                    
                if player_input.split()[0] not in commands: #split input first because some commands have args!
                    print("that is not a valid command!")
            else:
                print("what are you doing?")
    def display():
        #reset some variables
        entitiesinarea = []
        entitiesinareanames = []
        
        #gets global ID of entities in players area:
        IDofentitiesinarea = ([i for i,loc in enumerate(entitylocationlist) if loc == locID])
        for i in IDofentitiesinarea:
            entitiesinarea.append(entstat[i])
        #append names of entities in current area to a list
        for i in entitiesinarea:
            entitiesinareanames.append(i[0])
        
        #display information in the terminal:
        print("\n"*2)
        print("-------------------------------------------------------------")
        print("Current area:")
        print(area_data[locID][1],)
        print(area_data[locID][2],)
        print("exits:\n", area_data[locID][4])
        if len(entitiesinarea) != 0:
            print("there are ",len(entitiesinarea)," creature(s) here")
            print("you can see:")
            for i in entitiesinarea:
                print("a", i[0])
        print("-------------------------------------------------------------")

        print("\n")

    def over():
        print("game over.")
        time.sleep(long_dly)
        sys.exit()
        
###################################################################################################################################    

#spawning (this really could be a loop like come on)
entity.spawn(random.randint(1,3), 1)
entity.spawn(random.randint(1,3), 1)
entity.spawn(random.randint(1,3), 0)
entity.spawn(random.randint(1,3), 1)
entity.spawn(random.randint(1,3), 0)
entity.spawn(random.randint(1,4), 1)
entity.spawn(random.randint(1,4), 1)
entity.spawn(random.randint(1,4), 0)
entity.spawn(random.randint(1,5), 1)
entity.spawn(random.randint(1,5), 0)
entity.spawn(5, 3)
entity.spawn(2, 1)
entity.spawn(2, 0)

#game intro
def title_scr():
    option = input(">")
    if option == "play" or option == "Play":
        print("What is your name?")
        name = input(">")
        print("Welcome to Schplungeon {0}!".format(name))
        print("You must escape!")
        time.sleep(short_dly)
        gamerun()
    if option == "help" or option == "Help":
        print("Use commands n e s w to move and kill (enemy name) to attack. Use endgame to quit. Now type play and start your adventure")
        title_scr()
    if option == "quit" or option == "Quit" or option == "endgame" or option == "exitnow" or option == "quitnow":
        print("Exiting..")
        time.sleep(short_dly)
        sys.exit()
    else:
        print("Invalid command - type help")
        title_scr()
        

#runs the game         
def gamerun():
    while True: 
        game.display()
        game.turn()

print("-------------------------------")
print("Welcome to the Schplungeon.")
print("-------------------------------")   
title_scr()