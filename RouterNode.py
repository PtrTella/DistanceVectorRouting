#!/usr/bin/env python
import GuiTextArea, RouterPacket, F
from copy import deepcopy

class RouterNode():
    myID = None
    myGUI = None
    sim = None
    costs = None

    INIFINITY = 9999

    # Varible dclaration
    neighbourCosts = None
    minCosts = None
    nextHop = None
    PoisonReverse = False

    # Access simulator variables with:
    # self.sim.POISONREVERSE, self.sim.NUM_NODES, etc.

    # --------------------------------------------------
    def __init__(self, ID, sim, costs):
        self.myID = ID
        self.sim = sim
        self.myGUI = GuiTextArea.GuiTextArea("  Output window for Router #" + str(ID) + "  ")

        # Initialize class variables
        print("INSTANCE %d" % ID) 
        self.neighbourCosts = [[self.INIFINITY]*self.sim.NUM_NODES] * self.sim.NUM_NODES
        self.neighbourCosts[ID] = costs
        print(self.neighbourCosts)

        #self.minCosts = {self.infinity}


        self.costs = deepcopy(costs)


    # --------------------------------------------------
    def recvUpdate(self, pkt):
        pass


    # --------------------------------------------------
    def sendUpdate(self, pkt):
        self.sim.toLayer2(pkt)


    # --------------------------------------------------
    def printDistanceTable(self):
        self.myGUI.println("Current table for " + str(self.myID) +
                           "  at time " + str(self.sim.getClocktime()))
        self.myGUI.print(self.neighbourCosts)


    # --------------------------------------------------
    def updateLinkCost(self, dest, newcost):
        pass
