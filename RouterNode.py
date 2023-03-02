#!/usr/bin/env python
import GuiTextArea, RouterPacket, F
from copy import deepcopy

class RouterNode():
    myID = None
    myGUI = None
    sim = None
    costs = None

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
        self.PoisonReverse = self.sim.POISONREVERSE
        self.minCosts = costs

        self.neighbourCosts = [[self.sim.INFINITY]*self.sim.NUM_NODES] * self.sim.NUM_NODES
        self.neighbourCosts[ID] = costs

        #self.minCosts = [self.sim.INFINITY] * self.sim.NUM_NODES
        
        for i in range(self.sim.NUM_NODES):
                if (self.neighbourCosts[ID][i] < self.sim.INFINITY):
                    self.nextHop[i] = i
                else :
                    self.nextHop[i] = -1

        print("INSTANCE %d" % ID) 
        print(self.neighbourCosts)
        print(self.minCosts)
        print(self.nextHop)

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


    # --------------------------------------------------
    def updateLinkCost(self, dest, newcost):
        pass
