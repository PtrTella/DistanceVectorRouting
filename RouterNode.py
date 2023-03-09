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
    poisonReverse = False
    immidiateNeighbours = None
    

    # Access simulator variables with:
    # self.sim.POISONREVERSE, self.sim.NUM_NODES, etc.

    # --------------------------------------------------
    def __init__(self, ID, sim, costs):
        self.myID = ID
        self.sim = sim
        self.myGUI = GuiTextArea.GuiTextArea("  Output window for Router #" + str(ID) + "  ")

        # Initialize class variables
        self.poisonReverse = self.sim.POISONREVERSE
        self.minCosts = deepcopy(costs)
        self.immidiateNeighbours = self.minCosts
        self.neighbourCosts = [[self.sim.INFINITY]*self.sim.NUM_NODES] * self.sim.NUM_NODES
        self.neighbourCosts[ID] = costs        
        self.nextHop = [-1] * self.sim.NUM_NODES
        for i in range(self.sim.NUM_NODES):
                if (costs[i] < self.sim.INFINITY):
                    self.nextHop[i] = i

        print("NODE %d" % ID) 
        print(self.neighbourCosts)
        print(self.minCosts)
        print(self.nextHop)

    
    # --------------------------------------------------
    def recvUpdate(self, pkt):
        self.neighbourCosts[pkt.sourceid] = pkt.mincost
        for i in range (self.sim.NUM_NODES):
            if (i!=self.myID):
                newCost = self.neighbourCosts[self.myID][pkt.sourceid] + pkt.mincost[i]
                if(self.minCosts[i] > newCost):
                    self.minCosts[i] = newCost
                    self.neighbourCosts[self.myID][i] = self.minCosts[i]
                    self.nextHop[i] = pkt.sourceid
                    self.sendUpdate()

    # --------------------------------------------------
    def sendUpdate(self):

        for i in range(self.sim.NUM_NODES):
            if (self.immidiateNeighbours[i] != self.sim.INFINITY and i != self.myID):
                pkt = RouterPacket.RouterPacket(self.myID, i, deepcopy(self.minCosts))
                self.sim.toLayer2(pkt)


    # --------------------------------------------------
    def printDistanceTable(self):
        self.myGUI.println("Current table for " + str(self.myID) +
                           "  at time " + str(self.sim.getClocktime()))


    # --------------------------------------------------
    def updateLinkCost(self, dest, newcost):
        pass
