import sqlite3
import os
import json

db_file = os.getcwd() + '/saveData/users.db'
json_file = os.getcwd() + '/saveData/data.json'
dict = {'guest' : {
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
        }}

def resetDb():
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        
        sql_delete_all = 'DELETE FROM UserData;'
        cursor.execute(sql_delete_all)
        
        conn.commit()

    print("Database reset")

def resetJson():
     
     
    with open(json_file, 'w') as file:
        json.dump(dict, file)

    print('Json file reset')


resetDb()
resetJson()

