import customtkinter as ctk
import database
import utils
import datetime
from PIL import Image
from tkinter import messagebox


# Constants 
# Colour Palette
BUTTON_COLOUR = ("#8E3635", "#171717")
BUTTON_HOVER_COLOUR = ("#A8403E", "#7D0A0A")

TOP_BAR_FG_COLOUR = ("white", "#222831")
CONTENTS_FG_COLOUR = ("#F0F1F3", "#0F0F0F")
OPTIONS_FG_COLOUR = ("white", "#171717")
START_UP_FG_COLOUR = ("white", "#0F0F0F")

WINDOW_FG_COLOUR = ("white", "#0F0F0F")

TEXT_COLOUR = ("black", "white")
LABEL_TEXT_COLOUR = ("black", "white")
BUTTON_TEXT_COLOUR = ("white", "white")


# Fonts and Sizes
FONT_NAME = "Segoe UI"
FONT_SIZE_BUTTONS = 15
FONT_SIZE_CONTENTS = 12
FONT_SIZE_LOGIN = 15
FONT_SIZE_INTRO1 = 40
FONT_SIZE_INTRO2 = 20

OPTIONS_BUTTON_WIDTH = 200
OPTIONS_BUTTON_HEIGHT = 50

CORNER_R = 20

CONTENTS_BUTTON_WIDTH = 200
CONTENTS_BUTTON_HEIGHT = 50

INTRO_BUTTON_WIDTH = 100
INTRO_BUTTON_HEIGHT = 100

WIN_WIDTH = 1200
WIN_HEIGHT = 820

OPTIONS_PADDING = 10

OPTIONS_FRAME_WIDTH = 200
OPTIONS_FRAME_HEIGHT = 700

CONTENTS_FRAME_WIDTH = 980
CONTENTS_FRAME_HEIGHT = 700

INTRO_FRAME_WIDTH = 1200
INTRO_FRAME_HEIGHT = 100

START_UP_FRAME_WIDHT = 1200
START_UP_FRAME_HEIGHT = 800

STATS_CANVAS_WIDTH = 470
STATS_CANVAS_HEIGHT = 330

STATS_CANVAS_PAD_X = 10
STATS_CANVAS_PAD_Y = 10

COURSE_BUTTON_WIDTH = 600

CURRENT_YEAR = datetime.datetime.today().year


