import cv2
from cvzone.HandTrackingModule import HandDetector
import time
#it used for hand detecting wheather the button is clicked or not

class Button:
    def __init__(self,pos,width,height,value):
       self.pos=pos
       self.width=width
       self.height=height
       self.value=value
    
    def draw(self,img):
       cv2.rectangle(img,self.pos, (self.pos[0]+self.width,self.pos[1]+self.height),(225,225,225),cv2.FILLED)
       cv2.rectangle(img,self.pos,(self.pos[0]+self.width,self.pos[1]+self.height),(50,50,50),3)
       cv2.putText(img,self.value, (self.pos[0]+40,self.pos[1]+65),cv2.FONT_HERSHEY_PLAIN, 2,(50,50,50),2)

    def checkClick(self,x,y):
       if int(self.pos[0])<x<int(self.pos[0])+self.width  and  int(self.pos[1])<y<int(self.pos[1])+self.width:
           cv2.rectangle(img,self.pos, (self.pos[0]+self.width,self.pos[1]+self.height),(225,225,225),cv2.FILLED)
           cv2.rectangle(img,self.pos,(self.pos[0]+self.width,self.pos[1]+self.height),(50,50,50),3)
           cv2.putText(img,self.value, (self.pos[0]+20,self.pos[1]+70),cv2.FONT_HERSHEY_PLAIN, 5,(0,0,0),5)
           return True
       else:
          return False


#webcam
cap = cv2.VideoCapture(0)
cap.set(3,1280)#width
cap.set(4,720)#height
detector = HandDetector(detectionCon=0.8,maxHands=1)
#number of hands we used for it


#creating button

buttonListValues = [['7','8','9','*'],
                    ['4','5','6','-'],
                    ['1','2','3','+'],
                    ['0','/','.','=']
                    ]



buttonList=[]
for x in range(4):
  for y in range(4):
    xpos=x*100+800
    ypos=y*100+ 150
    buttonList.append(Button((xpos,ypos),100,100, buttonListValues[y][x]))


#variable
myEquation=''
delaycounter=0


while True:
    #get image from webcam
    success,img=cap.read()
    img =cv2.flip(img,1)# eihter 1 or 0

    #hand Detection
    hands,img = detector.findHands(img,flipType=False)

    #drwaing the buttion
    cv2.rectangle(img,(800,70),(800+400,70+100),(225,225,225),cv2.FILLED)
    cv2.rectangle(img,(800,70),(800+400,70+100),(50,50,50),3)
 
    for button in buttonList:
      button.draw(img)
    

    #check for Hand
    if hands:
       lmList=hands[0]['lmList']

       x = lmList[8][0]  # only (x, y)
       y = lmList[8][1]  # only (x, y)
       length, _, img = detector.findDistance((lmList[8][0], lmList[8][1]), (lmList[12][0], lmList[12][1]), img)
       print(length)

       if length<50:
          for i, button in enumerate(buttonList):
            if button.checkClick(x,y) and delaycounter==0:
              myValue=buttonListValues[int(i%4)][int(i/4)]
              if myValue== "=":
                 myEquation= str(eval(myEquation))

              else:
                myEquation +=myValue
              delaycounter=1

    if delaycounter!=0:
          delaycounter += 1
          if delaycounter>10:
             delaycounter=0
            

              
          
    #displaying result
    cv2.putText(img,myEquation,(810,120),cv2.FONT_HERSHEY_PLAIN, 2,(50,50,50),2)


    #display image
    cv2.imshow("image",img)
    key=cv2.waitKey(1)
    if key == ord('c'):
       myEquation = ''
   
