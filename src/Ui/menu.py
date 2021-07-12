import curses
from time import sleep

class Menu:
  def __init__(self, menu, height, width, y, x, message = None, help = None):
    self.menu = menu
    self.message = message
    self.help = help

    self.height = height
    self.width = width

    # Creates a window object
    self.w = curses.newwin(height, width, y, x)
    # I have no idea why this was set to 100
    self.w.timeout(-1)

    # 1- True -> Allow keypads to be handled by curses
    self.w.keypad(1)

    # Draw a border around the edges of the window. 
    # Each parameter specifies the character to use for a specific part of the border; 
    # see the table below for more details.
    # 0 uses a default table
    self.w.border(0)

    self.selection = 0

  def prompt(self):
    if self.message:
      self.w.addstr(0, 1, self.message)
    
    self.w.timeout(-1)
    curses.echo()
    
    # Get user input at y 1, x 2, 22 characters
    prompt = self.w.getstr(1, 2, 22)

    self.w.timeout(100)
    curses.noecho()

    return prompt.decode("utf-8").split(":")

  def createMenu(self):
    # try:
    while True:
      key = self.w.getch()

      # showing that getch() will return multiple keys
      keys = [key]
      # if key != -1:
      #   while (key := self.w.getch()) != -1:
      #     keys.append(key)
      

      if key == curses.KEY_UP:
        index = self.selection
        
        while True:  
          if index - 1 >= 0 and 'skip' in self.menu[index - 1]:
            index -= 1
          elif index - 1 >= 0:
            index -= 1
            break
          else:
            break

        self.selection = index
      
      elif key == curses.KEY_DOWN:
        index = self.selection
        
        while True:  
          if index + 1 <= len(self.menu) - 1 and 'skip' in self.menu[index + 1]:
            index += 1
          elif index + 1 <= len(self.menu) - 1:
            index += 1
            break
          else:
            break

        self.selection = index
      
      elif key == curses.KEY_RIGHT:
        if 'value' in self.menu[self.selection]:
          self.menu[self.selection]['value'] += 1
        
        elif 'boolean' in self.menu[self.selection]:
          self.menu[self.selection]['boolean'] = not self.menu[self.selection]['boolean']

      elif key == curses.KEY_LEFT:
        if 'value' in self.menu[self.selection]:
          self.menu[self.selection]['value'] = self.menu[self.selection]['value'] - 1 if self.menu[self.selection]['value'] >= 1 else 0
        
        elif 'boolean' in self.menu[self.selection]:
          self.menu[self.selection]['boolean'] = not self.menu[self.selection]['boolean']

      # Enter
      elif key == 10:
        # break after select
        if 'selectable' in self.menu[self.selection]:
          self.select()
          break
      elif key == 3:
        raise KeyboardInterrupt

      # curses.flushinp()
      # This constantly draws
      self.draw()
    # except KeyboardInterrupt:
    #   self.selection = -1

  def draw(self):
    self.w.erase()
    self.w.border(0)
    for index in range(0, len(self.menu)):
      item = self.menu[index]

      checked = '*' if index == self.selection else ' '
      value = f'{item["value"]}      ' if 'value' in item else ''
      boolean = f'{item["boolean"]} ' if 'boolean' in item else ''
      
      self.w.addstr(1 + index, 2, f'{checked} {self.menu[index]["Label"]} {value}{boolean}')

    if self.help: self.w.addstr(self.height - 1, 2, self.help)

  def select(self):
    label = self.menu[self.selection]['Label']
    index = self.selection

    for i in range(2):
      self.menu[index]['Label'] = ''
      self.draw()
      self.w.refresh()
      sleep(0.15)

      self.menu[index]['Label'] = label
      self.draw()
      self.w.refresh()
      sleep(0.15)