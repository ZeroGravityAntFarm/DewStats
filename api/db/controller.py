from sqlalchemy.orm import Session, load_only
from sqlalchemy import func
from db.models import models
from db.schemas import schemas
from internal.auth import verify_password
from datetime import datetime, timedelta
from internal.auth import *
from jose import jwt
from sqlalchemy import or_, desc, asc, func
from datetime import datetime

#Authenticate a user
def authenticate_user(db, username: str, password: str):
    user = get_user_auth(db, username)
    
    #Check if user exists
    if not user:
        return False
    
    #Check if account is active
    if not user.is_active:
        return False

    #Verify password against hashed password
    if not verify_password(password, user.hashed_password):
        return False

    return user


#Create a JWT access token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta

    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


#Query user profile 
def get_user(db: Session, user_name: str):
    user = db.query(models.User).filter(models.User.name == user_name).first()
    user_data = db.query(*[c for c in models.User.__table__.c if c.name != 'hashed_password' and c.name != 'role' and c.name != 'email']).filter(models.User.name == user_name).first()

    if user:
        if user.prof_views != None:
            user.prof_views += 1

        else:
            user.prof_views = 1
        db.commit()

    return user_data


#Query user profile
def get_userId(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    user_data = db.query(*[c for c in models.User.__table__.c if c.name != 'hashed_password' and c.name != 'role' and c.name != 'email']).filter(models.User.id == user_id).first()

    if user:
      return user_data


#Query user profile 
def get_user_auth(db: Session, user_name: str):
    user = db.query(models.User).filter(models.User.name == user_name).first()

    return user

#Get all users
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(*[c for c in models.User.__table__.c if c.name != 'hashed_password' and c.name != 'role' and c.name != 'email']).offset(skip).limit(limit).all()


#Query user by email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


#Create new user
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, name=user.name, hashed_password=hashed_password, rank="Recruit", about=" ")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


#Update user data
def update_user(db: Session, user: str, userName: str, userEmail: str, userAbout: str):
    user = db.query(models.User).filter(models.User.id == user.id).first()
    user.name = userName
    user.email = userEmail
    user.about = userAbout
    db.commit()

    return user


#Update user password
def update_user_password(db: Session, userPassword: int, user: str):
    user = db.query(models.User).filter(models.User.id == user.id).first()
    hashed_password = pwd_context.hash(userPassword)
    user.hashed_password = hashed_password
    db.commit()

    return user


#Get global stats
def get_global_stats(db: Session):

    game_count = db.query(models.Game).count()
    total_kills = db.query(func.sum(models.PlayerGameStats.kills)).scalar()
    total_medals =  db.query(func.sum(models.PlayerMedals.count)).scalar()
    zombies_killed = db.query(func.sum(models.PlayerGameStats.zombiesKilled)).scalar()
    humans_infected = db.query(func.sum(models.PlayerGameStats.humansInfected)).scalar()
    friendly_fire = db.query(func.sum(models.PlayerGameStats.betrayals)).scalar()



    global_stats = { 'games': game_count, 
                     'kill_count': total_kills,
                     'medal_count': total_medals,
                     'zombies_killed': zombies_killed,
                     'humans_infected':  humans_infected,
                     'friendly_fire': friendly_fire}

    return global_stats


#Get players by distinct uid
def get_players(db: Session):
    players = db.query(models.Player).distinct(models.Player.playerUID).options(load_only("playerName", "clientName", "serviceTag", "primaryColor", "playerExp", "playerRank", "time_created"))

    return players


#Get last 5 recent matches
def get_games(db):
    game_list = []
    games = db.query(models.Game).order_by(desc(models.Game.time_created)).limit(5)

    for game in games:
        server = db.query(models.Server).filter(models.Server.id == game.serverId).first()
        setattr(game, "server", server)
        setattr(game, "imagepath", f"/static/content/maps/small/{game.mapFile}.png")
        game.time_created = game.time_created.replace(microsecond=0)

        game_list.append(game)

    return game_list


#Get all matches
def get_all_games(db):
    game_list = []
    games = db.query(models.Game).order_by(desc(models.Game.time_created)).all()

    for game in games:
        server = db.query(models.Server).filter(models.Server.id == game.serverId).first()
        setattr(game, "server", server)
        setattr(game, "imagepath", f"/static/content/maps/small/{game.mapFile}.png")
        setattr(game, "matchLink", f'<a href="/api_v1/match/{game.id}">{game.mapName}</a>')
        game.time_created = game.time_created.replace(microsecond=0)

        game_list.append(game)

    return game_list


#Get leaderboard
def get_leaderboard(db):
    player_list = []
    players = db.query(models.Player).distinct(models.Player.playerUID).options(load_only("playerName", "clientName", "serviceTag", "primaryColor", "playerExp", "playerRank", "time_created"))

    for player in players:

        #Get all the game's this player has ever played
        player_ids = db.query(models.Player).filter(models.Player.playerUID == player.playerUID).options(load_only("playerName", "clientName", "serviceTag", "primaryColor", "playerExp", "playerRank", "time_created")).all()

        total_kills = 0
        total_deaths = 0

        #Iterate over every match this player has played and get their kills
        for id in player_ids:
            id_kills = db.query(func.sum(models.PlayerGameStats.kills)).filter(models.PlayerGameStats.playerId == id.id).scalar()
            total_kills += id_kills

            id_deaths = db.query(func.sum(models.PlayerGameStats.deaths)).filter(models.PlayerGameStats.playerId == id.id).scalar()
            total_deaths += id_deaths

        #Assign kill/death values to player object
        player.total_kills = total_kills
        player.total_deaths = total_deaths

        #Calculate k/d
        try:
            kd = player.total_kills / player.total_deaths
            player.kd_ratio = round(kd, 1)
        
        except ZeroDivisionError:
            player.kd_ratio = 0

        player_list.append(player)


    return player_list


