import curses
from time import sleep
import random, threading, json, socket
s = curses.initscr()

curses.noecho()

# keys=[]

# def push_inp():
#   s.timeout(-1)
#   while True:
#     keys.append(s.getch())

# threading.Thread(target=push_inp).start()

# while True:
#   curses.napms(100)



# # if -1 its blocking call
s.timeout(-1)

while True:
  # curses.flash()
  key = s.getch()
  if key == 3:
    break