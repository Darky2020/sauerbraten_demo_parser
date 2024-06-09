from .packet import Packet, PacketList
from dataclasses import dataclass
from .sauerconsts import *
from .utils import *
import gzip
import io


@dataclass
class Stamp:
    time: int
    channel: int
    length: int


@dataclass
class DemoHeader:
    magic: bytes
    file_version: int
    protocol_version: int


class DemoParser(object):
    def __init__(self):
        self.packets = []
        self.current_mode = -1

    def add_packet(self, packet, stamp, args=[], context={}):
        self.packets.append(Packet(packet, stamp.time, args, context))

    def read_stamp(self, stream):
        time = 0
        channel = 0
        length = 0
        error = None

        try:
            time = int.from_bytes(stream.read(4), byteorder="little")
            channel = int.from_bytes(stream.read(4), byteorder="little")
            length = int.from_bytes(stream.read(4), byteorder="little")
        except Exception as e:
            error = e

        return Stamp(time, channel, length), error

    def read_packet(self, stream):
        stamp, error = self.read_stamp(stream)
        if error:
            return None, None, error

        buff = bytes([])

        try:
            buff = stream.read(stamp.length)
        except Exception as e:
            return None, None, e

        return stamp, buff, None

    def read_header(self, stream):
        magic = b""
        file_version = 0
        protocol_version = 0

        try:
            magic = stream.read(16)
            file_version = int.from_bytes(stream.read(4), byteorder="little")
            protocol_version = int.from_bytes(
                stream.read(4), byteorder="little"
            )
        except Exception as e:
            return None, e

        if magic.decode("utf-8") != "SAUERBRATEN_DEMO":
            return None, "reading demo header: wrong magic (not a demo file?)"

        header = DemoHeader(magic, file_version, protocol_version)
        return header, None

    def parse_state(self, data, resume=False):
        args = []

        if resume:
            args.append(getint(data))
            args.append(getint(data))
            args.append(getint(data))
            args.append(getint(data))
            args.append(getint(data))

        args.append(getint(data))
        args.append(getint(data))
        args.append(getint(data))
        args.append(getint(data))
        args.append(getint(data))

        args.append(getint(data))

        for _ in range(GUN_PISTOL - GUN_SG + 1):
            args.append(getint(data))

        return args

    def parse_messages(self, _cn, stamp, data, error):
        if error:
            print(f"error parsing demo: {error}")

        data = io.BytesIO(data)

        while data.tell() < data.getbuffer().nbytes:
            packet = getint(data)

            if packet == N_DEMOPACKET:
                self.add_packet(N_DEMOPACKET, stamp)

            elif packet == N_SERVINFO:
                self.add_packet(
                    N_SERVINFO,
                    stamp,
                    [
                        getint(data),
                        getint(data),
                        getint(data),
                        getint(data),
                        getstr(data),
                        getstr(data),
                    ],
                )

            elif packet == N_WELCOME:
                self.add_packet(N_WELCOME, stamp)

            elif packet == N_PAUSEGAME:
                self.add_packet(
                    N_PAUSEGAME, stamp, [getint(data), getint(data)]
                )

            elif packet == N_GAMESPEED:
                self.add_packet(
                    N_GAMESPEED, stamp, [getint(data), getint(data)]
                )

            elif packet == N_CLIENT:
                cn = getint(data)
                length = getuint(data)
                buff = data.read(length)

                self.add_packet(N_CLIENT, stamp, [cn, length, buff])

                if length > 0:
                    self.parse_messages(
                        cn,
                        Stamp(stamp.time, stamp.channel, length),
                        buff,
                        error,
                    )

            elif packet == N_SOUND:
                self.add_packet(N_SOUND, stamp, [_cn, getint(data)])

            elif packet == N_TEXT:
                self.add_packet(N_TEXT, stamp, [_cn, getstr(data)])

            elif packet == N_SAYTEAM:
                self.add_packet(N_SAYTEAM, stamp, [getint(data), getstr(data)])

            elif packet == N_MAPCHANGE:
                args = [getstr(data)]

                mode = getint(data)
                args.append(mode)
                args.append(getint(data))

                self.current_mode = mode

                self.add_packet(N_MAPCHANGE, stamp, args)

            elif packet == N_FORCEDEATH:
                self.add_packet(N_FORCEDEATH, stamp, [getint(data)])

            elif packet == N_ITEMLIST:
                args = []
                while data.tell() < data.getbuffer().nbytes:
                    n = getint(data)
                    args.append(n)

                    if n < 0:
                        break

                    args.append(getint(data))

                self.add_packet(N_ITEMLIST, stamp, args)

            elif packet == N_INITCLIENT:
                self.add_packet(
                    N_INITCLIENT,
                    stamp,
                    [getint(data), getstr(data), getstr(data), getint(data)],
                )

            elif packet == N_SWITCHNAME:
                self.add_packet(N_SWITCHNAME, stamp, [_cn, getstr(data)])

            elif packet == N_SWITCHMODEL:
                self.add_packet(N_SWITCHMODEL, stamp, [_cn, getint(data)])

            elif packet == N_CDIS:
                self.add_packet(N_CDIS, stamp, [getint(data)])

            elif packet == N_SPAWN:
                self.add_packet(N_SPAWN, stamp, [_cn] + self.parse_state(data))

            elif packet == N_SPAWNSTATE:
                self.add_packet(
                    N_SPAWNSTATE, stamp, [getint(data)] + self.parse_state(data)
                )

            elif packet == N_SHOTFX:
                self.add_packet(
                    N_SHOTFX,
                    stamp,
                    [
                        getint(data),
                        getint(data),
                        getint(data),
                        getint(data),
                        getint(data),
                        getint(data),
                        getint(data),
                        getint(data),
                        getint(data),
                    ],
                )

            elif packet == N_EXPLODEFX:
                self.add_packet(
                    N_EXPLODEFX,
                    stamp,
                    [getint(data), getint(data), getint(data)],
                )

            elif packet == N_DAMAGE:
                self.add_packet(
                    N_DAMAGE,
                    stamp,
                    [
                        getint(data),
                        getint(data),
                        getint(data),
                        getint(data),
                        getint(data),
                    ],
                )

            elif packet == N_HITPUSH:
                self.add_packet(
                    N_HITPUSH,
                    stamp,
                    [
                        getint(data),
                        getint(data),
                        getint(data),
                        getint(data),
                        getint(data),
                        getint(data),
                    ],
                )

            elif packet == N_DIED:
                self.add_packet(
                    N_DIED,
                    stamp,
                    [getint(data), getint(data), getint(data), getint(data)],
                )

            elif packet == N_TEAMINFO:
                args = []

                while True:
                    text = getstr(data)
                    args.append(text)

                    if not data.tell() < data.getbuffer().nbytes or not text:
                        break

                    args.append(getint(data))

                    if not data.tell() < data.getbuffer().nbytes:
                        break

                self.add_packet(N_TEAMINFO, stamp, args)

            elif packet == N_GUNSELECT:
                self.add_packet(N_GUNSELECT, stamp, [_cn, getint(data)])

            elif packet == N_TAUNT:
                self.add_packet(N_TAUNT, stamp, [_cn])

            elif packet == N_RESUME:
                args = []

                while True:
                    cn = getint(data)
                    args.append(cn)

                    if not data.tell() < data.getbuffer().nbytes or cn < 0:
                        break

                    args += self.parse_state(data, resume=True)

                self.add_packet(N_RESUME, stamp, args)

            elif packet == N_ITEMSPAWN:
                self.add_packet(N_ITEMSPAWN, stamp, [getint(data)])

            elif packet == N_ITEMACC:
                self.add_packet(N_ITEMACC, stamp, [getint(data), getint(data)])

            elif packet == N_CLIPBOARD:
                self.add_packet(
                    N_CLIPBOARD,
                    stamp,
                    [getint(data), getint(data), getint(data), data],
                )

            elif packet == N_UNDO or packet == N_REDO:
                self.add_packet(
                    packet,
                    stamp,
                    [getint(data), getint(data), getint(data), data],
                )

            elif (
                packet == N_EDITF
                or packet == N_EDITT
                or packet == N_EDITM
                or packet == N_FLIP
                or packet == N_COPY
                or packet == N_PASTE
                or packet == N_ROTATE
                or packet == N_REPLACE
                or packet == N_DELCUBE
                or packet == N_EDITVSLOT
            ):
                args = [_cn]

                args.append(getint(data))
                args.append(getint(data))
                args.append(getint(data))

                args.append(getint(data))
                args.append(getint(data))
                args.append(getint(data))

                args.append(getint(data))
                args.append(getint(data))

                args.append(getint(data))
                args.append(getint(data))
                args.append(getint(data))
                args.append(getint(data))

                args.append(getint(data))

                if packet == N_EDITF or packet == N_EDITT or packet == N_EDITM:
                    args.append(getint(data))
                    args.append(getint(data))

                if packet == N_ROTATE:
                    args.append(getint(data))

                if packet == N_REPLACE:
                    args.append(getint(data))
                    args.append(getint(data))
                    args.append(getint(data))

                if packet == N_EDITVSLOT:
                    args.append(getint(data))
                    args.append(getint(data))

                self.add_packet(packet, stamp, args)

            elif packet == N_REMIP:
                self.add_packet(N_REMIP, stamp, [_cn])

            elif packet == N_EDITENT:
                self.add_packet(
                    N_EDITENT,
                    stamp,
                    [
                        _cn,
                        getint(data),
                        getint(data),
                        getint(data),
                        getint(data),
                        getint(data),
                        getint(data),
                        getint(data),
                        getint(data),
                        getint(data),
                        getint(data),
                    ],
                )

            elif packet == N_EDITVAR:
                args = [_cn]

                type = getint(data)
                args.append(type)

                args.append(getstr(data))

                if type == ID_VAR:
                    args.append(getint(data))

                elif type == ID_FVAR:
                    args.append(getfloat(data))

                elif type == ID_SVAR:
                    args.append(getstr(data))

                self.add_packet(N_EDITVAR, stamp, args)

            elif packet == N_PONG:
                self.add_packet(N_PONG, stamp, [getint(data)])

            elif packet == N_CLIENTPING:
                self.add_packet(N_CLIENTPING, stamp, [_cn, getint(data)])

            elif packet == N_TIMEUP:
                self.add_packet(N_TIMEUP, stamp, [getint(data)])

            elif packet == N_SERVMSG:
                self.add_packet(N_SERVMSG, stamp, [getstr(data)])

            elif packet == N_SENDDEMOLIST:
                args = []

                demos = getint(data)
                args.append(demos)

                for _ in range(demos):
                    args.append(getstr(data))

                    if not data.tell() < data.getbuffer().nbytes:
                        break

                self.add_packet(N_SENDDEMOLIST, stamp, args)

            elif packet == N_DEMOPLAYBACK:
                self.add_packet(
                    N_DEMOPLAYBACK, stamp, [getint(data), getint(data)]
                )

            elif packet == N_CURRENTMASTER:
                args = [getint(data)]

                while True:
                    mn = getint(data)

                    args.append(mn)

                    if mn < 0 or not data.tell() < data.getbuffer().nbytes:
                        break

                    args.append(getint(data))

                self.add_packet(N_CURRENTMASTER, stamp, args)

            elif packet == N_MASTERMODE:
                self.add_packet(N_MASTERMODE, stamp, [getint(data)])

            elif packet == N_EDITMODE:
                self.add_packet(N_EDITMODE, stamp, [_cn, getint(data)])

            elif packet == N_SPECTATOR:
                self.add_packet(
                    N_SPECTATOR, stamp, [getint(data), getint(data)]
                )

            elif packet == N_SETTEAM:
                self.add_packet(
                    N_SETTEAM, stamp, [getint(data), getstr(data), getint(data)]
                )

            elif packet == N_BASEINFO:
                self.add_packet(
                    N_BASEINFO,
                    stamp,
                    [
                        getint(data),
                        getstr(data),
                        getstr(data),
                        getint(data),
                        getint(data),
                    ],
                )

            elif packet == N_BASEREGEN:
                self.add_packet(
                    N_BASEREGEN,
                    stamp,
                    [
                        getint(data),
                        getint(data),
                        getint(data),
                        getint(data),
                        getint(data),
                    ],
                )

            elif packet == N_BASES:
                args = []

                numbases = getint(data)
                args.append(numbases)

                for _ in range(numbases):
                    args.append(getint(data))

                    args.append(getstr(data))
                    args.append(getstr(data))

                    args.append(getint(data))
                    args.append(getint(data))

                self.add_packet(N_BASES, stamp, args)

            elif packet == N_BASESCORE:
                self.add_packet(
                    N_BASESCORE,
                    stamp,
                    [getint(data), getstr(data), getint(data)],
                )

            elif packet == N_REPAMMO:
                self.add_packet(N_REPAMMO, stamp, [getint(data), getint(data)])

            elif packet == N_INITFLAGS:
                args = [getint(data), getint(data)]

                numflags = getint(data)
                args.append(numflags)

                for _ in range(numflags):
                    version = getint(data)
                    spawn = getint(data)
                    owner = getint(data)
                    invis = getint(data)

                    args.append(version)
                    args.append(spawn)
                    args.append(owner)
                    args.append(invis)

                    if owner < 0:
                        dropped = getint(data)
                        args.append(dropped)

                        if dropped:
                            for _ in range(3):
                                args.append(getint(data))

                    if self.current_mode in [
                        m_hold,
                        m_insta_hold,
                        m_effic_hold,
                    ]:
                        holdteam = getint(data)
                        args.append(holdteam)

                        if holdteam >= 0:
                            args.append(getint(data))

                self.add_packet(
                    N_INITFLAGS,
                    stamp,
                    args,
                    {"current_mode": self.current_mode},
                )

            elif packet == N_DROPFLAG:
                self.add_packet(
                    N_DROPFLAG,
                    stamp,
                    [
                        getint(data),
                        getint(data),
                        getint(data),
                        getint(data),
                        getint(data),
                        getint(data),
                    ],
                )

            elif packet == N_SCOREFLAG:
                self.add_packet(
                    N_SCOREFLAG,
                    stamp,
                    [
                        getint(data),
                        getint(data),
                        getint(data),
                        getint(data),
                        getint(data),
                        getint(data),
                        getint(data),
                        getint(data),
                        getint(data),
                    ],
                )

            elif packet == N_RETURNFLAG:
                self.add_packet(
                    N_RETURNFLAG,
                    stamp,
                    [getint(data), getint(data), getint(data)],
                )

            elif packet == N_TAKEFLAG:
                self.add_packet(
                    N_TAKEFLAG,
                    stamp,
                    [getint(data), getint(data), getint(data)],
                )

            elif packet == N_RESETFLAG:
                self.add_packet(
                    N_RESETFLAG,
                    stamp,
                    [
                        getint(data),
                        getint(data),
                        getint(data),
                        getint(data),
                        getint(data),
                    ],
                )

            elif packet == N_INVISFLAG:
                self.add_packet(
                    N_INVISFLAG, stamp, [getint(data), getint(data)]
                )

            elif packet == N_INITTOKENS:
                args = [getint(data), getint(data)]

                numtokens = getint(data)
                args.append(numtokens)

                for _ in range(numtokens):
                    for _ in range(6):
                        args.append(getint(data))

                    if not data.tell() < data.getbuffer().nbytes:
                        break

                while True:
                    cn = getint(data)
                    args.append(cn)

                    if cn < 0:
                        break

                    args.append(getint(data))

                    if not data.tell() < data.getbuffer().nbytes:
                        break

                self.add_packet(N_INITTOKENS, stamp, args)

            elif packet == N_TAKETOKEN:
                self.add_packet(
                    N_TAKETOKEN,
                    stamp,
                    [getint(data), getint(data), getint(data)],
                )

            elif packet == N_EXPIRETOKENS:
                args = []

                while True:
                    id = getint(data)
                    args.append(id)

                    if not data.tell() < data.getbuffer().nbytes or id < 0:
                        break

                self.add_packet(N_EXPIRETOKENS, stamp, args)

            elif packet == N_DROPTOKENS:
                args = [getint(data)]

                for _ in range(3):
                    args.append(getint(data))

                while True:
                    id = getint(data)
                    args.append(id)

                    if id < 0:
                        break

                    args.append(getint(data))
                    args.append(getint(data))

                    if not data.tell() < data.getbuffer().nbytes:
                        break

                self.add_packet(N_DROPTOKENS, stamp, args)

            elif packet == N_STEALTOKENS:
                args = [
                    getint(data),
                    getint(data),
                    getint(data),
                    getint(data),
                    getint(data),
                ]

                for _ in range(3):
                    args.append(getint(data))

                while True:
                    id = getint(data)
                    args.append(id)

                    if id < 0:
                        break

                    args.append(getint(data))

                    if not data.tell() < data.getbuffer().nbytes:
                        break

                self.add_packet(N_STEALTOKENS, stamp, args)

            elif packet == N_DEPOSITTOKENS:
                self.add_packet(
                    N_DEPOSITTOKENS,
                    stamp,
                    [
                        getint(data),
                        getint(data),
                        getint(data),
                        getint(data),
                        getint(data),
                        getint(data),
                    ],
                )

            elif packet == N_ANNOUNCE:
                self.add_packet(N_ANNOUNCE, stamp, [getint(data)])

            elif packet == N_NEWMAP:
                self.add_packet(N_NEWMAP, stamp, [_cn, getint(data)])

            elif packet == N_REQAUTH:
                self.add_packet(N_REQAUTH, stamp, [getstr(data)])

            elif packet == N_AUTHCHAL:
                self.add_packet(
                    N_AUTHCHAL,
                    stamp,
                    [getstr(data), getint(data), getstr(data)],
                )

            elif packet == N_INITAI:
                self.add_packet(
                    N_INITAI,
                    stamp,
                    [
                        getint(data),
                        getint(data),
                        getint(data),
                        getint(data),
                        getint(data),
                        getstr(data),
                        getstr(data),
                    ],
                )

            elif packet == N_SERVCMD:
                self.add_packet(N_SERVCMD, stamp, [getstr(data)])

            elif packet == N_POS:
                args = []

                cn = getuint(data)
                args.append(cn)

                physstate = int.from_bytes(data.read(1), byteorder="little")
                args.append(physstate)

                flags = getuint(data)
                args.append(flags)

                for k in range(3):
                    n = int.from_bytes(data.read(1), byteorder="little")
                    args.append(n)

                    tmp = int.from_bytes(data.read(1), byteorder="little")
                    args.append(tmp)

                    n |= tmp << 8

                    if flags & (1 << k):
                        tmp = int.from_bytes(data.read(1), byteorder="little")
                        args.append(tmp)

                        n |= tmp << 16

                        if n & 0x800000:
                            n |= ~0 << 24

                dir = int.from_bytes(data.read(1), byteorder="little")
                args.append(dir)

                tmp = int.from_bytes(data.read(1), byteorder="little")
                args.append(tmp)

                dir |= tmp << 8

                roll = int.from_bytes(data.read(1), byteorder="little")
                args.append(roll)

                mag = int.from_bytes(data.read(1), byteorder="little")
                args.append(mag)

                if flags & (1 << 3):
                    tmp = int.from_bytes(data.read(1), byteorder="little")
                    args.append(tmp)

                    mag |= tmp << 8

                dir = int.from_bytes(data.read(1), byteorder="little")
                args.append(dir)

                tmp = int.from_bytes(data.read(1), byteorder="little")
                args.append(tmp)

                dir |= tmp << 8

                if flags & (1 << 4):
                    mag = int.from_bytes(data.read(1), byteorder="little")
                    args.append(mag)

                    if flags & (1 << 5):
                        tmp = int.from_bytes(data.read(1), byteorder="little")
                        args.append(tmp)

                        mag |= tmp << 8

                    if flags & (1 << 6):
                        dir = int.from_bytes(data.read(1), byteorder="little")
                        args.append(dir)

                        tmp = int.from_bytes(data.read(1), byteorder="little")
                        args.append(tmp)

                        dir |= tmp << 8

                self.add_packet(N_POS, stamp, args)

            elif packet == N_TELEPORT:
                self.add_packet(
                    N_TELEPORT,
                    stamp,
                    [getint(data), getint(data), getint(data)],
                )

            elif packet == N_JUMPPAD:
                self.add_packet(N_JUMPPAD, stamp, [getint(data), getint(data)])

            else:
                error = f"Couldn't read packet: {packet}"
                getint(data)

    def parse_raw(self, raw, compressed=True):
        if compressed:
            raw = gzip.decompress(raw)

        stream = io.BytesIO(raw)

        header, error = self.read_header(stream)

        self.packets = []
        self.current_mode = -1

        if error:
            print(f"error parsing demo: {error}")
            return None, error

        if header.file_version != 1:
            print(
                "error: unsupported file version (only version 1 is supported)"
            )
            return None, "unsupported file version"

        stamp, data, error = self.read_packet(stream)
        self.parse_messages(-1, stamp, data, error)

        # Some demos have zero length packets inside the stream for some reason
        # so we use this mechanism to skip over them
        EMPTY_PACKET_TRESHOLD = 5
        empty_packet_count = 0

        while stream:
            stamp, data, error = self.read_packet(stream)

            if not data:
                empty_packet_count += 1

                if empty_packet_count > EMPTY_PACKET_TRESHOLD:
                    break

                continue

            empty_packet_count = 0
            self.parse_messages(-1, stamp, data, error)

        packet_list = PacketList(self.packets)

        return packet_list

    def parse(self, filename):
        stream = gzip.open(filename, "rb")

        return self.parse_raw(stream.read(), compressed=False)
