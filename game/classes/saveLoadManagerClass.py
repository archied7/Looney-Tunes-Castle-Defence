import os
import json

class SaveLoadManager():
    def __init__(self, file, main, userID):
        self.userID = userID
        self.file = file

        self.main = main

        self.heroes = [self.main.game.bugsBunny, self.main.game.daffyDuck, self.main.game.taz, self.main.game.yosemiteSam]
        self.towers = [self.main.game.healthTower, self.main.game.goldTower]

    def save(self, data=None):
        if data == None:
            dict = {}
            for i in self.heroes:
                if i not in self.main.game.ownedHeroes:
                    dict[i.name] = [1,0,0]

            for i in self.main.game.ownedHeroes:
                level = i.level
                pos = 0
                for slot, hero in self.main.game.currentHeroes.items():
                    if hero == i:
                        pos = slot
                        break
                dict[i.name] = [level, pos, 1]

            for i in self.towers:
                if i == self.main.game.currentTower:
                    dict[i.name] = [1,1]
                elif i in self.main.game.ownedTowers:
                    dict[i.name] = [0,1]
                else:
                    dict[i.name] = [0,0]
                
            dict['castleLevel'] = self.main.game.castle.level
            dict['archerLevel'] = self.main.game.archers.level
            dict['gold'] = self.main.game.gold
            dict['roundNum'] = self.main.game.round
        
        else:
            dict = data

        with open(self.file, 'r') as file:
            currentData = json.load(file)

        currentData[self.userID] = dict

        with open(self.file, 'w') as file:
            json.dump(currentData, file)

        

    def load(self):
        with open(self.file, 'r') as file:
            data = json.load(file)[self.userID]

        for i in range(1, data['bugsBunny'][0]):
            self.main.game.bugsBunny.levelUp()
        for i in range(1, data['daffyDuck'][0]):
            self.main.game.daffyDuck.levelUp()
        for i in range(1, data['yosemiteSam'][0]):
            self.main.game.yosemiteSam.levelUp()
        for i in range(1, data['taz'][0]):
            self.main.game.taz.levelUp()
        for i in range(1, data['castleLevel']):
            self.main.game.castle.upgrade()
        for i in range(1, data['archerLevel']):
            self.main.game.archers.levelUp()

        if data['bugsBunny'][1] != 0:
            self.main.game.currentHeroes[data['bugsBunny'][1]] = self.main.game.bugsBunny
        if data['bugsBunny'][2] == 1:
            self.main.game.ownedHeroes.append(self.main.game.bugsBunny)
        if data['daffyDuck'][1] != 0:
            self.main.game.currentHeroes[data['daffyDuck'][1]] = self.main.game.daffyDuck
        if data['daffyDuck'][2] == 1:
            self.main.game.ownedHeroes.append(self.main.game.daffyDuck)
        if data['yosemiteSam'][1] != 0:
            self.main.game.currentHeroes[data['yosemiteSam'][1]] = self.main.game.yosemiteSam
        if data['yosemiteSam'][2] == 1:
            self.main.game.ownedHeroes.append(self.main.game.yosemiteSam)
        if data['taz'][1] != 0:
            self.main.game.currentHeroes[data['taz'][1]] = self.main.game.taz
        if data['taz'][2] == 1:
            self.main.game.ownedHeroes.append(self.main.game.taz)

        if data['healthTower'][0] == 1:
            self.main.game.currentTower = self.main.game.healthTower
        if data['healthTower'][1] == 1:
            self.main.game.ownedTowers.append(self.main.game.healthTower)

        if data['goldTower'][0] == 1:
            self.main.game.currentTower = self.main.game.goldTower
        if data['goldTower'][1] == 1:
            self.main.game.ownedTowers.append(self.main.game.goldTower)


        self.main.game.gold = data['gold']
        self.main.game.round = data['roundNum']
        self.main.game.enemyAmount = (self.main.game.round // 3) + 3

        for i in range(1,data['roundNum']):
            if self.main.game.enemyFreq >= 500:
                    self.main.game.enemyFreq -= 100

    def newSave(self):
        counter = 0

        with open(self.file, 'r') as file:
            data = json.load(file)

        for i in data:
            counter += 1

        self.userID = str(counter)

        dict = {
            'bugsBunny' : [1,1,1],
            'daffyDuck' : [1,0,0],
            'taz' : [1,0,0],
            'yosemiteSam' : [1,0,0],
            'roundNum' : 1,
            'gold' : 0,
            'castleLevel' : 1,
            'archerLevel' : 0,
            'healthTower' : [0,0],
            'goldTower' : [0,0]
        }

        self.save(dict)

        return int(self.userID)




        