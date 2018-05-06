from tkinter import *
from tkinter import messagebox
import random
import math
import os

root = Tk()

class Block:
    _id = 0
    isBomb = 0
    near = 0
    opened = 0
    x = 0
    y = 0
    question = 0
    def __init__(self, _id, isBomb, x, y):
        self._id = _id
        self.isBomb = isBomb
        self.x = x
        self.y = y
        
    def tryOpenNear(self):
        global width
        global blocks
        x = self.x
        y = self.y
        ptc = [[x-1, y], [x,y-1], [x,y+1], [x+1, y]]
        
        for a in range(len(ptc)):
            try:
                xx = ptc[a][0]
                yy = ptc[a][1]
                if xx < 0 or yy < 0 or xx > (height-1) or yy > (width-1):
                    continue
                index = xx*width + yy
                if blocks[index].isBomb == 0 and blocks[index].opened == 0 and self.near < 2:
                    blocks[index].opened = 1
                    blocks[index].mouseClick()
            except:
                continue
            
    def mouseClick(self):
        if self.question == 1: return
        global blocksButtons        
        global begin
        global winCheck
        global marked
        if self.isBomb == 1:
            blocksButtons[self._id]['text'] = '¤'
            blocksButtons[self._id]['bg'] = '#cccccc'
            marked = 0
            messagebox.showinfo('End', 'Game Over')
            begin(None)
            return
        blocksButtons[self._id]['text'] = str(self.near)
        
        if self.near == 0:
            blocksButtons[self._id]['text'] = ''
            blocksButtons[self._id]['bg'] = '#cccccc'
            
        if self.near == 1:
            blocksButtons[self._id]['fg'] = '#2222ff'
            blocksButtons[self._id]['bg'] = '#cccccc'
            
        if self.near == 2:
            blocksButtons[self._id]['fg'] = '#22bb22'
            blocksButtons[self._id]['bg'] = '#cccccc'
            
        if self.near == 3:
            blocksButtons[self._id]['fg'] = '#ff2222'
            blocksButtons[self._id]['bg'] = '#cccccc'
            
        if self.near == 4:
            blocksButtons[self._id]['fg'] = '#cc00cc'
            blocksButtons[self._id]['bg'] = '#cccccc'
            
        if self.near == 5:
            blocksButtons[self._id]['fg'] = '#b37700'
            blocksButtons[self._id]['bg'] = '#cccccc'
            
        if self.near == 6:
            blocksButtons[self._id]['fg'] = '#ff751a'
            blocksButtons[self._id]['bg'] = '#cccccc'
            
        self.tryOpenNear()
        winCheck()
        

    def rightClick(self, event):
        global blocksButtons
        global marked
        if self.opened == 1: return
        if self.question == 0: 
            self.question = 1
            blocksButtons[self._id]['text'] = '?'
            marked += 1
            bombCount['text'] = str(marked) + '/' + str(bombs)
        else: 
            self.question = 0
            blocksButtons[self._id]['text'] = ''
            marked -= 1
            bombCount['text'] = str(marked) + '/' + str(bombs)


width = 10
height = 10
bombs = 0
marked = 0
blockSide = 40
diffs = [10,20,30,40,50,60,70,80,90]
currentDiff = 3
root.geometry(str(width * blockSide) + 'x' + str(height * blockSide + 40))
root.title('Minesweeper')

blocksButtons = []
blocks = []
n = 0

bombCount = Label(text='hello', height=1, font=('Helvetica', '18'))
bombCount.place(width=76, x=(width*blockSide/2)-38, y=5)

def begin(event):
    global width
    global height 
    global bombs
    global blocksButtons
    global blocks
    global n
    global blockSide
    global diffs
    global currentDiff
    width = 10
    height = 10
    bombs = 0
    marked = 0
    blockSide = 40
    blocksButtons = []
    blocks = []
    diffs = [10,20,30,40,50,60,70,80,90]    
    n = 0    
    for x in range(height):
        for y in range(width):
            b = 0
            if random.randint(1,100) > 100-diffs[currentDiff]:
                b = 1
                bombs = bombs + 1
                
            blocks.append(Block(n, b, x, y))
            
            blocksButtons.append(Button(command=blocks[n].mouseClick, font=('Helvetica', '20')))
            blocksButtons[n].bind("<Button-3>",blocks[n].rightClick)
            #blocksButtons[n].grid(row=x+1, column=y)
            blocksButtons[n].place(width=blockSide, height=blockSide, x=blockSide*x, y=blockSide*(y+1))
            
            n += 1
            
    bombCount['text'] = '0/' + str(bombs)
    
    for i in range(width*height):
        x = blocks[i].x
        y = blocks[i].y
        ptc = [[x-1,y-1], [x-1, y], [x-1, y+1], [x,y-1], [x,y+1], [x+1,y-1], [x+1, y], [x+1, y+1]]
        
        for a in range(len(ptc)):       
            try:    
                xx = int(ptc[a][0])
                yy = int(ptc[a][1])
                if xx < 0 or yy < 0 or xx > (height-1) or yy > (width-1):
                    continue
                index = xx*width + yy
                if blocks[index].isBomb == 1:
                    blocks[i].near += 1                            
            except:
                continue    
    
  


def winCheck():
    global width
    global height
    global blocks
    global bombs
    a = width*height
    n = 0
    for i in range(a):
        if blocks[i].opened == 1:
            n += 1
    if n == len(blocks) - bombs:
        messagebox.showinfo('Win!', 'Congratulations!')
        begin()

def addDifficulty(event):
    global currentDiff
    currentDiff += 1
    if currentDiff >= 9:
        currentDiff = 0
    messagebox.showinfo('Current difficult', str((currentDiff+1)*10))
    begin(None)
def subDifficulty(event):
    global currentDiff
    currentDiff -= 1 
    if currentDiff < 0:
        currentDiff = 8    
    messagebox.showinfo('Current difficult', str((currentDiff+1)*10))
    begin(None)
def help():
    h = Tk()
    h.title('Help window')
    h.geometry('400x130')
    l1 = Label(h, text='Current difficulty: ~40 mines per 100 blocks', font=('Helvetica', '14')).pack(anchor=NW, fill=Y)
    l2 = Label(h, text='\"E\" to add 10 to current difficulty', font=('Helvetica', '14')).pack(anchor=NW, fill=Y)
    l3 = Label(h, text='\"D\" to subtract 10 from current difficulty', font=('Helvetica', '14')).pack(anchor=NW, fill=Y)
    l4 = Label(h, text='\"R\" to restart the game', font=('Helvetica', '14')).pack(anchor=NW, fill=Y)
    h.mainloop()
begin(None)
#help()
root.bind('e', addDifficulty)
root.bind('d', subDifficulty)
root.bind('r', begin)
root.mainloop()
