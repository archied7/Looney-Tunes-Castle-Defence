class Game:
    def __init__(self) -> None:
        """"
        self.currentHeroes = {hero: position
                              hero: position
                              ...}
        """""
        self.enemies = []
        self.projectiles = []
        self.ownedTowers = []
        self.currentTower = None
        self.ownedHeroes = []
        self.currentHeroes = {}
        self.state = None

    #adds an enemy object to the enemies list
    def spawnEnemy(self, enemy: object) -> None:
        self.enemies.append(enemy)
    
    #removes an enemy object from the enemies list
    def removeEnemy(self, enemy: object) -> None:
        self.enemies.remove(enemy)

    #adds a projectile object to the projectiles list
    def spawnProjectile(self, projectile: object) -> None:
        self.projectiles.append(projectile)

    #removes a projectile object from the projectiles list
    def removeProjectile(self, projectile: object) -> None:
        self.projectiles.remove(projectile)

    #adds a hero object to the ownedHeroes list
    def purchaseHero(self, hero: object) -> None:
        self.ownedHeroes.append(hero)

    #modifies the currentHeroes list
    def changeHero(self, hero: object, change: str, position: int) -> None:
        if hero in self.ownedHeroes:
            if change == "remove":
                del(self.currentHeroes[hero])
            elif change == "add":
                self.currentHeroes[hero] = position
            elif change == "replace":
                for key in self.currentHeroes:
                    if self.currentHeroes[key] == position:
                        del(self.currentHeroes[key])
                        break
                self.currentHeroes[hero] = position
            else:
                print("Invalid 'change' value passed")
        else:
            print("Hero not owned")
            
        
    #adds a tower object to the ownedTowers list
    def purchaseTower(self, tower: object) -> None:
        self.ownedTowers.append(tower)

    #changes the tower stored in the currentTower attribute
    def changeTower(self, tower: object, change: str) -> None:
        if tower in self.ownedTowers:
            if change == "remove":
                self.currentTower = None
            elif change == "add" | change == "replace":
                self.currentTower = tower
            else:
                print("Invalid change value passed")
        else:
            print("Tower not owned")



