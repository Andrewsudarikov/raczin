import csv
import gi
import random
gi.require_version('Gtk', '3.0')
gi.require_version('Granite', '1.0')
from gi.repository import Gtk, Gdk, Gio, Granite, Pango

# Reading the number of lines in the CSV table
with open('raczin_data.txt', 'r') as f:
    mycsv = csv.reader(f)
    LimitMargin = len(list(mycsv)) + 1 #that's a correction value for the header

# Randomizing the task number shown on startup
TaskNum = random.randint(3,int(LimitMargin))
Task_Number_Text = "Task No. "+ str(TaskNum)

# Randomizing the matrix for number generator used in easy mode
EasyMode_Rand = random.randint(1,4)
CorrectAnswer = 0 

# Setting up the difficulty level
global Difficulty_Level
with open('raczin_data.txt', 'r') as f:
    mycsv = csv.reader(f)
    mycsv = list(mycsv)
    Difficulty_Level = int(mycsv[0][6])

# Placeholders in case you need them
TaskData_Placeholder_Text = "Here will be the description for the task number "+ str(TaskNum) +"."
TaskQuestion_Placeholder_Text = "Here will be the question for the task number "+ str(TaskNum) +"."
lblHint_Placeholder_Text = "Here will be a hint for the task number "

class OperationsWindow(Gtk.Window):

    def __init__(self):
        global TaskNum, EasyMode_Rand, CorrectAnswer
        Gtk.Window.__init__(self, title="Raczin")

#       Main form properties
        self.set_default_size(300,350)
        self.set_border_width(12)
        self.set_modal(True)
        self.set_resizable(False)
        self.modify_bg(Gtk.StateType(0), Gdk.color_parse('#fdf6e3'))

#       Setting up HeaderBar
        self.HeaderBar = Gtk.HeaderBar()
        self.HeaderBar.set_show_close_button(True)
        self.HeaderBar.set_title(self.get_title())
        self.set_titlebar(self.HeaderBar)
        self.HeaderBar.show()

#       Setting up Navigation bar container
        self.NavBar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.NavBar.show()

