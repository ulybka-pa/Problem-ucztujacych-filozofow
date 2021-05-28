#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Agnieszka Płoszaj 218353
import random
import threading
import time
from sys import stdout
n = int(input("Liczba filozofów: "))


class Philosopher(threading.Thread):
    def __init__(self, name, pid=1, left_fork=0, right_fork=1, repeat = 5):
        threading.Thread.__init__(self)
        self.name = name
        self.pid = pid
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.meals = 0
        self.end = 0
        self.repeat = repeat

    def run(self):
        stdout.write("\nFilozof " + str(self.pid) + " usiadł do stołu")
        #stdout.write("Filozof "+str(self.pid) + str(self.left_fork) + str(self.right_fork) + "\n")
        self.life_cycle()

    def life_cycle(self):
        while self.end < self.repeat:
            self.end += 1
            self.think()
            self.hunger()
        else:
            self.leave()

    def hunger(self):
        if int(self.pid) < n-1:
            stdout.write("\n" + u"\u001b[31;1m" + "Filozof " + str(self.pid) + " jest głodny.")
            self.left_fork.acquire()
            stdout.write("\n" + u"\u001b[37;1m" + "Filozof " + str(self.pid) + " trzyma lewy widelec.")
            self.right_fork.acquire()
            stdout.write("\n" + u"\u001b[37;1m" + "Filozof " + str(self.pid) + " trzyma prawy widelec.")
            self.eat()
        else:
            stdout.write("\n" + u"\u001b[31;1m" + "Filozof " + str(self.pid) + " jest głodny.")
            self.right_fork.acquire()
            stdout.write("\n" + u"\u001b[37;1m" + "Filozof " + str(self.pid) + " trzyma prawy widelec.")
            self.left_fork.acquire()
            stdout.write("\n" + u"\u001b[37;1m" + "Filozof " + str(self.pid) + " trzyma lewy widelec.")
            self.eat()

    def eat(self):
        self.meals += 1
        stdout.write("\n" + u"\u001b[33;1m" + "Filozof " + str(self.pid) + " je (" + str(self.meals) + ")")
        time.sleep(random.uniform(1, 3))
        self.right_fork.release()
        stdout.write("\n" + u"\u001b[37;1m" + "Filozof " + str(self.pid) + " zwolnił prawy widelec.")
        self.left_fork.release()
        stdout.write("\n" + u"\u001b[37;1m" + "Filozof " + str(self.pid) + " zwolnił lewy widelec.")
        self.life_cycle()

    def think(self):
        stdout.write("\n" + u"\u001b[37;1m" + "Filozof " + str(self.pid) + " myśli.")
        time.sleep(random.uniform(1, 3))

    def leave(self):
        print("\n" + u"\u001b[32;1m", "Liczba aktywnych wątków: ", threading.activeCount())
        stdout.write("\n" + u"\u001b[37;1m" + "Filozof " + str(self.pid) + " zakończył kolację.")
        exit()


def main():
    repeat = int(input("Liczba powtórzeń: "))

    w = [threading.Condition(threading.Lock()) for i in range(n)]
    f = [Philosopher("Filozof ", i, w[i % n], w[(i + 1) % n], repeat) for i in range(n)]
    for i in range(n):
        f[i].start()
    print("\n---------------------------------")
    print("Liczba aktywnych wątków: ", threading.activeCount())


if __name__ == "__main__":
    main()
