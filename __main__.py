e
#to do list:
#battle system
#player stats system
#item system
#inventory system
#system for using items
#write+read data from/to a file that is created in the saves directory when a play creates a new game
#write a guide on how to play and how to modify
#=========================================================================================================
#imports:
import os
import json
import random
#base player stats and stuff
locID = 1
playerhp = 20
playerac = 15
playeratkbonus = 5

#define some other variables:
movecommands = ["n", "e", "s", "w"]
commands = ["n", "e", "s", "w", "kill"]

#entity related variables:
entIDlist = [0]
entitylocationlist = [0]
entstat = [["null", 1]]

#functions:
def OSpath(path):
    fullpath=os.getcwd()+path
    return fullpath

def battle(turn, enemID):
    global entstat
    global playerhp
    while True:
        if turn == "player":
            print("you are attacking", entstat[enemID][0])
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
                entity.delete(enemID)
                print("victory royale! numbah one fortnite win!!1!11!")
                return
            turn = "entity"
        
        if turn == "entity":
            print(entstat[enemID][0], "is attacking you!")
            roll=random.randint(1,20)
            roll+=entstat[enemID][3]
            if roll > playerac:
                print("you were hit!")
                damroll = random.randint(1,8)
                playerhp -= damroll
                print(playerhp)
            if playerhp < 1:
                print("you dieded!")
                return
            turn = "player"

#load up the different types of entities:
with open(OSpath("\\data\\entitytypes.json"), "r") as temp:
    entitytypes = json.load(temp)
    temp.close()
#load up the area data list
with open(OSpath("\\data\\areadata.json"), "r") as temp:
    area_data = json.load(temp)
    temp.close()
#define all the classes
class entity():
    
    def spawn(start, entitytype):
        global entIDlist
        global entitylocationlist
        global entstat
        entIDlist.append(len(entIDlist))
        entitylocationlist.append(start)
        entstat.append(entitytypes[entitytype])
    
    def delete(IDtoberemoved):
        del entIDlist[IDtoberemoved]
        del entitylocationlist[IDtoberemoved]
        del entstat[IDtoberemoved]
        
        
    def entityturn(): #all entities take a turn
        None

class game():
    global locID
    global commands
    global movecommands
    def turn(): #the players turn
        entitiesinarea = []
        entitiesinareanames = []
        IDofentitiesinarea = ([i for i,loc in enumerate(entitylocationlist) if loc == locID])#ID of entities in current area
        for i in IDofentitiesinarea:
            entitiesinarea.append(entstat[i])
        for i in entitiesinarea:
            entitiesinareanames.append(i[0])
        global locID
        isplayerinputvalid = False
        while isplayerinputvalid != True:
            player_input = input()
            if len(player_input) != 0:
                if player_input not in area_data[locID][4]: #check if player_input is a movement cmd
                    if player_input in movecommands:
                        print("you cannot go in this direction")
                else:
                    isplayerinputvalid = True
                    locID = (area_data[locID][3][area_data[locID][4].index(player_input)])
                
                if len(player_input) > 1:
                    if player_input.split()[0] == "kill":
                
                        if player_input.split()[1] not in entitiesinareanames:
                            print("not here")
                        else:
                            isplayerinputvalid = True
                            idofentitybeingattacked = IDofentitiesinarea[entitiesinareanames.index(player_input.split()[1])]
                            battle("player", idofentitybeingattacked)

                if player_input.split()[0] not in commands: #split input first because some commands have args!
                    print("this is not a valid command!")
            else:
                print("what are you doing?")
    def display():
        #reset some variables
        entitiesinarea = []
        entitiesinareanames = []
        #get stats about entities in current area
        IDofentitiesinarea = ([i for i,loc in enumerate(entitylocationlist) if loc == locID])#ID of entities in current area
        for i in IDofentitiesinarea:
            entitiesinarea.append(entstat[i])
        #append names of entities in current area to a list
        for i in entitiesinarea:
            entitiesinareanames.append(i[0])
        print("\n"*10)
        print("<>\n","Current area:")
        print(area_data[locID][1], "\n<>")
        print(area_data[locID][2],)
        print("exits:\n", area_data[locID][4])
        if len(entitiesinarea) != 0:
            print("there are ",len(entitiesinarea)," creatures here")
            print("you can see:")
            for i in entitiesinarea:
                print("a", i[0])
    def over():
        print("game over")





entity.spawn(2, 1)
entity.spawn(2, 0)
game.display()
game.turn()
game.display()
game.turn()
game.display()
game.turn()
game.display()
game.turn()