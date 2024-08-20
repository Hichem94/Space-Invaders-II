import mysql.connector

connection_params = {
    'host': "localhost",
    'user': "rigolo",
    'password':"koala9494",
}

# Definition des requêtes
create_db_request     = "CREATE DATABASE space_invadersII"
use_request           = "USE space_invadersII"
table_PLAYER_request  = "CREATE TABLE player (\
                        id INTEGER NOT NULL AUTO_INCREMENT,\
                        pseudo VARCHAR(100) NOT NULL,\
                        PRIMARY KEY (id, pseudo)\
                        )"
table_SCORE_request   = "CREATE TABLE score (\
                        id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,\
                        score INTEGER NOT NULL,\
                        player_id INTEGER NOT NULL,\
                        FOREIGN KEY (player_id) REFERENCES player(id) ON DELETE CASCADE\
                        )"
requests = [create_db_request, use_request, table_PLAYER_request, table_SCORE_request]
try:
    with mysql.connector.connect(**connection_params) as db:
        with db.cursor() as c:
            for r in requests:
                c.execute(r)
                db.commit()
except:
    print("Base de données déjà créée.")


def ajouter_player_et_score(pseudo, score):
    insert_player       = "INSERT INTO player (`pseudo`) VALUES ('" + str(pseudo) + "')"
    request_pseudo_id   = "SELECT id FROM player WHERE pseudo = '" + str(pseudo) + "'"

    with mysql.connector.connect(**connection_params) as db:
        with db.cursor(buffered=True) as c:
                c.execute("USE space_invadersII")
                c.execute(request_pseudo_id)
                tmp = c.fetchone()
                if tmp: # Le pseudo existe, on récupère son id
                    pseudo_id = tmp[0]
                else:   # Le pseudo n'existe pas, on insère le player
                    c.execute(insert_player)
                    c.execute(request_pseudo_id)
                    pseudo_id = c.fetchone()[0]
                insert_score = "INSERT INTO score (`score`, `player_id`) VALUES ('" + str(score) + "', '" + str(pseudo_id) + "')"               
                c.execute(insert_score)
                db.commit()

# ajouter_player_et_score('rigolo', 100)
# ajouter_player_et_score('rigolo', 100)
# ajouter_player_et_score('poussin', 102)