# Ingrid Crant

# This is a Spiderman: Far From Home themed paint program
# users can draw with pencil and marker, erase, draw various shapes (line, rectangle, ellipse, polygon) filled and unfilled,
# spray paint, get the color at a point (eyedropper),
# select the transparency levels for these tools: pencil, marker, line, rectangle, ellipse, polygon, and spraypaint,
# fill areas with a specific color (bucket), and blits spiderman-themed stamps to the canvas.
# The user can also undo and redo actions, save drawn images and load them onto the canvas.

# TOOL FUNCTIONS
#----------------------------------------------------------------------------------------------

def makeTxt(fnt,c, wid, txt): # function that returns a surface with a string seperated on multiple lines
    lines = [] # list to save the seperated strings
    while fnt.size(txt)[0] > wid:
        p = len(txt)
        while fnt.size(txt[0:p])[0] > wid:
            p = txt.rfind(" ",0,p) # keeps on finding the last space to make the length of the beginning of the string to that space less than the width
        lines.append(txt[0:p])
        txt = txt[p+1:] # repeats the process until the first while loop isn't satisfied
    lines.append(txt)

    height = fnt.get_height()
    surf = Surface((wid,height*len(lines))).convert() # creates surface the size of the multiline rectangle
    surf.fill((1,1,1))
    surf.set_colorkey((1,1,1))
    for i,ln in enumerate(lines):
        txtPic = fnt.render(ln, True, c)
        surf.blit(txtPic,(0,height*i)) # renders and blits each element in lines
    return surf

def pencil(alphacolor,x1,y1,x2,y2):
    pencilsurface = Surface((1200,800), SRCALPHA) # creates surface to support transparency
    draw.aaline(pencilsurface,alphacolor,(x1,y1),(x2,y2)) # draws a antialiased (not jagged) line
    screen.blit(pencilsurface,(0,0))

def marker(alphacolor,x1,y1,x2,y2,size):
    markersurface = Surface((1200,800), SRCALPHA) # creates surface to support transparency
    sizetoradii = {1:3,2:5,3:7,4:10,5:13}
    dx = x2-x1 #width of triangle
    dy = y2-y1 #height of triangle
    maxlength = max(abs(dx),abs(dy))
    for i in range(maxlength):
        x = x1+int(i*(dx/maxlength)) # goes up in increments of 1 or x/y (less than 1)
        y = y1+int(i*(dy/maxlength)) # goes up in increments of 1 or y/x (less than 1)
        draw.circle(markersurface,alphacolor,(x,y),sizetoradii[size]) # draws each point on the hypotenuse of the triangle
    screen.blit(markersurface,(0,0))

def line(alphacolor,ax,ay,cx,cy,size,screencopy):
    linesurface = Surface((1200,800), SRCALPHA) # creates surface to support transparency
    sizetowidth = {1:2,2:4,3:7,4:10,5:12}
    screen.blit(screencopy,(0,0)) # only 1 line is drawn
    draw.line(linesurface,alphacolor,(ax,ay),(cx,cy),sizetowidth[size])
    screen.blit(linesurface,(0,0))

def rectangle(alphacolor,ax,ay,cx,cy,size,mode,screencopy):
    rectanglesurface = Surface((1200,800), SRCALPHA) # creates surface to support transparency
    screen.blit(screencopy,(0,0))
    sizetothickness = {1:2,2:4,3:7,4:10,5:12}
    if mode=="unfilled":
        draw.rect(rectanglesurface,alphacolor,(ax,ay,cx-ax,cy-ay),sizetothickness[size])
    elif mode=="filled":
        draw.rect(rectanglesurface,alphacolor,(ax,ay,cx-ax,cy-ay))
    screen.blit(rectanglesurface,(0,0))

def ellipse(alphacolor,ax,ay,cx,cy,size,mode,screencopy):
    ellipsesurface = Surface((1200,800), SRCALPHA) # creates surface to support transparency
    sizetothickness = {1:2,2:4,3:7,4:10,5:12}
    screen.blit(screencopy,(0,0))
    boundedrect = Rect(min(ax,cx),min(ay,cy),abs(cx-ax),abs(cy-ay)) # rectangle that bounds the ellipse
    if sizetothickness[size] < min(boundedrect[2],boundedrect[3])//2 and mode == "unfilled": # if thickness is less than the shortest side of boundedrect and mode is unfilled
        draw.ellipse(ellipsesurface,alphacolor,boundedrect,sizetothickness[size]) # draws outline of ellipse with thickness
    if sizetothickness[size] < min(boundedrect[2],boundedrect[3])//2 and mode == "filled": # if thickness is less than the shortest side of boundedrect and mode is filled
        draw.ellipse(ellipsesurface,alphacolor,boundedrect) # draws filled ellipse
    screen.blit(ellipsesurface,(0,0))

