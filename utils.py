from .sauerconsts import *
import struct
import math


def sauer2unicode(arg) -> str:
    result = ""

    for i in arg:
        if isinstance(i, int):
            result += unicode_characters[i]
        else:
            result += unicode_characters[int.from_bytes(i, byteorder="little")]

    return result


def getuint(stream) -> int:
    n = int.from_bytes(stream.read(1), byteorder="little")
    if n & (1 << 7):
        n += ((int.from_bytes(stream.read(1), byteorder="little")) << 7) - (
            1 << 7
        )
        if n & (1 << 14):
            n += (
                (int.from_bytes(stream.read(1), byteorder="little")) << 14
            ) - (1 << 14)
        if n & (1 << 21):
            n += (
                (int.from_bytes(stream.read(1), byteorder="little")) << 21
            ) - (1 << 21)
        if n & (1 << 28):
            n |= 4026531840
    return n


def getint(stream) -> int:
    c = int.from_bytes(stream.read(1), byteorder="little", signed=True)
    if c == -128:
        n = int.from_bytes(stream.read(1), byteorder="little")
        n |= (
            int.from_bytes(stream.read(1), byteorder="little", signed=True)
        ) << 8
        return n
    elif c == -127:
        n = int.from_bytes(stream.read(1), byteorder="little")
        n |= (int.from_bytes(stream.read(1), byteorder="little")) << 8
        n |= (int.from_bytes(stream.read(1), byteorder="little")) << 16
        n |= (int.from_bytes(stream.read(1), byteorder="little")) << 24
        return n
    else:
        return c


def getfloat(stream) -> float:
    return struct.unpack("f", stream.read(4))


def getstr(stream) -> str:
    buf = []
    val = int.from_bytes(stream.read(1), byteorder="little")
    while val != 0:
        buf.append(val)
        val = int.from_bytes(stream.read(1), byteorder="little")

    return sauer2unicode(buf)


def clamp(num, min_value, max_value):
    num = max(min(num, max_value), min_value)
    return num


