from sqlalchemy import Boolean, Column, ForeignKey, Integer, BigInteger, String, LargeBinary, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from db.session import Base


class User(Base):
    __tablename__ = "users"

    #Columns
    id = Column(Integer, primary_key=True, index=True)
    player_uid = Column(Integer, ForeignKey='player.playerUID')
    name = Column(String(128), unique=True, index=True)
    email = Column(String(128), unique=True, index=True)
    role = Column(String(64), unique=False, index=True)
    hashed_password = Column(String(128))
    is_active = Column(Boolean, default=True)
    prof_views = Column(Integer, index=True)
    about = Column(String(1200))


    #Automatic Created/Updated datetime columns
    time_created = Column(DateTime(timezone=True), default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    #Relationships
    player = relationship("Player", backref=backref("users", uselist=False))


class Server(Base):
    __tablename__ = "servers"

    #Columns
    id = Column(Integer, primary_key=True, index=True)
    serverName = Column(String(128), index=True)
    serverVersion = Column(String(1200))
    serverPort = Column(Integer, index=True)
    port = Column(Integer, index=True)
    hostPlayer = Column(String(128), index=True)

    #Automatic Created/Updated datetime columns
    time_created = Column(DateTime(timezone=True), default=func.now())

    #Relationships
    games = relationship("Game", back_populates="servers")

class Game(Base):
    __tablename__ = "games"

    #Columns
    id = Column(Integer, primary_key=True, index=True)
    server_id = Column("Integer", ForeignKey='servers.id')
    sprintEnabled = Column(Boolean)
    sprintUnlimitedEnabled = Column(Boolean)
    maxPlayers = Column(Integer)
    mapName = Column(String(128), index=True)
    mapFile = Column(String(128), index=True)
    variant = Column(String(128), index=True)
    variantType = Column(String(128), index=True)
    teamGame = Column(Boolean, index=True)
    
    #Automatic Created/Updated datetime columns
    time_created = Column(DateTime(timezone=True), default=func.now())

    #Relationships
    server = relationship("Server", back_populates="games")
    players = relationship("Player", secondary="players_link", back_populates="games")


#Link table required for the many-to-many relationship between games and player    
class PlayersLink(Base):
    __tablename__ = "players_link"

    #Columns
    gameId = Column(Integer, ForeignKey=('games.id'), primary_key=True)
    playerId = Column(Integer, ForeignKey=('player.id'), primary_key=True)
    
    #Automatic Created/Updated datetime columns
    time_created = Column(DateTime(timezone=True), default=func.now())


class Player(Base):
    __tablename__ = "player"

    #Columns
    id = Column(Integer, primary_key=True, index=True)
    playerName = Column(String(128), index=True)
    clientName = Column(String(64), index=True)
    serviceTag = Column(String(4), index=True)
    playerIp = Column(String(1200))
    team = Column(Integer)
    playerIndex = Column(Integer)
    playerUID = Column(String(128))
    primaryColor = Column(String(64))

    #Automatic Created/Updated datetime columns
    time_created = Column(DateTime(timezone=True), default=func.now())

    #Relationships
    games = relationship("Game", secondary="players_link", back_populates="players")



class PlayerGameStats(Base):
    __tablename__ = "playergamestats"
    
    #Columns
    id = Column(Integer, primary_key=True, index=True)
    playerId = Column(Integer, ForeignKey('player.id'))
    gameId = Column(Integer, ForeignKey('game.id'))
    score = Column(Integer)
    kills = Column(Integer)
    assists = Column(Integer)
    deaths = Column(Integer)
    betrayals = Column(Integer)
    timeAlive = Column(Integer)
    suicides = Column(Integer)
    bestStreak = Column(Integer)
    nemesisIndex = Column(Integer)
    kingsKilled = Column(Integer)
    humansInfected = Column(Integer)
    zombiesKilled = Column(Integer)
    timeInHill = Column(Integer)
    timeControllingHill = Column(Integer)
    playerVersusPlayerKills = Column(String(64))

    #Automatic Created/Updated datetime columns
    time_created = Column(DateTime(timezone=True), default=func.now())

    #Relationships
    player = relationship("Player")
    game = relationship("Game")



class PlayerMedals(Base):
    __tablename__  = "playermedals"

    #Columns
    id = Column(Integer, primary_key=True, index=True)
    playerId = Column(Integer, ForeignKey('player.id'))
    gameId = Column(Integer, ForeignKey('game.id'))
    medalName = Column(String(64))
    count = Column(Integer)

    #Automatic Created/Updated datetime columns
    time_created = Column(DateTime(timezone=True), default=func.now())

    #Relationships
    player = relationship("Player")
    game = relationship("Game")


class PlayerWeapons(Base):
    __tablename__ = "playerweapons"

    #Columns
    id = Column(Integer, primary_key=True, index=True)
    playerId = Column(Integer, ForeignKey('player.id'))
    gameId = Column(Integer, ForeignKey('game.id'))
    weaponName = Column(String(64))
    weaponIndex = Column(Integer)
    kills = Column(Integer)
    killedBy = Column(Integer)
    betraylsWith = Column(Integer)
    suicidesWith = Column(Integer)
    headShotsWith = Column(Integer)

    #Automatic Created/Updated datetime columns
    time_created = Column(DateTime(timezone=True), default=func.now())

    #Relationships
    player = relationship("Player")
    game = relationship("Game")