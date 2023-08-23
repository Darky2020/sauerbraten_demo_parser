N_CONNECT = 0
N_SERVINFO = 1
N_WELCOME = 2
N_INITCLIENT = 3
N_POS = 4
N_TEXT = 5
N_SOUND = 6
N_CDIS = 7
N_SHOOT = 8
N_EXPLODE = 9
N_SUICIDE = 10
N_DIED = 11
N_DAMAGE = 12
N_HITPUSH = 13
N_SHOTFX = 14
N_EXPLODEFX = 15
N_TRYSPAWN = 16
N_SPAWNSTATE = 17
N_SPAWN = 18
N_FORCEDEATH = 19
N_GUNSELECT = 20
N_TAUNT = 21
N_MAPCHANGE = 22
N_MAPVOTE = 23
N_TEAMINFO = 24
N_ITEMSPAWN = 25
N_ITEMPICKUP = 26
N_ITEMACC = 27
N_TELEPORT = 28
N_JUMPPAD = 29
N_PING = 30
N_PONG = 31
N_CLIENTPING = 32
N_TIMEUP = 33
N_FORCEINTERMISSION = 34
N_SERVMSG = 35
N_ITEMLIST = 36
N_RESUME = 37
N_EDITMODE = 38
N_EDITENT = 39
N_EDITF = 40
N_EDITT = 41
N_EDITM = 42
N_FLIP = 43
N_COPY = 44
N_PASTE = 45
N_ROTATE = 46
N_REPLACE = 47
N_DELCUBE = 48
N_REMIP = 49
N_EDITVSLOT = 50
N_UNDO = 51
N_REDO = 52
N_NEWMAP = 53
N_GETMAP = 54
N_SENDMAP = 55
N_CLIPBOARD = 56
N_EDITVAR = 57
N_MASTERMODE = 58
N_KICK = 59
N_CLEARBANS = 60
N_CURRENTMASTER = 61
N_SPECTATOR = 62
N_SETMASTER = 63
N_SETTEAM = 64
N_BASES = 65
N_BASEINFO = 66
N_BASESCORE = 67
N_REPAMMO = 68
N_BASEREGEN = 69
N_ANNOUNCE = 70
N_LISTDEMOS = 71
N_SENDDEMOLIST = 72
N_GETDEMO = 73
N_SENDDEMO = 74
N_DEMOPLAYBACK = 75
N_RECORDDEMO = 76
N_STOPDEMO = 77
N_CLEARDEMOS = 78
N_TAKEFLAG = 79
N_RETURNFLAG = 80
N_RESETFLAG = 81
N_INVISFLAG = 82
N_TRYDROPFLAG = 83
N_DROPFLAG = 84
N_SCOREFLAG = 85
N_INITFLAGS = 86
N_SAYTEAM = 87
N_CLIENT = 88
N_AUTHTRY = 89
N_AUTHKICK = 90
N_AUTHCHAL = 91
N_AUTHANS = 92
N_REQAUTH = 93
N_PAUSEGAME = 94
N_GAMESPEED = 95
N_ADDBOT = 96
N_DELBOT = 97
N_INITAI = 98
N_FROMAI = 99
N_BOTLIMIT = 100
N_BOTBALANCE = 101
N_MAPCRC = 102
N_CHECKMAPS = 103
N_SWITCHNAME = 104
N_SWITCHMODEL = 105
N_SWITCHTEAM = 106
N_INITTOKENS = 107
N_TAKETOKEN = 108
N_EXPIRETOKENS = 109
N_DROPTOKENS = 110
N_DEPOSITTOKENS = 111
N_STEALTOKENS = 112
N_SERVCMD = 113
N_DEMOPACKET = 114

