import pygame
from random import shuffle

from pygame.constants import NUMEVENTS


pygame.init()

SLEEPTIME = None  # milliseconds default value, will be changed further
NUM_BARS = None # default, will be changed further

#GLOBAL COLORS
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
BAR_COLOR = (3, 159, 251) # Taken from w3school

# CONSTANTS
WIDTH = 700
HEIGHT = 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Sorting Visualizer')

margin = 50
gap = None
array = None

maximum = None
barWidth = None

# Classes
class Bar:
    def __init__(self, item, index) -> None:
        self.number = item
        self.color = BAR_COLOR
        self.width = barWidth
        self.height = item/maximum * HEIGHT
        self.x = margin+index*(barWidth+gap)
        self.y = HEIGHT-self.height

    def draw(self):
        pygame.draw.rect(
            WIN, self.color, (self.x, self.y, self.width, self.height))

    def set_color(self, color):
        self.color = color

    def __str__(self):
        return str(self.number)

class Button:
    def __init__(self,color,text,x,y,w,h) -> None:
        self.color=color
        self.text=text
        self.x=x
        self.y=y
        self.width=w
        self.height=h
        self.selected=False
    def draw(self,win,border=None):
        if border:
            pygame.draw.rect(win,border,(self.x-2,self.y,self.width+4,self.height+4))
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.height))
        if self.text!='':
            myfont = pygame.font.SysFont('Comic Sans MS', 25)
            text= myfont.render(self.text, 1, (0, 0, 0))
            win.blit(text,(self.x+(self.width/2-text.get_width()/2),self.y+(self.height/2-text.get_height()/2)))
    def isClicked(self,pos):
        x,y=pos
        return x>=self.x and x<=self.x+self.width and y>=self.y and y<=self.y+self.height

# Functions
def prepareBarList(array):
    bars = []
    for index, item in enumerate(array):
        bar = Bar(item, index)
        bars.append(bar)
    return bars


bars = None


def drawBars(bars):
    WIN.fill(WHITE)
    for bar in bars:
        bar.draw()
    pygame.display.flip()


def checkExit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return True
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_m or event.key == pygame.K_ESCAPE):
            welcomePage1()
    return False

########################################SORTING ALGO SECTION############


def bubbleSort(*args):
    def update():
        global array, bars
        drawBars(bars)
        bars = prepareBarList(array)
        bars[i].set_color(GREEN)
        bars[j].set_color(GREEN)
        drawBars(bars)
        pygame.time.wait(SLEEPTIME)
        bars[i].set_color(BAR_COLOR)
        bars[j].set_color(BAR_COLOR)

    for i in range(len(array)-1):
        for j in range(i+1, len(array)):
            checkExit()
            if array[i] > array[j]:
                array[i], array[j] = array[j], array[i]
                update()
            update()


def insertionSort(*args):
    global array, bars

    def update():
        global array, bars
        bars = prepareBarList(array)
        bars[i].set_color(GREEN)
        bars[j].set_color(GREEN)
        drawBars(bars)
        pygame.time.wait(SLEEPTIME)
        bars[i].set_color(BAR_COLOR)
        bars[j].set_color(BAR_COLOR)
        drawBars(bars)
    j = 0
    temp = None  # Stores the value which is iterated to find its correct position
    for i in range(1, len(array)):
        temp = array[i]
        j = i-1
        while j >= 0 and array[j] > temp:
            checkExit()
            array[j + 1] = array[j]
            update()
            j -= 1
        array[j+1] = temp
        update()


def selectionSort(*args):
    global array, bars

    def update():
        global bars
        bars = prepareBarList(array)
        bars[i].set_color(GREEN)
        bars[j].set_color(RED)
        bars[min].set_color(GREEN)
        drawBars(bars)
        pygame.time.wait(SLEEPTIME)
        bars[i].set_color(BAR_COLOR)
        bars[j].set_color(BAR_COLOR)
        bars[min].set_color(BAR_COLOR)
    for i in range(len(array)):
        min = i
        for j in range(i, len(array)):
            checkExit()
            update()
            if array[j] < array[min]:
                min = j
        if min != i:
            array[i], array[min] = array[min], array[i]