def polygon(alphacolor,x,y,size,screencopy,polygonpoints,mouse_button,mode):
    polygonSurface = Surface((1200,800), SRCALPHA) # creates surface to support transparency
    sizetothickness = {1:2,2:4,3:7,4:10,5:12}
    if mode == "unfilled":
        if polygonpoints == []:
            if mouse_button == LEFT:
                polygonpoints.append((x,y))
        else:
            if mouse_button == LEFT:
                polygonpoints.append((x,y))
                screen.blit(screencopy,(0,0))
                draw.line(polygonSurface,alphacolor,polygonpoints[-2],polygonpoints[-1],sizetothickness[size]) # draws line from last point to point you just clicked
            elif mouse_button == RIGHT and len(polygonpoints) > 2: # only finishes polygon if there are more than 2 points
                screen.blit(screencopy,(0,0))
                draw.line(polygonSurface,alphacolor,polygonpoints[0],polygonpoints[-1],sizetothickness[size]) # draws line from last point to point you just clicked
                polygonpoints = [] # resets

    elif mode == "filled":
        if polygonpoints == []:
            if mouse_button == LEFT:
                polygonpoints.append((x,y))
        else:
            if mouse_button == LEFT:
                polygonpoints.append((x,y))
                screen.blit(screencopy,(0,0))
                draw.line(polygonSurface,alphacolor,polygonpoints[-2],polygonpoints[-1],sizetothickness[size]) # draws line from last point to point you just clicked
            elif mouse_button == RIGHT and len(polygonpoints) > 2:
                screen.blit(screencopy,(0,0))
                draw.line(polygonSurface,alphacolor,polygonpoints[0],polygonpoints[-1],sizetothickness[size]) # draws line from last point to point you just clicked
                screen.blit(polygonSurface,(0,0))
                draw.polygon(polygonSurface,alphacolor,polygonpoints) # fills in polygon
                polygonpoints = [] # resets

    screen.blit(polygonSurface,(0,0))
    return polygonpoints

def spraypaint(alphacolor,x1,y1,size):
    spraypaintsurface = Surface((1200,800), SRCALPHA) # creates surface to support transparency
    sizetoradii = {1:5,2:10,3:15,4:20,5:25}
    radius = sizetoradii[size]
    for i in range(20):
        x,y = randint(x1-radius,x1+radius),randint(y1-radius,y1+radius)
        if hypot(x-x1,y-y1) < radius: # makes it into a circle
            spraypaintsurface.set_at((x,y),alphacolor)
    screen.blit(spraypaintsurface,(0,0))

def eyedropper(mx,my):
    return screen.get_at((mx,my)) # returns color of the pixel at (mx,my)

def cleartool():
    screen.fill((255,255,255),canvasRect)

def paintbucket(color,x,y,canvascopy):
    choosecolor = screen.get_at((x,y))
    if choosecolor == color: #if the color you clicked on is the color you want to change it to, do nothing
        return
    choosecolorpoints = [(x,y)]
    while len(choosecolorpoints) > 0:
        x1,y1 = choosecolorpoints.pop()
        if screen.get_at((x1,y1)) == choosecolor: #takes only the pixels inside the 1 shape you clicked inside
            screen.set_at((x1,y1),color)
            choosecolorpoints += [(x1+1,y1),(x1-1,y1),(x1,y1+1),(x1,y1-1)] #adds the pixels around it and repeats the process