packet_names = [
    "N_CONNECT",
    "N_SERVINFO",
    "N_WELCOME",
    "N_INITCLIENT",
    "N_POS",
    "N_TEXT",
    "N_SOUND",
    "N_CDIS",
    "N_SHOOT",
    "N_EXPLODE",
    "N_SUICIDE",
    "N_DIED",
    "N_DAMAGE",
    "N_HITPUSH",
    "N_SHOTFX",
    "N_EXPLODEFX",
    "N_TRYSPAWN",
    "N_SPAWNSTATE",
    "N_SPAWN",
    "N_FORCEDEATH",
    "N_GUNSELECT",
    "N_TAUNT",
    "N_MAPCHANGE",
    "N_MAPVOTE",
    "N_TEAMINFO",
    "N_ITEMSPAWN",
    "N_ITEMPICKUP",
    "N_ITEMACC",
    "N_TELEPORT",
    "N_JUMPPAD",
    "N_PING",
    "N_PONG",
    "N_CLIENTPING",
    "N_TIMEUP",
    "N_FORCEINTERMISSION",
    "N_SERVMSG",
    "N_ITEMLIST",
    "N_RESUME",
    "N_EDITMODE",
    "N_EDITENT",
    "N_EDITF",
    "N_EDITT",
    "N_EDITM",
    "N_FLIP",
    "N_COPY",
    "N_PASTE",
    "N_ROTATE",
    "N_REPLACE",
    "N_DELCUBE",
    "N_REMIP",
    "N_EDITVSLOT",
    "N_UNDO",
    "N_REDO",
    "N_NEWMAP",
    "N_GETMAP",
    "N_SENDMAP",
    "N_CLIPBOARD",
    "N_EDITVAR",
    "N_MASTERMODE",
    "N_KICK",
    "N_CLEARBANS",
    "N_CURRENTMASTER",
    "N_SPECTATOR",
    "N_SETMASTER",
    "N_SETTEAM",
    "N_BASES",
    "N_BASEINFO",
    "N_BASESCORE",
    "N_REPAMMO",
    "N_BASEREGEN",
    "N_ANNOUNCE",
    "N_LISTDEMOS",
    "N_SENDDEMOLIST",
    "N_GETDEMO",
    "N_SENDDEMO",
    "N_DEMOPLAYBACK",
    "N_RECORDDEMO",
    "N_STOPDEMO",
    "N_CLEARDEMOS",
    "N_TAKEFLAG",
    "N_RETURNFLAG",
    "N_RESETFLAG",
    "N_INVISFLAG",
    "N_TRYDROPFLAG",
    "N_DROPFLAG",
    "N_SCOREFLAG",
    "N_INITFLAGS",
    "N_SAYTEAM",
    "N_CLIENT",
    "N_AUTHTRY",
    "N_AUTHKICK",
    "N_AUTHCHAL",
    "N_AUTHANS",
    "N_REQAUTH",
    "N_PAUSEGAME",
    "N_GAMESPEED",
    "N_ADDBOT",
    "N_DELBOT",
    "N_INITAI",
    "N_FROMAI",
    "N_BOTLIMIT",
    "N_BOTBALANCE",
    "N_MAPCRC",
    "N_CHECKMAPS",
    "N_SWITCHNAME",
    "N_SWITCHMODEL",
    "N_SWITCHTEAM",
    "N_INITTOKENS",
    "N_TAKETOKEN",
    "N_EXPIRETOKENS",
    "N_DROPTOKENS",
    "N_DEPOSITTOKENS",
    "N_STEALTOKENS",
    "N_SERVCMD",
    "N_DEMOPACKET",
]