# Iterative Merge sort (Bottom Up)


def mergeSort(*args):
    def update(i, k):
        global bars
        bars = prepareBarList(array)
        bars[i].set_color(GREEN)
        if k < len(array):
            bars[k].set_color(GREEN)
        drawBars(bars)
        pygame.time.wait(SLEEPTIME)
        bars[i].set_color(BAR_COLOR)
        if k < len(array):
            bars[k].set_color(BAR_COLOR)

    def merge(l, m, r):
        n1 = m - l + 1
        n2 = r - m
        L = [0] * n1
        R = [0] * n2
        for i in range(0, n1):
            L[i] = array[l + i]
        for i in range(0, n2):
            R[i] = array[m + i + 1]

        i, j, k = 0, 0, l
        while i < n1 and j < n2:
            checkExit()
            if L[i] > R[j]:
                array[k] = R[j]
                j += 1
            else:
                array[k] = L[i]
                i += 1
            k += 1
            update(j, k)
        while i < n1:
            checkExit()
            array[k] = L[i]
            i += 1
            k += 1
            update(j, k)

        while j < n2:
            checkExit()
            array[k] = R[j]
            j += 1
            k += 1
            update(j, k)
    current_size = 1

    while current_size < len(array) - 1:
        left = 0

        while left < len(array)-1:
            checkExit()

            mid = min((left + current_size - 1), (len(array)-1))

            right = ((2 * current_size + left - 1,
                      len(array) - 1)[2 * current_size
                                      + left - 1 > len(array)-1])

            merge(left, mid, right)
            left = left + current_size*2

        current_size = 2 * current_size


def quickSort(l=0, *args):
    h = len(array)-1

    def update(i, j):
        global bars
        bars = prepareBarList(array)
        bars[i].set_color(GREEN)
        bars[j].set_color(GREEN)
        drawBars(bars)
        pygame.time.wait(SLEEPTIME)
        bars[i].set_color(BAR_COLOR)
        bars[j].set_color(BAR_COLOR)

    def partition(l, h):
        i = (l - 1)
        x = array[h]

        for j in range(l, h):
            checkExit()
            if array[j] <= x:

                # increment index of smaller element
                i = i+1
                array[i], array[j] = array[j], array[i]
            update(i, j)
        array[i+1], array[h] = array[h], array[i+1]
        return (i+1)

     # Create an auxiliary stack
    size = h - l + 1
    stack = [0] * (size)

    # initialize top of stack
    top = -1

    # push initial values of l and h to stack
    top = top + 1
    stack[top] = l
    top = top + 1
    stack[top] = h

    # Keep popping from stack while is not empty
    while top >= 0:
        checkExit()
        # Pop h and l
        h = stack[top]
        top = top - 1
        l = stack[top]
        top = top - 1

        # Set pivot element at its correct position in
        # sorted array
        p = partition(l, h)

        # If there are elements on left side of pivot,
        # then push left side to stack
        if p-1 > l:
            top = top + 1
            stack[top] = l
            top = top + 1
            stack[top] = p - 1

        # If there are elements on right side of pivot,
        # then push right side to stack
        if p+1 < h:
            top = top + 1
            stack[top] = p + 1
            top = top + 1
            stack[top] = h


