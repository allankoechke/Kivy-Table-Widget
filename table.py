'''
Kivy Table
Author: Allan K
version:0.0.1
still under developement

'''
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.core.window import Window

Builder.load_string('''
<Cell>:
    size_hint_y:None
    height:'30dp'
    multiline:False
    readonly:True
<Table>:
    orientation:'vertical'
    GridLayout:
        rows:1
        cols:4
        size_hint_y:None
        height:'40dp'
        Button:
            id:clear
            text:'Clear Table'
            on_press:root.clear_tables()
        Button:
            id:delete_
            text:'Delete Selected'
            on_press:root.delete_item()
            background_color:[1,0,1,1]
            disabled:True
        Button:
            id:refresh
            text:'Refresh Table'
            on_press:root.redraw()
            background_color:[0,1,1,1]
            disabled:True
        Button:
            text:'Close'
            on_press:root.close()
            background_color:[1,0,0,.6]
            
    GridLayout:
        id:grid
<NoCell>:
	id:tb
	size_hint:None,None
	size:40,30
	disabled:True
	group:'a'

    
            

''')

class Cell(TextInput):
    pass

class NoCell(ToggleButton):
	def pressed(self,n):
		print(n)

	def released(self,m):
		print(m)
 
class Table(BoxLayout):
    def __init__(self,**kwargs):
        super(Table,self).__init__(**kwargs)
        
        self.is_selected_=False
        
    def tables(self, data):
        self.data=data
        
        if len(self.data)==0:
            pass
        
        else:
            self.ids.refresh.disabled=False
            self.ids.grid.cols=len(self.data[0])+1
            self.rows=len(self.data)
            
            for i in range(len(self.data)):
                for j in range(len(self.data[0])+1):
                    cell=Cell()
                    no=NoCell()
                    if j==0:
                    	no.text=str(i+1)
                    	no.bind(on_press=self.pressed)
                    	self.ids.grid.add_widget(no)
                    else:
                    	cell.text=str(self.data[i][j-1])
                    	self.ids.grid.add_widget(cell)
                    	
						
            #self.select(0)
    def pressed(self,no):
    	print(no.text)
    	if no.state=='down':
    		print('down')
    		self.ids.delete_.disabled=False
    		self.sel=int(no.text)-1
    		self.select(int(no.text)-1)
    	else:
    		print('Up')
    		self.ids.delete_.disabled=True
    		self.redraw()
    
    
    def select(self,x):
        if len(self.data)==0:
            pass
        
        else:
            self.ids.grid.clear_widgets()
            self.ids.grid.cols=len(self.data[0])+1
            self.rows=len(self.data)
            
            for i in range(len(self.data)):
                for j in range(len(self.data[0])+1):
                    cell=Cell()
                    no=NoCell()
                    if j==0:
                        if x==i:
                            no.state='down'
                        no.text=str(i+1)
                        no.bind(on_press=self.pressed)
                        self.ids.grid.add_widget(no)
                    else:
                        if x==i:
                            cell.background_color=[0,1,0,1]
                            self.is_selected_=True
                            
                        cell.text=str(self.data[i][j-1])
                        self.ids.grid.add_widget(cell)

    def is_selected(self):
        if self.is_selected_==True:
            return True
        else:
            return False
    
    def redraw(self):
        '''does same thing as tables but doesnt take a parameter list'''
        if len(self.data)==0:
            pass
        
        else:
            self.ids.delete_.disabled=True
            self.is_selected_=False
            self.ids.grid.clear_widgets()
            self.ids.grid.cols=len(self.data[0])+1
            self.rows=len(self.data)
            
            for i in range(len(self.data)):
                for j in range(len(self.data[0])+1):
                    cell=Cell()
                    no=NoCell()
                    if j==0:
                    	no.text=str(i+1)
                    	no.bind(on_press=self.pressed)
                    	self.ids.grid.add_widget(no)
                    else:
                    	cell.text=str(self.data[i][j-1])
                    	self.ids.grid.add_widget(cell)
    
    def clear_tables(self):
        self.ids.grid.clear_widgets()
        self.ids.refresh.disabled=True
        del self.data
        pop=Popup(title='Clear...',content=Label(text="All tables cleared\n Add new tables")\
                      ,size_hint=(None,None),size=(300,200))
        pop.open()

    def get_rows(self):
        return self.rows
        
    def get_cols(self):
        if len(self.data)>0:
            return len(self.data[0])
        else:
            return 0
            
    def delete_item(self):
        x=self.is_selected()
        if x==True:
            row=self.sel
            del self.data[row]
            self.redraw()
            pop=Popup(title='Delete...',content=Label(text="Selected row deleted...")\
                      ,size_hint=(None,None),size=(300,200))
            pop.open()
        else:
            pop=Popup(title='Nothing Selected...',content=Label(text="Found '0' selected rows")\
                      ,size_hint=(None,None),size=(300,200))
            pop.open()
        
    
        
    def add_item(self,a):
        '''Functionality to add a row'''
        '''TODO...'''
        #self.data.append(a)
        #return self.item
        pass
        
    def close(self,*args):
        App.get_running_app().stop()
        
        
        
class MyApp(App):
    def build(self):
        Window.clearcolor=(1,1,1,1)
        self.title='kivy Table'
        
        '''Sample Data'''
        x=[]
        for i in range(20):
            y=[]
            for j in range(6):
                t='text'+str(j+1)
                y.append(t)
            x.append(y)
            del y

        '''Populate the table'''
        tbl=Table()
        tbl.tables(x)
        return tbl
        
if __name__=='__main__':
    MyApp().run()