unicode_characters = [
    # Basic Latin (deliberately omitting most control characters)
    "\x00",
    # Latin-1 Supplement (selected letters)
    "À",
    "Á",
    "Â",
    "Ã",
    "Ä",
    "Å",
    "Æ",
    "Ç",
    # Basic Latin (cont.)
    "\t",
    "\n",
    "\v",
    "\f",
    "\r",
    # Latin-1 Supplement (cont.)
    "È",
    "É",
    "Ê",
    "Ë",
    "Ì",
    "Í",
    "Î",
    "Ï",
    "Ñ",
    "Ò",
    "Ó",
    "Ô",
    "Õ",
    "Ö",
    "Ø",
    "Ù",
    "Ú",
    "Û",
    # Basic Latin (cont.)
    " ",
    "!",
    '"',
    "#",
    "$",
    "%",
    "&",
    "'",
    "(",
    ")",
    "*",
    "+",
    ",",
    "-",
    ".",
    "/",
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    ":",
    ";",
    "<",
    "=",
    ">",
    "?",
    "@",
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
    "[",
    "\\",
    "]",
    "^",
    "_",
    "`",
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "{",
    "|",
    "}",
    "~",
    # Latin-1 Supplement (cont.)
    "Ü",
    "Ý",
    "ß",
    "à",
    "á",
    "â",
    "ã",
    "ä",
    "å",
    "æ",
    "ç",
    "è",
    "é",
    "ê",
    "ë",
    "ì",
    "í",
    "î",
    "ï",
    "ñ",
    "ò",
    "ó",
    "ô",
    "õ",
    "ö",
    "ø",
    "ù",
    "ú",
    "û",
    "ü",
    "ý",
    "ÿ",
    # Latin Extended-A (selected letters)
    "Ą",
    "ą",
    "Ć",
    "ć",
    "Č",
    "č",
    "Ď",
    "ď",
    "Ę",
    "ę",
    "Ě",
    "ě",
    "Ğ",
    "ğ",
    "İ",
    "ı",
    "Ł",
    "ł",
    "Ń",
    "ń",
    "Ň",
    "ň",
    "Ő",
    "ő",
    "Œ",
    "œ",
    "Ř",
    "ř",
    "Ś",
    "ś",
    "Ş",
    "ş",
    "Š",
    "š",
    "Ť",
    "ť",
    "Ů",
    "ů",
    "Ű",
    "ű",
    "Ÿ",
    "Ź",
    "ź",
    "Ż",
    "ż",
    "Ž",
    "ž",
    # Cyrillic (selected letters, deliberately omitting letters visually identical to characters in Basic Latin)
    "Є",
    "Б",
    "Г",
    "Д",
    "Ж",
    "З",
    "И",
    "Й",
    "Л",
    "П",
    "У",
    "Ф",
    "Ц",
    "Ч",
    "Ш",
    "Щ",
    "Ъ",
    "Ы",
    "Ь",
    "Э",
    "Ю",
    "Я",
    "б",
    "в",
    "г",
    "д",
    "ж",
    "з",
    "и",
    "й",
    "к",
    "л",
    "м",
    "н",
    "п",
    "т",
    "ф",
    "ц",
    "ч",
    "ш",
    "щ",
    "ъ",
    "ы",
    "ь",
    "э",
    "ю",
    "я",
    "є",
    "Ґ",
    "ґ",
]

GUN_FIST = 0
GUN_SG = 1
GUN_CG = 2
GUN_RL = 3
GUN_RIFLE = 4
GUN_GL = 5
GUN_PISTOL = 6
GUN_FIREBALL = 7
GUN_ICEBALL = 8
GUN_SLIMEBALL = 9
GUN_BITE = 10
GUN_BARREL = 11
NUMGUNS = 12

ID_VAR = 0
ID_FVAR = 1
ID_SVAR = 2
ID_COMMAND = 3
ID_ALIAS = 4
ID_LOCAL = 5

m_ffa = 0
m_coop_edit = 1
m_teamplay = 2
m_insta = 3
m_insta_team = 4
m_effic = 5
m_effic_team = 6
m_tac = 7
m_tac_team = 8
m_capture = 9
m_regen_capture = 10
m_ctf = 11
m_insta_ctf = 12
m_protect = 13
m_insta_protect = 14
m_hold = 15
m_insta_hold = 16
m_effic_ctf = 17
m_effic_protect = 18
m_effic_hold = 19
m_collect = 20
m_insta_collect = 21
m_effic_collect = 22