def heapSort(*args):
    def update(i, j):
        global bars
        bars = prepareBarList(array)
        bars[i].set_color(GREEN)
        bars[j].set_color(GREEN)
        drawBars(bars)
        pygame.time.wait(SLEEPTIME)
        bars[i].set_color(BAR_COLOR)
        bars[j].set_color(BAR_COLOR)

    def buildMaxHeap():
        for i in range(len(array)):

            if array[i] > array[int((i - 1) / 2)]:
                j = i

                while array[j] > array[int((j - 1) / 2)]:
                    checkExit()
                    array[j], array[(j - 1) //
                                    2] = array[(j - 1) // 2], array[j]
                    update(i, j)
                    j = (j - 1) // 2

    buildMaxHeap()

    for i in range(len(array) - 1, 0, -1):
        j = 0
        array[j], array[i] = array[i], array[j]
        update(i, j)
        j, index = 0, 0

        while True:
            checkExit()
            index = 2 * j + 1

            if (index < (i - 1) and
                    array[index] < array[index + 1]):
                index += 1

            if index < i and array[j] < array[index]:
                array[j], array[index] = array[index], array[j]
            update(i, j)
            j = index
            if index >= i:
                break

########################################################################
def mainPage(sortFunc):
    global array, bars
    running = True
    while running:
        drawBars(bars)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and array!=sorted(array):
                    sortFunc()
                if event.key == pygame.K_r:
                    shuffle(array)
                    bars = prepareBarList(array)
                if event.key == pygame.K_m or event.key == pygame.K_ESCAPE:
                    welcomePage1()
        pygame.display.flip()


def welcomePage2(func):
    global NUM_BARS, SLEEPTIME, array, maximum, barWidth, bars, gap
    selectedSize = None
    numDict = {}
    bar1 = Button(BLUE, "20", 100, 250, 100, 100)
    numDict[bar1] = 20
    bar3 = Button(BLUE, "500", WIDTH-200, 250, 100, 100)
    numDict[bar3] = 500
    bar2 = Button(BLUE, "100", (bar1.x+bar3.x)//2, 250, 100, 100)
    numDict[bar2] = 100
    buttonList = list(numDict.keys())
    SleeptimeDict = {20: 200, 100: 20, 500: 2}
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m or event.key == pygame.K_ESCAPE:
                    welcomePage1()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in buttonList:
                    if button.isClicked(pos):
                        selectedSize = button
                        NUM_BARS = numDict[selectedSize]
                        SLEEPTIME = SleeptimeDict[NUM_BARS]
                        array = [i for i in range(1, NUM_BARS+1)]
                        shuffle(array)
                        maximum = max(array)
                        gap = 1 if NUM_BARS <= 300 else 0
                        barWidth = (WIDTH-2*margin-len(array)*gap)//len(array)
                        bars = prepareBarList(array)
                        mainPage(func)
        WIN.fill(WHITE)
        myfont = pygame.font.SysFont('Comic Sans MS', 25)
        text = myfont.render(
            'Select Number of Elements To Sort in Visualization', 1, (0, 0, 0))
        WIN.blit(text, ((WIDTH/2-text.get_width()/2), 50))
        bar1.draw(WIN)
        bar2.draw(WIN)
        bar3.draw(WIN)
        pygame.display.flip()


def welcomePage1():
    selectedSort = None
    funcDict = {}
    quick = Button(GREEN, "Quick Sort", 50, 150, 200, 100)
    funcDict[quick] = quickSort
    heap = Button(GREEN, "Heap Sort", 250, 150, 200, 100)
    funcDict[heap] = heapSort
    bubble = Button(GREEN, "Bubble Sort", 450, 150, 200, 100)
    funcDict[bubble] = bubbleSort
    selection = Button(GREEN, "Selection Sort", 50, 300, 200, 100)
    funcDict[selection] = selectionSort
    insertion = Button(GREEN, "Insertion Sort", 250, 300, 200, 100)
    funcDict[insertion] = insertionSort
    merge = Button(GREEN, "Merge Sort", 450, 300, 200, 100)
    funcDict[merge] = mergeSort
    buttonList = list(funcDict.keys())
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in buttonList:
                    if button.isClicked(pos):
                        selectedSort = button
                        welcomePage2(funcDict[selectedSort])
        WIN.fill(WHITE)
        myfont = pygame.font.SysFont('Comic Sans MS', 25)
        text = myfont.render(
            'Select Sorting Technique To Visualize', 1, (0, 0, 0))
        WIN.blit(text, ((WIDTH/2-text.get_width()/2), 50))
        quick.draw(WIN, WHITE)
        heap.draw(WIN, WHITE)
        bubble.draw(WIN, WHITE)
        selection.draw(WIN, WHITE)
        merge.draw(WIN, WHITE)
        insertion.draw(WIN, WHITE)
        pygame.display.flip()


def startApp():
    welcomePage1()


if __name__ == "__main__":
    startApp()
