from pysfc.model import *

__author__ = 'weigl'

def t():
    return False

class MySFC(SFC):
    STATES = [
        "A",
        "B1",
        "B2",
        "C1",
        "C2",
        "D",
        "E"
    ]

    TRANSITIONS = [
        ("A", "B1|B2"),
        ("B1", "C1"),
        ("B2", "C2"),
        ("C1|C2", "E"),
        ("E", "A"),
    ]

    def A_active(self):
        print "A"
        self.a = 1

    def B1_active(self):
        print "B1"
        self.a +=1

    def B2_active(self):
        print "B2"
        self.a +=1

    def C1_active(self):
        print "C"
        self.a +=1

    def C2_active(self):
        print "C"
        self.a +=1

    def D_active(self):
        print "D"
        self.a +=1

    def E_active(self):
        print "E"
        self.a +=1


a = MySFC()

print a.states
print a.transitions

for i in range(10):
    a()
    print a._current_states

