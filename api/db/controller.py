from sqlalchemy.orm import Session
from sqlalchemy import func
from db.models import models
from db.schemas import schemas
from internal.auth import verify_password
from datetime import datetime, timedelta
from internal.auth import *
from jose import jwt
from sqlalchemy import or_, desc, asc


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


#Create Match Stats
def create_stats(db: Session, stats: str):
    #Check if server record exist already (Not much unique data to go by here so we filter on name and player host)
    server = db.query(models.Server).filter(models.Server.serverName == stats["serverName"]).filter(models.Server.hostPlayer == stats["hostPlayer"]).first()

    if not server:
        #Create server record
        server = models.Server(serverName=stats["serverName"], 
                            serverVersion=stats["gameVersion"], 
                            serverPort=stats["serverPort"], 
                            port=stats["port"], 
                            hostPlayer=stats["hostPlayer"])
        db.add(server)
        db.commit()

    #Create match record
    game = models.Game(serverId=server.id, 
                       sprintEnabled=stats["game"]["sprintEnabled"], 
                       sprintUnlimitedEnabled=stats["game"]["sprintUnlimitedEnabled"], 
                       maxPlayers=stats["game"]["maxPlayers"], 
                       mapName=stats["game"]["mapName"], 
                       mapFile=stats["game"]["mapFile"], 
                       variant=stats["game"]["variant"], 
                       variantType=stats["game"]["variantType"], 
                       teamGame=stats["game"]["teamGame"])
    db.add(game)
    db.commit()

    #Iterate over players in match and create records for them if they don't already exist
    for playerData in stats["players"]:
        #Check if player exists already
        player = db.query(models.Player).filter(models.Player.playerUID == playerData["uid"]).first()
        
        if not player:
            #Add player info
            player = models.Player(playerName=playerData["name"],
                                   clientName=playerData["clientName"],
                                   serviceTag=playerData["serviceTag"],
                                   playerIp=playerData["ip"],
                                   team=playerData["team"],
                                   playerIndex=playerData["playerIndex"],
                                   playerUID=playerData["uid"],
                                   primaryColor=playerData["primaryColor"],)
            
            db.add(player)
            db.commit()


        #Add player match stats
        player_stats = models.PlayerGameStats(playerId=player.id, 
                                              gameId=game.id, 
                                              score=playerData["playerGameStats"]["score"], 
                                              kills=playerData["playerGameStats"]["kills"], 
                                              assists=playerData["playerGameStats"]["assists"], 
                                              deaths=playerData["playerGameStats"]["deaths"], 
                                              betrayals=playerData["playerGameStats"]["betrayals"], 
                                              timeAlive=playerData["playerGameStats"]["timeSpentAlive"], 
                                              suicides=playerData["playerGameStats"]["suicides"], 
                                              bestStreak=playerData["playerGameStats"]["bestStreak"])
        
        db.add(player_stats)
        db.commit()

        #Add player id and match id to link table
        link_table = models.PlayersLink(gameId=game.id, playerId=player.id)

        db.add(link_table)
        db.commit()

        #Iterate over medals earned for our player in recent match
        for medal in playerData["playerMedals"]:
            medal = models.PlayerMedals(playerId=player.id, 
                                        gameId=game.id, 
                                        medalName=medal["medalName"], 
                                        count=medal["count"])

            db.add(medal)
            db.commit()

        #Iterate over player weapons for recent match
        for weapon in playerData["playerWeapons"]:
            weapon = models.PlayerWeapons(playerId=player.id, 
                                          gameId=game.id, 
                                          weaponName=weapon["weaponName"], 
                                          weaponIndex=weapon["weaponIndex"], 
                                          kills=weapon["kills"], 
                                          killedBy=weapon["killedBy"], 
                                          betrayalsWith=weapon["betrayalsWith"], 
                                          suicidesWith=weapon["suicidesWith"], 
                                          headShotsWith=weapon["headshotsWith"])
            
            db.add(weapon)
            db.commit()

    return True
