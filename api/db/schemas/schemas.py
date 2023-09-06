from pydantic import BaseModel
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str = None


class TokenData(BaseModel):
    sub: str = None
    exp: int = None


class UserBase(BaseModel):
    name: str
    email: str
    

class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    role: str | None = None
    about: str | None = None
    prof_views: str | None = None


class ServerBase(BaseModel):
    serverName: str
    serverVersion: str
    serverPort: int
    port: int
    hostPlayer: str


class GameBase(BaseModel):
    sprintEnabled: bool
    sprintUnlimitedEnabled: bool
    maxPlayers: int
    mapName: str
    mapFile: str
    variant: str
    variantType: str
    teamGame: bool


class PlayerBase(BaseModel):
    playerName: str
    clientName: str
    serviceTag: str
    playerIp: str
    team: int
    playerIndex: int
    playerUID: str
    primaryColor: str
    playerExp: int
    playerRank: int


class PlayerGameStatsBase(BaseModel):
    score: int
    kills: int
    assists: int
    deaths: int
    betrayals: int
    timeAlive: int
    suicides: int
    bestStreak: int
    nemesisIndex: int
    kingsKilled: int
    humansInfected: int
    zombiesKilled: int
    timeInHill: int
    timeControllingHill: int
    playerVersusPlayerKills: str


class PlayerMedalsBase(BaseModel):
    medalName: str
    count: int


class PlayerWeaponsBase(BaseModel):
    weaponName: str
    weaponIndex: str
    kills: int
    killedBy: str
    betraylsWith: int
    suicidesWith: int
    headShotWith: int
    
