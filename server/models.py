from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Server(db.Model):
    __tablename__ = "cs_servers"
    serverID = db.Column(db.Integer, primary_key=True)
    serverAddress = db.Column(db.VARCHAR(32))
    hostName = db.Column(db.VARCHAR(64))
    dateCreated = db.Column(db.TIMESTAMP)
    currentMap = db.Column(db.VARCHAR(64))
    isBotEnabled = db.Column(db.Integer)
    serverKey = db.Column(db.VARCHAR(128))

    def __init__(self, address, hostname, enabled):
        self.serverAddress = address
        self.hostName = hostname
        self.isBotEnabled = enabled


class Map(db.Model):
    __tablename__ = "cs_maps"
    mapID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(45))
    difficulty = db.Column(db.Integer)
    checkpoints = db.Column(db.Integer)
    mapType = db.Column(db.Integer)
    author = db.Column(db.VARCHAR(45))
    bonuses = db.Column(db.Integer)
    active = db.Column(db.Integer)
    prehop = db.Column(db.Integer)
    enableBakedTriggers = db.Column(db.Integer)


class Player(db.Model):
    __tablename__ = "cs_players"
    playerID = db.Column(db.Integer, primary_key=True)
    steamid = db.Column(db.VARCHAR(45))
    name = db.Column(db.VARCHAR(45))
    playerIP = db.Column(db.VARCHAR(45))
    dateCreated = db.Column(db.TIMESTAMP)
    dateUpdated = db.Column(db.TIMESTAMP)
    replays = db.relationship("Replay", lazy="dynamic")


class Time(db.Model):
    __tablename__ = "cs_times"
    runID = db.Column(db.Integer, primary_key=True)
    mapID = db.Column(db.Integer, db.ForeignKey(Map.mapID))
    map = db.relationship("Map")
    playerID = db.Column(db.Integer, db.ForeignKey(Player.playerID))
    player = db.relationship("Player")
    type = db.Column(db.Integer)
    stage = db.Column(db.Integer)
    time = db.Column(db.FLOAT)
    rank = db.Column(db.Integer)
    dateCreated = db.Column(db.TIMESTAMP)
    dateUpdated = db.Column(db.TIMESTAMP)
    serverID = db.Column(db.Integer, db.ForeignKey(Server.serverID))
    server = db.relationship("Server")
    completions = db.Column(db.Integer)
    bestRank = db.Column(db.Integer)
    dateDemoted = db.Column(db.TIMESTAMP)


class Replay(db.Model):
    __tablename__ = "cs_recordings"
    recordingID = db.Column(db.Integer, primary_key=True)
    mapID = db.Column(db.Integer, db.ForeignKey(Map.mapID))
    map = db.relationship("Map")
    playerID = db.Column(db.Integer, db.ForeignKey(Player.playerID))
    player = db.relationship("Player")
    stage = db.Column(db.Integer)
    type = db.Column(db.Integer)
    time = db.Column(db.Float)
    completionDate = db.Column(db.TIMESTAMP)
    isUploaded = db.Column(db.Integer)
    isDeleted = db.Column(db.Integer)
    md5 = db.Column(db.VARCHAR(64))
    length = db.Column(db.Integer)

    def to_dict(self):
        return dict(recording_id=self.recordingID, map_id=self.mapID, player_id=self.playerID, user_name=self.player.name,
                    stage=self.stage, type=self.type, time=self.time, completion_date=str(self.completionDate),
                    is_uploaded=self.isUploaded, is_deleted=self.isDeleted, file_name=self.get_file_name(),
                    length=self.length, is_record=self.is_record())

    def get_file_name(self):
        return f'{self.map.name}_{self.recordingID}_{self.type}_{self.stage}.rec'

    def is_record(self):
        record = Time.query.filter_by(rank=1, mapID=self.mapID, type=self.type,
                                      stage=self.stage, playerID=self.playerID).order_by(Time.type, Time.stage).first()

        return True if record else False

