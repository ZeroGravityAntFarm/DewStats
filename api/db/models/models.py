from sqlalchemy import Boolean, Column, ForeignKey, Integer, BigInteger, String, LargeBinary, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), unique=True, index=True)
    email = Column(String(128), unique=True, index=True)
    role = Column(String(64), unique=False, index=True)
    hashed_password = Column(String(128))
    is_active = Column(Boolean, default=True)
    prof_views = Column(Integer, index=True)
    about = Column(String(1200))

    time_created = Column(DateTime(timezone=True), default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())


class Server(Base):
    __tablename__ = "servers"

    id = Column(Integer, primary_key=True, index=True)
    serverName = Column(String(128), index=True)
    serverVersion = Column(String(1200))
    serverPort = Column(Integer, index=True)
    port = Column(Integer, index=True)
    hostPlayer = Column(String(128), index=True)

    time_created = Column(DateTime(timezone=True), default=func.now())


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    sprintEnabled = Column(Boolean)
    sprintUnlimitedEnabled = Column(Boolean)
    maxPlayers = Column(Integer)
    mapName = Column(String(128), index=True)
    mapFile = Column(String(128), index=True)
    variant = Column(String(128), index=True)
    variantType = Column(String(128), index=True)
    teamGame = Column(Boolean, index=True)
    
    time_created = Column(DateTime(timezone=True), default=func.now())

    
class Players(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    gameId = Column(Integer, index=True)
    playerId = Column(Integer)
    
    time_created = Column(DateTime(timezone=True), default=func.now())


class Player(Base):
    __tablename__ = "player"

    id = Column(Integer, primary_key=True, index=True)
    playerName = Column(String(128), index=True)
    clientName = Column(String(64), index=True)
    serviceTag = Column(String(4), index=True)
    playerIp = Column(String(1200))
    team = Column(Integer)
    playerIndex = Column(Integer)
    playerUID = Column(String(128))
    primaryColor = Column(String(64))


    time_created = Column(DateTime(timezone=True), default=func.now())


class PlayerGameStats(Base):
    __tablename__ = "playergamestats"
    
    id = Column(Integer, primary_key=True, index=True)
    playerId = Column(Integer)
    gameId = Column(Integer)
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

    time_created = Column(DateTime(timezone=True), default=func.now())


class PlayerMedals(Base):
    __tablename__  = "playermedals"

    id = Column(Integer, primary_key=True, index=True)
    playerId = Column(Integer)
    gameId = Column(Integer)
    medalName = Column(String(64))
    count = Column(Integer)

    time_created = Column(DateTime(timezone=True), default=func.now())


class PlayerWeapons(Base):
    __tablename__ = "playerweapons"

    id = Column(Integer, primary_key=True, index=True)
    playerId = Column(Integer)
    gameId = Column(Integer)
    weaponName = Column(String(64))
    weaponIndex = Column(Integer)
    kills = Column(Integer)
    killedBy = Column(Integer)
    betraylsWith = Column(Integer)
    suicidesWith = Column(Integer)
    headShotsWith = Column(Integer)

    time_created = Column(DateTime(timezone=True), default=func.now())