def get_match(db: Session, id: int):
    match = db.query(models.Game).filter(models.Game.id == id).first()
    server = db.query(models.Server).filter(models.Server.id == match.serverId).first()
    playersLink = db.query(models.PlayersLink).filter(models.PlayersLink.gameId == id).all()
    
    players_list = []
    mvp_tracker = 0
    player_mvp = "Guardians"
    
    for player in playersLink:
        #Get our player object from link table
        player_instance = db.query(*[c for c in models.Player.__table__.c if c.name != 'playerIp' and c.name != 'playerUID']).filter(models.Player.id == player.playerId).first()

        #Get player stats then add them to our dict
        player_kills = db.query(func.sum(models.PlayerGameStats.kills)).filter(models.PlayerGameStats.gameId == match.id).filter(models.PlayerGameStats.playerId == player_instance.id).scalar()
        player_deaths = db.query(func.sum(models.PlayerGameStats.deaths)).filter(models.PlayerGameStats.gameId == match.id).filter(models.PlayerGameStats.playerId == player_instance.id).scalar()

        if player_kills >= mvp_tracker:
            mvp_tracker = player_kills
            player_mvp = player_instance.playerName

        #Calculate K/D
        try:
            kd = player_kills / player_deaths
            kd_ratio = round(kd, 1)
        
        except ZeroDivisionError:
            kd_ratio = 0        

        player_data = {
            "playerName": player_instance.playerName,
            "serviceTag": player_instance.serviceTag,
            "team": player_instance.team,
            "playerIndex": player_instance.playerIndex,
            "primaryColor": player_instance.primaryColor,
            "playerKills": player_kills,
            "playerDeaths": player_deaths,
            "kdRatio": kd_ratio
        }

        players_list.append(player_data)

    server = {
        "serverName": server.serverName,
        "serverVersion": server.serverVersion,
        "serverPort": server.serverPort,
        "port": server.port,
        "hostPlayer": server.hostPlayer
    }

    match = {
        "sprintEnabled": match.sprintEnabled,
        "sprintUnlimitedEnabled": match.sprintUnlimitedEnabled,
        "maxPlayers": match.maxPlayers,
        "mapName": match.mapName,
        "mapFile": match.mapFile,
        "variant": match.variant,
        "variantType": match.variantType,
        "maxPlayers": match.maxPlayers,
        "teamGame": match.teamGame,
        "time_created": match.time_created,
        "mapImage": f"/static/content/maps/large/{match.mapFile}.jpg",
        "server": server,
        "players": players_list,
        "mvp": player_mvp
    }

    return match

#Return should be list of players as winners
def getWinner(gameData):

    #Get Slayer Winner
    if gameData["game"]["variantType"] == "slayer":
        if gameData["game"]["teamGame"]:
            
            #Find all teams in our game and sum their player scores
            teams = {}
            for player in gameData["players"]:
                if player["team"] not in teams:
                    teams[player["team"]] = player["playerGameStats"]["kills"]

                else:
                    teams[player["team"]] = player["playerGameStats"]["kills"] + teams[player["team"]]

            win_team = max(teams, key=teams.get)

            win_players = []
            for player in gameData["players"]:
                if player["team"] == win_team:
                    win_players.append(player["uid"])

            return win_players

        else:
            kills = 0
            winner = []
            for player in gameData["players"]:
                if player["playerGameStats"]["kills"] >= kills:
                    kills = player["playerGameStats"]["kills"]
                    winner.append(player["uid"])

            return winner
    
    #Get CTF Winner
    elif gameData["game"]["variantType"] == "ctf":
        teams = {}
        for player in gameData["players"]:
            if player["team"] not in teams:
                for medal in player["playerMedals"]:
                    if medal["medalName"] == "flag_captured":
                        teams[player["team"]] = medal["count"]

            else:
                for medal in player["playerMedals"]:
                    if medal["medalName"] == "flag_captured":
                        teams[player["team"]] = medal["count"] + teams[player["team"]]

        win_team = max(teams, key=teams.get)

        win_players = []
        for player in gameData["players"]:
            if player["team"] == win_team:
                win_players.append(player["uid"])

        return win_players

    elif gameData["game"]["variantType"] == "infection":
        #Iterate over players and get sum of zombies killed
        zombs = 0
        winner = ""
        for player in gameData["players"]:
            if player["otherStats"]["zombiesKilled"] >= zombs:
                zombs = player["otherStats"]["zombiesKilled"]
                winner = (player["uid"])

        return [winner]
    
    elif gameData["game"]["variantType"] == "vip":
        if gameData["game"]["teamGame"]:
            #This one gonna be fun
            return
        
        else:
            #This one gonna be fun
            return
    
    elif gameData["game"]["variantType"] == "koth":
        if gameData["game"]["teamGame"]:
            return
        
        else:
            #Iterate over players and find max timeControllingHill
            return
    
    elif gameData["game"]["variantType"] == "oddball":
        if gameData["game"]["teamGame"]:
            #Iterate over teams and find team sum max score
            return
        
        else:
            #Iterate over players and find max score
            return

    elif gameData["game"]["variantType"] == "territories":
        if gameData["game"]["teamGame"]:
            #Iterate over teams and find team sum max score
            return
        
        else:
            #Iterate over players and find max score
            return
        
    else:
        return ['Guardians']