# Αρχικό GUI 
class StartUpGUI(ctk.CTk):
    

    def __init__(self):
        super().__init__()
        self.configure(fg_color=WINDOW_FG_COLOUR)
        self.iconbitmap("images\logo.ico")
        self.title("Progress 2.0")
        self.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")
        self.resizable(False,False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.configure(fg_colour=WINDOW_FG_COLOUR)
        
        # Βασικό Frame
        self.main_frame = ctk.CTkFrame(master=self, width=START_UP_FRAME_WIDHT, height=START_UP_FRAME_HEIGHT, fg_color=START_UP_FG_COLOUR)
        self.main_frame.grid(row=0, column=0, padx=300, pady=300)

        # Πεδίο Εισαγωγής username
        self.usernameLabel = ctk.CTkLabel(master=self.main_frame
                                          , text='Username'
                                          , font=(FONT_NAME, FONT_SIZE_LOGIN)
                                          , text_color=LABEL_TEXT_COLOUR)
        self.usernameLabel.grid(row=3, column=0)

        self.usernameInput = ctk.CTkEntry(master=self.main_frame, width=200)
        self.usernameInput.grid(row=3, column=1)

        # Πεδίο Εισαγωγής password
        self.passwordLabel = ctk.CTkLabel(master=self.main_frame
                                          , text='Password'
                                          , font=(FONT_NAME, FONT_SIZE_LOGIN)
                                          , text_color=LABEL_TEXT_COLOUR)
        self.passwordLabel.grid(row=5, column=0)

        self.passwordInput = ctk.CTkEntry(master=self.main_frame, width=200, show='*')
        self.passwordInput.grid(row=5, column=1)

        # Διακόπτης για την εμφάνιση του κωδικού
        self.show_password_switch = ctk.CTkSwitch(master=self.main_frame
                                                  , text="Show password"
                                                  , command=self.toggle_password1
                                                  , font=(FONT_NAME, FONT_SIZE_LOGIN)
                                                  , fg_color=BUTTON_COLOUR
                                                  , progress_color=BUTTON_HOVER_COLOUR
                                                  , text_color=TEXT_COLOUR)
        self.show_password_switch.grid(row=5, column=2, padx=10)

        # Κουμπί για την είσοδο στην εφαρμογή
        self.log_in_button = ctk.CTkButton(master=self.main_frame
                                           , text="Log In"
                                           , command= lambda: StartUpGUI.log_in(self, self.usernameInput.get(), self.passwordInput.get())
                                           , font=(FONT_NAME, FONT_SIZE_LOGIN)
                                           , fg_color=BUTTON_COLOUR
                                           , hover_color=BUTTON_HOVER_COLOUR
                                           , corner_radius=CORNER_R
                                           , text_color=BUTTON_TEXT_COLOUR)
        self.log_in_button.grid(row=7, column=1, pady=10)

        # Κουμπί για την δημιουργία λογαριασμού
        self.sign_up_button = ctk.CTkButton(master=self.main_frame
                                            , text="Εγγραφή", command= lambda: StartUpGUI.sign_up(self)
                                            , font=(FONT_NAME, FONT_SIZE_LOGIN)
                                            , fg_color=BUTTON_COLOUR
                                            , hover_color=BUTTON_HOVER_COLOUR
                                            , corner_radius=CORNER_R
                                            , text_color=BUTTON_TEXT_COLOUR)
        self.sign_up_button.grid(row=8, column=1, pady=10)

        # Κουμπί για την αλλαγή κωδικού
        self.change_password_button = ctk.CTkButton(master=self.main_frame
                                            , text="Αλλαγή Κωδικού", command= lambda: StartUpGUI.change_pass(self)
                                            , font=(FONT_NAME, FONT_SIZE_LOGIN)
                                            , fg_color=BUTTON_COLOUR
                                            , hover_color=BUTTON_HOVER_COLOUR
                                            , corner_radius=CORNER_R
                                            , text_color=BUTTON_TEXT_COLOUR)
        self.change_password_button.grid(row=9, column=1, pady=10)

        # Μενού επιλογών για την εμφάνιση της εφαρμογής
        self.label_mode = ctk.CTkLabel(master=self.main_frame
                                       , text="Appearance Mode:"
                                       , font=(FONT_NAME, FONT_SIZE_LOGIN)
                                       , text_color=LABEL_TEXT_COLOUR)
        self.label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")

        self.optionmenu = ctk.CTkOptionMenu(master=self.main_frame
                                            , values=["Dark", "Light", "System"]
                                            , command=self.change_appearance_mode
                                            , font=(FONT_NAME, FONT_SIZE_LOGIN)
                                            , button_color=BUTTON_COLOUR
                                            , button_hover_color=BUTTON_HOVER_COLOUR
                                            , fg_color=BUTTON_COLOUR
                                            , corner_radius=CORNER_R
                                            , text_color=BUTTON_TEXT_COLOUR)
        self.optionmenu.grid(row=11, column=0, pady=10, padx=20, sticky="w")

        self.show_password = False # Μεταβλητή για την εμφάνιση του κωδικού


    def sign_up(self):
        '''Δημιουργεί το παράθυρο για την εγγραφή στην εφαρμογή'''

        print("sign_up")
        self.clear_frame(self.main_frame)

        # Πεδίο Εισαγωγής ΑΜ ή ΑΤ
        self.enter_username_label = ctk.CTkLabel(master=self.main_frame
                                           , text="Εισάγετε τον Αριθμό Μητρώου σας"
                                           , font=(FONT_NAME, FONT_SIZE_LOGIN)
                                           , text_color=LABEL_TEXT_COLOUR)
        self.enter_username_label.grid(row=0, column=0, pady=10, padx=20, sticky="w")

        self.enter_username_input = ctk.CTkEntry(master=self.main_frame, width=200)
        self.enter_username_input.grid(row=0, column=1, pady=10, padx=20, sticky="w")

        # Πεδίο Εισαγωγής password
        self.enter_password_label = ctk.CTkLabel(master=self.main_frame
                                                 , text="Εισάγετε τον Κωδικό σας"
                                                 , font=(FONT_NAME, FONT_SIZE_LOGIN)
                                                 , text_color=LABEL_TEXT_COLOUR)
        self.enter_password_label.grid(row=1, column=0, pady=10, padx=20, sticky="w")

        self.enter_password_input = ctk.CTkEntry(master=self.main_frame, width=200, show='*')
        self.enter_password_input.grid(row=1, column=1, pady=10, padx=20, sticky="w")

        # Πεδίο Εισαγωγής password(ξανά)
        self.reenter_password_label = ctk.CTkLabel(master=self.main_frame
                                                   , text="Ξαναεισάγετε τον Κωδικό σας"
                                                   , font=(FONT_NAME, FONT_SIZE_LOGIN)
                                                   , text_color=LABEL_TEXT_COLOUR)
        self.reenter_password_label.grid(row=2, column=0, pady=10, padx=20, sticky="w")

        self.enter_new_password_input = ctk.CTkEntry(master=self.main_frame, width=200, show='*')
        self.enter_new_password_input.grid(row=2, column=1, pady=10, padx=20, sticky="w")

        # Διακόπτης για την εμφάνιση του κωδικού
        self.show_password_switch = ctk.CTkSwitch(master=self.main_frame
                                                  , text="Show password"
                                                  , command=self.toggle_password2
                                                  , font=(FONT_NAME, FONT_SIZE_LOGIN)
                                                  , fg_color=BUTTON_COLOUR
                                                  , progress_color=BUTTON_HOVER_COLOUR
                                                  , text_color=TEXT_COLOUR)
        self.show_password_switch.grid(row=1, column=2, padx=10)

        # Μενού επιλογών για την εμφάνιση της εφαρμογής
        self.label_mode = ctk.CTkLabel(master=self.main_frame
                                       , text="Appearance Mode:"
                                       , font=(FONT_NAME, FONT_SIZE_LOGIN)
                                       , text_color=LABEL_TEXT_COLOUR)
        self.label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")

        self.optionmenu = ctk.CTkOptionMenu(master=self.main_frame
                                            , values=["Dark", "Light", "System"]
                                            , command=self.change_appearance_mode
                                            , font=(FONT_NAME, FONT_SIZE_LOGIN)
                                            , button_color=BUTTON_COLOUR
                                            , button_hover_color=BUTTON_HOVER_COLOUR
                                            , fg_color=BUTTON_COLOUR
                                            , corner_radius=CORNER_R
                                            , text_color=BUTTON_TEXT_COLOUR)
        self.optionmenu.grid(row=11, column=0, pady=10, padx=20, sticky="w")

        # Κουμπί για την δημιουργία λογαριασμού
        self.create_account_button = ctk.CTkButton(master=self.main_frame
                                                   , text="Create Account"
                                                   , command= lambda: StartUpGUI.create_account(self, self.enter_username_input.get(), self.enter_password_input.get(), self.enter_new_password_input.get())
                                                   , font=(FONT_NAME, FONT_SIZE_LOGIN)
                                                   , fg_color=BUTTON_COLOUR
                                                   , hover_color=BUTTON_HOVER_COLOUR
                                                   , corner_radius=CORNER_R
                                                   , text_color=BUTTON_TEXT_COLOUR)
        self.create_account_button.grid(row=3, column=1, pady=10)


    def log_in(self, username, password):
        '''Ελέγχει αν το username και το password είναι σωστά και εμφανίζει την κατάλληλη εφαρμογή'''

        print(username, password)
        if database.user_exists(username):
            if database.check_password(username, password):
                if database.is_admin(username):
                    print("Admin")
                    self.destroy()
                    app = AdminGUI(username)
                    app.mainloop()
                else:
                    print("Student")
                    self.destroy()
                    app = StudentGUI(username)
                    app.mainloop()
            else:
                messagebox.showerror("Error", "Wrong password")
        else:
            messagebox.showerror("Error", "User does not exist")
        

    def create_account(self, id, password, reenter_password):
        '''Δημιουργεί τον λογαριασμό του χρήστη'''
        print("create_account")

        # Ελέγχει αν υπάρχει ήδη ο χρήστης
        if database.user_exists(f"up{id}"):
            messagebox.showerror("Error", "User already exists")
            self.destroy()
            app = StartUpGUI()
            app.mainloop()
        else:
            if password == reenter_password:
                database.create_user(id, password)
                messagebox.showinfo("Success", "Account created successfully")
                self.destroy()
                app = StartUpGUI()
                app.mainloop()
            else:
                messagebox.showerror("Error", "Passwords do not match")


    def change_pass(self):
        '''Δημιουργεί το παράθυρο για την αλλαγή κωδικού'''
        print("change pass")
        self.clear_frame(self.main_frame)

        # Πεδίο Εισαγωγής username
        self.enter_username_label = ctk.CTkLabel(master=self.main_frame
                                           , text="Εισάγετε το username σας"
                                           , font=(FONT_NAME, FONT_SIZE_LOGIN)
                                           , text_color=LABEL_TEXT_COLOUR)
        self.enter_username_label.grid(row=0, column=0, pady=10, padx=20, sticky="w")

        self.enter_username_input = ctk.CTkEntry(master=self.main_frame, width=200)
        self.enter_username_input.grid(row=0, column=1, pady=10, padx=20, sticky="w")

        # Πεδίο Εισαγωγής παλιού password
        self.enter_old_password_label = ctk.CTkLabel(master=self.main_frame
                                                 , text="Εισάγετε τον παλιό Κωδικό σας"
                                                 , font=(FONT_NAME, FONT_SIZE_LOGIN)
                                                 , text_color=LABEL_TEXT_COLOUR)
        self.enter_old_password_label.grid(row=1, column=0, pady=10, padx=20, sticky="w")

        self.enter_password_input = ctk.CTkEntry(master=self.main_frame, width=200, show='*')
        self.enter_password_input.grid(row=1, column=1, pady=10, padx=20, sticky="w")

        # Πεδίο Εισαγωγής νέου password
        self.enter_new_password_label = ctk.CTkLabel(master=self.main_frame
                                                   , text="Εισάγετε το νέο Κωδικό σας"
                                                   , font=(FONT_NAME, FONT_SIZE_LOGIN)
                                                   , text_color=LABEL_TEXT_COLOUR)
        self.enter_new_password_label.grid(row=2, column=0, pady=10, padx=20, sticky="w")

        self.enter_new_password_input = ctk.CTkEntry(master=self.main_frame, width=200, show='*')
        self.enter_new_password_input.grid(row=2, column=1, pady=10, padx=20, sticky="w")

        # Διακόπτης για την εμφάνιση του κωδικού
        self.show_password_switch = ctk.CTkSwitch(master=self.main_frame
                                                  , text="Show password"
                                                  , command=self.toggle_password2
                                                  , font=(FONT_NAME, FONT_SIZE_LOGIN)
                                                  , fg_color=BUTTON_COLOUR
                                                  , progress_color=BUTTON_HOVER_COLOUR
                                                  , text_color=TEXT_COLOUR)
        self.show_password_switch.grid(row=1, column=2, padx=10)

        # Μενού επιλογών για την εμφάνιση της εφαρμογής
        self.label_mode = ctk.CTkLabel(master=self.main_frame
                                       , text="Appearance Mode:"
                                       , font=(FONT_NAME, FONT_SIZE_LOGIN)
                                       , text_color=LABEL_TEXT_COLOUR)
        self.label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")

        self.optionmenu = ctk.CTkOptionMenu(master=self.main_frame
                                            , values=["Dark", "Light", "System"]
                                            , command=self.change_appearance_mode
                                            , font=(FONT_NAME, FONT_SIZE_LOGIN)
                                            , button_color=BUTTON_COLOUR
                                            , button_hover_color=BUTTON_HOVER_COLOUR
                                            , fg_color=BUTTON_COLOUR
                                            , corner_radius=CORNER_R
                                            , text_color=BUTTON_TEXT_COLOUR)
        self.optionmenu.grid(row=11, column=0, pady=10, padx=20, sticky="w")

        # Κουμπί για την αλλαγή κωδικού
        self.change_password_button = ctk.CTkButton(master=self.main_frame
                                                   , text="Αλλαγή Κωδικού"
                                                   , command= lambda: StartUpGUI.change_password(self, self.enter_username_input.get(), self.enter_password_input.get(), self.enter_new_password_input.get())
                                                   , font=(FONT_NAME, FONT_SIZE_LOGIN)
                                                   , fg_color=BUTTON_COLOUR
                                                   , hover_color=BUTTON_HOVER_COLOUR
                                                   , corner_radius=CORNER_R
                                                   , text_color=BUTTON_TEXT_COLOUR)
        self.change_password_button.grid(row=3, column=1, pady=10)


    def change_password(self, username, old_password, new_password):
        '''Αλλάζει τον κωδικό του χρήστη'''

        print("change_password")
        # print(database.check_password(username, old_password))
        # Eλέγχει αν υπάρχει ο χρήστης και αν ο παλιός κωδικός είναι σωστός
        if database.user_exists(username):
            if database.check_password(username, old_password):
                database.change_password(username, new_password)
                messagebox.showinfo("Success", "Password changed successfully")
                self.destroy()
                app = StartUpGUI()
                app.mainloop()
            else:
                messagebox.showerror("Error", "Wrong old password")
        else:
            messagebox.showerror("Error", "User does not exist, Please Sign Up")
            self.destroy()
            app = StartUpGUI()
            app.mainloop()


    def toggle_password1(self):
        '''Εμφανίζει τον κωδικό του χρήστη στο παράθυρο εισαγωγής sign_in'''

        self.show_password = not self.show_password
        # print(self.var)
        if self.show_password:
            self.passwordInput.configure(show="")
        else:
            self.passwordInput.configure(show="*")


    def toggle_password2(self):
        '''Εμφανίζει τον κωδικό του χρήστη στο παράθυρο εισαγωγής sign_up και change_password'''

        self.show_password = not self.show_password
        if self.show_password:
            self.enter_password_input.configure(show="")
            self.enter_new_password_input.configure(show="")
        else:
            self.enter_password_input.configure(show="*")
            self.enter_new_password_input.configure(show="*")


    def change_appearance_mode(self, new_appearance_mode):
        '''Αλλάζει το appearance mode της εφαρμογής'''
        ctk.set_appearance_mode(new_appearance_mode)


    def clear_frame(self, frame):
        '''Καθαρίζει το frame'''
        for widget in frame.winfo_children():
            widget.destroy()
    

    def on_closing(self, event=0):
        '''Κλείνει την εφαρμογή'''

        self.destroy()

# GUi για τον φοιτητή
class StudentGUI(ctk.CTk):


    def __init__(self, username):
        super().__init__()
        self.username = username
        self.id = database.get_id_from_user(username)
        self.student = database.get_student(self.id)
        self.month = "FEBR"
        self.semester_type = "Χειμερινό"
        self.configure(fg_color=WINDOW_FG_COLOUR)
        self.iconbitmap("images\logo.ico")
        self.title("Progress 2.0")
        self.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")
        self.resizable(False,False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.main_app()


    def main_app(self):
        '''Δημιουργεί το κύριο παράθυρο της εφαρμογής'''

        # Κύρια Frames
        self.intro_frame = ctk.CTkFrame(master=self, width=INTRO_FRAME_WIDTH, height=INTRO_FRAME_HEIGHT, fg_color=TOP_BAR_FG_COLOUR)
        self.intro_frame.grid(row=0, column=0, columnspan=2, sticky="nw")
        self.top_bar_app()

        self.options_frame = ctk.CTkFrame(master=self, width=OPTIONS_FRAME_WIDTH, height=OPTIONS_FRAME_HEIGHT, fg_color=OPTIONS_FG_COLOUR)
        self.options_frame.grid(row=1, column=0, sticky="n")
        self.options_app()
        
        self.contents_frame = ctk.CTkScrollableFrame(master=self, width=CONTENTS_FRAME_WIDTH, height=CONTENTS_FRAME_HEIGHT, fg_color=CONTENTS_FG_COLOUR)
        self.contents_frame.grid(row=1, column=1, sticky="w")

    
        self.start_app()

        
    def options_app(self):
        '''Δημιουργεί το παράθυρο με τις επιλογές του χρήστη'''

        # Options widgets

        # Κουμπί για την καρτέλα
        self.kartela_button = ctk.CTkButton(master=self.options_frame
                                            , width=OPTIONS_BUTTON_WIDTH
                                            , height=OPTIONS_BUTTON_HEIGHT
                                            , text="Καρτέλα Φοιτητή"
                                            , command= lambda: StudentGUI.kartela_app(self)
                                            , font=(FONT_NAME, FONT_SIZE_BUTTONS)
                                            , fg_color=BUTTON_COLOUR
                                            , hover_color=BUTTON_HOVER_COLOUR
                                            , corner_radius=CORNER_R
                                            , text_color=BUTTON_TEXT_COLOUR)
        self.kartela_button.grid(row=0, column=0, pady=OPTIONS_PADDING)

        # Κουμπί για τα ακαδημαϊκο έργο
        self.akadhmaiko_ergo_button = ctk.CTkButton(master=self.options_frame
                                                    , width=OPTIONS_BUTTON_WIDTH
                                                    , height=OPTIONS_BUTTON_HEIGHT
                                                    , text="Ακαδημαϊκό Έργο"
                                                    , command= lambda: StudentGUI.captcha_app(self)
                                                    , font=(FONT_NAME, FONT_SIZE_BUTTONS)
                                                    , fg_color=BUTTON_COLOUR
                                                    , hover_color=BUTTON_HOVER_COLOUR
                                                    , corner_radius=CORNER_R
                                                    , text_color=BUTTON_TEXT_COLOUR)
        self.akadhmaiko_ergo_button.grid(row=1, column=0, pady=OPTIONS_PADDING)

        # Κουμπί για την δήλωση μαθημάτων
        self.dhlwsh_mathimatwn_button = ctk.CTkButton(master=self.options_frame
                                                      , width=OPTIONS_BUTTON_WIDTH
                                                      , height=OPTIONS_BUTTON_HEIGHT
                                                      , text="Δήλωση Μαθημάτων"
                                                      , command= lambda: StudentGUI.sign_up_to_courses(self)
                                                      , font=(FONT_NAME, FONT_SIZE_BUTTONS)
                                                      , fg_color=BUTTON_COLOUR
                                                      , hover_color=BUTTON_HOVER_COLOUR
                                                      , corner_radius=CORNER_R
                                                      , text_color=BUTTON_TEXT_COLOUR)
        self.dhlwsh_mathimatwn_button.grid(row=4, column=0, pady=OPTIONS_PADDING)

        # Κουμπί για την δήλωση κατεύθυνσης
        self.dhlwsh_kateythinshs_button = ctk.CTkButton(master=self.options_frame
                                                        , width=OPTIONS_BUTTON_WIDTH
                                                        , height=OPTIONS_BUTTON_HEIGHT
                                                         , text="Δήλωση Κατεύθυνσης"
                                                         , command= lambda: StudentGUI.dhlwsh_kateythinshs(self)
                                                         , font=(FONT_NAME, FONT_SIZE_BUTTONS)
                                                         , fg_color=BUTTON_COLOUR
                                                         , hover_color=BUTTON_HOVER_COLOUR
                                                         , corner_radius=CORNER_R
                                                         , text_color=BUTTON_TEXT_COLOUR)
        self.dhlwsh_kateythinshs_button.grid(row=5, column=0, pady=OPTIONS_PADDING)

        # Κουμπί για την δήλωση διπλωματικής
        self.diplwmatikh_button = ctk.CTkButton(master=self.options_frame
                                                , width=OPTIONS_BUTTON_WIDTH
                                                , height=OPTIONS_BUTTON_HEIGHT
                                                 , text="Δήλωση Διπλωματικής"
                                                 , command= lambda: StudentGUI.dhlwsh_diplwmatikhs(self)
                                                 , font=(FONT_NAME, FONT_SIZE_BUTTONS)
                                                 , fg_color=BUTTON_COLOUR
                                                 , hover_color=BUTTON_HOVER_COLOUR
                                                 , corner_radius=CORNER_R
                                                 , text_color=BUTTON_TEXT_COLOUR)
        self.diplwmatikh_button.grid(row=6, column=0, pady=OPTIONS_PADDING)

        # Κουμπί για εμφάνιση στατιστικών
        self.statistics_button = ctk.CTkButton(master=self.options_frame
                                                , width=OPTIONS_BUTTON_WIDTH
                                                , height=OPTIONS_BUTTON_HEIGHT
                                                 , text="Στατιστικά"
                                                 , command= lambda: StudentGUI.statistics_app(self)
                                                 , font=(FONT_NAME, FONT_SIZE_BUTTONS)
                                                 , fg_color=BUTTON_COLOUR
                                                 , hover_color=BUTTON_HOVER_COLOUR
                                                 , corner_radius=CORNER_R
                                                 , text_color=BUTTON_TEXT_COLOUR)
        self.statistics_button.grid(row=7, column=0, pady=OPTIONS_PADDING)

        # Μενού επιλογών για την αλλαγή μήνα
        self.current_month_label = ctk.CTkLabel(master=self.options_frame, width=100
                                                , text="Τρέχον Μήνας"
                                                , font=(FONT_NAME, FONT_SIZE_BUTTONS)
                                                , text_color=LABEL_TEXT_COLOUR)
        self.current_month_label.grid(row=8, column=0, pady=(200, 0))

        self.months_list = ["Ιανουάριος", "Φεβρουάριος", "Μάρτιος", "Απρίλιος", "Μάιος", "Ιούνιος", "Ιούλιος", "Άυγουστος", "Σεπτέμβριος", "Οκτώβριος", "Νοέμβριος", "Δεκέμβριος"]
        self.current_month_options = ctk.CTkOptionMenu(master=self.options_frame, width=OPTIONS_BUTTON_WIDTH, height=OPTIONS_BUTTON_HEIGHT
                                            , values=self.months_list
                                            , command= self.change_current_month
                                            , font=(FONT_NAME, FONT_SIZE_LOGIN)
                                            , button_color=BUTTON_COLOUR
                                            , button_hover_color=BUTTON_HOVER_COLOUR
                                            , fg_color=BUTTON_COLOUR
                                            , corner_radius=CORNER_R
                                            , text_color=BUTTON_TEXT_COLOUR)
        self.current_month_options.grid(row=9, column=0, pady=OPTIONS_PADDING)


    def change_current_month(self, new_month):
        '''Αλλάζει τον τρέχον μήνα και θέτει τον τύπο του εξαμήνου και εξεταστικής περιόδου'''

        print("change_current_month")
        month_index = self.months_list.index(new_month)
        if 7 <= month_index <= 8: 
            self.month = "SEPT"
        elif 2 <= month_index <= 6: 
            self.month = "JUNE"
        elif month_index <= 1 or month_index >= 9: 
            self.month = "FEBR"
        print(self.month)
        self.semester_type = "Εαρινό" if self.month == "JUNE" else "Χειμερινό"
        self.start_app()


    def statistics_app(self):
        '''Δημιουργεί το παράθυρο με τα στατιστικά'''

        print("statistics")
        StudentGUI.clear_frame(self, self.contents_frame)

        # Λίστα με όλα εξάμηνα
        semester_list = [str(i) for i in range(1, 10)]

        # Κουμπί και Dropdow menu για την επιλογή εξαμήνου
        semester_label = ctk.CTkLabel(master=self.contents_frame, width=100
                                      , text="Εξάμηνο"
                                      , font=(FONT_NAME, FONT_SIZE_BUTTONS)
                                      , text_color=LABEL_TEXT_COLOUR)
        semester_label.grid(row=0, column=0)

        self.combo_semester = ctk.CTkComboBox(master=self.contents_frame, width=50
                                            , values=semester_list
                                            , font=(FONT_NAME, FONT_SIZE_CONTENTS)
                                            , text_color=TEXT_COLOUR)
        self.combo_semester.grid(row=0, column=1, padx=10, pady=10)

        self.choose_semester_button = ctk.CTkButton(master=self.contents_frame
                                                    , width=OPTIONS_BUTTON_WIDTH
                                                    , height=OPTIONS_BUTTON_HEIGHT
                                                    , text="Επιλογή"
                                                    , command= lambda: StudentGUI.choose_semester(self, self.combo_semester.get())
                                                    , font=(FONT_NAME, FONT_SIZE_BUTTONS)
                                                    , fg_color=BUTTON_COLOUR
                                                    , hover_color=BUTTON_HOVER_COLOUR
                                                    , corner_radius=CORNER_R
                                                    , text_color=BUTTON_TEXT_COLOUR)
        self.choose_semester_button.grid(row=2, column=0, padx=10, pady=10)
        
        
    def choose_semester(self, semester):

        print("choose_semester")
        StudentGUI.clear_frame(self, self.contents_frame)

        semester = int(semester)
        self.courses_by_semester = [course for course in database.get_all_courses() if course.semester == semester]
        
        buttons = []
        for i in range(len(self.courses_by_semester)):
            self.choose_course_button = ctk.CTkButton(master=self.contents_frame, width=COURSE_BUTTON_WIDTH, height=50
                                            , text=self.courses_by_semester[i].title
                                            , command= lambda i=i: StudentGUI.stats(self, self.courses_by_semester, i)
                                            , font=(FONT_NAME, FONT_SIZE_BUTTONS)
                                            , fg_color=BUTTON_COLOUR
                                            , hover_color=BUTTON_HOVER_COLOUR
                                            , corner_radius=CORNER_R
                                            , text_color=BUTTON_TEXT_COLOUR)
            self.choose_course_button.grid(row=i, column=1, padx=10, pady=10)
        #     print(self.choose_course_button.winfo_reqwidth())
        #     buttons.append(self.choose_course_button)
        # max_width = max(button.winfo_reqwidth() for button in buttons)

        # for index, button in enumerate(buttons):
        #     button.configure(width=max_width)

        
    def stats(self, courses, i):
        '''Παρουσιάζει τα στατιστικά ενός μαθήματος'''

        print("stats")
        StudentGUI.clear_frame(self, self.contents_frame)

        data = database.course_grade_bar_chart(courses[i].code)

        if not data:
            messagebox.showerror("Error", "Δεν υπάρχουν στατιστικά για αυτό το μάθημα")
            return

        # bar chart 
        grade_list = [i_/2 for i_ in range(21)]
        self.bar_chart_canvas = ctk.CTkCanvas(master=self.contents_frame
                                               , width=960
                                               , height=STATS_CANVAS_HEIGHT
                                               , bg = OPTIONS_FG_COLOUR[1]
                                               , highlightthickness=0)
        self.bar_chart_canvas.grid(row=1, column=0, sticky="s", columnspan=2, padx=STATS_CANVAS_PAD_X, pady=STATS_CANVAS_PAD_Y)
        self.bar_chart_canvas.create_text(480, 50
                                          , anchor="center"
                                          , text="Κατανομή Βαθμών"
                                          , fill="white"
                                          , font="{FONT_NAME} 20")
        bar_width = 30
        max_value = max(data)
        max_height = 30 

        for j in range(len(grade_list)):
            bar_height = int(data[j] / max_value * max_height)
            x1 = j * (bar_width + 10) + 50
            y1 = 200 - bar_height
            x2 = x1 + bar_width
            y2 = 200

            self.bar_chart_canvas.create_rectangle(x1, y1, x2, y2, fill=BUTTON_COLOUR[0])

            self.bar_chart_canvas.create_text(x1 + bar_width/2
                                              , y1 - max_height/2
                                              , anchor="n"
                                              , text=str(data[j])
                                              , fill="white")
            self.bar_chart_canvas.create_text(x2 - bar_width/2
                                              , y2 + max_height/2
                                              , anchor="s"
                                              , text=str(grade_list[j])
                                              , fill="white")

        # Top performers
        self.top_performers_canvas = ctk.CTkCanvas(master=self.contents_frame
                                               , width=STATS_CANVAS_WIDTH
                                               , height=STATS_CANVAS_HEIGHT
                                               , bg = OPTIONS_FG_COLOUR[1]
                                               , highlightthickness=0)
        self.top_performers_canvas.grid(row=0, column=0, sticky="nw", padx=STATS_CANVAS_PAD_X, pady=STATS_CANVAS_PAD_Y)

        top_performers = database.top_performers(courses[i].code)
        self.top_performers_canvas.create_text(200, 50
                                             , anchor="center"
                                             , text=f"Κορυφαίοι Φοιτητές"
                                             , fill="white"
                                             , font="{FONT_NAME} 20")
        medal = ["🥇", "🥈", "🥉"]
        for tp in range(len(top_performers)):
            self.top_performers_canvas.create_text(200, 150+tp*50
                                             , anchor="center"
                                             , text=f"{medal[tp]} {top_performers[tp][0].fname} {top_performers[tp][0].lname} : {top_performers[tp][1]}"
                                             , fill="white"
                                             , font="{FONT_NAME} 16")

        
        # Success rate
        success_rate = database.course_pass_percentage(courses[i].code) * 100
    
        fail_rate = 100 - success_rate
        print(success_rate)

        self.success_rate_canvas = ctk.CTkCanvas(master=self.contents_frame
                                               , width=STATS_CANVAS_WIDTH
                                               , height=STATS_CANVAS_HEIGHT
                                               , bg = OPTIONS_FG_COLOUR[1]
                                               , highlightthickness=0)
        self.success_rate_canvas.grid(row=0, column=1, sticky="ne", padx=STATS_CANVAS_PAD_X, pady=STATS_CANVAS_PAD_Y)

        self.success_rate_canvas.create_text(200, 50
                                             , anchor="center"
                                             , text=f"Ποσοστό Επιτυχίας: {round(success_rate)}%"
                                             , fill="white"
                                             , font="{FONT_NAME} 20")
        
        if success_rate == 100:
            self.success_rate_canvas.create_oval(100, 100, 300, 300, fill=BUTTON_COLOUR[0], outline=BUTTON_COLOUR[0])
        elif success_rate == 0:
            self.success_rate_canvas.create_oval(100, 100, 300, 300, fill="grey", outline="grey")
        else:
            PieV=[success_rate, fail_rate]
            colV=[BUTTON_COLOUR[0], "grey"]
            st = 0
            coord = (100, 100, 300, 300)
            
            for val,col in zip(PieV,colV):    
                self.success_rate_canvas.create_arc(coord
                                                    , start=st
                                                    , extent = val*3.6
                                                    , fill=col
                                                    , outline=col)
                st = st + val * 3.6
            

    def top_bar_app(self):
        '''Δημιουργεί το πλαίσιο με το logo του Πανεπιστημίου, το κουμπί για αλλαγή εμφάνισης και το κουμπί αποσύνδεσης'''
        # Intro Widgets
        # Εικόνα με το λογότυπο του Πανεπιστημίου
        bgimage = ctk.CTkImage(dark_image=Image.open("images\logo_upatras.png")
                               , light_image=Image.open("images\logo_upatras.png")
                               , size=(100, 100))
        self.intro_label = ctk.CTkButton(master=self.intro_frame
                                         ,text=""
                                         , image=bgimage
                                         , command= lambda: StudentGUI.start_app(self)
                                         , hover=False
                                         , fg_color="transparent"
                                         , text_color=BUTTON_TEXT_COLOUR)
        self.intro_label.grid(row=0, column=0, sticky="w", columnspan=2)

        # Ετικέτα με το όνομα του Πανεπιστημίου
        self.intro_label2 = ctk.CTkLabel(master=self.intro_frame
                                         , text="Πανεπιστήμιο Πατρών"
                                         , font=(FONT_NAME, 50)
                                         , text_color=LABEL_TEXT_COLOUR)
        self.intro_label2.grid(row=0, column=3)

        # Κουμπί αποσύνδεσης
        sign_out_image = ctk.CTkImage(dark_image=Image.open("images\exit_dark_mode.jpg")
                                      , light_image=Image.open("images\exit_light_mode.jpg")
                                      , size=(100, 100))
        self.sign_out_button = ctk.CTkButton(master=self.intro_frame, width=INTRO_BUTTON_WIDTH, height=INTRO_BUTTON_HEIGHT
                                         , command= lambda: StudentGUI.sign_out(self, self.options_frame, self.contents_frame, self.intro_frame)
                                         , text=""
                                         , font=(FONT_NAME, FONT_SIZE_BUTTONS)
                                         , fg_color="transparent"
                                         , hover=False
                                         , image=sign_out_image
                                         , text_color=BUTTON_TEXT_COLOUR)
        self.sign_out_button.grid(row=0, column=7, sticky="w")

        # Κουμπί αλλαγής εμφάνισης
        ctk.set_appearance_mode("dark")
        self.mode = "dark"
        mode_image = ctk.CTkImage(dark_image=Image.open("images\dark.jpg")
                               , light_image=Image.open("images\light.jpg"), size=(152, 81))
        self.appearance_button = ctk.CTkButton(master=self.intro_frame, width=INTRO_BUTTON_WIDTH, height=INTRO_BUTTON_HEIGHT
                                         , command= lambda: StudentGUI.change_appearance_mode(self)
                                         , text="", font=(FONT_NAME, FONT_SIZE_BUTTONS)
                                         , image=mode_image
                                         , fg_color="transparent"
                                         , hover=False
                                         , corner_radius=CORNER_R
                                         , text_color=BUTTON_TEXT_COLOUR)
        self.appearance_button.grid(row=0, column=6,padx=(235, 0), sticky="w")


    def start_app(self):
        '''Δημιουργεί τα αρχικά widgets της εφαρμογής''' 

        print("start_app")
        StudentGUI.clear_frame(self, self.contents_frame)

        # Start Widgets
        self.intro_label = ctk.CTkLabel(master=self.contents_frame, width=100
                                        , text=f"Ακαδημαϊκό Έτος {CURRENT_YEAR-1}-{CURRENT_YEAR}"
                                        , font=(FONT_NAME, FONT_SIZE_INTRO1)
                                        , text_color=LABEL_TEXT_COLOUR)
        self.intro_label.grid(row=0, column=0, padx=200, pady=150)

        self.intro_label2 = ctk.CTkLabel(master=self.contents_frame, width=100
                                         , text="Καλωσήρθατε στο Progress 2.0!"
                                         , font=(FONT_NAME, FONT_SIZE_INTRO2)
                                         , text_color=LABEL_TEXT_COLOUR)
        self.intro_label2.grid(row=1, column=0, padx=10, pady=10)


    def kartela_app(self):
        '''Δημιουργεί το παράθυρο με την καρτέλα του φοιτητή'''

        print("kartela_app")
        StudentGUI.clear_frame(self, self.contents_frame)
        
        # Λίστα με τους τύπους στοιχείων της καρτέλας
        lst = ["Ονοματεπώνυμο", "ΑΜ", "Κινητό", "Email", "Ημερομηνία Εισαγωγής"]
        
        # Λίστα με τα στοιχεία του φοιτητή
        student_info = [self.student.fname + " " + self.student.minit + " " + self.student.lname, self.student.AM, self.student.phone, self.student.email, self.student.admission_date]
        print(student_info)

        # Ετικέτες με τα στοιχεία του φοιτητή
        for i in range(len(lst)):
            self.l = ctk.CTkLabel(master=self.contents_frame, width=100
                                  , text=lst[i]
                                  , font=(FONT_NAME, FONT_SIZE_CONTENTS)
                                  , text_color=LABEL_TEXT_COLOUR)
            self.l.grid(row=i, column=0, sticky="nw", padx=10, pady=10)

        # Πεδία εισαγωγής με τα στοιχεία του φοιτητή      
        for i in range(len(student_info)):
            entry_text = ctk.StringVar()
            self.e = ctk.CTkEntry(master=self.contents_frame, width=200, state="readonly", font=(FONT_NAME, FONT_SIZE_CONTENTS), textvariable=entry_text)
            entry_text.set(student_info[i])
            self.e.grid(row=i, column=1, sticky="nw", padx=10, pady=10)
        

    def akadhmaiko_app(self):
        '''Δημιουργεί το παράθυρο με το ακαδημαϊκό έργο του φοιτητή'''

        print("akadhmaiko_app")
        StudentGUI.clear_frame(self, self.contents_frame)
        
        # Λίστα με τους τύπους στοιχείων του ακαδημαϊκού έργου
        course_info_title = ["Εξάμηνο", "Κωδικός", "Τίτλος", "Grade", "Academic Session", "Appr.Status", "Bkg Status", "ΣΒ", "ECTS", "ΔΜ"]

        # Λίστα με τα μαθήματα του φοιτητή
        courses = database.get_students_courses(self.id)

        # Έλεγχος αν ο φοιτητής έχει δηλώσει μαθήματα
        if not courses:
            self.no_courses_label = ctk.CTkLabel(master=self.contents_frame, width=100
                                                , text="Δεν έχετε δηλώσει μαθήματα"
                                                , text_color=LABEL_TEXT_COLOUR
                                                , font=(FONT_NAME, FONT_SIZE_CONTENTS))
            self.no_courses_label.grid(row=0, column=0)
            return
        
        # Αριθμός μαθημάτων
        courses_num = len(courses)

        # Μέσος όρος
        average_grade = database.calculate_average_grade(self.id)

        # Ετικέτα με τον μέσο όρο
        self.average_grade_label = ctk.CTkLabel(master=self.contents_frame, width=40
                                                , text=f"Μέσος Όρος: {average_grade}"
                                                , text_color=LABEL_TEXT_COLOUR
                                                , font=(FONT_NAME, FONT_SIZE_CONTENTS))
        self.average_grade_label.grid(row=0, column=0, columnspan=2)

        
        # Ετικέτες/Κουμπιά με τους τύπους στοιχείων του ακαδημαϊκού έργου τα ταξινομούν τα μαθήματα αναλόγως τον τύπο
        for i in range(len(course_info_title)):
            width_ = 100

            if i == 0:
                width_ = 75

            if i == 1:
                width_ = 75
            
            if i == 2:
                width_ = 320

            if i == 3:
                width_ = 50
            
            if i == 4:
                    width_ = 110

            if i in range(7, 10):
                width_ = 40
            self.l = ctk.CTkButton(master=self.contents_frame, width=width_
                                , text=course_info_title[i]
                                , font=(FONT_NAME, FONT_SIZE_CONTENTS)
                                , fg_color= "transparent"
                                , hover_color= "grey"
                                , text_color=BUTTON_TEXT_COLOUR
                                , command= lambda i=i: StudentGUI.sort_courses(self, i))
            self.l.grid(row=1, column=i, sticky="w")

        self.entry_list = []

        # Πεδία εισαγωγής με τα στοιχεία του ακαδημαϊκού έργου
        for i in range(courses_num):

            semester = courses[i].course.semester
            code = courses[i].course.code
            title = courses[i].course.title
            grade_mark = database.calculate_course_grade(self.id, code).mark
            academic_session = "Εαρινό Εξάμηνο" if semester % 2 == 0 else "Χειμερινό Εξάμηνο"
            appr_status = database.calculate_course_grade(self.id, code).status
            bkg_status = courses[i].status
            weight = courses[i].course.weight
            ects = courses[i].course.ECTS
            credits = courses[i].course.credits
            
            course_info = [semester, code, title, grade_mark, academic_session, appr_status, bkg_status, weight, ects, credits]
            
            for j in range(len(course_info_title)):
                
                entry_text = ctk.StringVar()
                text = course_info[j]
                width_ = 100
                text_colour = TEXT_COLOUR

                if j == 0:
                    width_ = 75

                if j == 1:
                    width_ = 75

                if j == 2:
                    width_ = 320

                if j == 3:
                    width_ = 50

                    if text:
                        text_colour = "green" if grade_mark >= 5 else "red"

                    if text == -1.0:
                        text = "NS"
                        text_colour = "red"
                    
                    if text == -2.0:
                        text = ""

                if j == 4:
                    width_ = 110

                if j in range(7, 10):
                    width_ = 40
                

                entry = ctk.CTkEntry(master=self.contents_frame, width=width_, state="readonly"
                                    , font=(FONT_NAME, FONT_SIZE_CONTENTS)
                                    , textvariable=entry_text
                                    , text_color=text_colour)
                entry_text.set(text)
                self.entry_list.append(entry)
                entry.grid(row=i+2, column=j)


    def sort_courses(self, i):
        '''Ταξινομεί τα μαθήματα ανάλογα με τον τύπο'''

        print("sort_courses")
        courses = database.get_students_courses(self.id)

        if i == 0:
            courses.sort(key=lambda x: x.course.semester)
        elif i == 1:
            courses.sort(key=lambda x: x.course.code)
        elif i == 2:
            courses.sort(key=lambda x: x.course.title)
        elif i == 3:
            courses.sort(key=lambda x: database.calculate_course_grade(self.id, x.course.code).mark)
        elif i == 4:
            courses.sort(key=lambda x: x.course.semester)
        elif i == 5:
            courses.sort(key=lambda x: database.calculate_course_grade(self.id, x.course.code).status)
        elif i == 6:
            courses.sort(key=lambda x: x.status)
        elif i == 7:
            courses.sort(key=lambda x: x.course.weight)
        elif i == 8:
            courses.sort(key=lambda x: x.course.ECTS)
        elif i == 9:
            courses.sort(key=lambda x: x.course.credits)
        
        courses_num = len(courses)
        
        for i in range(courses_num):

            semester = courses[i].course.semester
            code = courses[i].course.code
            title = courses[i].course.title
            grade_mark = database.calculate_course_grade(self.id, code).mark
            academic_session = "Εαρινό Εξάμηνο" if semester % 2 == 0 else "Χειμερινό Εξάμηνο"
            appr_status = database.calculate_course_grade(self.id, code).status
            bkg_status = courses[i].status
            weight = courses[i].course.weight
            ects = courses[i].course.ECTS
            credits = courses[i].course.credits
            
            course_info = [semester, code, title, grade_mark, academic_session, appr_status, bkg_status, weight, ects, credits]

            for j in range(len(course_info)):
                text_colour = TEXT_COLOUR
                text = course_info[j]
                if j == 3:
                    if text:
                        text_colour = "green" if grade_mark >= 5 else "red"
                    if text == -1.0:
                        text = "NS"
                        text_colour = "red"
                    if text == -2.0:
                        text = ""
                        
                entry_text = ctk.StringVar()
                
                self.entry_list[i * len(course_info)+j].configure(textvariable=entry_text, text_color=text_colour)
                entry_text.set(text)


    def captcha_app(self): 
        '''Δημιουργεί το παράθυρο με το captcha'''

        print("check_captcha")
        StudentGUI.clear_frame(self, self.contents_frame)

        # Εικόνα με το captcha
        captcha = utils.Captcha(6)
   
        captcha_image = ctk.CTkImage(dark_image=captcha.image
                               , light_image=captcha.image
                               , size=(160, 60))
        captcha_label_pic = ctk.CTkLabel(master=self.contents_frame, width=100
                                         , image=captcha_image
                                         , text="")
        captcha_label_pic.grid(row=0, column=0, padx=10, pady=10)

        # Πεδίο εισαγωγής για το captcha
        captcha_entry = ctk.CTkEntry(master=self.contents_frame, width=100)
        captcha_entry.grid(row=1, column=0, padx=10, pady=10)

        # Κουμπί για ανανέωση του captcha
        captcha_reload_image = ctk.CTkImage(dark_image=Image.open("images\crefresh.png")
                                            , light_image=Image.open("images\crefresh.png")
                                            , size=(25, 25))
        captcha_reload_button = ctk.CTkButton(master=self.contents_frame, width=50, height=50
                                              , text=""
                                              , image=captcha_reload_image
                                              , command= lambda: self.captcha_app()
                                              , fg_color=BUTTON_COLOUR
                                              , hover_color=BUTTON_HOVER_COLOUR
                                              , corner_radius=CORNER_R)
        captcha_reload_button.grid(row=0, column=1)

        # Κουμπί για υποβολή του captcha
        captcha_submit_button = ctk.CTkButton(master=self.contents_frame
                                              , width=CONTENTS_BUTTON_WIDTH
                                              , height=CONTENTS_BUTTON_HEIGHT
                                              , text="Submit"
                                              , command= lambda: self.check_captcha(captcha_entry, captcha.string)
                                              , font=(FONT_NAME, FONT_SIZE_CONTENTS)
                                              , fg_color=BUTTON_COLOUR
                                              , hover_color=BUTTON_HOVER_COLOUR
                                              , corner_radius=CORNER_R
                                              , text_color=BUTTON_TEXT_COLOUR)
        captcha_submit_button.grid(row=0, column=2)


    def check_captcha(self, captcha_entry, captcha_string):
        '''Ελέγχει αν το captcha που έδωσε ο χρήστης είναι σωστό'''

        if captcha_entry.get() == captcha_string:
            print("Correct")
            StudentGUI.clear_frame(self, self.contents_frame)
            self.akadhmaiko_app()
        else:
            messagebox.showerror("Error", "Wrong captcha")
        
        

    def sign_up_to_courses(self):
        '''Δημιουργεί το παράθυρο με την δήλωση μαθημάτων'''
        print("dhlwsh_mathimatwn")
        StudentGUI.clear_frame(self, self.contents_frame)

        # Έλεγχος αν ο φοιτητής έχει δηλώσει μαθήματα
        if database.has_signed_up_to_courses(self.id, self.month):
            self.dhlwthikan_mathimata_label = ctk.CTkLabel(master=self.contents_frame, width=100
                                                       , text="Έχετε ήδη δηλώσει μαθήματα"
                                                       , font=(FONT_NAME, FONT_SIZE_CONTENTS)
                                                       , text_color=LABEL_TEXT_COLOUR)
            self.dhlwthikan_mathimata_label.grid(row=0, column=0, padx=200, pady=150)
            return

        # Ετικέτα με τα διαθέσιμα μαθήματα
        self.diathesima_mathimata_label = ctk.CTkLabel(master=self.contents_frame, width=100
                                                       , text="Διαθέσιμα Μαθήματα"
                                                       , font=(FONT_NAME, FONT_SIZE_CONTENTS)
                                                       , text_color=LABEL_TEXT_COLOUR)
        self.diathesima_mathimata_label.grid(row=0, column=0, padx=10, pady=10)

        # Λίστα με τα διαθέσιμα μαθήματα
        available_courses = database.get_students_available_courses(self.id, self.month)


        checkboxes = []

        # Checkboxes με τα διαθέσιμα μαθήματα
        for i in range(len(available_courses)):
            self.ck = ctk.CTkCheckBox(master=self.contents_frame, width=320, height=50
                                      , text=available_courses[i].title
                                      , text_color=TEXT_COLOUR)
            self.ck.grid(row=i+1, column=0, padx=10, pady=10)
            checkboxes.append(self.ck)
        
        
        # Κουμπί για την οριστική δήλωση
        self.dhlwthikan_mathimata_buttom = ctk.CTkButton(master=self.contents_frame, width=100, height=50
                                            , text="Οριστική Δήλωση"
                                            , command= lambda: self.signed_up_to_courses(checkboxes, available_courses)
                                            , font=(FONT_NAME, FONT_SIZE_CONTENTS)
                                            , fg_color=BUTTON_COLOUR
                                            , hover_color=BUTTON_HOVER_COLOUR
                                            , corner_radius=CORNER_R
                                            , text_color=BUTTON_TEXT_COLOUR)
        self.dhlwthikan_mathimata_buttom.grid(row=0, column=1, padx=10, pady=10, sticky="s")
        

    def signed_up_to_courses(self, checkboxes, mathimata):
        '''Παρουσιάζει τα μαθήματα που δήλωσε ο φοιτητής'''

        print("signed_up_to_courses")
        dhlwmena = []
        counter = -1
    
        for checkbox in checkboxes:
            counter += 1
            if checkbox.get() == 1:
                dhlwmena.append(mathimata[counter])
        dhlwmena_title = [mathima.title for mathima in dhlwmena]
        dhlwmena_code= [mathima.code for mathima in dhlwmena]

        # Έλεγχος αν ο φοιτητής έχει ξεπεράσει το όριο δήλωσης ECTS
        if not database.sign_up_to_courses(self.id, dhlwmena_code, self.semester_type):
            orio_dhlwsh_label = ctk.CTkLabel(master=self.contents_frame, width=100
                                                       , text="Ξεπεράσατε το όριο δήλωσης ECTS"
                                                       , font=(FONT_NAME, FONT_SIZE_CONTENTS)
                                                       , text_color=LABEL_TEXT_COLOUR)
            orio_dhlwsh_label.grid(row=0, column=2)

            return
        StudentGUI.clear_frame(self, self.contents_frame)

        # Ετικέτα με τα δηλωμένα μαθήματα
        self.dhlwthikan_mathimata_label = ctk.CTkLabel(master=self.contents_frame, width=100
                                                       , text="Δηλωμένα Μαθήματα:"
                                                       , font=(FONT_NAME, FONT_SIZE_CONTENTS)
                                                       , text_color=LABEL_TEXT_COLOUR)
        self.dhlwthikan_mathimata_label.grid(row=0, column=0, padx=10, pady=10)

        for i in range(len(dhlwmena)):
            self.ck = ctk.CTkLabel(master=self.contents_frame, width=100
                                   , text=dhlwmena_title[i]
                                   , font=(FONT_NAME, FONT_SIZE_CONTENTS)
                                   , text_color=LABEL_TEXT_COLOUR)
            self.ck.grid(row=i+1, column=0, padx=10, pady=10)


    def dhlwsh_kateythinshs(self):
        '''Δημιουργεί το παράθυρο με την δήλωση κατεύθυνσης'''

        print("dhlwsh_kateythinshs")
        StudentGUI.clear_frame(self, self.contents_frame)

        # Λίστα με τις διαθέσιμες κατευθύνσεις
        fos_list = database.get_all_fields_of_study()
        fos_dict = dict(zip([fos.title for fos in fos_list], fos_list))
        
        # Έλεγχος αν ο φοιτητής έχει δηλώσει κατεύθυνση
        if not database.get_field_of_study(self.id):
            self.combo_semester = ctk.CTkComboBox(master=self.contents_frame, width=300
                                            , values=[fos.title for fos in fos_list]
                                            , font=(FONT_NAME, FONT_SIZE_CONTENTS)
                                            , text_color=TEXT_COLOUR)
            self.combo_semester.grid(row=0, column=0, padx=10, pady=10)

            self.epilogh_kat = ctk.CTkButton(master=self.contents_frame, width=100, height=50
                                                , text="Επιλογή"
                                                , command= lambda: self.epilexthike_fos(fos_dict[self.combo_semester.get()])
                                                , font=(FONT_NAME, FONT_SIZE_CONTENTS)
                                                , fg_color=BUTTON_COLOUR
                                                , hover_color=BUTTON_HOVER_COLOUR
                                                , corner_radius=CORNER_R
                                                , text_color=BUTTON_TEXT_COLOUR)
            self.epilogh_kat.grid(row=0, column=1, padx=10, pady=10)
        else:
            fos_dhlwmenh_label = ctk.CTkLabel(master=self.contents_frame, width=100
                                        , text=f"Έχετε ήδη δηλώσει την κατεύθυνση:"
                                        , font=(FONT_NAME, 40)
                                        , text_color=LABEL_TEXT_COLOUR)
            fos_dhlwmenh_label.grid(row=0, column=0, padx=200, pady=150)

            fos_dhlwmenh_label2 = ctk.CTkLabel(master=self.contents_frame, width=100
                                         , text=f"{database.get_field_of_study(self.id)}"
                                         , font=(FONT_NAME, 20)
                                         , text_color=LABEL_TEXT_COLOUR)
            fos_dhlwmenh_label2.grid(row=1, column=0, padx=10, pady=10)
            

    def epilexthike_fos(self, fos):
        '''Δηλώνει την κατεύθυνση που επέλεξε ο φοιτητής'''

        print("epilexthike_kat")
        
        # Έλεγχος αν ο φοιτητής έχει δικαίωμα δήλωσης κατεύθυνσης ανάλογα το έτος εισαγωγής
        if database.can_set_field_of_study(self.id):
            StudentGUI.clear_frame(self, self.contents_frame)

            database.set_field_of_study(self.id, fos.code)

            self.dhlwthike_label = ctk.CTkLabel(master=self.contents_frame, width=100
                                                , text=f"Δήλωθηκε η Κατεύθυνση: {fos.title}"
                                                , font=(FONT_NAME, FONT_SIZE_CONTENTS)
                                                , text_color=LABEL_TEXT_COLOUR)
            self.dhlwthike_label.grid(row=0, column=0, padx=10, pady=10)
        else:
            self.dhlwthike_label = ctk.CTkLabel(master=self.contents_frame, width=100
                                                , text=f"Δεν έχετε δικαίωμα δήλωσης κατεύθυνσης ακόμα"
                                                , font=(FONT_NAME, FONT_SIZE_CONTENTS)
                                                , text_color=LABEL_TEXT_COLOUR)
            self.dhlwthike_label.grid(row=1, column=0, padx=10, pady=10)


    def dhlwsh_diplwmatikhs(self):
        '''Εμφανίζει το παράθυρο με την δήλωση διπλωματικής'''

        print("diplwmatikh")
        StudentGUI.clear_frame(self, self.contents_frame)

        # Λίστα με τις διαθέσιμες διπλωματικές
        diathesimes_dipl = [thesis.title for thesis in database.get_all_theses()]

        # Έλεγχος αν ο φοιτητής έχει δηλώσει διπλωματική
        if database.get_thesis(self.id):
            print("Exei dhlwthei diplwmatikh")
            diplwmatikh_label = ctk.CTkLabel(master=self.contents_frame, width=100
                                             , text=f"Έχετε δηλώσει την Διπλωματική\n{database.get_thesis(self.id)}"
                                             , font=(FONT_NAME, 20)
                                             , text_color=LABEL_TEXT_COLOUR)
            diplwmatikh_label.grid(row=0, column=0, padx=2, pady=150)
        else:
            self.combo_theses = ctk.CTkComboBox(master=self.contents_frame, width=300
                                            , values=diathesimes_dipl
                                            , font=(FONT_NAME, FONT_SIZE_CONTENTS)
                                            , text_color=TEXT_COLOUR)
            self.combo_theses.grid(row=0, column=0, padx=10, pady=10)

            self.select_thesis_button = ctk.CTkButton(master=self.contents_frame, width=100, height=50
                                                , text="Επιλογή", command= lambda: self.dhlwthike_diplwmatikh(self.combo_theses.get())
                                                , font=(FONT_NAME, FONT_SIZE_CONTENTS)
                                                , corner_radius=CORNER_R
                                                , fg_color=BUTTON_COLOUR
                                                , hover_color=BUTTON_HOVER_COLOUR
                                                , text_color=BUTTON_TEXT_COLOUR)
            self.select_thesis_button.grid(row=0, column=1, padx=10, pady=10)
    

    def dhlwthike_diplwmatikh(self, thesis_title):
        '''Δηλώνει την διπλωματική που επέλεξε ο φοιτητής'''

        print("dhlwthike_diplwmatikh")
        StudentGUI.clear_frame(self, self.contents_frame)
        # Λεξικό με τις διαθέσιμες διπλωματικές και του κωδικούς τους
        theses_dict = dict(zip([thesis.title for thesis in database.get_all_theses()], [thesis.code for thesis in database.get_all_theses()]))
        
        # Έλεγχος αν ο φοιτητής έχει δικαίωμα δήλωσης διπλωματικής ανάλογα το έτος εισαγωγής
        if not database.set_thesis(self.id, theses_dict[thesis_title], self.semester_type):
            self.dhlwthike_label = ctk.CTkLabel(master=self.contents_frame, width=100
                                                , text=f"Δεν έχετε δικαίωμα δήλωσης διπλωματικής ακόμα"
                                                , font=(FONT_NAME, FONT_SIZE_CONTENTS)
                                                , text_color=LABEL_TEXT_COLOUR)
            self.dhlwthike_label.grid(row=1, column=0, padx=10, pady=10)
            return
        self.dhlwthike_label = ctk.CTkLabel(master=self.contents_frame, width=100
                                            , text=f"Δήλωθηκε η Διπλωματική με τίτλο: {thesis_title}"
                                            , font=(FONT_NAME, FONT_SIZE_CONTENTS)
                                            , text_color=LABEL_TEXT_COLOUR)
        self.dhlwthike_label.grid(row=0, column=0, padx=10, pady=10)


    def sign_out(self, options_frame, contents_frame, intro_frame):
        '''Επιστρέφει στο αρχικό παράθυρο'''

        StudentGUI.clear_frame(self, intro_frame)
        intro_frame.grid_forget()
        StudentGUI.clear_frame(self, options_frame)
        options_frame.grid_forget()
        StudentGUI.clear_frame(self, contents_frame)
        contents_frame.grid_forget()
        
        self.destroy()
        app = StartUpGUI()
        app.mainloop()
    

    def change_appearance_mode(self):
        '''Αλλάζει το mode της εμφάνισης της εφαρμογής'''
        if self.mode == "dark":
            self.mode = "light"
            ctk.set_appearance_mode(self.mode)     
        else:
            self.mode = "dark"
            ctk.set_appearance_mode(self.mode)
        

    def clear_frame(self, frame):
        '''Καθαρίζει το frame'''

        for widget in frame.winfo_children():
            widget.destroy()


    def on_closing(self, event=0):
        '''Κλείνει την εφαρμογή'''

        self.destroy()

# GUI για τον καθηγητή
class AdminGUI(ctk.CTk):


    def __init__(self, username):
        super().__init__()
        self.username = username
        self.id = database.get_id_from_user(username)
        self.professor = database.get_professor(self.id)
        self.month = "FEBR"
        self.iconbitmap("images\logo.ico")
        self.configure(fg_color=WINDOW_FG_COLOUR)
        self.title("Progress 2.0")
        self.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")
        self.resizable(False,False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.main_app()
    

    def main_app(self):
        '''Δημιουργεί το βασικά πλαίσια της εφαρμογής'''
        
        # Main Frames
        self.intro_frame = ctk.CTkFrame(master=self, width=INTRO_FRAME_WIDTH, height=INTRO_FRAME_HEIGHT, fg_color=TOP_BAR_FG_COLOUR)
        self.intro_frame.grid(row=0, column=0, columnspan=2, sticky="nw")
        self.top_bar_app()

        self.options_frame = ctk.CTkFrame(master=self, width=OPTIONS_FRAME_WIDTH, height=OPTIONS_FRAME_HEIGHT, fg_color=OPTIONS_FG_COLOUR)
        self.options_frame.grid(row=1, column=0, sticky="n")
        self.options_app()
        

        self.contents_frame = ctk.CTkScrollableFrame(master=self, width=CONTENTS_FRAME_WIDTH, height=CONTENTS_FRAME_HEIGHT, fg_color=CONTENTS_FG_COLOUR)
        self.contents_frame.grid(row=1, column=1, sticky="n")

        
        
        self.start_app()

    
    def options_app(self):
        '''Δημιουργεί το παράθυρο με τις επιλογές'''

        self.kartela_button = ctk.CTkButton(master=self.options_frame, width=OPTIONS_BUTTON_WIDTH, height=OPTIONS_BUTTON_HEIGHT
                                            , text="Καρτέλα Διδάσκων"
                                            , command= lambda: AdminGUI.kartela_app(self)
                                            , font=(FONT_NAME, FONT_SIZE_BUTTONS)
                                            , fg_color=BUTTON_COLOUR
                                            , hover_color=BUTTON_HOVER_COLOUR
                                            , corner_radius=CORNER_R
                                            , text_color=BUTTON_TEXT_COLOUR)
        self.kartela_button.grid(row=0, column=0, pady=OPTIONS_PADDING)

        self.akadhmaiko_ergo_button = ctk.CTkButton(master=self.options_frame, width=OPTIONS_BUTTON_WIDTH, height=OPTIONS_BUTTON_HEIGHT
                                                    , text="Επεξεργασία Βαθμών"
                                                    , command= lambda: AdminGUI.captcha_app(self)
                                                    , font=(FONT_NAME, FONT_SIZE_BUTTONS)
                                                    , fg_color=BUTTON_COLOUR
                                                    , hover_color=BUTTON_HOVER_COLOUR
                                                    , corner_radius=CORNER_R
                                                    , text_color=BUTTON_TEXT_COLOUR)
        self.akadhmaiko_ergo_button.grid(row=1, column=0, pady=OPTIONS_PADDING)

        self.statistics_button = ctk.CTkButton(master=self.options_frame
                                                , width=OPTIONS_BUTTON_WIDTH
                                                , height=OPTIONS_BUTTON_HEIGHT
                                                 , text="Στατιστικά"
                                                 , command= lambda: AdminGUI.statistics_app(self)
                                                 , fg_color=BUTTON_COLOUR
                                                 , hover_color=BUTTON_HOVER_COLOUR
                                                 , corner_radius=CORNER_R
                                                 , text_color=BUTTON_TEXT_COLOUR
                                                 , font=(FONT_NAME, FONT_SIZE_BUTTONS))
        self.statistics_button.grid(row=3, column=0, pady=OPTIONS_PADDING)

        self.current_month_label = ctk.CTkLabel(master=self.options_frame, width=100
                                                , text="Τρέχον Μήνας"
                                                , font=(FONT_NAME, FONT_SIZE_BUTTONS)
                                                , text_color=LABEL_TEXT_COLOUR)
        self.current_month_label.grid(row=4, column=0, pady=(400, 0))

        self.months_list = ["Ιανουάριος", "Φεβρουάριος", "Μάρτιος", "Απρίλιος", "Μάιος", "Ιούνιος", "Ιούλιος", "Άυγουστος", "Σεπτέμβριος", "Οκτώβριος", "Νοέμβριος", "Δεκέμβριος"]
        self.current_month_options = ctk.CTkOptionMenu(master=self.options_frame, width=OPTIONS_BUTTON_WIDTH, height=OPTIONS_BUTTON_HEIGHT
                                            , values=self.months_list
                                            , command= self.change_current_month
                                            , font=(FONT_NAME, FONT_SIZE_LOGIN)
                                            , button_color=BUTTON_COLOUR
                                            , button_hover_color=BUTTON_HOVER_COLOUR
                                            , fg_color=BUTTON_COLOUR
                                            , corner_radius=CORNER_R
                                            , text_color=BUTTON_TEXT_COLOUR)
        self.current_month_options.grid(row=5, column=0, pady=(0, 200))


    def statistics_app(self):
        '''Δημιουργεί το παράθυρο με τα στατιστικά'''

        print("statistics")
        StudentGUI.clear_frame(self, self.contents_frame)

        semester_list = [str(i) for i in range(1, 10)]

        semester_label = ctk.CTkLabel(master=self.contents_frame, width=100
                                      , text="Εξάμηνο"
                                      , font=(FONT_NAME, FONT_SIZE_BUTTONS)
                                      , text_color=LABEL_TEXT_COLOUR)
        semester_label.grid(row=0, column=0)

        self.combo_semester = ctk.CTkComboBox(master=self.contents_frame, width=50
                                            , values=semester_list
                                            , font=(FONT_NAME, FONT_SIZE_CONTENTS)
                                            , text_color=TEXT_COLOUR)
        self.combo_semester.grid(row=0, column=1, padx=10, pady=10)

        self.choose_semester_button = ctk.CTkButton(master=self.contents_frame
                                                    , width=OPTIONS_BUTTON_WIDTH
                                                    , height=OPTIONS_BUTTON_HEIGHT
                                                    , text="Επιλογή"
                                                    , command= lambda: AdminGUI.choose_semester(self, self.combo_semester.get())
                                                    , font=(FONT_NAME, FONT_SIZE_BUTTONS)
                                                    , fg_color=BUTTON_COLOUR
                                                    , hover_color=BUTTON_HOVER_COLOUR
                                                    , corner_radius=CORNER_R
                                                    , text_color=BUTTON_TEXT_COLOUR)
        self.choose_semester_button.grid(row=2, column=0, padx=10, pady=10)
        
        
    def choose_semester(self, semester):
        '''Επιλέγει το εξάμηνο για τα στατιστικά'''

        print("choose_semester")
        StudentGUI.clear_frame(self, self.contents_frame)

        semester = int(semester)
        self.courses_by_semester = [course for course in database.get_all_courses() if course.semester == semester]
        
        buttons = []
        for i in range(len(self.courses_by_semester)):
            self.choose_course_button = ctk.CTkButton(master=self.contents_frame, width=COURSE_BUTTON_WIDTH, height=50
                                            , text=self.courses_by_semester[i].title
                                            , command= lambda i=i: AdminGUI.stats(self, self.courses_by_semester, i)
                                            , font=(FONT_NAME, FONT_SIZE_BUTTONS)
                                            , fg_color=BUTTON_COLOUR
                                            , hover_color=BUTTON_HOVER_COLOUR
                                            , corner_radius=CORNER_R
                                            , text_color=BUTTON_TEXT_COLOUR)
            self.choose_course_button.grid(row=i, column=1, padx=10, pady=10)

        
    def stats(self, courses, i):
        '''Παρουσιάζει τα στατιστικά ενός μαθήματος'''

        print("stats")
        StudentGUI.clear_frame(self, self.contents_frame)

        data = database.course_grade_bar_chart(courses[i].code)

        if not data:
            messagebox.showerror("Error", "Δεν υπάρχουν στατιστικά για αυτό το μάθημα")
            return

        # bar chart 
        grade_list = [i_/2 for i_ in range(21)]
        self.bar_chart_canvas = ctk.CTkCanvas(master=self.contents_frame
                                               , width=960
                                               , height=STATS_CANVAS_HEIGHT
                                               , bg = OPTIONS_FG_COLOUR[1]
                                               , highlightthickness=0)
        self.bar_chart_canvas.grid(row=1, column=0, sticky="s", columnspan=2, padx=STATS_CANVAS_PAD_X, pady=STATS_CANVAS_PAD_Y)
        self.bar_chart_canvas.create_text(480, 50
                                          , anchor="center"
                                          , text="Κατανομή Βαθμών"
                                          , fill="white"
                                          , font="{FONT_NAME} 20")
        bar_width = 30
        max_value = max(data)
        max_height = 30 

        for j in range(len(grade_list)):
            bar_height = int(data[j] / max_value * max_height)
            x1 = j * (bar_width + 10) + 50
            y1 = 200 - bar_height
            x2 = x1 + bar_width
            y2 = 200

            self.bar_chart_canvas.create_rectangle(x1, y1, x2, y2, fill=BUTTON_COLOUR[0])

            self.bar_chart_canvas.create_text(x1 + bar_width/2
                                              , y1 - max_height/2
                                              , anchor="n"
                                              , text=str(data[j])
                                              , fill="white")
            self.bar_chart_canvas.create_text(x2 - bar_width/2
                                              , y2 + max_height/2
                                              , anchor="s"
                                              , text=str(grade_list[j])
                                              , fill="white")

        # Top performers
        self.top_performers_canvas = ctk.CTkCanvas(master=self.contents_frame
                                               , width=STATS_CANVAS_WIDTH
                                               , height=STATS_CANVAS_HEIGHT
                                               , bg = OPTIONS_FG_COLOUR[1]
                                               , highlightthickness=0)
        self.top_performers_canvas.grid(row=0, column=0, sticky="nw", padx=STATS_CANVAS_PAD_X, pady=STATS_CANVAS_PAD_Y)

        top_performers = database.top_performers(courses[i].code)
        self.top_performers_canvas.create_text(200, 50
                                             , anchor="center"
                                             , text=f"Κορυφαίοι Φοιτητές"
                                             , fill="white"
                                             , font="{FONT_NAME} 20")
        medal = ["🥇", "🥈", "🥉"]
        for tp in range(len(top_performers)):
            self.top_performers_canvas.create_text(200, 150+tp*50
                                             , anchor="center"
                                             , text=f"{medal[tp]} {top_performers[tp][0].fname} {top_performers[tp][0].lname} : {top_performers[tp][1]}"
                                             , fill="white"
                                             , font="{FONT_NAME} 16")

        
        # Success rate
        success_rate = database.course_pass_percentage(courses[i].code) * 100
    
        fail_rate = 100 - success_rate
        print(success_rate)

        self.success_rate_canvas = ctk.CTkCanvas(master=self.contents_frame
                                               , width=STATS_CANVAS_WIDTH
                                               , height=STATS_CANVAS_HEIGHT
                                               , bg = OPTIONS_FG_COLOUR[1]
                                               , highlightthickness=0)
        self.success_rate_canvas.grid(row=0, column=1, sticky="ne", padx=STATS_CANVAS_PAD_X, pady=STATS_CANVAS_PAD_Y)

        self.success_rate_canvas.create_text(200, 50
                                             , anchor="center"
                                             , text=f"Ποσοστό Επιτυχίας: {round(success_rate)}%"
                                             , fill="white"
                                             , font="{FONT_NAME} 20")
        
        if success_rate == 100:
            self.success_rate_canvas.create_oval(100, 100, 300, 300, fill=BUTTON_COLOUR[0], outline=BUTTON_COLOUR[0])
        elif success_rate == 0:
            self.success_rate_canvas.create_oval(100, 100, 300, 300, fill="grey", outline="grey")
        else:
            PieV=[success_rate, fail_rate]
            colV=[BUTTON_COLOUR[0], "grey"]
            st = 0
            coord = (100, 100, 300, 300)
            
            for val,col in zip(PieV,colV):    
                self.success_rate_canvas.create_arc(coord
                                                    , start=st
                                                    , extent = val*3.6
                                                    , fill=col
                                                    , outline=col)
                st = st + val * 3.6


    def change_current_month(self, new_month):
        '''Αλλάζει τον τρέχοντα μήνα'''

        print("change_current_month")
        month_index = self.months_list.index(new_month)
        if 7 <= month_index <= 8: 
            self.month = "SEPT"
        elif 2 <= month_index <= 6: 
            self.month = "JUNE"
        elif month_index <= 1 or month_index >= 9: 
            self.month = "FEBR"
        print(self.month)
        self.semester_type = "Εαρινό" if self.month == "JUNE" else "Χειμερινό"
        self.start_app()
        

    def top_bar_app(self):
        '''Δημιουργεί το πλαίσιο με το logo του Πανεπιστημίου, το κουμπί για αλλαγή εμφάνισης και το κουμπί αποσύνδεσης'''

        print("top_bar")
        # Intro Widgets
        # Εικόνα με το λογότυπο του Πανεπιστημίου
        bgimage = ctk.CTkImage(dark_image=Image.open("images\logo_upatras.png")
                               , light_image=Image.open("images\logo_upatras.png")
                               , size=(100, 100))
        self.intro_label = ctk.CTkButton(master=self.intro_frame
                                         ,text=""
                                         , image=bgimage
                                         , command= lambda: StudentGUI.start_app(self)
                                         , hover=False
                                         , fg_color="transparent"
                                         , text_color=BUTTON_TEXT_COLOUR)
        self.intro_label.grid(row=0, column=0, sticky="w", columnspan=2)

        # Ετικέτα με το όνομα του Πανεπιστημίου
        self.intro_label2 = ctk.CTkLabel(master=self.intro_frame
                                         , text="Πανεπιστήμιο Πατρών"
                                         , font=(FONT_NAME, 50)
                                         , text_color=LABEL_TEXT_COLOUR)
        self.intro_label2.grid(row=0, column=3)

        # Κουμπί αποσύνδεσης
        sign_out_image = ctk.CTkImage(dark_image=Image.open("images\exit_dark_mode.jpg")
                                      , light_image=Image.open("images\exit_light_mode.jpg")
                                      , size=(100, 100))
        self.sign_out_button = ctk.CTkButton(master=self.intro_frame, width=INTRO_BUTTON_WIDTH, height=INTRO_BUTTON_HEIGHT
                                         , command= lambda: StudentGUI.sign_out(self, self.options_frame, self.contents_frame, self.intro_frame)
                                         , text=""
                                         , font=(FONT_NAME, FONT_SIZE_BUTTONS)
                                         , fg_color="transparent"
                                         , hover=False
                                         , image=sign_out_image
                                         , text_color=BUTTON_TEXT_COLOUR)
        self.sign_out_button.grid(row=0, column=7, sticky="w")

        # Κουμπί αλλαγής εμφάνισης
        ctk.set_appearance_mode("dark")
        self.mode = "dark"
        mode_image = ctk.CTkImage(dark_image=Image.open("images\dark.jpg")
                               , light_image=Image.open("images\light.jpg"), size=(152, 81))
        self.appearance_button = ctk.CTkButton(master=self.intro_frame, width=INTRO_BUTTON_WIDTH, height=INTRO_BUTTON_HEIGHT
                                         , command= lambda: StudentGUI.change_appearance_mode(self)
                                         , text="", font=(FONT_NAME, FONT_SIZE_BUTTONS)
                                         , image=mode_image
                                         , fg_color="transparent"
                                         , hover=False
                                         , corner_radius=CORNER_R
                                         , text_color=BUTTON_TEXT_COLOUR)
        self.appearance_button.grid(row=0, column=6,padx=(235, 0), sticky="w")


    def start_app(self):
        '''Εμφανίζει την αρχική σελίδα'''

        print("start_app")
        AdminGUI.clear_frame(self, self.contents_frame)

        # Start Widgets
        self.intro_label = ctk.CTkLabel(master=self.contents_frame, width=100
                                        , text=f"Ακαδημαϊκό Έτος {CURRENT_YEAR-1}-{CURRENT_YEAR}"
                                        , font=(FONT_NAME, FONT_SIZE_INTRO1)
                                        , text_color=LABEL_TEXT_COLOUR)
        self.intro_label.grid(row=0, column=0, padx=200, pady=150)

        self.intro_label2 = ctk.CTkLabel(master=self.contents_frame, width=100
                                         , text="Καλωσήρθατε στο Progress 2.0!"
                                         , font=(FONT_NAME, FONT_SIZE_INTRO2)
                                         , text_color=LABEL_TEXT_COLOUR)
        self.intro_label2.grid(row=1, column=0, padx=10, pady=10)


    def kartela_app(self):
        '''Εμφανίζει την καρτέλα του καθηγητή'''

        print("kartela_app")
        AdminGUI.clear_frame(self, self.contents_frame)
        
        lst = ["Ονοματεπώνυμο", "ΑΜ", "Κινητό", "Email", "Βαθμίδα"]
        
        professor_info = [self.professor.fname + " " + self.professor.minit + " " + self.professor.lname, self.professor.ID, self.professor.phone, self.professor.email, self.professor.bathmida]
        print(professor_info)

        for i in range(len(lst)):
            self.l = ctk.CTkLabel(master=self.contents_frame, width=100
                                  , text=lst[i]
                                  , font=(FONT_NAME, FONT_SIZE_CONTENTS)
                                  , text_color=LABEL_TEXT_COLOUR)
            self.l.grid(row=i, column=0, sticky="nw", padx=10, pady=10)
        
        for i in range(len(professor_info)):
            entry_text = ctk.StringVar()
            self.e = ctk.CTkEntry(master=self.contents_frame, width=200
                                  , state="readonly"
                                  , font=(FONT_NAME, FONT_SIZE_CONTENTS)
                                  , textvariable=entry_text)
            entry_text.set(professor_info[i])
            self.e.grid(row=i, column=1, sticky="nw", padx=10, pady=10)
    

    def captcha_app(self): 
        '''Εμφανίζει το captcha'''

        print("check_captcha")
        StudentGUI.clear_frame(self, self.contents_frame)
        captcha = utils.Captcha(6)
   
        captcha_image = ctk.CTkImage(dark_image=captcha.image
                               , light_image=captcha.image
                               , size=(160, 60))
        captcha_label_pic = ctk.CTkLabel(master=self.contents_frame, width=100
                                         , image=captcha_image
                                         , text="")
        captcha_label_pic.grid(row=0, column=0, padx=10, pady=10)

        captcha_entry = ctk.CTkEntry(master=self.contents_frame, width=100)
        captcha_entry.grid(row=1, column=0, padx=10, pady=10)

        captcha_reload_image = ctk.CTkImage(dark_image=Image.open("images\crefresh.png")
                                            , light_image=Image.open("images\crefresh.png")
                                            , size=(25, 25))
        captcha_reload_button = ctk.CTkButton(master=self.contents_frame, width=50, height=50
                                              , text=""
                                              , image=captcha_reload_image
                                              , command= lambda: self.captcha_app()
                                              , fg_color=BUTTON_COLOUR
                                              , hover_color=BUTTON_HOVER_COLOUR
                                              , corner_radius=CORNER_R)
        captcha_reload_button.grid(row=0, column=1)

        captcha_submit_button = ctk.CTkButton(master=self.contents_frame
                                              , width=CONTENTS_BUTTON_WIDTH
                                              , height=CONTENTS_BUTTON_HEIGHT
                                              , text="Submit"
                                              , command= lambda: self.check_captcha(captcha_entry, captcha.string)
                                              , font=(FONT_NAME, FONT_SIZE_CONTENTS)
                                              , fg_color=BUTTON_COLOUR
                                              , hover_color=BUTTON_HOVER_COLOUR
                                              , corner_radius=CORNER_R
                                              , text_color=BUTTON_TEXT_COLOUR)
        captcha_submit_button.grid(row=0, column=2)
    

    def check_captcha(self, captcha_entry, captcha_string):
        '''Ελέγχει αν το captcha είναι σωστό'''
        if captcha_entry.get() == captcha_string:
            print("Correct")
            AdminGUI.clear_frame(self, self.contents_frame)
            self.akadhmaiko_app()
        else:
            messagebox.showerror("Error", "Wrong captcha")
        
        


    def akadhmaiko_app(self):
        '''Εμφανίζει τα μαθήματα που διδάσκει ο καθηγητής ανάλογα την εξεταστική περίοδο'''
        print("akadhmaiko_app")
        AdminGUI.clear_frame(self, self.contents_frame)

        self.mathimata_pou_didaskei_label = ctk.CTkLabel(master=self.contents_frame, width=100
                                                         , text_color=LABEL_TEXT_COLOUR
                                                         , text="Μαθήματα που διδάσκεται:")
        self.mathimata_pou_didaskei_label.grid(row=0, column=0, padx=10, pady=10)

        # Επιλογή Μαθημάτων που έχει αναλάβει ο καθηγητής ανάλογα την εξεταστική περίοδο
        if self.month == 'SEPT':
            professor_courses = database.get_professors_courses(self.id)
        elif self.month == 'FEBR':
            professor_courses = [professor_course for professor_course in database.get_professors_courses(self.id) if professor_course.course.semester % 2]
        elif self.month == 'JUNE':
            professor_courses = [professor_course for professor_course in database.get_professors_courses(self.id) if not professor_course.course.semester % 2]
        
        

        AdminGUI.clear_frame(self, self.contents_frame)


        for i in range(len(professor_courses)):
            self.b = ctk.CTkButton(master=self.contents_frame, width=COURSE_BUTTON_WIDTH, height=50
                                            , text=f"{professor_courses[i].course.title}"
                                            , command= lambda i=i: AdminGUI.epilogh_drasthriothtas_app(self, i, professor_courses)
                                            , font=(FONT_NAME, FONT_SIZE_CONTENTS)
                                            , fg_color=BUTTON_COLOUR
                                            , hover_color=BUTTON_HOVER_COLOUR
                                            , corner_radius=CORNER_R
                                            , text_color=BUTTON_TEXT_COLOUR)
            self.b.grid(row=i, column=0, padx=10, pady=10)

        
    def epilogh_drasthriothtas_app(self, i, professor_courses):
        '''Εμφανίζει τις δραστηριότητες του μαθήματος'''

        print("epilogh_drasthriothtas_app")
        AdminGUI.clear_frame(self, self.contents_frame)

        course = professor_courses[i].course
        activities = professor_courses[i].activities

        self.course_label = ctk.CTkLabel(master=self.contents_frame, width=100
                                         , text=f"{course.title}"
                                         , text_color=LABEL_TEXT_COLOUR
                                         , font=(FONT_NAME, FONT_SIZE_CONTENTS))
        self.course_label.grid(row=0, column=0, padx=2, pady=2, columnspan=4)

        for i in range(len(activities)):
            self.b = ctk.CTkButton(master=self.contents_frame, width=COURSE_BUTTON_WIDTH, height=50
                                            , text=activities[i].title
                                            , command= lambda i=i: AdminGUI.eggegramenoi_foithtes_app(self, course, activities[i])
                                            , font=(FONT_NAME, FONT_SIZE_CONTENTS)
                                            , fg_color=BUTTON_COLOUR
                                            , hover_color=BUTTON_HOVER_COLOUR
                                            , corner_radius=CORNER_R
                                            , text_color=BUTTON_TEXT_COLOUR)
            self.b.grid(row=i+1, column=0, padx=10, pady=10)
            
    
    def eggegramenoi_foithtes_app(self, course, activity):
        '''Εμφανίζει τους εγγεγραμμένους φοιτητές στη δραστηριότητα'''

        print("eggegramenoi_foithtes_app")
        AdminGUI.clear_frame(self, self.contents_frame)
        
        foithtes = database.get_students_by_course(course.code)
        if not foithtes:
            self.course_label = ctk.CTkLabel(master=self.contents_frame, width=100
                                         , text=f"Δεν υπάρχουν εγγεγραμμένοι φοιτητές στο μάθημα {course.title} {activity.title}"
                                         , font=(FONT_NAME, FONT_SIZE_CONTENTS)
                                         , text_color=LABEL_TEXT_COLOUR)
            self.course_label.grid(row=0, column=0, padx=200, pady=150)
            return
        
        
        self.course_label = ctk.CTkLabel(master=self.contents_frame, width=100
                                            , text=f"Μάθημα:   {course.title}\nΔραστηριότητα:   {activity.title}"
                                            , font=(FONT_NAME, FONT_SIZE_CONTENTS) 
                                            , text_color=LABEL_TEXT_COLOUR)
        self.course_label.grid(row=0, column=0, padx=10, pady=20)

        stoixeia = ["Ονοματεπώνυμο", "ΑΜ", "Βαθμός"]

        self.pedia_bathmou = []

        for stoixeio in stoixeia:
            self.stoixeio_label = ctk.CTkLabel(master=self.contents_frame, width=100
                                               , text_color=LABEL_TEXT_COLOUR
                                               , text=stoixeio)
            self.stoixeio_label.grid(row=2, column=stoixeia.index(stoixeio), padx=2, pady=2)

        for i in range(len(foithtes)):
            self.name_label = ctk.CTkLabel(master=self.contents_frame, width=100
                                           , text_color=LABEL_TEXT_COLOUR
                                           , text=f"{foithtes[i].fname} {foithtes[i].minit} {foithtes[i].lname}")
            self.name_label.grid(row=i+3, column=0, sticky="nw", padx=2, pady=2)
            
            self.l_am = ctk.CTkLabel(master=self.contents_frame, width=100
                                     , text_color=LABEL_TEXT_COLOUR
                                     , text=f"{foithtes[i].AM}")
            self.l_am.grid(row=i+3, column=1, sticky="nw", padx=2, pady=2)

            entry_text = ctk.StringVar()
            self.pedio_bathmou = ctk.CTkEntry(master=self.contents_frame, width=100, textvariable=entry_text)

            grade = database.get_grade(foithtes[i].AM, activity.activity_code, self.month)
            
            
             
            if not grade:
                entry_text.set("")
            else:
                if grade.mark == -1.0: 
                    entry_text.set("NS")
                else: 
                    entry_text.set(grade.mark)
                
                if "Τελικό" in grade.status:
                    self.pedio_bathmou.configure(state="readonly")

            
            
            self.pedio_bathmou.grid(row=i+3, column=2, sticky="nw", padx=2, pady=2)
            self.pedia_bathmou.append(self.pedio_bathmou)


        self.apothikeysh_button = ctk.CTkButton(master=self.contents_frame, width=100, height=50
                                                             , text="Αποθήκευση Βαθμών"
                                                             , command= lambda: AdminGUI.save_grade(self, foithtes, activity)
                                                             , corner_radius=20
                                                             , fg_color=BUTTON_COLOUR
                                                             , hover_color=BUTTON_HOVER_COLOUR
                                                             , font=(FONT_NAME, FONT_SIZE_CONTENTS)
                                                             , text_color=BUTTON_TEXT_COLOUR)
        self.apothikeysh_button.grid(row=0, column=3)


    def save_grade(self, foithtes, activity): 
        '''Αποθηκεύει τους βαθμούς της δραστηριότητας ως προσωρνινούς'''

        print("save_grade_app")  
        
        # Αποθήκευση βαθμών στη βάση δεδομένων ως προσωρινούς
        for i, pedio_bathmou in enumerate(self.pedia_bathmou):
            
            if not pedio_bathmou.get():
                print("not pedio_bathmou.get()")
                database.set_grade(foithtes[i].AM, activity.activity_code, -1.0, self.month)
            else:
                try:
                    if float(pedio_bathmou.get()) > 10 or float(pedio_bathmou.get()) < 0:
                        messagebox.showerror("Error", "Ο βαθμός πρέπει να είναι από 0 έως 10!")
                        return
                    database.set_grade(foithtes[i].AM, activity.activity_code, float(pedio_bathmou.get()), self.month)
            
                except:
                    messagebox.showerror("Error", "Ο βαθμός πρέπει να είναι αριθμός!")
                    return 
                
        self.saved_label = ctk.CTkLabel(master=self.contents_frame, width=100
                                        , text="Οι βαθμοί αποθηκεύτηκαν!"
                                        , font=(FONT_NAME, FONT_SIZE_CONTENTS)
                                        , text_color=LABEL_TEXT_COLOUR)
        self.saved_label.grid(row=2, column=3)

        self.finalize_button = ctk.CTkButton(master=self.contents_frame, width=100, height=50
                                             , text="Οριστικοποίηση Βαθμών"
                                             , command= lambda: AdminGUI.finalize_grades(self, activity)
                                             , corner_radius=CORNER_R
                                             , fg_color=BUTTON_COLOUR
                                             , hover_color=BUTTON_HOVER_COLOUR
                                             , font=(FONT_NAME, FONT_SIZE_CONTENTS)
                                             , text_color=BUTTON_TEXT_COLOUR)
        self.finalize_button.grid(row=0, column=4)
    

    def finalize_grades(self, activity):
        '''Οριστικοποιεί τους βαθμούς της δραστηριότητας'''

        print("finalize_grades")

        # Οριστικοποίηση βαθμών στη βάση δεδομένων
        database.finalize_grades(activity.activity_code, self.month)

        self.finalized_label = ctk.CTkLabel(master=self.contents_frame, width=100
                                        , text="Οι βαθμοί οριστικοποιήθηκαν!"
                                        , font=(FONT_NAME, FONT_SIZE_CONTENTS)
                                        , text_color=LABEL_TEXT_COLOUR)
        self.finalized_label.grid(row=2, column=4)


    def sign_out(self, options_frame, contents_frame, intro_frame):
        '''Επιστρέφει στο αρχικό παράθυρο'''

        AdminGUI.clear_frame(self, intro_frame)
        intro_frame.grid_forget()
        AdminGUI.clear_frame(self, options_frame)
        options_frame.grid_forget()
        AdminGUI.clear_frame(self, contents_frame)
        contents_frame.grid_forget()
        
        self.destroy()
        app = StartUpGUI()
        app.mainloop()


    def change_appearance_mode(self):
        '''Αλλάζει το mode της εμφάνισης της εφαρμογής'''

        if self.mode == "dark":
            self.mode = "light"
            ctk.set_appearance_mode(self.mode)     
        else:
            self.mode = "dark"
            ctk.set_appearance_mode(self.mode)


    def clear_frame(self, frame):
        '''Καθαρίζει το frame'''

        for widget in frame.winfo_children():
            widget.destroy()


    def on_closing(self, event=0):
        '''Κλείνει την εφαρμογή'''

        self.destroy()




if __name__ == '__main__':

    app = StartUpGUI()
    app.mainloop()
