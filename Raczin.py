import random
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Granite', '1.0')
from gi.repository import Gtk, Gio, GLib, Granite

Difficulty_Level = 2
TaskNum = random.randint(1,990)
Task_Number_Text = "Task No. "+ str(TaskNum)
TaskData_Placeholder_Text = "Here will be the description for the task number "+ str(TaskNum) +"."
TaskQuestion_Placeholder_Text = "Here will be the question for the task number "+ str(TaskNum) +"."

class OperationsWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Raczin")
# Main form properties
        self.set_default_size(420,420)
        self.set_border_width(5)
        self.set_modal(True)
        self.set_resizable(False)
# Setting up HeaderBar
        self.HeaderBar = Gtk.HeaderBar()
        self.HeaderBar.set_show_close_button(True)
        self.HeaderBar.set_title(self.get_title())
        self.set_titlebar(self.HeaderBar)
# Setting up Navigation bar container
        self.NavBar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(self.NavBar.get_style_context(), "linked")
# Setting up NavBar controls
        btnPrev = Gtk.Button()
        icon = Gio.ThemedIcon(name="go-previous-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        btnPrev.add(image)
        btnPrev.set_size_request(35, -1)
        btnPrev.connect("clicked", self.task_previous_clicked)
        
        self.fldTask = Gtk.Entry()
        self.fldTask.set_max_length(3)
        self.fldTask.set_width_chars(4)
        self.fldTask.set_alignment(xalign=0.5)
        self.fldTask.set_text(str(TaskNum))
        
        btnNext = Gtk.Button()
        icon = Gio.ThemedIcon(name="go-next-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        btnNext.add(image)
        btnNext.set_size_request(35, -1)
        btnNext.connect("clicked", self.task_next_clicked)
# Placing NavBar onto Header Bar
        self.NavBar.add(btnPrev)
        self.NavBar.add(self.fldTask)
        self.NavBar.add(btnNext)
        self.HeaderBar.pack_start(self.NavBar)
# Placing a random task button
        btnRand = Gtk.Button()
        icon = Gio.ThemedIcon(name="mail-send-receive-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        btnRand.add(image)
        btnRand.set_size_request(20, -1)
        btnRand.connect("clicked", self.task_randomizer_clicked)
        self.HeaderBar.pack_start(btnRand)
# Placing a settings button
        btnSettings=Gtk.Button()
        icon = Gio.ThemedIcon(name="open-menu-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        btnSettings.add(image)
        btnSettings.set_size_request(30, -1)
        self.HeaderBar.pack_end(btnSettings)
        btnSettings.connect("clicked", self.settings_clicked)
# Placing a dark mode switch
        modeSwitch = Granite.ModeSwitch.from_icon_name ("display-brightness-symbolic", "weather-clear-night-symbolic")
        modeSwitch.set_valign(Gtk.Align.CENTER)
        self.HeaderBar.pack_end(modeSwitch)
# Setting up main window container
        self.MainContainer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.MainContainer)
# Setting up Task dispays:
#   Task number label:
        self.lblTaskNumber = Gtk.Label()
        self.lblTaskNumber.set_use_markup(True)
        self.lblTaskNumber.set_text("Task No. "+ str(TaskNum))
        self.lblTaskNumber.set_markup("<big>%s</big>" % Task_Number_Text)
        self.MainContainer.pack_start(self.lblTaskNumber, True, True, 0)
#   Task description box: 
        self.TaskData = Gtk.Label()
        self.TaskData.set_alignment(0,0)
        self.TaskData.set_text(TaskData_Placeholder_Text)
        self.MainContainer.pack_start(self.TaskData, True, True, 2)
#   Task question box: 
        self.TaskQuestion = Gtk.Label()
        self.TaskQuestion.set_markup("<i>%s</i>" % TaskQuestion_Placeholder_Text)
        self.MainContainer.pack_start(self.TaskQuestion, True, True, 2)
# Setting up answer string: 
        self.AnswerBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(self.AnswerBox.get_style_context(), "linked")
        self.AnswerEntry = Gtk.Entry()
        self.AnswerEntry.set_size_request(-1, 34)
        self.AnswerEntry.set_placeholder_text("Type your answer here")
        self.AnswerBox.pack_start(self.AnswerEntry, True, True, 0)
        btnAnswer = Gtk.Button()
        icon = Gio.ThemedIcon(name="object-select-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        btnAnswer.add(image)
        btnAnswer.set_size_request(50, -1)
        self.AnswerBox.pack_end(btnAnswer, False, True, 0)
        self.MainContainer.pack_start(self.AnswerBox, False, True, 5)
# Setting up hint buttons
        self.HelperBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(self.HelperBox.get_style_context(), "linked")
        btn1 = Gtk.Button(label = "Answer 1")
        btn1.set_size_request(-1, 34)
        self.HelperBox.pack_end(btn1, True, True, 0)
        btn2 = Gtk.Button(label = "Answer 2")
        btn2.set_size_request(-1, 34)
        self.HelperBox.pack_end(btn2, True, True, 0)
        btn3 = Gtk.Button(label = "Answer 3")
        btn3.set_size_request(-1, 34)
        self.HelperBox.pack_end(btn3, True, True, 0)
        btn4 = Gtk.Button(label = "Answer 4")
        btn4.set_size_request(-1, 34)
        self.HelperBox.pack_end(btn4, True, True, 0)
        self.MainContainer.pack_start(self.HelperBox, False, True, 0)
# OPERATIONS FOR HEADERBAR BUTTONS AND FIELDS
# Operating btnRand function
    def task_randomizer_clicked(self,btnRand):
        TaskNum = random.randint(1,990)
        self.fldTask.set_text(str(TaskNum))
        self.lblTaskNumber.set_text("Task No. "+ str(TaskNum))
# Operating btnPrev function
    def task_previous_clicked(self,btnPrev):
        calcString = self.fldTask.get_text()
        TaskNum = int(calcString) - 1
        self.fldTask.set_text(str(TaskNum))
        self.lblTaskNumber.set_text("Task No. "+ str(TaskNum))
# Operating btnNext function
    def task_next_clicked(self,btnPrev):
        calcString = self.fldTask.get_text()
        TaskNum = int(calcString) + 1
        self.fldTask.set_text(str(TaskNum))
        self.lblTaskNumber.set_text("Task No. "+ str(TaskNum))
# Operating Settings button
    def settings_clicked(self,btnSettings):
# Setting up Settings menu popover window
        self.Settings_Popover = Gtk.Popover()
        self.Settings_Popover.set_position(Gtk.PositionType.BOTTOM)
        self.Settings_Popover.set_size_request(20,40)
        self.Settings_Popover.set_border_width(5)
        self.Settings_Container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.Settings_Popover.add(self.Settings_Container)
# Setting up difficulty level container
        self.Settings_DifficultyBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(self.Settings_DifficultyBox.get_style_context(), "linked")
# Setting up difficulty level selector toggle buttons
        btnEasy = Gtk.ToggleButton(label='Easy')
        btnEasy.set_size_request(-1, 34)
        self.Settings_DifficultyBox.pack_start(btnEasy, True, True, 0)
        btnNormal = Gtk.ToggleButton(label="Normal")
        btnNormal.set_size_request(-1, 34)
        btnNormal.set_active(True)
        self.Settings_DifficultyBox.pack_start(btnNormal, True, True, 0)
        btnHard = Gtk.ToggleButton(label="Hard")
        btnHard.set_size_request(-1, 34)
        self.Settings_DifficultyBox.pack_start(btnHard, True, True, 0)
#Adding difficulty level selector and its label to Settings container
        self.lblDifficulty_Setting = Gtk.Label("Difficulty level:")
        self.Settings_Container.pack_start(self.lblDifficulty_Setting, True, True, 2)
        self.Settings_Container.pack_start(self.Settings_DifficultyBox, True, True, 0)
# Displaying popover window
        self.Settings_Popover.set_relative_to(btnSettings)
        self.Settings_Popover.show_all()
        self.Settings_Popover.popup()

window = OperationsWindow()
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()
