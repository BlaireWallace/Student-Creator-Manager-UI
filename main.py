# Create a UI of listing all students 
# Create a new student UI

import os
import csv

import tkinter as tk
import ttkbootstrap as ttk

themetype = str.lower("Lumen")

student_csv = "Student_Data.csv"

inputNumTxt = "Please input a number"
inputStrTxt = "Please input text"

directory = "/Users/Wallace/OneDrive/Desktop/Development/Visual Studio Code/Student Creator/" + student_csv 

# check if CSV exist
if not os.path.exists(directory):
    # create csv file
    with open(directory,'w',newline='') as csv_file:
        placeholder =  [["Name","Age","Gender","Ethnicity","Id"]]
        # Create a CSV writer object
        csv_writer = csv.writer(csv_file)

        csv_writer.writerows(placeholder)
        print("Created Student Data CSV")

class UI:
    def __init__(self):
        self.Menu, self.studentCount = self.mainMenu()

        self.studentCountVar = tk.StringVar()
        self.studentCount.configure(textvariable = self.studentCountVar)

        self.CreateStudentUI = self.createStudent()
        self.StudentListUI = self.listStudentsUI()

        # load current students
        self.loadStudents()
        self.updateStudentCount()

        self.Menu.mainloop()

    def loadStudents(self): # load students that are in the csv currently
        with open(directory,'r') as file:
            reader = csv.reader(file)
            num = 0
            for row in reader:
                for i in range(5):
                    desclabel = ttk.Label(self.StudentListUI["ItemFrame"],text=row[i],font=("Arial",num == 0 and 20 or 10))
                    desclabel.grid(row=num,column=i,padx=35)
                num += 1

    def updateStudentCount(self):
        with open(directory,'r') as file:
            reader = csv.reader(file)
            num = 0
            for row in reader:
                num += 1
            self.studentCountVar.set(f"Student Count: {num - 1}")

    def mainMenu(self):
        screen = ttk.Window(themename=themetype)
        screen.geometry("500x300")
        screen.resizable(False,False)
        screen.title("Student Manager")

        title = ttk.Label(screen,text="Texas Tech University Student Manager",font=('Arial',15))
        title.pack(expand=False)

        studentCount = ttk.Label(screen,text="Student Count: N/A",font=('Arial',10))
        studentCount.pack(pady=10)

        buttonFrame = ttk.Frame(screen)
        buttonFrame.pack(fill='both',expand=True)

        #button style
        #button_style = ttk.Style()
        #button_style.configure('Button.Style',font=('Arial',30))

        createStudentButton = ttk.Button(buttonFrame,text='New Student',command=self.openCreateStudent)
        createStudentButton.pack(side='left',expand=True, fill='both')

        listStudentButton = ttk.Button(buttonFrame,text='List Students',command=self.openListStudents)
        listStudentButton.pack(side='left',expand=True, fill='both')
        return screen, studentCount
    
    def End(self):
        self.Menu.destroy()

    def createStudent(self):
        def createUI(name,widget,value):
            def on_entry_clicked(event):
                if registerStudentInfo[name] != None:
                    if registerStudentInfo[name]['variable'].get() == inputNumTxt or registerStudentInfo[name]['variable'].get() == inputStrTxt:
                        widgetValue.delete(0, tk.END)  # Clear the Entry widget
                        #widgetValue.config(fg='black')  # Change text color to black
            
            def on_entry_leave(event):
                if registerStudentInfo[name] != None and registerStudentInfo[name]['variable'].get() == "":
                    registerStudentInfo[name]['variable'].set("Enter text here")  # Restore the placeholder text
                    #registerStudentInfo[name]['variable'].config(fg='gray')  # Change text color to gray

            frame = ttk.Frame(screen)
            frame.pack(fill="x",expand=True)

            text = ttk.Label(frame,text=name,font=('Arial',10))
            text.pack(side='left',expand=True)

            widgetValue = widget(frame)
            widgetValue.pack(side='left',expand=True)
            
            if widget == ttk.Combobox and value != None:
                widgetValue.configure(values=value)
            
            if widget == ttk.Entry:
                widgetValue.bind("<FocusIn>",on_entry_clicked)
                #widgetValue.bind("<FocusOut>",on_entry_leave)

            if registerStudentInfo[name] != None:
                widgetValue.configure(textvariable=registerStudentInfo[name]['variable'])
                registerStudentInfo[name]['label'] = widgetValue

            return frame
        
        registerStudentInfo = {
            "Name": {'variable': tk.StringVar()},
            "Age": {'variable': tk.StringVar()},
            "Gender": {'variable': tk.StringVar()},
            "Ethnicity": {'variable': tk.StringVar()}}
        
        screen = tk.Toplevel(self.Menu)
        screen.geometry("250x300")
        screen.resizable(False,False)
        screen.title("Register Student")

        title = ttk.Label(screen,text="Register Student",font=('Airal',20))
        title.pack()

        createUI("Name",ttk.Entry,None)
        createUI("Age",ttk.Entry,None)
        createUI("Gender",ttk.Combobox,['Male','Female','Other'])
        createUI("Ethnicity",ttk.Combobox,['African Ameraican','White','Hispanic','Other'])

        selectionbutton = ttk.Frame(screen)
        selectionbutton.pack(expand=True,fill='x')

        closeButton = ttk.Button(selectionbutton,text="Close",command=self.openMenu)
        closeButton.pack(expand=True,fill='both',side='left')

        registerButton = ttk.Button(selectionbutton,text="Register",command=self.registerStudent)
        registerButton.pack(expand=True,fill='both',side='left')

        screen.protocol('WM_DELETE_WINDOW',self.End)

        screen.withdraw() # hide frame
        return {"Screen": screen,"Description": registerStudentInfo}
    
    def listStudentsUI(self):

        def on_canvas_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        screen = tk.Toplevel(self.Menu)
        screen.geometry('800x600')
        screen.resizable(False,False)
        screen.title("List of Students")

        title = ttk.Label(screen,text="Texas Tech's Students",font=("Arial",20))
        title.pack()

        closeButton = ttk.Button(screen,text="Close",command=self.openMenu)
        closeButton.pack()

        # create scroll bar
        scrollbar = ttk.Scrollbar(screen,orient='vertical')
        scrollbar.pack(side='right',fill='y')
        # canvas
        canvas = tk.Canvas(screen,yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=canvas.yview)

        # create a item frame for the items to be put on 
        items_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=items_frame, anchor=tk.NW)

        canvas.yview_moveto(0)
        canvas.bind("<Configure>", on_canvas_configure)
        screen.withdraw() # hide frame

        screen.protocol('WM_DELETE_WINDOW',self.End)

        return {"Screen":screen, "ItemFrame":items_frame}
    
    def addStudentToPage(self,info):
        order_ = ["Name","Age","Gender","Ethnicity","Id"]
        for name in info:
            index = None
            for i in range(len(order_)): # get the apporiate order 
                if order_[i] == name:
                    index = i
            desclabel = ttk.Label(self.StudentListUI["ItemFrame"],text=info[name],font=("Arial",10))
            desclabel.grid(row=info["Id"],column=index,padx=35)
        self.updateStudentCount()
    
    def registerStudent(self):
        errorArouse = False
        studentdesc = {}
        for name in self.CreateStudentUI["Description"]:
            try:
                variable = self.CreateStudentUI["Description"][name]['variable'].get()
                if name == "Age" and not int(variable):
                    pass
                elif variable == "" or variable == inputStrTxt or variable == inputNumTxt: 
                    errorArouse = True
                    self.CreateStudentUI["Description"][name]['variable'].set(name == "Age" and inputNumTxt or inputStrTxt)
                    pass
                else:
                    studentdesc[name] = variable
                
            except:
                errorArouse = True
                self.CreateStudentUI["Description"][name]['variable'].set(name == "Age" and inputNumTxt or inputStrTxt)

        if errorArouse:
            return
               
        student = newStudent(studentdesc)
        self.addStudentToPage(student.StudentInfo)
        self.openListStudents()

    def openListStudents(self):
        self.StudentListUI["Screen"].deiconify()
        self.CreateStudentUI["Screen"].withdraw()
        self.Menu.withdraw()
    
    def openMenu(self):
         self.Menu.deiconify()
         self.CreateStudentUI["Screen"].withdraw()
         self.StudentListUI["Screen"].withdraw()
    def openCreateStudent(self):
        self.Menu.withdraw() # hide frame
        self.StudentListUI["Screen"].withdraw()
        # reset 
        for name in self.CreateStudentUI["Description"]:
            variable = self.CreateStudentUI["Description"][name]['variable']
            self.CreateStudentUI["Description"][name]['variable'].set(variable==tk.IntVar and 0 or "")

        self.CreateStudentUI["Screen"].deiconify() # show the frame