#       Setting up NavBar controls
        self.btnPrev = Gtk.Button()
        icon = Gio.ThemedIcon(name="go-previous-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        image.show()
        self.btnPrev.add(image)
        self.btnPrev.set_size_request(35, -1)
        self.btnPrev.connect("clicked", self.task_previous_clicked)
        self.btnPrev.show()

        self.fldTask = Gtk.Entry()
        self.fldTask.set_max_length(3)
        self.fldTask.set_width_chars(4)
        self.fldTask.set_alignment(xalign=0.5)
        self.fldTask.set_text(str(TaskNum))
        self.fldTask.connect("activate", self.fldTask_ManualInput)
        self.fldTask.show()

        self.btnNext = Gtk.Button()
        icon = Gio.ThemedIcon(name="go-next-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        image.show()
        self.btnNext.add(image)
        self.btnNext.set_size_request(35, -1)
        self.btnNext.connect("clicked", self.task_next_clicked)
        self.btnNext.show()

#       Placing NavBar onto Header Bar
        self.NavBar.add(self.btnPrev)
        self.NavBar.add(self.fldTask)
        self.NavBar.add(self.btnNext)
        self.HeaderBar.pack_start(self.NavBar)

#       Placing a random task button
        btnRand = Gtk.Button()
        icon = Gio.ThemedIcon(name="mail-send-receive-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        image.show()
        btnRand.add(image)
        btnRand.set_size_request(20, -1)
        btnRand.connect("clicked", self.task_randomizer_clicked)
        btnRand.show()
        self.HeaderBar.pack_start(btnRand)

#       Placing a settings button
        btnSettings=Gtk.Button()
        icon = Gio.ThemedIcon(name="open-menu-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        image.show()
        btnSettings.add(image)
        btnSettings.set_size_request(30, -1)
        btnSettings.connect("clicked", self.settings_clicked)
        btnSettings.show()
        self.HeaderBar.pack_end(btnSettings)

#       Placing a dark mode switch
        modeSwitch = Granite.ModeSwitch.from_icon_name ("display-brightness-symbolic", "weather-clear-night-symbolic")
        modeSwitch.set_valign(Gtk.Align.CENTER)
        self.HeaderBar.pack_end(modeSwitch)

#       Setting up Settings menu popover window
        self.Settings_Popover = Gtk.Popover()
        self.Settings_Popover.set_position(Gtk.PositionType.BOTTOM)
        self.Settings_Popover.set_size_request(20,40)
        self.Settings_Popover.set_border_width(5)
        self.Settings_Container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.Settings_Popover.add(self.Settings_Container)

#       Setting up difficulty level container
        self.Settings_DifficultyBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(self.Settings_DifficultyBox.get_style_context(), "linked")

#       Setting up difficulty level selector buttons
        self.btnHarder = Gtk.Button()
        icon = Gio.ThemedIcon(name="go-up-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        self.btnHarder.add(image)
        self.btnHarder.set_size_request(35, -1)
        self.Settings_DifficultyBox.pack_start(self.btnHarder, True, True, 0)
        self.btnHarder.connect("clicked", self.btnHarder_clicked)

#       Setting up difficulty level indicator
        self.lblDifficulty_Setting = Gtk.Button()
        self.lblDifficulty_Setting.set_sensitive(False)
        self.lblDifficulty_Setting.set_size_request(50, 25)
        if Difficulty_Level == 1:
            self.lblDifficulty_Setting.set_label("EASY")
        if Difficulty_Level == 2:
            self.lblDifficulty_Setting.set_label("NORM")
        if Difficulty_Level == 3:
            self.lblDifficulty_Setting.set_label("HARD")
        self.lblDifficulty_Setting
        self.Settings_DifficultyBox.pack_start(self.lblDifficulty_Setting, False, False, 0)
        self.btnEasier = Gtk.Button()
        icon = Gio.ThemedIcon(name="go-down-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        self.btnEasier.add(image)
        self.btnEasier.set_size_request(35, -1)
        self.Settings_DifficultyBox.pack_start(self.btnEasier, True, True, 0)
        self.btnEasier.connect("clicked", self.btnEasier_clicked)

#       Setting up main window container
        self.MainContainer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.MainContainer)
        self.MainContainer.show()

# === Setting up Task dispays ===

#       Task number label:
        self.lblTaskNumber = Gtk.Label()
        self.lblTaskNumber.set_use_markup(True)
        self.lblTaskNumber.set_alignment(0,0.5)
        self.lblTaskNumber.modify_fg(Gtk.StateType(0), Gdk.color_parse('#7a0000'))
        self.lblTaskNumber.modify_font(Pango.FontDescription("Garamond 18"))
        self.lblTaskNumber.set_text("Task No. "+ str(TaskNum))
        self.MainContainer.pack_start(self.lblTaskNumber, True, True, 0)
        self.lblTaskNumber.show()

#       Task description box array: 
        self.TaskData = Gtk.Label()
        self.TaskData1 = Gtk.Label()
        self.TaskData2 = Gtk.Label()
        self.TaskData.set_alignment(0,0)
        self.TaskData.modify_fg(Gtk.StateType(0), Gdk.color_parse('#3d211b'))
        self.TaskData.modify_font(Pango.FontDescription("Garamond 12"))
        self.TaskData1.set_alignment(0,0)
        self.TaskData1.modify_fg(Gtk.StateType(0), Gdk.color_parse('#3d211b'))
        self.TaskData1.modify_font(Pango.FontDescription("Garamond 12"))
        self.TaskData2.set_alignment(0,0)
        self.TaskData2.modify_fg(Gtk.StateType(0), Gdk.color_parse('#3d211b'))
        self.TaskData2.modify_font(Pango.FontDescription("Garamond 12"))
        with open('raczin_data.txt', 'r') as f:
            mycsv = csv.reader(f)
            mycsv = list(mycsv)
            TaskData_Text = mycsv[TaskNum][1]
            TaskData1_Text = mycsv[TaskNum][2]
            TaskData2_Text = mycsv[TaskNum][3]
        self.TaskData.set_text(TaskData_Text)
        self.TaskData1.set_text(TaskData1_Text)
        self.TaskData2.set_text(TaskData2_Text)
        self.MainContainer.pack_start(self.TaskData, False, True, 3)
        self.MainContainer.pack_start(self.TaskData1, False, True, 3)
        self.MainContainer.pack_start(self.TaskData2, False, True, 3)
        self.TaskData.show()
        self.TaskData1.show()
        self.TaskData2.show()

#       Task question box: 
        self.TaskQuestion = Gtk.Label()
        self.TaskQuestion.modify_fg(Gtk.StateType(0), Gdk.color_parse('#3d211b'))
        self.TaskQuestion.modify_font(Pango.FontDescription("Garamond italic 12"))
        self.TaskQuestion.set_line_wrap(True)
        with open('raczin_data.txt', 'r') as f:
            mycsv = csv.reader(f)
            mycsv = list(mycsv)
            TaskQuestion_Text = mycsv[TaskNum][4]
        self.TaskQuestion.set_text(TaskQuestion_Text)
        self.MainContainer.pack_start(self.TaskQuestion, True, True, 2)
        self.TaskQuestion.show()

#       Setting up answer container: 
        self.AnswerBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(self.AnswerBox.get_style_context(), "linked")
        self.AnswerBox.show()

#       Setting up entry box: 
        self.AnswerEntry = Gtk.Entry()
        self.AnswerEntry.set_size_request(-1, 34)
        self.AnswerEntry.set_placeholder_text("Type your answer here")
        self.AnswerEntry.connect("activate", self.AnswerEntry_ManualInput)
        self.AnswerEntry.set_input_purpose(Gtk.InputPurpose.NUMBER)
        self.AnswerBox.pack_start(self.AnswerEntry, True, True, 0)
        self.AnswerEntry.show()

#       Setting up hint button
        self.btnHint = Gtk.Button()
        self.btnHint.modify_bg(Gtk.StateType(0), Gdk.color_parse('#fbefce'))
        self.btnHint.modify_fg(Gtk.StateType(0), Gdk.color_parse('#7a0000'))
        icon = Gio.ThemedIcon(name="help-contents-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        image.show()
        self.btnHint.add(image)
        self.btnHint.set_size_request(50, -1)
        self.btnHint.connect("clicked", self.btnHint_clicked)
        self.btnHint.show()

#       Setting up answer button
        self.btnAnswer = Gtk.Button()
        self.btnAnswer.modify_bg(Gtk.StateType(0), Gdk.color_parse('#fbefce'))
        self.btnAnswer.modify_fg(Gtk.StateType(0), Gdk.color_parse('#7a0000'))
        icon = Gio.ThemedIcon(name="object-select-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        image.show()
        self.btnAnswer.add(image)
        self.btnAnswer.set_size_request(50, -1)
        self.btnAnswer.connect("clicked", self.btnAnswer_clicked)
        self.btnAnswer.show()

#       Setting up Next Task button
        self.btnNextTask = Gtk.Button()
        self.btnNextTask.modify_bg(Gtk.StateType(0), Gdk.color_parse('#d1ff82'))
        icon = Gio.ThemedIcon(name="go-jump-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        image.show()
        self.btnNextTask.add(image)
        self.btnNextTask.set_size_request(50, -1)
        self.btnNextTask.connect("clicked", self.btnNextTask_clicked)
        self.AnswerBox.pack_end(self.btnNextTask, False, True, 0)

#       Describing answer controls layout
        self.AnswerBox.pack_end(self.btnAnswer, False, True, 0)
        self.AnswerBox.pack_end(self.btnHint, False, True, 0)
        self.MainContainer.pack_start(self.AnswerBox, False, True, 0)

#       Setting up hint buttons
        self.HelperBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(self.HelperBox.get_style_context(), "linked")
        self.btn1 = Gtk.Button()
        self.btn1.modify_bg(Gtk.StateType(0), Gdk.color_parse('#fbefce'))
        self.btn1.modify_fg(Gtk.StateType(0), Gdk.color_parse('#7a0000'))
        self.btn1.set_size_request(-1, 34)
        self.btn1.connect("clicked", self.btn1_clicked)
        self.btn1.show()
        self.HelperBox.pack_end(self.btn1, True, True, 0)
        self.btn2 = Gtk.Button()
        self.btn2.modify_bg(Gtk.StateType(0), Gdk.color_parse('#fbefce'))
        self.btn2.modify_fg(Gtk.StateType(0), Gdk.color_parse('#7a0000'))
        self.btn2.set_size_request(-1, 34)
        self.btn2.connect("clicked", self.btn2_clicked)
        self.btn2.show()
        self.HelperBox.pack_end(self.btn2, True, True, 0)
        self.btn3 = Gtk.Button()
        self.btn3.modify_bg(Gtk.StateType(0), Gdk.color_parse('#fbefce'))
        self.btn3.modify_fg(Gtk.StateType(0), Gdk.color_parse('#7a0000'))
        self.btn3.set_size_request(-1, 34)
        self.btn3.connect("clicked", self.btn3_clicked)
        self.btn3.show()
        self.HelperBox.pack_end(self.btn3, True, True, 0)
        self.btn4 = Gtk.Button()
        self.btn4.modify_bg(Gtk.StateType(0), Gdk.color_parse('#fbefce'))
        self.btn4.modify_fg(Gtk.StateType(0), Gdk.color_parse('#7a0000'))
        self.btn4.set_size_request(-1, 34)
        self.btn4.connect("clicked", self.btn4_clicked)
        self.btn4.show()
        self.HelperBox.pack_end(self.btn4, True, True, 0)
        self.MainContainer.pack_start(self.HelperBox, False, True, 0)

#       Setting up numbers on hint buttons
        with open('raczin_data.txt', 'r') as f:
            mycsv = csv.reader(f)
            mycsv = list(mycsv)
            AnswerData = int(mycsv[TaskNum][5])
        if EasyMode_Rand == 1:
            TestVar1 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
            TestVar2 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
            TestVar3 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
            TestVar4 = int(AnswerData)
            CorrectAnswer = 4
        if EasyMode_Rand == 2:
            TestVar1 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
            TestVar2 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
            TestVar3 = int(AnswerData)
            TestVar4 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
            CorrectAnswer = 3
        if EasyMode_Rand == 3:
            TestVar1 = int(AnswerData)
            TestVar2 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
            TestVar3 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
            TestVar4 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
            CorrectAnswer = 1
        if EasyMode_Rand == 4:
            TestVar1 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
            TestVar2 = int(AnswerData)
            TestVar3 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
            TestVar4 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
            CorrectAnswer = 2

#       Applying labels to hint buttons
        self.btn1.set_label(str(TestVar1))
        self.btn2.set_label(str(TestVar2))
        self.btn3.set_label(str(TestVar3))
        self.btn4.set_label(str(TestVar4))

#       Setting up a hint popover bubble
        self.Hint_Popover = Gtk.Popover()
        self.Hint_Popover.set_position(Gtk.PositionType.TOP)
        self.Hint_Popover.set_size_request(20,40)
        self.Hint_Popover.set_border_width(5)
        self.lblHint = Gtk.Label()
        self.Hint_Popover.add(self.lblHint)

# === OPERATIONS FOR HEADERBAR BUTTONS AND FIELDS ===

#   Operating btnRand function
    def task_randomizer_clicked(self,btnRand):
        global CorrectAnswer
        TaskNum = random.randint(1,14)
        self.AnswerEntry.set_text("")
        self.btnAnswer.modify_bg(Gtk.StateType(0), Gdk.color_parse('#fbefce'))
        self.fldTask.set_text(str(TaskNum))
        self.lblTaskNumber.set_text("Task No. "+ str(TaskNum))
        with open('raczin_data.txt', 'r') as f:
            mycsv = csv.reader(f)
            mycsv = list(mycsv)
            TaskData_Text = mycsv[TaskNum][1]
            TaskData1_Text = mycsv[TaskNum][2]
            TaskData2_Text = mycsv[TaskNum][3]
            TaskQuestion_Text = mycsv[TaskNum][4]
            AnswerData = mycsv[TaskNum][5]
            lblHint_Text = mycsv[TaskNum][6]
        self.TaskData.set_text(TaskData_Text)
        self.TaskData1.set_text(TaskData1_Text)
        self.TaskData2.set_text(TaskData2_Text)
        self.TaskQuestion.set_text(TaskQuestion_Text)
        self.lblHint.set_text(lblHint_Text)

#       Re-enabling hint buttons
        self.btn1.modify_bg(Gtk.StateType(0), Gdk.color_parse('#fbefce'))
        self.btn1.set_sensitive(True)
        self.btn2.modify_bg(Gtk.StateType(0), Gdk.color_parse('#fbefce'))
        self.btn2.set_sensitive(True)
        self.btn3.modify_bg(Gtk.StateType(0), Gdk.color_parse('#fbefce'))
        self.btn3.set_sensitive(True)
        self.btn4.modify_bg(Gtk.StateType(0), Gdk.color_parse('#fbefce'))
        self.btn4.set_sensitive(True)

#       Ranodmizing numbers on hint buttons
        EasyMode_Rand = random.randint(1,4)
        with open('raczin_data.txt', 'r') as f:
            mycsv = csv.reader(f)
            mycsv = list(mycsv)
            AnswerData = int(mycsv[TaskNum][5])
        if EasyMode_Rand == 1:
            TestVar1 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
            TestVar2 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
            TestVar3 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
            TestVar4 = int(AnswerData)
            CorrectAnswer = 4
        if EasyMode_Rand == 2:
            TestVar1 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
            TestVar2 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
            TestVar3 = int(AnswerData)
            TestVar4 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
            CorrectAnswer = 3
        if EasyMode_Rand == 3:
            TestVar1 = int(AnswerData)
            TestVar2 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
            TestVar3 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
            TestVar4 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
            CorrectAnswer = 1
        if EasyMode_Rand == 4:
            TestVar1 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
            TestVar2 = int(AnswerData)
            TestVar3 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
            TestVar4 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
            CorrectAnswer = 2

#       Applying labels to hint buttons
        self.btn1.set_label(str(TestVar1))
        self.btn2.set_label(str(TestVar2))
        self.btn3.set_label(str(TestVar3))
        self.btn4.set_label(str(TestVar4))

#   Operating self.btnPrev function
    def task_previous_clicked(self,btnPrev):

#       Reading main operational variables
        global CorrectAnswer
        calcString = self.fldTask.get_text()
        TaskNum = int(calcString)
        with open('raczin_data.txt', 'r') as f:
            mycsv = csv.reader(f)
            LimitMargin = len(list(mycsv)) - 1

#       Declaring main operational condition
        if TaskNum > 1:

#           Switching Prev and Next buttons on and off if needed
            if TaskNum == LimitMargin:
                self.btnNext.set_sensitive(True)
            if TaskNum == 2: 
                self.btnPrev.set_sensitive(False)

#           Working with CSV table filling the fields on the form
            calcString = self.fldTask.get_text()
            TaskNum = int(calcString) - 1
            self.fldTask.set_text(str(TaskNum))
            self.lblTaskNumber.set_text("Task No. "+ str(TaskNum))
            with open('raczin_data.txt', 'r') as f:
                mycsv = csv.reader(f)
                mycsv = list(mycsv)
                TaskData_Text = mycsv[TaskNum][1]
                TaskData1_Text = mycsv[TaskNum][2]
                TaskData2_Text = mycsv[TaskNum][3]
                TaskQuestion_Text = mycsv[TaskNum][4]
                AnswerData = mycsv[TaskNum][5]
                lblHint_Text = mycsv[TaskNum][6]
            self.TaskData.set_text(TaskData_Text)
            self.TaskData1.set_text(TaskData1_Text)
            self.TaskData2.set_text(TaskData2_Text)
            self.TaskQuestion.set_text(TaskQuestion_Text)
            self.lblHint.set_text(lblHint_Text)

#           Re-enabling hint buttons
            self.btn1.modify_bg(Gtk.StateType(0), Gdk.color_parse('#fbefce'))
            self.btn1.set_sensitive(True)
            self.btn2.modify_bg(Gtk.StateType(0), Gdk.color_parse('#fbefce'))
            self.btn2.set_sensitive(True)
            self.btn3.modify_bg(Gtk.StateType(0), Gdk.color_parse('#fbefce'))
            self.btn3.set_sensitive(True)
            self.btn4.modify_bg(Gtk.StateType(0), Gdk.color_parse('#fbefce'))
            self.btn4.set_sensitive(True)

#           Ranodmizing numbers on hint buttons
            EasyMode_Rand = random.randint(1,4)
            with open('raczin_data.txt', 'r') as f:
                mycsv = csv.reader(f)
                mycsv = list(mycsv)
                AnswerData = int(mycsv[TaskNum][5])
            if EasyMode_Rand == 1:
                TestVar1 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
                TestVar2 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
                TestVar3 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
                TestVar4 = int(AnswerData)
                CorrectAnswer = 4
            if EasyMode_Rand == 2:
                TestVar1 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
                TestVar2 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
                TestVar3 = int(AnswerData)
                TestVar4 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
                CorrectAnswer = 3
            if EasyMode_Rand == 3:
                TestVar1 = int(AnswerData)
                TestVar2 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
                TestVar3 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
                TestVar4 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
                CorrectAnswer = 1
            if EasyMode_Rand == 4:
                TestVar1 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
                TestVar2 = int(AnswerData)
                TestVar3 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
                TestVar4 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
                CorrectAnswer = 2

#           Applying labels to hint buttons
            self.btn1.set_label(str(TestVar1))
            self.btn2.set_label(str(TestVar2))
            self.btn3.set_label(str(TestVar3))
            self.btn4.set_label(str(TestVar4))

#   OPERATING self.btnNext FUNCTIONS
    def task_next_clicked(self,btnNext):

#       Reading main operational variables
        global CorrectAnswer
        calcString = self.fldTask.get_text()
        TaskNum = int(calcString)
        with open('raczin_data.txt', 'r') as f:
            mycsv = csv.reader(f)
            LimitMargin = len(list(mycsv)) - 1

#       Declaring main operational condition
        if TaskNum < LimitMargin:

#           Switching Prev and Next buttons on and off if needed
            if TaskNum == LimitMargin - 1:
                self.btnNext.set_sensitive(False)
            if TaskNum == 1: 
                self.btnPrev.set_sensitive(True)

#           Working with CSV table filling the fields on the form
            calcString = self.fldTask.get_text()
            TaskNum = int(calcString) + 1
            self.fldTask.set_text(str(TaskNum))
            self.lblTaskNumber.set_text("Task No. "+ str(TaskNum))
            with open('raczin_data.txt', 'r') as f:
                mycsv = csv.reader(f)
                mycsv = list(mycsv)
                TaskData_Text = mycsv[TaskNum][1]
                TaskData1_Text = mycsv[TaskNum][2]
                TaskData2_Text = mycsv[TaskNum][3]
                TaskQuestion_Text = mycsv[TaskNum][4]
                AnswerData = mycsv[TaskNum][5]
                lblHint_Text = mycsv[TaskNum][6]
            self.TaskData.set_text(TaskData_Text)
            self.TaskData1.set_text(TaskData1_Text)
            self.TaskData2.set_text(TaskData2_Text)
            self.TaskQuestion.set_text(TaskQuestion_Text)
            self.lblHint.set_text(lblHint_Text)

#           Re-enabling hint buttons
            self.btn1.modify_bg(Gtk.StateType(0), Gdk.color_parse('#fbefce'))
            self.btn1.set_sensitive(True)
            self.btn2.modify_bg(Gtk.StateType(0), Gdk.color_parse('#fbefce'))
            self.btn2.set_sensitive(True)
            self.btn3.modify_bg(Gtk.StateType(0), Gdk.color_parse('#fbefce'))
            self.btn3.set_sensitive(True)
            self.btn4.modify_bg(Gtk.StateType(0), Gdk.color_parse('#fbefce'))
            self.btn4.set_sensitive(True)

#           Ranodmizing numbers on hint buttons
            EasyMode_Rand = random.randint(1,4)
            AnswerData = int(mycsv[TaskNum][5])
            if EasyMode_Rand == 1:
                TestVar1 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
                TestVar2 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
                TestVar3 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
                TestVar4 = int(AnswerData)
                CorrectAnswer = 4
            if EasyMode_Rand == 2:
                TestVar1 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
                TestVar2 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
                TestVar3 = int(AnswerData)
                TestVar4 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
                CorrectAnswer = 3
            if EasyMode_Rand == 3:
                TestVar1 = int(AnswerData)
                TestVar2 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
                TestVar3 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
                TestVar4 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
                CorrectAnswer = 1
            if EasyMode_Rand == 4:
                TestVar1 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
                TestVar2 = int(AnswerData)
                TestVar3 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
                TestVar4 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
                CorrectAnswer = 2

#           Applying labels to hint buttons
            self.btn1.set_label(str(TestVar1))
            self.btn2.set_label(str(TestVar2))
            self.btn3.set_label(str(TestVar3))
            self.btn4.set_label(str(TestVar4))

#   Processing ENTER keypress when fldTask is in focus
    def fldTask_ManualInput(self,fldTask):
        global CorrectAnswer, EasyMode_Rand
        EasyMode_Rand = random.randint(1,4)
        calcString = self.fldTask.get_text()
        TaskNum = int(calcString)
        self.lblTaskNumber.set_text("Task No. "+ str(TaskNum))
        with open('raczin_data.txt', 'r') as f:
            mycsv = csv.reader(f)
            mycsv = list(mycsv)
            TaskData_Text = mycsv[TaskNum][1]
            TaskData1_Text = mycsv[TaskNum][2]
            TaskData2_Text = mycsv[TaskNum][3]
            TaskQuestion_Text = mycsv[TaskNum][4]
            AnswerData = mycsv[TaskNum][5]
            lblHint_Text = mycsv[TaskNum][6]
        self.TaskData.set_text(TaskData_Text)
        self.TaskData1.set_text(TaskData1_Text)
        self.TaskData2.set_text(TaskData2_Text)
        self.TaskQuestion.set_text(TaskQuestion_Text)
        self.lblHint.set_text(lblHint_Text)

#       Randomizing easy mode buttons
        AnswerData = int(mycsv[TaskNum][5])
        if EasyMode_Rand == 1:
            TestVar1 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
            TestVar2 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
            TestVar3 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
            TestVar4 = int(AnswerData)
            CorrectAnswer = 4
        if EasyMode_Rand == 2:
            TestVar1 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
            TestVar2 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
            TestVar3 = int(AnswerData)
            TestVar4 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
            CorrectAnswer = 3
        if EasyMode_Rand == 3:
            TestVar1 = int(AnswerData)
            TestVar2 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
            TestVar3 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
            TestVar4 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
            CorrectAnswer = 1
        if EasyMode_Rand == 4:
            TestVar1 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
            TestVar2 = int(AnswerData)
            TestVar3 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
            TestVar4 = random.randint(int(0.75*AnswerData),int(1.25*AnswerData))
            CorrectAnswer = 2

#           Applying labels to hint buttons
            self.btn1.set_label(str(TestVar1))
            self.btn2.set_label(str(TestVar2))
            self.btn3.set_label(str(TestVar3))
            self.btn4.set_label(str(TestVar4))

#   Operating Settings button
    def settings_clicked(self,btnSettings):

#       Adding difficulty level selector and its label to Settings container
        self.Settings_Container.pack_start(self.Settings_DifficultyBox, True, True, 0)

#       Displaying Settings popover window
        self.Settings_Popover.set_relative_to(btnSettings)
        self.Settings_Popover.show_all()
        self.Settings_Popover.popup()

#   Operating difficulty buttons
    def btnHarder_clicked(self,btnHarder):
        global Difficulty_Level
        if Difficulty_Level == 2:
            Difficulty_Level = 3
            self.lblDifficulty_Setting.set_label("HARD")
            with open('raczin_data.txt', 'r') as f:
                setcsv = csv.writer
                
            self.btnHint.hide()
            self.btnHarder.set_sensitive(False)
        if Difficulty_Level == 1:
            Difficulty_Level = 2
            self.lblDifficulty_Setting.set_label("NORM")
            self.HelperBox.hide()
            self.AnswerBox.show()
            self.btnEasier.set_sensitive(True)
    def btnEasier_clicked(self,btnEasier):
        global Difficulty_Level
        if Difficulty_Level == 2:
            Difficulty_Level = 1
            self.lblDifficulty_Setting.set_label("EASY")
            self.AnswerBox.hide()
            self.HelperBox.show()
            self.btnEasier.set_sensitive(False)
        if Difficulty_Level == 3:
            Difficulty_Level = 2
            self.lblDifficulty_Setting.set_label("OKAY")
            self.btnHint.show()
            self.btnHarder.set_sensitive(True)

# === OPERATING GAME BUTTONS ===

#   Operating Hint button
    def btnHint_clicked(self, btnHint):
        calcString = self.fldTask.get_text()
        TaskNum = int(calcString)
        self.Hint_Popover.set_relative_to(btnHint)
        with open('raczin_data.txt', 'r') as f:
            mycsv = csv.reader(f)
            mycsv = list(mycsv)
            lblHint_Text = mycsv[TaskNum][6]
        self.lblHint.set_text(lblHint_Text)
        self.Hint_Popover.show_all()
        self.Hint_Popover.popup()

#   Operating Answer button
    def btnAnswer_clicked(self,btnAnswer):
        calcString = self.fldTask.get_text()
        TaskNum = int(calcString)
        AnswerString = self.AnswerEntry.get_text()
        with open('raczin_data.txt', 'r') as f:
            mycsv = csv.reader(f)
            mycsv = list(mycsv)
            AnswerData = mycsv[TaskNum][5]
        if AnswerString == AnswerData:
            self.AnswerEntry.modify_base(Gtk.StateType(0), Gdk.color_parse('#fbefce'))
            self.btnAnswer.hide()
            self.btnNextTask.show()
        else:
            self.AnswerEntry.modify_bg(Gtk.StateType(0), Gdk.color_parse('#ff8c82'))
            self.btnAnswer.modify_bg(Gtk.StateType(0), Gdk.color_parse('#ff8c82'))

#   Operating manual answer input
    def AnswerEntry_ManualInput(self,AnswerEntry):
        calcString = self.fldTask.get_text()
        TaskNum = int(calcString)
        AnswerString = self.AnswerEntry.get_text()
        with open('raczin_data.txt', 'r') as f:
            mycsv = csv.reader(f)
            mycsv = list(mycsv)
            AnswerData = mycsv[TaskNum][5]
        if AnswerString == AnswerData:
            self.AnswerEntry.modify_base(Gtk.StateType(0), Gdk.color_parse('#fbefce'))
            self.btnAnswer.hide()
            self.btnNextTask.show()
        else:
            self.AnswerEntry.modify_bg(Gtk.StateType(0), Gdk.color_parse('#ff8c82'))
            self.btnAnswer.modify_bg(Gtk.StateType(0), Gdk.color_parse('#ff8c82'))

#   Operating Next Task button
    def btnNextTask_clicked(self,btnNextTask):
        self.AnswerEntry.set_text("")
        self.btnAnswer.modify_bg(Gtk.StateType(0), Gdk.color_parse('#fbefce'))
        calcString = self.fldTask.get_text()
        TaskNum = int(calcString) + 1
        self.fldTask.set_text(str(TaskNum))
        self.lblTaskNumber.set_text("Task No. "+ str(TaskNum))
        with open('raczin_data.txt', 'r') as f:
            mycsv = csv.reader(f)
            mycsv = list(mycsv)
            TaskData_Text = mycsv[TaskNum][1]
            TaskData1_Text = mycsv[TaskNum][2]
            TaskData2_Text = mycsv[TaskNum][3]
            TaskQuestion_Text = mycsv[TaskNum][4]
            AnswerData = mycsv[TaskNum][5]
            lblHint_Text = mycsv[TaskNum][6]
        self.TaskData.set_text(TaskData_Text)
        self.TaskData1.set_text(TaskData1_Text)
        self.TaskData2.set_text(TaskData2_Text)
        self.TaskQuestion.set_text(TaskQuestion_Text)
        self.lblHint.set_text(lblHint_Text)
        self.btnNextTask.hide()
        self.btnAnswer.show()

#   Operating Easy Mode BUTTON 1
    def btn1_clicked(self,btn1):
        global CorrectAnswer
        if CorrectAnswer == 1:
            self.btn1.modify_bg(Gtk.StateType(0), Gdk.color_parse('#d1ff82'))
            self.btn2.set_sensitive(False)
            self.btn3.set_sensitive(False)
            self.btn4.set_sensitive(False)
        else:
            self.btn1.modify_bg(Gtk.StateType(0), Gdk.color_parse('#ff8c82'))

#   Operating Easy Mode BUTTON 2
    def btn2_clicked(self,btn2):
        global CorrectAnswer
        if CorrectAnswer == 2:
            self.btn2.modify_bg(Gtk.StateType(0), Gdk.color_parse('#d1ff82'))
            self.btn1.set_sensitive(False)
            self.btn3.set_sensitive(False)
            self.btn4.set_sensitive(False)
            CorrectAnswer = 0
        else:
            self.btn2.modify_bg(Gtk.StateType(0), Gdk.color_parse('#ff8c82'))

#   Operating Easy Mode BUTTON 3
    def btn3_clicked(self,btn3):
        global CorrectAnswer
        if CorrectAnswer == 3:
            self.btn3.modify_bg(Gtk.StateType(0), Gdk.color_parse('#d1ff82'))
            self.btn2.set_sensitive(False)
            self.btn1.set_sensitive(False)
            self.btn4.set_sensitive(False)
            CorrectAnswer = 0
        else:
            self.btn3.modify_bg(Gtk.StateType(0), Gdk.color_parse('#ff8c82'))

#   Operating Easy Mode BUTTON 4
    def btn4_clicked(self,btn4):
        global CorrectAnswer
        if CorrectAnswer == 4:
            self.btn4.modify_bg(Gtk.StateType(0), Gdk.color_parse('#d1ff82'))
            self.btn2.set_sensitive(False)
            self.btn3.set_sensitive(False)
            self.btn1.set_sensitive(False)
            CorrectAnswer = 0
        else:
            self.btn4.modify_bg(Gtk.StateType(0), Gdk.color_parse('#ff8c82'))

window = OperationsWindow()
window.connect("delete-event", Gtk.main_quit)
window.show()
Gtk.main()