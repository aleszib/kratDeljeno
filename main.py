# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 21:46:17 2020

@author: zibernaa
"""
 

from random import randint
from random import choices
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from  kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

from kivy.storage.jsonstore import JsonStore
from os.path import join
from datetime import datetime


from kivy.uix.screenmanager import ScreenManager, Screen


class MainApp(App):
    def build(self):
        
        self.widgetsFontSize=[]
        self.widgetsFontSizeSmall=[]
        data_dir = getattr(self, 'user_data_dir')
        print(data_dir)
        self.store = JsonStore(join(data_dir,'KratDeljeno.json'))
        if "settings" in self.store:
            settings=self.store["settings"]
            self.settings=settings["settings"]
            if "fontSize" in self.settings:
                self.fontSize=self.settings["fontSize"]
            else:
                self.fontSize=72
            if "fontSizeSmall" in self.settings:
                self.fontSizeSmall=self.settings["fontSizeSmall"]
            else:
                self.fontSizeSmall=36
            if "poMeri" not in self.settings:
                self.settings['poMeri']=None
            
        else:
            self.settings=dict()
            self.fontSize=72
            self.fontSizeSmall=36
            self.settings['poMeri']=None
        self.n=0
#        print(self.settings)
#        print (join(data_dir, 'KratDeljeno.json'))
#        if "hist" not in self.store:
#           self.store["hist"]={}
        if "data" in self.store:
            data=self.store["data"]
            if "hist" in data:
                self.histDict=data["hist"]
            else: self.histDict={}
#            print(self.histDict)
        else: self.histDict={}
        self.id=""
        
        self.operators=["*",":"]
        weightsMed=[7.92, 11.58, 16.91, 22.85, 14.43, 27.19, 28.66, 32.62, 25.81, 12.68]
        minWeight=min(weightsMed)
        weightsDiff=weightsMed[:]
        for i in range(len(weightsDiff)): weightsDiff[i]=weightsDiff[i]-minWeight
        weightsEasy=[1 for i in range(10)]
        self.diff="Srednje"
        self.baseWeights={"Lahko":weightsEasy,
                      "Srednje":weightsMed,
                      "Težko":weightsDiff}
        self.sm = ScreenManager()
        

        
        
        ## Start screen
        StartScreen=Screen(name="Start")
        self.sm.add_widget(StartScreen)
        startLayout=BoxLayout(orientation="vertical")
        select_layout=BoxLayout(orientation="horizontal",size_hint = (1, 4))

        
        # Težavnost
        diff_layout=BoxLayout(orientation="vertical", padding=15)
        select_layout.add_widget(diff_layout)
        
        diffLabel=Label(text="Težavnost", font_size=self.fontSize)
        diff_layout.add_widget(diffLabel)
        if "fontSize" not in self.settings:
                self.fontSize=self.setTextToFit(diffLabel,self.fontSize)
                self.fontSizeSmall=self.fontSize/2
        
        self.widgetsFontSize.append(diffLabel)
        
        self.diffEasy_TB=ToggleButton(text="Lahko", font_size=self.fontSize, group="diff")
        self.widgetsFontSize.append(self.diffEasy_TB)
        diff_layout.add_widget(self.diffEasy_TB)
        
        self.diffMed_TB=ToggleButton(text="Srednje", font_size=self.fontSize, state='down', group="diff")
        diff_layout.add_widget(self.diffMed_TB)
        self.widgetsFontSize.append(self.diffMed_TB)
        
        self.diffDiff_TB=ToggleButton(text="Težko", font_size=self.fontSize, group="diff")
        diff_layout.add_widget(self.diffDiff_TB)    
        self.widgetsFontSize.append(self.diffDiff_TB)
      
        # Številke
        num_layout=BoxLayout(orientation="vertical", padding=15, size_hint=(1.1,1))
        select_layout.add_widget(num_layout)
        
        najStevLabel=Label(text="Največja\nštevilka", font_size=self.fontSize)
        self.widgetsFontSize.append(najStevLabel)
        num_layout.add_widget(najStevLabel)
        numIzbor_layount=BoxLayout(orientation="vertical", padding=(0,0,0,15), size_hint=(1,2))
        num_layout.add_widget(numIzbor_layount)
        num5_10_layout=BoxLayout(orientation="horizontal")
        numIzbor_layount.add_widget(num5_10_layout)
        
        self.num10_TB=ToggleButton(text="10", font_size=self.fontSize, group="num", state='down')
        num5_10_layout.add_widget(self.num10_TB)
        self.widgetsFontSize.append(self.num10_TB)

        self.num5_TB=ToggleButton(text="5", font_size=self.fontSize, group="num")
        num5_10_layout.add_widget(self.num5_TB)
        self.widgetsFontSize.append(self.num5_TB)

        if self.settings['poMeri']:
            tmpPoMeri=self.settings['poMeri']
            if len(tmpPoMeri)==1:
                tmpPoMeri=tmpPoMeri[0]
        else:
            tmpPoMeri="?"
        self.numPoMeri_TB=ToggleButton(text=f"{tmpPoMeri}", font_size=self.fontSize, group="num")
        if not self.settings['poMeri']:
            self.numPoMeri_TB.disabled =True
        numIzbor_layount.add_widget(self.numPoMeri_TB)
        self.widgetsFontSize.append(self.numPoMeri_TB)
        
        ButtonNastaviPoMeri=Button(text="Nastavi", font_size=self.fontSize)
        ButtonNastaviPoMeri.bind(on_press=self.startPoMeri)
        num_layout.add_widget(ButtonNastaviPoMeri)
        self.widgetsFontSize.append(ButtonNastaviPoMeri)
    

        # Operatorji
        op_layout=BoxLayout(orientation="vertical", padding=15)
        select_layout.add_widget(op_layout)
        
        operacijeLabel=Label(text="Operacije", font_size=self.fontSize)
        self.widgetsFontSize.append(operacijeLabel)
        op_layout.add_widget(operacijeLabel)

        self.opKrat_TB=ToggleButton(text="*", font_size=self.fontSize, group="op")
        op_layout.add_widget(self.opKrat_TB)
        self.widgetsFontSize.append(self.opKrat_TB)

        self.opDeljeno_TB=ToggleButton(text=":", font_size=self.fontSize, group="op")
        op_layout.add_widget(self.opDeljeno_TB)
        self.widgetsFontSize.append(self.opDeljeno_TB)
        
        self.opOba_TB=ToggleButton(text="* in :", font_size=self.fontSize, group="op", state='down' )
        op_layout.add_widget(self.opOba_TB)
        self.widgetsFontSize.append(self.opOba_TB)
        

        ##
        startLayout.add_widget(select_layout)
        StartScreen.add_widget(startLayout)
        

        startButton=Button(text="Start",pos_hint={"center_x": 0.5, "center_y": 0.5}, font_size=self.fontSize
                )
        startButton.bind(on_press=self.startPLay)
        startLayout.add_widget(startButton)
        self.widgetsFontSize.append(startButton)
        
        
        ostalo_layount = BoxLayout(orientation="horizontal")
        startLayout.add_widget(ostalo_layount)     
        
        histButton=Button(text="Zgodovina", font_size=self.fontSize)
        histButton.bind(on_press=self.startHist)
        ostalo_layount.add_widget(histButton)
        self.widgetsFontSize.append(histButton)

        fontPlusButton=Button(text="Font +", font_size=self.fontSize)
        fontPlusButton.bind(on_press=self.fontPlus)
        ostalo_layount.add_widget(fontPlusButton)
        self.widgetsFontSize.append(fontPlusButton)

        fontMinusButton=Button(text="Font -", font_size=self.fontSize)
        fontMinusButton.bind(on_press=self.fontMinus)
        ostalo_layount.add_widget(fontMinusButton)
        self.widgetsFontSize.append(fontMinusButton)
        
        
        
        ## Main/play screen
        PlayScreen=Screen(name="Play")
        self.sm.add_widget(PlayScreen)        
        main_layout = BoxLayout(orientation="vertical")
        self.navodilo=Label(text="Vpiši rezultat!", font_size=self.fontSize)
        main_layout.add_widget(self.navodilo)
        self.widgetsFontSize.append( self.navodilo)
        
        self.racLabel=Label(text="", font_size=self.fontSize)
        main_layout.add_widget(self.racLabel)
        self.widgetsFontSize.append( self.racLabel)
        
        self.solution = TextInput(
            multiline=False, readonly=True, halign="right", font_size=self.fontSize
        )
        main_layout.add_widget(self.solution)
        self.widgetsFontSize.append( self.solution)
                
        buttons = [
            ["7", "8", "9"],
            ["4", "5", "6"],
            ["1", "2", "3"],
            ["","0", "<-"],
        ]
        for row in buttons:
            h_layout = BoxLayout()
            for label in row:
                button = Button(
                    text=label,
                    pos_hint={"center_x": 0.5, "center_y": 0.5}, font_size=self.fontSize
                )
                self.widgetsFontSize.append(button)
                button.bind(on_press=self.on_button_press)
                h_layout.add_widget(button)
            main_layout.add_widget(h_layout)

        check_button = Button(
            text="Preveri", pos_hint={"center_x": 0.5, "center_y": 0.5}, font_size=self.fontSize
        )
        check_button.bind(on_press=self.on_solution)
        main_layout.add_widget(check_button)
        self.widgetsFontSize.append(check_button)
        
        h_layout = BoxLayout()
        self.uspesnostLabel = Label(text="", font_size=self.fontSizeSmall)
        h_layout.add_widget(self.uspesnostLabel)
        self.widgetsFontSizeSmall.append(self.uspesnostLabel)

        self.odgovorLabel = Label(text="", font_size=self.fontSizeSmall)
        h_layout.add_widget(self.odgovorLabel)
        self.widgetsFontSizeSmall.append(self.odgovorLabel)
        
        main_layout.add_widget(h_layout )
        
        stopButton=Button(text="Meni", font_size=self.fontSize)
        stopButton.bind(on_press=self.startStart)
        main_layout.add_widget(stopButton)       
        self.widgetsFontSize.append(stopButton)
        
        PlayScreen.add_widget(main_layout)
        

        ## Hist screen
        HistScreen=Screen(name="Hist")
        self.sm.add_widget(HistScreen)

        main_layout = BoxLayout(orientation="vertical")
        self.zgodovina=""

        for i in self.histDict:
            self.zgodovina= self.histDict[i] + "\n" + self.zgodovina
        scrollViewHist=ScrollView(size_hint=(None,5), size=(Window.width, Window.height))
        self.ZgodovinaLabel=Label(text=self.zgodovina,size_hint=(None, None), padding=[10,0], font_size=self.fontSizeSmall)
        self.ZgodovinaLabel.bind(texture_size=self.ZgodovinaLabel.setter('size'))
        self.ZgodovinaLabel.bind(size_hint_min_x=self.ZgodovinaLabel.setter('width'))
        scrollViewHist.add_widget(self.ZgodovinaLabel)
        self.widgetsFontSizeSmall.append(self.ZgodovinaLabel)
        main_layout.add_widget(scrollViewHist)
        stopButton=Button(text="Meni", font_size=self.fontSize)
        stopButton.bind(on_press=self.startStart)
        main_layout.add_widget(stopButton)      
        self.widgetsFontSize.append(stopButton)
        HistScreen.add_widget(main_layout)        
        
        
        ## PoMeri screen
        PoMeriSreen=Screen(name="PoMeri")
        self.sm.add_widget(PoMeriSreen)  
        main_layout = BoxLayout(orientation="vertical")
        st1_layount = BoxLayout(orientation="horizontal")
        main_layout.add_widget(st1_layount)
        
        tmpLabel=Label(text = "Št. 1", font_size=self.fontSize)
        st1_layount.add_widget(tmpLabel)
        self.widgetsFontSize.append(tmpLabel)
        self.st1_input=TextInput(multiline=False, font_size=self.fontSize, 
             pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        st1_layount.add_widget(self.st1_input)
        self.widgetsFontSize.append(self.st1_input)
        
        st2_layount = BoxLayout(orientation="horizontal")
        main_layout.add_widget(st2_layount)
        tmpLabel=Label(text = "Št. 2", font_size=self.fontSize)
        st2_layount.add_widget(tmpLabel)
        self.widgetsFontSize.append(tmpLabel)
        self.st2_input=TextInput(text="lahko prazno", multiline=False, font_size=self.fontSize, 
             pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        st2_layount.add_widget(self.st2_input)
        ButtonNastavi=Button(text="Nastavi", font_size=self.fontSize)
        ButtonNastavi.bind(on_press=self.nastaviStPoMeri)
        main_layout.add_widget(ButtonNastavi)
        self.widgetsFontSize.append(ButtonNastavi)
        PoMeriSreen.add_widget(main_layout)
        
        ## Warn screen
        WarnScreen=Screen(name="Warn")
        self.sm.add_widget(WarnScreen)

        main_layout = BoxLayout(orientation="vertical")
        self.WarnLabel=Label(text="", font_size=self.fontSizeSmall)
        main_layout.add_widget(self.WarnLabel)
        stopButton=Button(text="Meni", font_size=self.fontSize)
        stopButton.bind(on_press=self.startStart)
        main_layout.add_widget(stopButton)      
        self.widgetsFontSize.append(stopButton)
        WarnScreen.add_widget(main_layout)            

        return self.sm
    
    def startPLay(self, instance):
        self.nPrav=0
        self.n=0
        
        if self.num10_TB.state=='down':   
            self.maxNum1=10
            self.maxNum2=10
        elif self.num5_TB.state=='down':
            self.maxNum1=5
            self.maxNum2=5
        elif self.numPoMeri_TB.state=='down':
            if not self.settings['poMeri']:
                self.warningFun("Izbran je ?, kar ni dovoljeno. Najprej nastavite vrednost po meri!")
                return 1
            elif len(self.settings['poMeri'])==2:
                self.maxNum1=self.settings['poMeri'][0]
                self.maxNum2=self.settings['poMeri'][1]
            else:
                self.maxNum2=self.maxNum1=self.settings['poMeri'][0]

        if not isinstance(self.maxNum1,int):
            self.num1=self.maxNum1
        else:
            self.num1 = [i for i in range(1,self.maxNum1+1)]
        if not isinstance(self.maxNum2,int):
            self.num2=self.maxNum2
        else:
            self.num2 = [i for i in range(1,self.maxNum2+1)]
        
        if self.opKrat_TB.state=='down':
            self.operators=["*"]
        elif self.opDeljeno_TB.state=='down':
            self.operators=[":"]
        elif self.opOba_TB.state=='down':
            self.operators=["*",":"]
        else:
            self.operators=["*",":"]
           

        
        if self.diffEasy_TB.state=='down':   
            self.diff="Lahko"
        elif self.diffDiff_TB.state=='down':
            self.diff="Težko"
        else:
            self.diff="Srednje"
 
        if isinstance(self.maxNum1,int) and self.maxNum1<=20:
            self.weights1=self.baseWeights[self.diff]
            if len(self.weights1)>self.maxNum1:
                 self.weights1=self.weights1[:self.maxNum1]
            else:
                while len(self.weights1)<self.maxNum1:
                    if self.diff=="Lahko":
                        newWeight=max(self.weights1)
                    elif self.diff=="Srednje":
                        newWeight=max(self.weights1)*1.05
                    else:
                        newWeight=max(self.weights1)*1.1
                    self.weights1.append(newWeight)


        if isinstance(self.maxNum2,int) and self.maxNum2<=20:
            self.weights2=self.baseWeights[self.diff]
            if len(self.weights2)>self.maxNum2:
                 self.weights2=self.weights1[:self.maxNum2]
            else:
                while len(self.weights2)<self.maxNum2:
                    if self.diff=="Lahko":
                        newWeight=max(self.weights2)
                    elif self.diff=="Srednje":
                        newWeight=max(self.weights2)*1.05
                    else:
                        newWeight=max(self.weights2)*1.1
                    self.weights2.append(newWeight)
             
                       
       
        self.sm.current="Play"
        self.startTime=datetime.now()
        self.id=self.startTime.strftime("%Y%m%d%H%M%S")
        if self.maxNum1==self.maxNum2:
            maxNum=self.maxNum1
        else: 
            maxNum=(self.maxNum1,self.maxNum2)
        self.uspesnostLabel.text=f"Težavnost: {'|'.join(self.operators)}-{maxNum}-{self.diff}\nUspešnost:{self.nPrav} / {self.n}"
        self.novRacun()

    def startStart(self, instance):
        if self.id and self.n>0:
            self.zgodovina= self.histDict[self.id] + "\n" + self.zgodovina
            self.ZgodovinaLabel.text=self.zgodovina        
            self.n=0
        self.sm.current="Start"

    def startHist(self, instance):
       self.sm.current="Hist"


    def fontPlus(self, instance):
       self.fontSize=self.fontSize+1
       self.fontSizeSmall=self.fontSizeSmall+0.5
       self.settings["fontSize"]=self.fontSize
       self.settings["fontSizeSmall"]=self.fontSizeSmall
       self.store.put("settings",settings=self.settings)
       for iWidget in self.widgetsFontSize:
           iWidget.font_size=self.fontSize
       for iWidget in self.widgetsFontSizeSmall:
           iWidget.font_size=self.fontSizeSmall


    def fontMinus(self, instance):
       self.fontSize=self.fontSize-1
       self.fontSizeSmall=self.fontSizeSmall-0.5       
       self.settings["fontSize"]=self.fontSize
       self.settings["fontSizeSmall"]=self.fontSizeSmall
       self.store.put("settings",settings=self.settings)
       for iWidget in self.widgetsFontSize:
           iWidget.font_size=self.fontSize
       for iWidget in self.widgetsFontSizeSmall:
           iWidget.font_size=self.fontSizeSmall
           
           
    def startPoMeri(self, instance):
       self.sm.current="PoMeri"       

    def on_button_press(self, instance):
        current = self.solution.text
        button_text = instance.text

        if button_text == "<-":
            self.solution.text = current[:-1]
        else:
                new_text = current + button_text
                self.solution.text = new_text
        
    def on_solution(self, instance):
        text = self.solution.text
        self.n +=1
        if text:
            podanRez = int(self.solution.text)
            if podanRez==self.rez:
                self.odgovorLabel.text="Pravilno!"
                self.nPrav +=1
            else:
                self.odgovorLabel.text=f"Napačno!\n{self.rac}{self.rez}"
            if self.maxNum1==self.maxNum2:
                maxNum=self.maxNum1
            else: 
                maxNum=(self.maxNum1,self.maxNum2)
            self.uspesnostLabel.text=f"Težavnost: {'|'.join(self.operators)}-{maxNum}-{self.diff}\nUspešnost:{self.nPrav} / {self.n}"
            if self.maxNum1==self.maxNum2:
                maxNum=self.maxNum1
            else: 
                maxNum=(self.maxNum1,self.maxNum2)
            self.histDict[self.id]=f"Začetek: {self.startTime.strftime('%d.%m.%Y %H:%M:%S')}\nTežavnost: {'|'.join(self.operators)}-{maxNum}-{self.diff}\nUspešnost: {self.nPrav} / {self.n}\nZdaj: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n"
            self.store.put("data",hist=self.histDict)
            self.novRacun()
    
    def novRacun(self):
        if not isinstance(self.maxNum1,int):
            x = choices(self.num1)[0]
        elif self.maxNum1<=20:
            x = choices(self.num1, self.weights1)[0]
        else:
            x = randint(1,self.maxNum1)
        
        if not isinstance(self.maxNum2,int):
            x = choices(self.num2)[0]
        elif self.maxNum2<=20:
            y = choices(self.num2, self.weights2)[0]
        else:
            y = randint(1,self.maxNum2)
        
        prod=x*y
        if len(self.operators)==2:
            op=self.operators[randint(0,1)]
        else:
            op=self.operators[0]
        if op == "*":
            self.rac = f"{x} x {y} = "
            self.rez=prod
        else:
            self.rac=f"{prod} : {x} = "
            self.rez=y
        self.racLabel.text=self.rac
        self.solution.text = ""
    
    def warningFun(self, text=""):
        self.WarnLabel.text=text
        self.sm.current="Warn"
    
    def setTextToFit(self,widget,fontSize):
        widget.font_size=fontSize
        widget.texture_update()
        while fontSize>10 and widget.texture_size[0]>(2*widget.width):
            fontSize=fontSize-1
            widget.font_size=fontSize
            widget.texture_update()
        return fontSize
        
    def nastaviStPoMeri(self,instance):
        st1=None
        st2=None
        
        def readSt(text):
            st1=None
            try:
                st1tmp=int(text)
                if st1tmp < 2:
                    self.warningFun("Število po meri mora biti vsaj 2!")
                else:
                    st1=st1tmp
            except:
                tmpOk=False
                try:
                    st1tmp=text.split()
                    if len(st1tmp)>1:
                        tmpOk=True
                        for i in range(len(st1tmp)):
                            st1tmp[i]=int(st1tmp[i])
                            if st1tmp[i]<1:
                                self.warningFun("Vsak člen mora biti vsaj 1!")
                                tmpOk=False
                    if tmpOk:
                        st1=st1tmp

                except:
                    tmpOk=False
                
                if not tmpOk:
                    try:
                        st1tmp=text.split(",")
                        if len(st1tmp)>1:
                            tmpOk=True
                            for i in range(len(st1tmp)):
                                st1tmp[i]=int(st1tmp[i])
                                if st1tmp[i]<1:
                                    self.warningFun("Vsak člen mora biti vsaj 1!")
                                    tmpOk=False
                        if tmpOk:
                            st1=st1tmp
                    except:
                        tmpOk=False
            return st1
        
        st1 = readSt(self.st1_input.text)
        st2 = readSt(self.st2_input.text)
        
        if st1 and st2:
            self.settings['poMeri']=(st1,st2)
            self.store.put("settings",settings=self.settings)
            self.numPoMeri_TB.text=f"{self.settings['poMeri']}"
            self.numPoMeri_TB.disabled =False
            self.startStart(None)
        elif st1 or st2:
            if st1:
                self.settings['poMeri']=(st1)
                self.store.put("settings",settings=self.settings)
                self.numPoMeri_TB.text=f"{self.settings['poMeri'][0]}"
                self.numPoMeri_TB.disabled =False
                self.startStart(None)
            else:
                self.settings['poMeri']=(st2)
                self.store.put("settings",settings=self.settings)
                self.warningFun("Število po meri nastavljeno na št. 2!")
                self.numPoMeri_TB.text=f"{self.settings['poMeri'][0]}"                
                self.numPoMeri_TB.disabled =False
                self.startStart(None)
        else:
            self.warningFun("Nepravilen vnos, poskusite ponovno!")
                
MainApp().run()