# new student logic
class newStudent:
    def __init__(self,info: dict):
        self.StudentInfo = {
            "Name": info["Name"],
            "Age": info["Age"] or 'N/A',
            "Gender": info["Gender"] or 'N/A',
            "Ethnicity": info["Ethnicity"] or 'N/A',
            "Id": self.generateId() # we will have a function for this
        }

        # put info in a CSV
        data = [
            [self.StudentInfo["Name"],self.StudentInfo["Age"],self.StudentInfo["Gender"],self.StudentInfo["Ethnicity"],self.StudentInfo["Id"]]
                ]
        # Write the data to the CSV file
        with open(directory, 'a', newline='') as csv_file:
            # Create a CSV writer object
            csv_writer = csv.writer(csv_file)

            data = [[self.StudentInfo["Name"],self.StudentInfo["Age"],self.StudentInfo["Gender"],self.StudentInfo["Ethnicity"],self.StudentInfo["Id"]]]
            # add data to CSV
            csv_writer.writerows(data)
        
        #create UI
    
    def generateId(self):
        num = 0
        if os.path.exists(directory):
            with open(directory,'r') as file:
                csv_reader = csv.reader(file)
            
               # Iterate through each row in the CSV file
                for row in csv_reader:
                    num += 1
        else:
            num = 1
        return num

newUI = UI()
print("Operation Closed")

#s = newStudent({"Name":"Billy A Washington","Age":23,"Gender":"Male","Ethnicity":"White"})



