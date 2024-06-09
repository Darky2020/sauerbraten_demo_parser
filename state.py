from .sauerconsts import *


class State(object):
    def __init__(
        self,
        state=CS_SPECTATOR,
        frags=0,
        flags=0,
        deaths=0,
        quadmillis=0,
        lifesequence=0,
        health=100,
        maxhealth=100,
        armour=0,
        armourtype=A_BLUE,
        gunselect=0,
        ammo_SG=0,
        ammo_CG=0,
        ammo_RL=0,
        ammo_RIFLE=0,
        ammo_GL=1,
        ammo_PISTOL=40,
    ):
        self.state = state
        self.frags = frags
        self.flags = flags
        self.deaths = deaths
        self.quadmillis = quadmillis
        self.lifesequence = lifesequence
        self.health = health
        self.maxhealth = maxhealth
        self.armour = armour
        self.armourtype = armourtype
        self.gunselect = gunselect

        self.ammo_SG = ammo_SG
        self.ammo_CG = ammo_CG
        self.ammo_RL = ammo_RL
        self.ammo_RIFLE = ammo_RIFLE
        self.ammo_GL = ammo_GL
        self.ammo_PISTOL = ammo_PISTOL