def spiderweb(x,y,image):
    screen.blit(image,(x-(image.get_width()//2),y-(image.get_height()//2)))

def text():
    textfont = font.Font("Roboto-Bold.ttf", 17)
    textArea = Rect(12,311,270,91) # types text on top of this area
    word = "" # word will be built one character at a time

    screen.set_clip(textArea)
    while True:
        for e in event.get():
            if e.type == QUIT:
                event.post(e)   # puts QUIT back in event list so main quits
                return ""
            if e.type == KEYDOWN:
                if e.key == 8:    # 8 is backspace, remove last letter
                    if len(word)>0:
                        word = word[:-1]
                elif e.key == 13: # 13 is enter
                    return word # returns word to be later blitted onto the canvas
                elif e.key < 256:
                    word += chr(e.key) # converts ascii to character

            draw.rect(screen,(255,255,255),(15,311,260,90))
            draw.rect(screen,(0,0,0),(15,311,260,90),2)
            wordTxt = makeTxt(textfont,(0,0,0),250,word)
            screen.blit(wordTxt,(20,315)) # blits wordTxt on top the text rect area
            display.flip()

def save():
    name = "" # final answer will be built one letter at a time.
    spiderfonttype = font.Font("Roboto-Bold.ttf", 17)
    backpage = screen.copy() # copy screen so we can replace it when done
    textArea = Rect(10,285,375,25)

    screen.set_clip(textArea)
    typing = True
    while typing:
        for e in event.get():
            if e.type == QUIT:
                event.post(e) # puts QUIT back in event list so main quits
                return ""
            if e.type == KEYDOWN:
                if e.key == 8: # remove last letter
                    if len(name)>0:
                        name = name[:-1]
                elif e.key == 13:
                    typing = False
                elif e.key < 256:
                    name += chr(e.key) # add character to ans

        txtPic = spiderfonttype.render(name, True, (0,0,0))
        draw.rect(screen,(255,255,255),textArea)
        draw.rect(screen,(0,0,0),textArea,2)
        screen.blit(txtPic,(textArea.x+3,textArea.y+8))

        display.flip()
    screen.set_clip(None)
    screen.blit(backpage,(0,0))
    return name

def load():
    namerects = [] # list to store rects of where each image name is
    spiderfonttype = font.Font("Roboto-Bold.ttf", 17)

    imagenameslist = os.listdir('canvasprojects/') # list that stores the names of each file in the folder canvasprojects (for drawn canvases)
    for i in imagenameslist:
        if i.find('DS_Store') != -1: # removes any sort of DS_Store from imagenameslist
            imagenameslist.remove(i) # removes DS_Store from imagenameslist list

    if len(imagenameslist) > 0:
        choiceArea = Rect(10,285,375,len(imagenameslist)*21) # rect area showing each element of imagenameslist (height changes with length of imagenameslist)
        draw.rect(screen,(202,104,95),choiceArea)
        draw.rect(screen,(0,0,0),choiceArea,2)

    for i in range(len(imagenameslist)):
        name = spiderfonttype.render(imagenameslist[i], True, (0,0,0))
        namerect = Rect(choiceArea[0]+5,choiceArea[1]+5+i*name.get_height(),375,name.get_height())
        screen.blit(name,namerect)

        namerects.append(namerect)

    return [namerects,imagenameslist]


# INITIALIZING
#-----------------------------------------------------------------------------

from pygame import *
from math import hypot
from random import randint
from glob import *
import datetime
import os

font.init()
mixer.init()

screen = display.set_mode((1200,780))

eyecolor1list = [239,268,239,270,239,271,238,271,238,272,236,272,236,273,234,273,233,273,233,274,229,274,229,275,227,275,227,273,227,274,222,274,222,273,221,273,221,272,217,272,217,270,215,270,215,269,214,269,213,269,213,267,212,268,212,266,209,267,209,264,208,263,207,262,206,260,206,257,205,257,205,254,204,254,204,253,203,253,203,251,202,251,202,248,201,248,201,245,199,245,200,241,199,241,199,238,198,238,198,234,197,234,197,227,196,228,196,211,197,211,197,212,198,212,198,213,199,213,199,214,200,214,200,215,201,215,201,216,202,216,202,217,203,217,203,218,205,218,204,219,206,219,206,221,207,221,207,222,208,222,208,223,209,223,209,224,210,224,210,225,211,225,211,226,212,226,212,227,213,227,213,228,214,228,214,229,215,229,215,231,216,231,216,232,217,232,217,233,218,233,218,236,219,236,219,237,220,237,220,238,221,238,221,239,222,239,222,240,223,240,223,241,224,241,224,243,225,243,225,244,226,244,226,246,227,246,227,247,228,247,228,249,229,249,229,251,230,251,230,252,231,252,231,253,232,253,232,255,233,255,233,258,234,258,234,260,235,260,235,261,236,261,236,263,237,264,238,264,238,265,239,266,239,267,240,268,240,269,239,269] # list of coordinates for the polygon that makes the first eye
eyecolor1polypoints = [(eyecolor1list[i],eyecolor1list[i+1]) for i in range(0,len(eyecolor1list),2)] # used list comprehension to put it into the form [(x,y),(x,y)..]

eyecolor2list = [294,280,294,277,296,277,296,276,297,276,297,275,298,275,298,274,299,274,299,272,300,272,300,271,301,271,301,270,303,270,302,269,302,267,303,267,303,266,304,266,304,267,305,267,305,266,306,266,306,263,308,263,308,262,310,262,310,261,311,261,311,258,313,258,313,257,314,257,314,256,315,256,315,255,317,255,317,254,317,253,318,253,319,253,319,252,320,252,321,252,321,251,322,251,322,250,323,250,323,248,325,248,325,247,326,247,326,246,329,246,329,244,330,244,330,243,331,243,331,242,335,242,335,241,336,241,336,240,338,240,338,239,340,239,340,238,342,238,342,237,344,237,344,236,346,236,346,235,347,235,347,234,348,234,348,233,352,233,352,232,354,232,354,231,355,231,355,232,355,239,354,239,354,246,354,247,353,247,353,250,352,250,352,254,351,254,351,257,350,257,350,258,349,258,349,261,349,262,348,262,348,263,347,263,347,265,346,265,346,266,345,266,345,268,344,268,344,270,344,271,343,271,343,272,342,272,342,273,341,273,341,274,340,274,340,276,338,276,338,277,338,278,336,278,336,280,335,280,335,281,334,281,334,282,333,282,333,283,331,283,331,284,329,284,329,285,328,285,328,286,327,286,327,287,322,287,322,288,311,288,311,287,307,287,303,287,303,286,301,286,301,284,299,285,299,283,295,283,295,281,294,281,294,279,294,278,294,279,294,277,294,280,294,278,294,277,294,281] # list of coordinates for the polygon that makes the second eye
eyecolor2polypoints = [(eyecolor2list[i],eyecolor2list[i+1]) for i in range(0,len(eyecolor2list),2)] # used list comprehension to put it into the form [(x,y),(x,y)..]

draw.rect(screen,(255,255,255),(0,0,1200,780))
background = transform.scale(image.load("images/spidybackground.jpg"),(1200,780)) # spiderman background of program
screen.blit(background,(0,0))

spidytitle = transform.scale(image.load("images/spidermantitle.png"),(500,150))
screen.blit(spidytitle,(525,20))

colourwheel = transform.scale(image.load("images/colourwheel.png"),(150,150)) # colour selector shaped like a circle
screen.blit(colourwheel,(20,60))

canvasRect = Rect(400,180,750,450)
canvasborderRect = Rect(395,175,760,460)
draw.rect(screen,(0,0,0),canvasborderRect)
draw.rect(screen,(255,255,255),canvasRect)

draw.rect(screen,(0,0,0),(5,415,290,360)) # stamp background

#font stuff
spiderfont=font.Font("Far-From-Homecoming.otf", 50)

spiderfontmedium = font.Font("KOMIKAX_.ttf", 14) #for coords
spiderfontlarge = font.Font("KOMIKAX_.ttf", 20) #for coords

# icons for play/pause
playicon = transform.scale(image.load("images/playicon.png"),(40,40))
pauseicon = transform.scale(image.load("images/pauseicon.png"),(40,40))

musicbox = Rect(20,10,40,40)
is_music_playing = True # keeps track of when its playing and when its not
screen.blit(pauseicon,musicbox)

musicboxcover = transform.scale(image.load("images/musicboxcover.png"),(58,57)) # screenshot of area under play/pause icon
textboxcover = transform.scale(image.load("images/textboxcover.png"),(292-12,413-282)) # screenshot of area under text box
tooltypecover = transform.scale(image.load("images/tooltypecover.png"),(96,197))
coordscover = transform.scale(image.load("images/coordscover.png"),(105,34))
timeboxcover = transform.scale(image.load("images/timeboxcover.png"),(1189-1090,47-10))

volume =  5
volumerect = Rect(125,10,40,40)
volumeuprect = Rect(170,10,40,40)
volumedownrect = Rect(80,10,40,40)
volumeupicon = transform.scale(image.load("images/volumeupicon.png"),(40,40))
volumedownicon = transform.scale(image.load("images/volumedownicon.png"),(40,40))
screen.blit(volumeupicon,volumeuprect)
screen.blit(volumedownicon,volumedownrect)
draw.rect(screen,(0,0,0),volumerect)
volumewriting = spiderfontlarge.render(str(volume),True,(255,255,255))
screen.blit(volumewriting,(volumerect[0],volumerect[1]))

mixer.music.load("songs/farfromhomesuite.wav")
mixer.music.play(-1) # music plays indefinitely

subtitle = spiderfont.render("Paint From Home",True,(255,255,255))
subtitlewidth = subtitle.get_width()
screen.blit(subtitle,(775-subtitlewidth//2,110)) # centers subtitle above the canvas

screencopy = screen.copy()

spiderwebimage = transform.scale(image.load("images/spiderweb.png"),(700,700)) # to be used for the spiderweb tool

col = (0,0,0) # colour

undolist = [screen.subsurface(canvasRect).copy()]
redolist = []

size = 1
alpha = 255 # alpha is transparency level
alpharect = Rect(65,230,40,40)
draw.rect(screen,(0,0,0),alpharect)
alphawriting = spiderfontlarge.render(str(alpha),True,(255,255,255))
screen.blit(alphawriting,(alpharect[0],alpharect[1]))
transparencytitleshade = spiderfontmedium.render("Transparency Level",True,(0,0,0))
transparencytitle = spiderfontmedium.render("Transparency Level",True,(255,255,255))
screen.blit(transparencytitleshade,((85-transparencytitle.get_width()//2)-2,(230-transparencytitle.get_height())-2))
screen.blit(transparencytitle,(85-transparencytitle.get_width()//2,230-transparencytitle.get_height()))

alphachanges = ["minus","plus"]
alphachangerects = [Rect(40,230,23,40),Rect(107,230,23,40)]

tools = ["text","spiderweb","pencil","marker","eraser","line","rect","ellipse","polygon","spraypaint","paintbucket","eyedropper","spidermanstamp","spidermansymbolstamp","spidermantextstamp","edithglassesstamp","midtownhighstamp","marvelstamp"]
toolrects = [Rect(325,715,70,70),Rect(325,640,70,70),Rect(400,640,70,70),Rect(475,640,70,70),Rect(550,640,70,70),Rect(625,640,70,70),Rect(700,640,70,70),Rect(775,640,70,70),Rect(850,640,70,70),Rect(925,640,70,70),Rect(1000,640,70,70),Rect(1075,640,70,70),Rect(5,430,145,115),Rect(150,430,145,115),Rect(5,545,145,115),Rect(150,545,145,115),Rect(5,660,145,115),Rect(150,660,200,115)]

actions = ["undo","redo","clear","save","load"]
actionrects = [Rect(400,715,140,70),Rect(550,715,140,70),Rect(700,715,140,70),Rect(850,715,140,70),Rect(1000,715,140,70)]

tooltypes = ["unfilled","filled"]
tooltyperects = [Rect(320,480,70,70),Rect(320,555,70,70)]

tool="pencil"
tooltype = "unfilled"
tooltype_on = False
toolnorm = []
toolhover = []
toolclick = []
actionnorm = []
actionhover = []
actionclick = []
alphachangenorm = []
alphachangehover = []
alphachangeclick = []
tooltypenorm = []
tooltypehover = []
tooltypeclick = []
polygonpointslist = []
choosecolorpoints = []
imagenames = []
imagenamerects = []
imagerects = []
action = "none"

# creates icons for mx,my not on top of it (norm), mx,my hovering on it (hover), and mx,my clicking on it (click)
for t in tooltypes:
    tooltypenorm += [transform.scale(image.load("images/"+t+"3.png"),(70,70))]
    tooltypehover += [transform.scale(image.load("images/"+t+"1.png"),(70,70))]
    tooltypeclick += [transform.scale(image.load("images/"+t+"2.png"),(70,70))]

for t in tools[:12]: # only makes normal, hover and click icons for tools that aren't stamps
    toolnorm += [transform.scale(image.load("images/"+t+"3.png"),(70,70))]
    toolhover += [transform.scale(image.load("images/"+t+"1.png"),(70,70))]
    toolclick += [transform.scale(image.load("images/"+t+"2.png"),(70,70))]

for a in actions:
    actionnorm += [transform.scale(image.load("images/"+a+"3.png"),(140,50))]
    actionhover += [transform.scale(image.load("images/"+a+"1.png"),(140,50))]
    actionclick += [transform.scale(image.load("images/"+a+"2.png"),(140,50))]

for a in alphachanges:
    alphachangenorm += [transform.scale(image.load("images/"+a+"3.png"),(23,40))]
    alphachangehover += [transform.scale(image.load("images/"+a+"1.png"),(23,40))]
    alphachangeclick += [transform.scale(image.load("images/"+a+"2.png"),(23,40))]

for s in tools[12:]: # tools[12:] are the stamps
    stampimage = image.load("images/"+s+".png")
    w = stampimage.get_width()
    h = stampimage.get_height()
    stampratio = 140/w # we want a standard width of 140 for all stamps
    toolnorm += [transform.scale(stampimage,(int(w*stampratio),int(h*stampratio)))]

LEFT = 1
RIGHT = 3

ax,ay = 1,1

# RUNNING LOOP
#------------------------------------------------------------------------------

running=True
while running:

    for evt in event.get():

        if evt.type==QUIT:
            running=False

        if evt.type==MOUSEBUTTONDOWN:
            if tool == "polygon":
                ax,ay = mouse.get_pos()
                if canvasRect.collidepoint((ax,ay)):
                    polygonpointslist = polygon(col[:3]+(alpha,),ax,ay,size,screencopy,polygonpointslist,evt.button,tooltype)
            if evt.button == LEFT:
                ax,ay = mouse.get_pos() # these are my anchor points
                screencopy = screen.copy()
                canvascopy = screen.subsurface(canvasRect).copy()
                for actioni in range(len(actionrects)):
                    if actionrects[actioni].collidepoint(ax,ay):
                        action = actions[actioni]

                        polygonpointslist=[] #if you click on an action, the polygon points list resets

                        if action == "undo":
                            if len(undolist)>1:
                                redolist.append(undolist.pop()) # appends what you just undid to the redo list
                                screen.blit(undolist[-1],canvasRect) # takes last one in the undo list and blits it on

                        elif action == "redo":
                            if len(redolist)>0:
                                undolist.append(redolist.pop()) # appends what you just redid to the undo list
                            if len(undolist)>1:
                                screen.blit(undolist[-1],canvasRect) # takes last one in the undo list and blits it on

                        elif action == "clear":
                            cleartool()

                        elif action == "save":
                            filename = save()
                            if filename == "": #so it doesn't crash
                                pass
                            elif "." not in filename:
                                filename += ".bmp" # adds .bmp as an ending to filename
                                image.save(screen.subsurface(canvasRect),"canvasprojects/"+filename)
                            elif filename[filename.index("."):] not in ".bmp":
                                filename = filename[:filename.index(".")]
                                filename += ".bmp" #replaces any other ending with .bmp
                                image.save(screen.subsurface(canvasRect),"canvasprojects/"+filename)
                            else:
                                image.save(screen.subsurface(canvasRect),"canvasprojects/"+filename)

                        elif action == "load":
                            backpage = screen.copy()
                            loadoutput = load()
                            imagenamerects = loadoutput[0]
                            imagenames = loadoutput[1]

                if musicbox.collidepoint(mx,my):
                    screen.blit(musicboxcover,(8,1))
                    if is_music_playing:
                        mixer.music.pause() # pauses if playing
                        screen.blit(playicon,musicbox)
                    else:
                        mixer.music.unpause()
                        screen.blit(pauseicon,musicbox) # plays if paused
                    is_music_playing = not is_music_playing # sets is_music_playing to it's opposite

                if volumedownrect.collidepoint(mx,my):
                    volume -= 1
                    if volume < 0:
                        volume = 0 # makes 0 the min
                elif volumeuprect.collidepoint(mx,my):
                    volume += 1
                    if volume > 10:
                        volume = 10 # makes 10 the max
                draw.rect(screen,(0,0,0),volumerect)
                volumewriting = spiderfontlarge.render(str(volume),True,(255,255,255))
                screen.blit(volumewriting,(volumerect[0],volumerect[1]))
                mixer.music.set_volume(volume/10)

            elif evt.button == 4:
                size += 1
                if size > 5:
                    size = 5 # makes max size 5
            elif evt.button==5:
                size -= 1
                if size < 1:
                    size = 1 # makes min size 1

        if evt.type==MOUSEBUTTONUP:
            if canvasRect.collidepoint(ax,ay): # only records the canvas if you did something in the canvas
                undolist.append(screen.subsurface(canvasRect).copy())

    #out of the event loop now
    mx,my = mouse.get_pos()
    mb = mouse.get_pressed()
    mouse_pressed = (mb[0]==1)

    for i in range(len(tools[:12])):
        screen.blit(toolnorm[i],toolrects[i]) # blits the normal icon
        if toolrects[i].collidepoint(mx,my):
            screen.blit(toolhover[i],toolrects[i]) # blits the hovering icon
        if toolrects[i].collidepoint(ax,ay): # uses ax,ay bc tool wron't reset if I'm pressing and hover somewhere else
            tool = tools[i] # sets tool to what is pressed

    if action == "load":
        pass # don't want stamps to blit on top of load rect
    else:
        for i in range(len(tools[12:])): # iterates through the stamps
            # uses [i+12] bc the related indexes are 12 from i
            screen.blit(toolnorm[i+12],(toolrects[i+12][0],toolrects[i+12][1]+(toolrects[i+12][3]-toolnorm[i+12].get_height())//2)) # blits stamps on their respective rects
            if toolrects[i+12].collidepoint(ax,ay):
                tool = tools[i+12] # sets that stamp as the tool

    if tool == "text":
        textscreencopy = screen.copy()
        textoutput = text()
        if len(textoutput) != 0:
            textword = textoutput
            tool = "textstamp" # redirects tool to textstamp
            (ax,ay) = (1,1) # resets ax,ay so that tool doesn't reset to text
            screen.blit(textboxcover,(12,282))

    for i in range(len(alphachanges)):
        screen.blit(alphachangenorm[i],alphachangerects[i]) # blits the normal icon
        if alphachangerects[i].collidepoint(mx,my):
            screen.blit(alphachangehover[i],alphachangerects[i]) # blits the hovering icon
            if mouse_pressed:
                screen.blit(alphachangeclick[i],alphachangerects[i]) # blits the clicked icon
                if alphachanges[i] == "plus":
                    alpha += 1
                    if alpha > 255:
                        alpha = 255 # makes max alpha 255
                else:
                    alpha -= 1
                    if alpha < 0:
                        alpha = 0 # makes min alpha 0

                draw.rect(screen,(0,0,0),alpharect)
                alphawriting = spiderfontlarge.render(str(alpha),True,(255,255,255))
                screen.blit(alphawriting,(alpharect[0],alpharect[1]))

    if action == "load" or tool == "text":
        pass # stops a surface from being blit on top of the load rect or textbox
    else:
        if tool == "rect" or tool == "ellipse" or tool == "polygon": # blits the filled and unfilled selectors only for the tools that need it
            for i in range(len(tooltypes)):
                screen.blit(tooltypenorm[i],tooltyperects[i]) # blits normal icons
                if tooltyperects[i].collidepoint(mx,my):
                    screen.blit(tooltypehover[i],tooltyperects[i]) # blits hovered icons
                if tooltyperects[i].collidepoint(ax,ay):
                    tooltype = tooltypes[i] # sets tooltype to what you pressed: "unfilled" or "filled"
            screen.blit(tooltypeclick[tooltypes.index(tooltype)],tooltyperects[tooltypes.index(tooltype)]) # blits the clicked icon of your tooltype
        else:
            screen.blit(tooltypecover,(297,432)) # blits a screenshot of the area before the filled and unfilled icons covered it

    for i in range(len(actions)):
        screen.blit(actionnorm[i],actionrects[i]) # blits the normal icon
        if actionrects[i].collidepoint(mx,my):
            screen.blit(actionhover[i],actionrects[i]) # blits the hovered icon
            if mouse_pressed:
                screen.blit(actionclick[i],actionrects[i]) # blits the clicked icon

    for i in range(len(imagenames)): # references the list of image names from the load function
        if imagenamerects[i].collidepoint(ax,ay):
            screen.blit(backpage,(0,0)) # blits screencopy to cover text area
            screen.blit(transform.scale(image.load("canvasprojects/"+imagenames[i]),(750,450)),(400,180)) # blits the selected image onto the canvas
            imagenames = [] # resets imagenames and imagenamerects so that you can't click and select anymore
            imagenamerects = []
            action = "none" # so that stamps and "filled" and "unfilled" can work
            break # breaks so that an index error doesn't occur if the loop continues

    if tool in tools[:12]: # if tool is not a stamp
        screen.blit(toolclick[tools.index(tool)],toolrects[tools.index(tool)]) # blits the clicked icon of that tool

    if canvasRect.collidepoint(mx,my):
        screen.set_clip(canvasRect) # you are restricted to the canvas
        if mouse_pressed:
            if tool=="pencil":
                pencil(col[:3]+(alpha,),mx,my,mx2,my2)
            elif tool=="marker":
                marker(col[:3]+(alpha,),mx,my,mx2,my2,size)
            elif tool == "line":
                line(col[:3]+(alpha,),ax,ay,mx,my,size,screencopy)
            elif tool == "rect":
                if tooltype == "filled":
                    rectangle(col[:3]+(alpha,),ax,ay,mx,my,size,"filled",screencopy)
                elif tooltype == "unfilled":
                    rectangle(col[:3]+(alpha,),ax,ay,mx,my,size,"unfilled",screencopy)
            elif tool=="ellipse":
                if tooltype == "filled":
                    ellipse(col[:3]+(alpha,),ax,ay,mx,my,size,"filled",screencopy)
                elif tooltype == "unfilled":
                    ellipse(col[:3]+(alpha,),ax,ay,mx,my,size,"unfilled",screencopy)
            elif tool == "spraypaint":
                spraypaint(col[:3]+(alpha,),mx,my,size)
            elif tool == "eraser":
                marker((255,255,255,255),mx,my,mx2,my2,size)
            elif tool == "eyedropper":
                col = eyedropper(mx,my)
            elif tool == "paintbucket":
                paintbucket(col[:3],mx,my,canvascopy)
            elif tool == "spiderweb":
                spiderweb(ax,ay,spiderwebimage)
            elif tool == "textstamp":
                sizetofont = {1:12,2:15,3:18,4:21,5:24} # converts size to the font size of textword
                txtfont = font.Font("KOMIKAX_.ttf", sizetofont[size])
                textsurface = txtfont.render(textword,True,col[:3]) # renders the text from text() with the selected colour
                screen.blit(textsurface,(ax-(textsurface.get_width()//2),ay-(textsurface.get_height()//2))) # holding it from the middle of the surface
                display.flip()
            elif tool[-5:]=="stamp": #if its a stamp
                screen.blit(screencopy,(0,0))
                stampimage = toolnorm[tools.index(tool)]
                screen.blit(stampimage,(mx-(stampimage.get_width()/2),(my-(stampimage.get_height()/2)))) # holding it from the middle of the stamp

    screen.set_clip(None) #you can do stuff outside of the canvas

    if hypot(mx-95,my-135) <= 63: # (95,135) is the center of the colour wheel; 63 is the radius
        if mouse_pressed:
            col = screen.get_at((mx,my))

    if col == (0,0,0):
        eyecolor1surface = Surface((1200,800), SRCALPHA)
        eyecolor2surface = Surface((1200,800), SRCALPHA)
        draw.polygon(eyecolor1surface,(255,255,255,255),eyecolor1polypoints)
        draw.polygon(eyecolor2surface,(255,255,255,255),eyecolor2polypoints)
        screen.blit(eyecolor1surface,(0,0))
        screen.blit(eyecolor2surface,(0,0))
    else:
        # sets the polygon of both eyes the color of col and transparency of alpha
        eyecolor1surface = Surface((1200,800), SRCALPHA)
        eyecolor2surface = Surface((1200,800), SRCALPHA)
        draw.polygon(eyecolor1surface,col[:3]+(alpha,),eyecolor1polypoints)
        draw.polygon(eyecolor2surface,col[:3]+(alpha,),eyecolor2polypoints)
        screen.blit(eyecolor1surface,(0,0))
        screen.blit(eyecolor2surface,(0,0))

    mx2,my2 = mx,my

    screen.blit(coordscover,(1077,49)) # blits screenshot of area under the coordinates to account for shifting width

    coords = spiderfontmedium.render("("+str(mx)+","+str(my)+")",True,(255,255,255)) # coords are the string form of (mx,my)
    draw.rect(screen,(0,0,0),(1100,50,coords.get_width(),coords.get_height())) # draws black rect to go under coords
    screen.blit(coords,(1100,50))

    curtime = str(datetime.datetime.today())[11:16] #current time
    timewriting = spiderfontlarge.render(curtime,True,(255,255,255))
    draw.rect(screen,(0,0,0),(1998,13,timewriting.get_width()+4,timewriting.get_height()+4))
    screen.blit(timeboxcover,(1090,10)) # blits screenshot of area under the time to account; no overlap between timewriting
    screen.blit(timewriting,(1100,15)) # blits time

    display.flip()
quit()