def packet_dict(packet) -> dict:
    args = packet.raw_args

    res = {}

    if packet._type == N_DEMOPACKET:
        pass
    elif packet._type == N_SERVINFO:
        res = {
            "mycn": args[0],
            "prot": args[1],
            "sessionid": args[2],
            "pwdprotected": args[3],
            "servinfo": args[4],
            "servauth": args[5],
        }
    elif packet._type == N_WELCOME:
        pass
    elif packet._type == N_PAUSEGAME:
        res = {"val": args[0], "cn": args[1]}
    elif packet._type == N_GAMESPEED:
        res = {"val": args[0], "cn": args[1]}
    elif packet._type == N_CLIENT:
        res = {
            "cn": args[0],
            "length": args[1],
            "buff": args[2].decode("latin1"),
        }
    elif packet._type == N_SOUND:
        res = {"cn": args[0], "val": args[1]}
    elif packet._type == N_TEXT:
        res = {"cn": args[0], "text": args[1]}
    elif packet._type == N_SAYTEAM:
        res = {"cn": args[0], "text": args[1]}
    elif packet._type == N_MAPCHANGE:
        res = {"map": args[0], "mode": args[1], "spawnitems": args[2]}
    elif packet._type == N_FORCEDEATH:
        res = {"cn": args[0]}
    elif packet._type == N_ITEMLIST:
        ents = []

        for i in range(int((len(args) - 1) / 2)):
            ents.append((args[i * 2], args[i * 2 + 1]))

        res = {"ents": ents}
    elif packet._type == N_INITCLIENT:
        res = {
            "cn": args[0],
            "name": args[1],
            "team": args[2],
            "model": args[3],
        }
    elif packet._type == N_SWITCHNAME:
        res = {"cn": args[0], "name": args[1]}
    elif packet._type == N_SWITCHMODEL:
        res = {"cn": args[0], "model": args[1]}
    elif packet._type == N_CDIS:
        res = {"cn": args[0]}
    elif packet._type == N_SPAWN:
        res = {
            "cn": args[0],
            "lifesequence": args[1],
            "health": args[2],
            "maxhealth": args[3],
            "armour": args[4],
            "armourtype": args[5],
            "gunselect": args[6],
            "ammo": {
                "SG": args[7],
                "CG": args[8],
                "RL": args[9],
                "RIFLE": args[10],
                "GL": args[11],
                "PISTOL": args[12],
            },
        }
    elif packet._type == N_SPAWNSTATE:
        res = {
            "cn": args[0],
            "lifesequence": args[1],
            "health": args[2],
            "maxhealth": args[3],
            "armour": args[4],
            "armourtype": args[5],
            "gunselect": args[6],
            "ammo": {
                "SG": args[7],
                "CG": args[8],
                "RL": args[9],
                "RIFLE": args[10],
                "GL": args[11],
                "PISTOL": args[12],
            },
        }
    elif packet._type == N_SHOTFX:
        res = {
            "cn": args[0],
            "gunselect": args[1],
            "id": args[2],
            "from": {
                "x": args[3] / DMF,
                "y": args[4] / DMF,
                "z": args[5] / DMF,
            },
            "to": {"x": args[6] / DMF, "y": args[7] / DMF, "z": args[8] / DMF},
        }
    elif packet._type == N_EXPLODEFX:
        res = {"cn": args[0], "gun": args[1], "id": args[2]}
    elif packet._type == N_DAMAGE:
        res = {
            "tcn": args[0],
            "acn": args[1],
            "damage": args[2],
            "armour": args[3],
            "health": args[4],
        }
    elif packet._type == N_HITPUSH:
        res = {
            "cn": args[0],
            "gun": args[1],
            "damage": args[2],
            "dir": {"x": args[3] / DMF, "y": args[4] / DMF, "z": args[5] / DMF},
        }
    elif packet._type == N_DIED:
        res = {
            "vcn": args[0],
            "acn": args[1],
            "frags": args[2],
            "tfrags": args[3],
        }
    elif packet._type == N_TEAMINFO:
        res = {}

        for i in range(int(len(args) / 2)):
            res[args[i * 2]] = args[i * 2 + 1]

    elif packet._type == N_GUNSELECT:
        res = {"cn": args[0], "gun": args[1]}
    elif packet._type == N_TAUNT:
        res = {"cn": args[0]}
    elif packet._type == N_RESUME:
        res = {}

        len_ = 18

        for i in range(int(len(args) / len_)):
            res[args[i * len_]] = {
                "state": args[i * len_ + 1],
                "frags": args[i * len_ + 2],
                "flags": args[i * len_ + 3],
                "deaths": args[i * len_ + 4],
                "quadmillis": args[i * len_ + 5],
                "lifesequence": args[i * len_ + 6],
                "health": args[i * len_ + 7],
                "maxhealth": args[i * len_ + 8],
                "armour": args[i * len_ + 9],
                "armourtype": args[i * len_ + 10],
                "gunselect": args[i * len_ + 11],
                "ammo": {
                    "SG": args[i * len_ + 12],
                    "CG": args[i * len_ + 13],
                    "RL": args[i * len_ + 14],
                    "RIFLE": args[i * len_ + 15],
                    "GL": args[i * len_ + 16],
                    "PISTOL": args[i * len_ + 17],
                },
            }

    elif packet._type == N_ITEMSPAWN:
        res = {"entid": args[0]}
    elif packet._type == N_ITEMACC:
        res = {"entid": args[0], "cn": args[1]}
    elif packet._type == N_CLIPBOARD:
        res = {
            "cn": args[0],
            "unpacklen": args[1],
            "packlen": args[2],
            "buff": args[3].decode("latin1"),
        }
    elif packet._type == N_UNDO or packet._type == N_REDO:
        res = {
            "cn": args[0],
            "unpacklen": args[1],
            "packlen": args[2],
            "buff": args[3].decode("latin1"),
        }
    elif (
        packet._type == N_EDITF
        or packet._type == N_EDITT
        or packet._type == N_EDITM
        or packet._type == N_FLIP
        or packet._type == N_COPY
        or packet._type == N_PASTE
        or packet._type == N_ROTATE
        or packet._type == N_REPLACE
        or packet._type == N_DELCUBE
        or packet._type == N_EDITVSLOT
    ):

        res = {
            "cn": args[0],
            "sel": {
                "o": {
                    "x": args[1],
                    "y": args[2],
                    "z": args[3],
                },
                "s": {
                    "x": args[4],
                    "y": args[5],
                    "z": args[6],
                },
                "grid": args[7],
                "orient": args[8],
                "cx": args[9],
                "cxs": args[10],
                "cy": args[11],
                "cys": args[12],
                "corner": args[13],
            },
        }

        if packet._type == N_EDITF:
            res["dir"] = args[14]
            res["mode"] = args[15]

        if packet._type == N_EDITT:
            res["tex"] = args[14]
            res["allfaces"] = args[15]

        if packet._type == N_EDITM:
            res["mat"] = args[14]
            res["filter"] = args[15]

        if packet._type == N_ROTATE:
            res["dir"] = args[14]

        if packet._type == N_REPLACE:
            res["oldtex"] = args[14]
            res["newtex"] = args[15]
            res["insel"] = args[16]

        if packet._type == N_EDITVSLOT:
            res["delta"] = args[14]
            res["allfaces"] = args[15]

    elif packet._type == N_REMIP:
        res = {"cn": args[0]}

    elif packet._type == N_EDITENT:
        res = {
            "cn": args[0],
            "entid": args[1],
            "x": args[2] / DMF,
            "y": args[3] / DMF,
            "z": args[4] / DMF,
            "type": args[5],
            "attr1": args[6],
            "attr2": args[7],
            "attr3": args[8],
            "attr4": args[9],
            "attr5": args[10],
        }

    elif packet._type == N_EDITVAR:
        res = {"cn": args[0], "type": args[1], "name": args[2], "val": args[3]}

    elif packet._type == N_PONG:
        res = {"ping": args[0]}

    elif packet._type == N_CLIENTPING:
        res = {"cn": args[0], "ping": args[1]}

    elif packet._type == N_TIMEUP:
        res = {"secs": args[0]}

    elif packet._type == N_SERVMSG:
        res = {"msg": args[0]}

    elif packet._type == N_SENDDEMOLIST:
        demos = []

        for i in range(args[0]):
            demos.append(args[i + 1])

        res = {"numdemos": args[0], "demos": demos}

    elif packet._type == N_DEMOPLAYBACK:
        res = {"on": args[0], "cn": args[1]}

    elif packet._type == N_CURRENTMASTER:
        res = {"mastermode": args[0], "clients": {}}

        for i in range(int(len(args) / 2) - 2):
            res["clients"][args[i * 2 + 1]] = args[(i + 1) * 2]

    elif packet._type == N_MASTERMODE:
        res = {"mastermode": args[0]}

    elif packet._type == N_EDITMODE:
        res = {"cn": args[0], "val": args[1]}

    elif packet._type == N_SPECTATOR:
        res = {"cn": args[0], "val": args[1]}

    elif packet._type == N_SETTEAM:
        res = {"cn": args[0], "team": args[1], "reason": args[2]}

    elif packet._type == N_BASEINFO:
        res = {
            "base": args[0],
            "owner": args[1],
            "enemy": args[2],
            "converted": args[3],
            "ammo": args[4],
        }

    elif packet._type == N_BASEREGEN:
        res = {
            "cn": args[0],
            "health": args[1],
            "armour": args[2],
            "ammotype": args[3],
            "ammo": args[4],
        }

    elif packet._type == N_BASES:
        res = {"numbases": args[0], "bases": []}

        len_ = 5

        for i in range(args[0]):
            base = {
                "ammotype": args[i * len_ + 1],
                "owner": args[i * len_ + 2],
                "enemy": args[i * len_ + 3],
                "converted": args[i * len_ + 4],
                "ammo": args[i * len_ + 5],
            }

            res["bases"].append(base)

    elif packet._type == N_BASESCORE:
        res = {"base": args[0], "team": args[1], "total": args[2]}

    elif packet._type == N_REPAMMO:
        res = {"cn": args[0], "ammotype": args[1]}

    elif packet._type == N_INITFLAGS:
        res = {"scores": [args[0], args[1]], "numflags": args[2], "flags": []}

        offset = 3

        for i in range(args[2]):
            flag = {
                "version": args[offset],
                "spawn": args[offset + 1],
                "owner": args[offset + 2],
                "invis": args[offset + 3],
            }

            offset += 4

            if flag["owner"] < 0:
                flag["dropped"] = args[offset]

                offset += 1

                if flag["dropped"]:
                    flag["droploc"] = {
                        "x": args[offset] / DMF,
                        "y": args[offset + 1] / DMF,
                        "z": args[offset + 2] / DMF,
                    }

                    offset += 3

            if packet.context["current_mode"] in [
                m_hold,
                m_insta_hold,
                m_effic_hold,
            ]:
                flag["holdteam"] = args[offset]

                offset += 1

                if flag["holdteam"] >= 0:
                    flag["holdtime"] = args[offset] * 100

                    offset += 1

            res["flags"].append(flag)

    elif packet._type == N_DROPFLAG:
        res = {
            "cn": args[0],
            "flag": args[1],
            "version": args[2],
            "droploc": {
                "x": args[3] / DMF,
                "y": args[4] / DMF,
                "z": args[5] / DMF,
            },
        }

    elif packet._type == N_SCOREFLAG:
        res = {
            "cn": args[0],
            "relayflag": args[1],
            "relayversion": args[2],
            "goalflag": args[3],
            "goalversion": args[4],
            "goalspawn": args[5],
            "team": args[6],
            "score": args[7],
            "oflags": args[8],
        }

    elif packet._type == N_RETURNFLAG:
        res = {"cn": args[0], "flag": args[1], "version": args[2]}

    elif packet._type == N_TAKEFLAG:
        res = {"cn": args[0], "flag": args[1], "version": args[2]}

    elif packet._type == N_RESETFLAG:
        res = {
            "flag": args[0],
            "version": args[1],
            "spawnindex": args[2],
            "team": args[3],
            "score": args[4],
        }

    elif packet._type == N_INVISFLAG:
        res = {"flag": args[0], "invis": args[1]}

    elif packet._type == N_INITTOKENS:
        res = {
            "scores": [args[0], args[1]],
            "numtokens": args[2],
            "tokens": [],
            "clients": [],
        }

        offset = 3

        for i in range(args[2]):
            token = {
                "id": args[offset],
                "team": args[offset + 1],
                "yaw": args[offset + 2],
                "o": {
                    "x": args[offset + 3] / DMF,
                    "y": args[offset + 4] / DMF,
                    "z": args[offset + 5] / DMF,
                },
            }

            res["tokens"].append(token)

            offset += 6

        for i in range(int((len(args) + 1 - offset) / 2)):
            res["clients"].append(
                {"cn": args[offset + i * 2], "tokens": args[offset + i * 2 + 1]}
            )

    elif packet._type == N_TAKETOKEN:
        res = {"cn": args[0], "id": args[1], "total": args[2]}

    elif packet._type == N_EXPIRETOKENS:
        res = {"tokens": args}

    elif packet._type == N_DROPTOKENS:
        res = {
            "cn": args[0],
            "droploc": {
                "x": args[1] / DMF,
                "y": args[2] / DMF,
                "z": args[3] / DMF,
            },
            "tokens": [],
        }

        offset = 4

        for i in range(int((len(args) - 4) / 3)):
            res["tokens"].append(
                {
                    "id": args[offset + i * 3],
                    "team": args[offset + i * 3 + 1],
                    "yaw": args[offset + i * 3 + 2],
                }
            )

    elif packet._type == N_STEALTOKENS:
        res = {
            "cn": args[0],
            "team": args[1],
            "basenum": args[2],
            "enemyteam": args[3],
            "score": args[4],
            "droploc": {
                "x": args[5] / DMF,
                "y": args[6] / DMF,
                "z": args[7] / DMF,
            },
            "tokens": [],
        }

        offset = 8

        for i in range(int((len(args) - 8) / 2)):
            res["tokens"].append(
                {"id": args[offset + i * 2], "yaw": args[offset + i * 2 + 1]}
            )

    elif packet._type == N_DEPOSITTOKENS:
        res = {
            "cn": args[0],
            "base": args[1],
            "deposited": args[2],
            "team": args[3],
            "score": args[4],
            "flags": args[5],
        }

    elif packet._type == N_ANNOUNCE:
        res = {"type": args[0]}

    elif packet._type == N_NEWMAP:
        res = {"cn": args[0], "size": args[1]}

    elif packet._type == N_REQAUTH:
        res = {"authdomain": args[0]}

    elif packet._type == N_AUTHCHAL:
        res = {"desc": args[0], "id": args[1], "authchallenge": args[2]}

    elif packet._type == N_INITAI:
        res = {
            "bn": args[0],
            "on": args[1],
            "aitype": args[2],
            "skill": args[3],
            "pm": args[4],
            "name": args[5],
            "team": args[6],
        }

    elif packet._type == N_SERVCMD:
        res = {"command": args[0]}

    elif packet._type == N_POS:
        res = {"cn": args[0], "o": {}}

        physstate = args[1]
        flags = args[2]

        offset = 3

        for i in range(3):
            EYEHEIGHT = 14

            n = args[offset]
            offset += 1
            n |= args[offset] << 8
            offset += 1

            if flags & (1 << i):
                n |= args[offset] << 16
                offset += 1

            if n & 0x800000:
                n |= ~0 << 24

            if i == 0:
                res["o"]["x"] = n / DMF

            if i == 1:
                res["o"]["y"] = n / DMF

            if i == 2:
                res["o"]["z"] = n / DMF
                res["o"]["z"] += EYEHEIGHT

        dir = args[offset]
        dir |= args[offset + 1] << 8

        yaw = dir % 360
        pitch = clamp(dir / 360, 0, 180) - 90
        roll = clamp(args[offset + 2], 0, 180) - 90

        mag = args[offset + 3]

        offset += 4

        if flags & (1 << 3):
            mag |= args[offset] << 8
            offset += 1

        dir = args[offset]
        dir |= args[offset + 1] << 8

        offset += 2

        falling = {"x": 0, "y": 0, "z": 0}

        vel = {
            "x": -math.sin(math.radians(dir % 360)),
            "y": math.cos(math.radians(dir % 360)),
            "z": 0,
        }

        if clamp(dir / 360, 0, 180) - 90:
            vel["x"] *= math.cos(math.radians(clamp(dir / 360, 0, 180) - 90))
            vel["y"] *= math.cos(math.radians(clamp(dir / 360, 0, 180) - 90))
            vel["z"] = math.sin(math.radians(clamp(dir / 360, 0, 180) - 90))

        vel["x"] *= mag
        vel["y"] *= mag
        vel["z"] *= mag

        if flags & (1 << 4):
            mag = args[offset]
            offset += 1

            if flags & (1 << 5):
                mag |= args[offset] << 8
                offset += 1

            if flags & (1 << 6):
                dir = args[offset]
                dir |= args[offset + 1] << 8

                offset += 2

                falling["x"] = -math.sin(math.radians(dir % 360))
                falling["y"] = math.cos(math.radians(dir % 360))

                if clamp(dir / 360, 0, 180) - 90:
                    falling["x"] *= math.cos(
                        math.radians(clamp(dir / 360, 0, 180) - 90)
                    )
                    falling["y"] *= math.cos(
                        math.radians(clamp(dir / 360, 0, 180) - 90)
                    )
                    falling["z"] = math.sin(
                        math.radians(clamp(dir / 360, 0, 180) - 90)
                    )

            else:
                falling["x"] = 0
                falling["y"] = 0
                falling["z"] = -1

            falling["x"] *= mag
            falling["y"] *= mag
            falling["z"] *= mag

        seqcolor = (physstate >> 3) & 1

        res["yaw"] = yaw
        res["pitch"] = pitch
        res["roll"] = roll
        res["move"] = -1 if (physstate >> 4) & 2 else (physstate >> 4) & 1
        res["strafe"] = -1 if (physstate >> 6) & 2 else (physstate >> 6) & 1
        res["vel"] = vel
        res["falling"] = falling
        res["physstate"] = physstate

    elif packet._type == N_TELEPORT:
        res = {"cn": args[0], "tp": args[1], "td": args[2]}

    elif packet._type == N_JUMPPAD:
        res = {"cn": args[0], "jp": args[1]}

    return res


class InvalidVariable(Exception):
    pass


class InvalidAction(Exception):
    pass