mode_to_str = {
    m_ffa: "m_ffa",
    m_coop_edit: "m_coop_edit",
    m_teamplay: "m_teamplay",
    m_insta: "m_insta",
    m_insta_team: "m_insta_team",
    m_effic: "m_effic",
    m_effic_team: "m_effic_team",
    m_tac: "m_tac",
    m_tac_team: "m_tac_team",
    m_capture: "m_capture",
    m_regen_capture: "m_regen_capture",
    m_ctf: "m_ctf",
    m_insta_ctf: "m_insta_ctf",
    m_protect: "m_protect",
    m_insta_protect: "m_insta_protect",
    m_hold: "m_hold",
    m_insta_hold: "m_insta_hold",
    m_effic_ctf: "m_effic_ctf",
    m_effic_protect: "m_effic_protect",
    m_effic_hold: "m_effic_hold",
    m_collect: "m_collect",
    m_insta_collect: "m_insta_collect",
    m_effic_collect: "m_effic_collect",
}

DMF = 16

NOTUSED = 0
LIGHT = 1
MAPMODEL = 2
PLAYERSTART = 3
ENVMAP = 4
PARTICLES = 5
MAPSOUND = 6
SPOTLIGHT = 7
I_SHELLS = 8
I_BULLETS = 9
I_ROCKETS = 10
I_ROUNDS = 11
I_GRENADES = 12
I_CARTRIDGES = 13
I_HEALTH = 14
I_BOOST = 15
I_GREENARMOUR = 16
I_YELLOWARMOUR = 17
I_QUAD = 18
TELEPORT = 19
TELEDEST = 20
MONSTER = 21
CARROT = 22
JUMPPAD = 23
BASE = 24
RESPAWNPOINT = 25
BOX = 26
BARREL = 27
PLATFORM = 28
ELEVATOR = 29
FLAG = 30
MAXENTTYPES = 31

CS_ALIVE = 0
CS_DEAD = 1
CS_SPAWNING = 2
CS_LAGGED = 3
CS_EDITING = 4
CS_SPECTATOR = 5

S_JUMP = 0
S_LAND = 1
S_RIFLE = 2
S_PUNCH1 = 3
S_SG = 4
S_CG = 5
S_RLFIRE = 6
S_RLHIT = 7
S_WEAPLOAD = 8
S_ITEMAMMO = 9
S_ITEMHEALTH = 10
S_ITEMARMOUR = 11
S_ITEMPUP = 12
S_ITEMSPAWN = 13
S_TELEPORT = 14
S_NOAMMO = 15
S_PUPOUT = 16
S_PAIN1 = 17
S_PAIN2 = 18
S_PAIN3 = 19
S_PAIN4 = 20
S_PAIN5 = 21
S_PAIN6 = 22
S_DIE1 = 23
S_DIE2 = 24
S_FLAUNCH = 25
S_FEXPLODE = 26
S_SPLASH1 = 27
S_SPLASH2 = 28
S_GRUNT1 = 29
S_GRUNT2 = 30
S_RUMBLE = 31
S_PAINO = 32
S_PAINR = 33
S_DEATHR = 34
S_PAINE = 35
S_DEATHE = 36
S_PAINS = 37
S_DEATHS = 38
S_PAINB = 39
S_DEATHB = 40
S_PAINP = 41
S_PIGGR2 = 42
S_PAINH = 43
S_DEATHH = 44
S_PAIND = 45
S_DEATHD = 46
S_PIGR1 = 47
S_ICEBALL = 48
S_SLIMEBALL = 49
S_JUMPPAD = 50
S_PISTOL = 51
S_V_BASECAP = 52
S_V_BASELOST = 53
S_V_FIGHT = 54
S_V_BOOST = 55
S_V_BOOST10 = 56
S_V_QUAD = 57
S_V_QUAD10 = 58
S_V_RESPAWNPOINT = 59
S_FLAGPICKUP = 60
S_FLAGDROP = 61
S_FLAGRETURN = 62
S_FLAGSCORE = 63
S_FLAGRESET = 64
S_BURN = 65
S_CHAINSAW_ATTACK = 66
S_CHAINSAW_IDLE = 67
S_HIT = 68
S_FLAGFAIL = 69

A_BLUE = 0
A_GREEN = 1
A_YELLOW = 2
