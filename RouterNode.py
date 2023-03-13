#!/usr/bin/env python
import GuiTextArea
import RouterPacket
import F
from copy import deepcopy


class RouterNode():
    myID = None
    myGUI = None
    sim = None
    costs = None

    # Variable declaration
    neighbourCosts = None
    routingTable = None
    minCosts = None
    nextHop = None
    poisonReverse = False

    # Access simulator variables with:
    # self.sim.POISONREVERSE, self.sim.NUM_NODES, etc.

    # --------------------------------------------------

    def __init__(self, ID, sim, costs):
        self.myID = ID
        self.sim = sim
        self.myGUI = GuiTextArea.GuiTextArea(
            "  Output window for Router #" + str(ID) + "  ")

        # Initialize class variables
        self.poisonReverse = False#self.sim.POISONREVERSE

        self.neighbourCosts = deepcopy(costs)
        self.minCosts = deepcopy((costs))
        self.routingTable = [[self.sim.INFINITY] *
                             self.sim.NUM_NODES] * self.sim.NUM_NODES
        self.routingTable[self.myID] = deepcopy(self.neighbourCosts)
        self.nextHop = [-1] * self.sim.NUM_NODES

        for i in range(self.sim.NUM_NODES):
            if (costs[i] < self.sim.INFINITY):
                self.nextHop[i] = i
        self.myGUI.println("My initial routing table is :")
        self.myGUI.println(str(self.routingTable) + "\n")

        self.prepare_send(None)

    # --------------------------------------------------

    def recvUpdate(self, pkt):
        self.myGUI.println("I'm " + str(self.myID) + ", Got an update from " + str(pkt.sourceid) +
                           ", its news minimum costs are : " + str(pkt.mincost))
        print("I'm " + str(self.myID) + ", Got an update from " + str(pkt.sourceid) +
              ", its news minimum costs are : " + str(pkt.mincost))
        self.routingTable[pkt.sourceid] = pkt.mincost
        print("My currently min costs are" + str(self.minCosts))
        previousMinCosts = deepcopy(self.minCosts)
        print("My currently min costs are" + str(previousMinCosts))

        for i in range(self.sim.NUM_NODES):
            if i != self.myID:
                self.myGUI.println(
                    "Compute min cost to go to " + str(i) + " from " + str(self.myID))
                possibleCost = self.neighbourCosts[i]
                print(" Cost to go directly to " +
                      str(i) + " is " + str(possibleCost))
                
                for j in range(self.sim.NUM_NODES):
                    if (j != i and j != self.myID):
                        possibleCost1 = self.neighbourCosts[j] + \
                            self.routingTable[j][i]
                        print("possible cost by " + str(j) + " to go to " +
                              str(i) + " is " + str(possibleCost1))
                        if possibleCost1 < possibleCost:
                            possibleCost = possibleCost1
                            self.nextHop[i] = j
                self.minCosts[i] = possibleCost
                print("Finally my min cost to go to " +
                      str(i) + " is " + str(self.minCosts[i]))

        print("Finally my min cost after computation is " + str(self.minCosts))
        print("My previous one was: " + str(previousMinCosts))
        if self.minCosts != previousMinCosts:
            print(" chaneg so I send new one")
            self.prepare_send(None)
        else:
            print("No change, I do nothing")

    # -------------------------------

    def prepare_send(self, nodePoisoned):
        self.myGUI.println("My new min cost is: " + str(self.minCosts))
        self.routingTable[self.myID] = self.minCosts
        
        nodePoisoned = []
        for i in range(self.sim.NUM_NODES):


            if (self.poisonReverse and self.nextHop[i] != i):
                self.myGUI.println("POSIONING")
                fakeMinCosts = deepcopy(self.minCosts)
                fakeMinCosts[i] = self.sim.INFINITY
                pkt = RouterPacket.RouterPacket(self.myID, self.nextHop[i], fakeMinCosts)
                self.myGUI.println("POISON At time " + str(self.sim.getClocktime()) +
                                   " I'm sending my minimum cost " + str(fakeMinCosts) + "to " + str(pkt.destid))
                self.sendUpdate(pkt)
                nodePoisoned.append(self.nextHop[i])

            if (self.neighbourCosts[i] < self.sim.INFINITY and i != self.myID):

                if(i in nodePoisoned):
                    pass
                else:

                    pkt = RouterPacket.RouterPacket(
                        self.myID, i, deepcopy(self.minCosts))
                    self.myGUI.println("At time " + str(self.sim.getClocktime()) +
                                    " I'm sending my minimum cost " + str(self.minCosts) + "to " + str(pkt.destid))
                    self.sendUpdate(pkt)




        self.myGUI.println("\n")
    # --------------------------------------------------

    def sendUpdate(self, pkt):
        self.sim.toLayer2(pkt)

    # --------------------------------------------------

    def printDistanceTable(self):

        self.myGUI.println("Current routing table for " + str(self.myID) +
                           "  at time " + str(self.sim.getClocktime()))
        self.myGUI.println(str(self.routingTable) + "\n")
        self.myGUI.println("My neighbour costs are : " +
                           str(self.neighbourCosts) + "\n")
        # We print the route for each
        for i in range(self.sim.NUM_NODES):
            if i != self.myID:
                self.myGUI.println("Next hop to go to " + str(i) +
                                   " is " + str(self.nextHop[i]))
        self.myGUI.println("\n")
    # --------------------------------------------------

    def updateLinkCost(self, dest, newcost):
        self.poisonReverse = self.sim.POISONREVERSE
        self.myGUI.println("updated link cost to " +
                           str(dest) + "(" + str(newcost) + ")")

        for i in range(self.sim.NUM_NODES):
            if i == dest:
                self.neighbourCosts[i] = newcost

        self.myGUI.println("My news neighbours costs are :" +
                           str(self.neighbourCosts))
        self.myGUI.println("I going to compute my new min costs")


        for i in range(self.sim.NUM_NODES):
            if i != self.myID:
                self.myGUI.println(
                    "Compute min cost to go to " + str(i)+" from " + str(self.myID))
                possibleCost = self.neighbourCosts[i] + self.routingTable[i][i]
                self.nextHop[i] = i
                self.myGUI.println(str(possibleCost))
                self.minCosts[i] = possibleCost
                self.routingTable[self.myID][i] = self.minCosts[i]

        for i in range(self.sim.NUM_NODES):        
            pkt = RouterPacket.RouterPacket(
                        self.myID, i, deepcopy(self.minCosts))
            self.myGUI.println("At time " + str(self.sim.getClocktime()) +
                                   " I'm sending my minimum cost " + str(self.minCosts) + "to " + str(pkt.destid))
            self.sendUpdate(pkt)


