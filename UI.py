import tkinter as tk
from tkinter import messagebox, Label, Toplevel
from tkinter import ttk
from statsandgraphs import *
import json, random
from PIL import Image, ImageTk

class UserData:
    def __init__(self):
        self.first = ""
        self.last = ""
        self.password = ""
        self.daily_budget = 0
        self.weekly_budget = 0
        self.monthly_budget = 0
        self.load_profile_data()

    def load_profile_data(self):
        try:
            with open('config.json', 'r') as file:
                config = json.load(file)
                user_data = config.get('user', {})
                self.first = user_data.get("first", "")
                self.last = user_data.get("last", "")
                self.password = user_data.get("password", "")
                self.daily_budget = user_data.get("daily_budget", 0)
                self.weekly_budget = user_data.get("weekly_budget", 0)
                self.monthly_budget = user_data.get("monthly_budget", 0)
        except FileNotFoundError:
            print("config.json not found, running with default user data.")

    def edit_profile_data(self, key, new_value):
        with open('config.json', 'r+') as file:
            config = json.load(file)
            config['user'][key] = new_value
            file.seek(0)
            json.dump(config, file, indent=4)
            file.truncate()

class LoginPage(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Pynance: Personal Edition")
        self.iconbitmap("assets/icon.ico")
        self.geometry("400x400")
        self.resizable(0, 0)

        # Michaelsoft Windows styling
        style = ttk.Style()
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10))
        style.configure("TEntry", font=("Segoe UI", 10))
        style.configure("LabelFrame", font=("Segoe UI", 12))

        # load available data
        self.userdata = UserData()

        # logo
        original_image = Image.open("assets/logo.png")
        resized_image = original_image.resize((200, 75))
        self.logo_image = ImageTk.PhotoImage(resized_image)
        
        img_label = Label(self, image=self.logo_image)
        img_label.pack(pady=(30, 0))


        # Welcome label
        self.welcome_label = tk.Label(self, text="Welcome!", font=("Segoe UI", 12))
        self.welcome_label.pack(pady=(0, 20))

        # Password Frame
        self.password_frame = ttk.LabelFrame(self, text=" Login ")
        self.password_frame.pack(pady=10, padx=50, fill="x")

        # Password Entry
        self.entry_pw = ttk.Entry(self.password_frame, show="*", width=22)
        self.entry_pw.grid(row=0, column=0, pady=(10, 10), padx=(20, 0))
        
        # Show Password Toggle
        self.show_password = tk.BooleanVar()
        self.show_password_toggle = ttk.Checkbutton(self.password_frame, text="Show Password", 
                                                    variable=self.show_password, command=self.toggle_password_show)
        self.show_password_toggle.grid(row=1, column=0, padx=20)

        # Login Button
        self.login_btn = ttk.Button(self.password_frame, text="Login", command=self.validate_login)
        self.login_btn.grid(row=0, column=1, pady=10, padx=10)

        # Registration Frame
        self.registration_frame = ttk.LabelFrame(self, text=" Not you? ")
        self.registration_frame.pack(pady=10, padx=50, fill="x")

        # Registration Label and Button
        self.register_label = ttk.Label(self.registration_frame, text="Register an Account")
        self.register_label.grid(row=0, column=0, padx=20, pady=10)
        self.register_btn = ttk.Button(self.registration_frame, text="Register", command= lambda: RegistrationForm(self))
        self.register_btn.grid(row=0, column=1, padx=10, pady=10)

    def toggle_password_show(self):
        """Toggle the visibility of the password in the entry widget."""
        if self.show_password.get():
            self.entry_pw.config(show="")
        else:
            self.entry_pw.config(show="*")

    def validate_login(self):
        """Validate the entered password against stored credentials."""
        entered_password = self.entry_pw.get()
        if entered_password == self.userdata.password:
            messagebox.showinfo("Login Successful", f"Welcome {self.userdata.first}!")
            self.open_main_app()
        else:
            messagebox.showerror("Login Failed", "Incorrect password.")

    def open_main_app(self):
        self.destroy()
        app = MyApp(self.userdata)
        app.mainloop()  

class RegistrationForm(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Registration")
        self.iconbitmap("assets/icon.ico")
        self.geometry("350x400")
        
        # Use Segoe UI font for the Windows look
        style = ttk.Style(self)
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10))
        style.configure("TEntry", font=("Segoe UI", 10))
        style.configure("LabelFrame", font=("Segoe UI", 12))

        # Name Section
        name_frame = ttk.LabelFrame(self, text=" Name ")
        name_frame.place(x=20, y=20, width=310, height=100)

        # Password Section
        password_frame = ttk.LabelFrame(self, text=" Password ")
        password_frame.place(x=20, y=130, width=310, height=70)

        # Budgets Section
        budgets_frame = ttk.LabelFrame(self, text=" Budgets ")
        budgets_frame.place(x=20, y=210, width=310, height=130)

        self.entries = {}
        field_locations = {
            "First Name": (name_frame, 0),
            "Last Name": (name_frame, 1),
            "Password": (password_frame, 0),
            "Daily Budget": (budgets_frame, 0),
            "Weekly Budget": (budgets_frame, 1),
            "Monthly Budget": (budgets_frame, 2)
        }

        for field, (frame, index) in field_locations.items():
            ttk.Label(frame, text=field).grid(row=index, column=0, sticky="w", padx=5, pady=5)
            entry_var = tk.StringVar()
            entry = ttk.Entry(frame, textvariable=entry_var, width=25)
            entry.grid(row=index, column=1, padx=5, pady=5)
            self.entries[field] = entry_var

        # Submit button
        ttk.Button(self, text="Register", command=self.save_config).place(x=125, y=350)


    def save_config(self):
        user_data = {
            "user": {
                "first": self.entries["First Name"].get(),
                "last": self.entries["Last Name"].get(),
                "password": self.entries["Password"].get(),
                "daily_budget": self.entries["Daily Budget"].get(),
                "weekly_budget": self.entries["Weekly Budget"].get(),
                "monthly_budget": self.entries["Monthly Budget"].get(),
                "pwd": self.entries["Password"].get(),
                "budget_d": self.entries["Daily Budget"].get(),
                "budget_w": self.entries["Weekly Budget"].get(),
                "budget_m": self.entries["Monthly Budget"].get()
            }
        }
        
        # Write to config.json
        with open("config.json", "w") as file:
            json.dump(user_data, file, indent=4)
        
        messagebox.showinfo("Success", "Registration successful!")
        
        # Clear the form
        for entry in self.entries.values():
            entry.set("")

class MenuBar(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent)

        menu_dashboard = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Dashboard", menu=menu_dashboard)
        menu_dashboard.add_command(label="Profile", command=lambda: parent.show_frame("Dashboard"))
        menu_dashboard.add_separator()
        menu_dashboard.add_command(label="Exit Application", command=parent.Quit_application)

        # Sheets menu
        menu_sheets = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Sheets", menu=menu_sheets)
        menu_sheets.add_command(label="Page One", command=lambda: parent.show_frame("Some_Widgets"))

        # Notes menu
        menu_notes = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Notes", menu=menu_notes)
        menu_notes.add_command(label="Page One", command=lambda: parent.show_frame("PageTwo"))

        # Settings menu
        menu_settings = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Settings", menu=menu_settings)
        menu_settings.add_command(label="Page One", command=lambda: parent.show_frame("PageTwo"))

class MyApp(tk.Tk):
    def __init__(self, userdata):
        super().__init__()
        self.title("Pynance: Personal Edition")
        self.geometry("1300x600")
        self.iconbitmap("assets/icon.ico")
        self.userdata = userdata

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')

        self.dashboard_tab = Dashboard(self.notebook, self, userdata)
        self.sheets_tab = Sheets(self.notebook, self, userdata)
        self.notes_tab = Notes(self.notebook, self, userdata)
        self.settings_tab = Settings(self.notebook, self, userdata)

        self.notebook.add(self.dashboard_tab, text='Dashboard')
        self.notebook.add(self.sheets_tab, text='Sheets')
        self.notebook.add(self.notes_tab, text='Notes')
        self.notebook.add(self.settings_tab, text='Settings')

        # Start at the Dashboard tab
        self.notebook.select(self.dashboard_tab)


class GUI(tk.Frame):
    def __init__(self, parent, controller, userdata=None):
        super().__init__(parent)
        self.controller = controller
        self.userdata = userdata
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill="both", expand=True)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)


class Dashboard(GUI):
    def __init__(self, parent, controller, userdata):
        super().__init__(parent, controller, userdata)

        # start generating those graphs
        self.graphs = Graphs()

        # Add content to the main_frame
        self.header_label = ttk.Label(self.main_frame, text="Dashboard", font=("Segoe UI", 16))
        self.header_label.pack(side="top", pady=(10, 20))

        # Assuming BudgetManager is defined correctly and imported
        stats = BudgetManager()
        self.daily_budget_balance = stats.daily_budget_balance
        self.weekly_budget_balance = stats.weekly_budget_balance
        self.monthly_budget_balance = stats.monthly_budget_balance
        self.annual_budget_balance = stats.annual_budget_balance
        
        # Sample greetings
        greetings = [
            "Hello, {}! Welcome back!",
            "Greetings, {}! Good to see you.",
            "{}! Hope you're doing well today.",
            "What's up, {}? Here's your stats.",
            "Hey {}, check out your latest stats!",
            "Welcome, {}! Your stats await."
        ]

        greeting_message = random.choice(greetings).format(userdata.first)

        # Header with greeting, placed in the main frame
        self.header_label = ttk.Label(self.main_frame, text=greeting_message, font=("Segoe UI", 16))
        self.header_label.pack(side="top", pady=(10, 20))

        # Frames for daily, weekly, monthly, and annual statistics placed in the main frame
        #self.create_stats_frame(f"Daily Budget Balance: {self.daily_budget_balance}", "View Daily Image", lambda: self.view_graph("daily"))
        self.create_stats_frame(f"Weekly Budget Balance: {self.weekly_budget_balance}", "View Weekly Image", lambda: self.view_graph("weekly"))
        self.create_stats_frame(f"Monthly Budget Balance: {self.monthly_budget_balance}", "View Monthly Graph", lambda: self.view_graph("monthly"))
        self.create_stats_frame(f"Annual Budget Balance: {self.annual_budget_balance}", "View Annual Graph", lambda: self.view_graph("annual"))

    def create_stats_frame(self, frame_title, button_text, command):
        frame = ttk.Frame(self.main_frame)
        frame.pack(side="left", padx=20, pady=10, fill="x", expand=True)

        ttk.Label(frame, text=frame_title, font=("Segoe UI", 14)).pack(side="top", fill="x", pady=(0, 10))
        ttk.Button(frame, text=button_text, command=command).pack(side="top")
    
    def view_graph(self, period):
        image_path = f"graphs/line_{period}.png"

        popout = Toplevel(self)
        popout.title(f"{period.capitalize()} Graph")
        
        # Load and display the image
        img = Image.open(image_path)
        img = img.resize((600, 300))
        photo = ImageTk.PhotoImage(img)

        label = Label(popout, image=photo)
        label.image = photo
        label.pack()

class Notes(GUI):
    def __init__(self, parent, controller, userdata):
        super().__init__(parent, controller, userdata)
        
        self.header_label = ttk.Label(self.main_frame, text="Notes", font=("Segoe UI", 16))
        self.header_label.pack(side="top", pady=(10, 20), padx=20)

        self.left_frame = ttk.Frame(self.main_frame)
        self.left_frame.pack(side="left", fill="y", padx=10, expand=False)

        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10)

        self.notes_listbox = tk.Listbox(self.left_frame, width=40, height=20)
        self.notes_listbox.pack(padx=10, pady=10, fill="y", expand=False)
        self.notes_listbox.bind("<<ListboxSelect>>", self.load_selected_note)

        self.title_entry = ttk.Entry(self.right_frame, font=("Segoe UI", 10))
        self.title_entry.pack(fill="x", expand=False, padx=20, pady=(0, 10))

        self.description_text = tk.Text(self.right_frame, wrap="word", font=("Segoe UI", 10))
        self.description_text.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        scrollb = ttk.Scrollbar(self.right_frame, command=self.description_text.yview)
        scrollb.pack(side="right", fill="y", expand=False)
        self.description_text['yscrollcommand'] = scrollb.set

        self.button_frame = ttk.Frame(self.right_frame)
        self.button_frame.pack(fill="x", expand=False, padx=20, pady=10)

        self.save_button = ttk.Button(self.button_frame, text="Save", command=self.save_note)
        self.save_button.pack(side="left", padx=10)
        self.discard_button = ttk.Button(self.button_frame, text="Discard Current Note", command=self.discard_note)
        self.discard_button.pack(side="left", padx=10)
        self.new_note_button = ttk.Button(self.button_frame, text="New Note", command=self.new_note)
        self.new_note_button.pack(side="left", padx=10)

        self.load_notes()

    def new_note(self):
        self.title_entry.delete(0, tk.END)
        self.description_text.delete("1.0", tk.END)

    def save_note(self):
        title = self.title_entry.get()
        description = self.description_text.get("1.0", tk.END).strip()
        if title and description:
            with open('notes.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([title, description])
            messagebox.showinfo("Success", "Note saved successfully.")
            self.load_notes()
        else:
            messagebox.showwarning("Warning", "Title and description cannot be empty.")

    def load_notes(self):
        self.notes_listbox.delete(0, tk.END)
        try:
            with open('notes.csv', 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.notes_listbox.insert(tk.END, row['title'])
        except FileNotFoundError:
            with open('notes.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=['title', 'description'])
                writer.writeheader()

    def load_selected_note(self, event):
        selection = self.notes_listbox.curselection()
        if selection:
            index = selection[0]
            with open('notes.csv', 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                rows = list(reader)
                if index < len(rows):
                    title = rows[index]['title']
                    description = rows[index]['description']
                    self.title_entry.delete(0, tk.END)
                    self.title_entry.insert(0, title)
                    self.description_text.delete("1.0", tk.END)
                    self.description_text.insert(tk.END, description)

    def discard_note(self):
        if messagebox.askyesno("Discard Note", "Are you sure you want to discard the changes?"):
            self.load_selected_note(None)

class Sheets(GUI):
    def __init__(self, parent, controller, userdata):
        super().__init__(parent, controller, userdata)

        self.entry_container = ttk.Frame(self.main_frame)
        self.entry_container.pack(fill="x", pady=10)
        self.new_entry_label = tk.Label(self.entry_container, text="Add a new entry", font=("Segoe UI", 10))
        self.new_entry_label.pack()
        self.entries_frame = ttk.Frame(self.entry_container)
        self.entries_frame.pack(fill='x', expand=True)

        # Entry fields creation loop
        fields = [('Name', 'name'), ('Amount', 'amount'), ('Date', 'date'), ('Description', 'description')]
        for field, attr in fields:
            frame = ttk.Frame(self.entries_frame)
            frame.pack(side=tk.LEFT, padx=5, fill='x', expand=True)
            tk.Label(frame, text=field).pack(side=tk.TOP, fill='x')
            setattr(self, 'entry_' + attr, tk.Entry(frame))
            getattr(self, 'entry_' + attr).pack(side=tk.TOP, fill='x')

        self.add_button = tk.Button(self.entries_frame, text="Add", command=self.add_data)
        self.add_button.pack(side=tk.LEFT, padx=10, pady=2)


        # Treeview
        self.tree = None
        self.load_csv('sheet.csv')

    def load_csv(self, csv_file_path):
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            self.data = list(reader)
            self.display_data()

    def display_data(self):
        if self.tree:
            self.tree.destroy()

        self.tree = ttk.Treeview(self.main_frame, columns=list(self.data[0].keys()), show='headings')
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        for col in self.data[0].keys():
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_by(c, False))
            self.tree.column(col, width=100)

        for item in self.data:
            self.tree.insert('', 'end', values=list(item.values()))

    def sort_by(self, col, descending):
        """ Sort tree contents when a column header is clicked on. """
        data_list = [(self.tree.set(child_id, col), child_id) for child_id in self.tree.get_children('')]
        
        # Change the data type based on the column header
        if col == 'date':
            data_list.sort(key=lambda x: datetime.strptime(x[0], '%Y-%m-%d'), reverse=descending)
        elif col == 'amount':
            data_list.sort(key=lambda x: float(x[0].replace(',', '').replace('$', '')), reverse=descending)

        for index, (val, k) in enumerate(data_list):
            self.tree.move(k, '', index)

        self.tree.heading(col, command=lambda c=col: self.sort_by(c, not descending))

    def add_data(self):
        name = self.entry_name.get()
        amount = self.entry_amount.get()
        date = self.entry_date.get()
        description = self.entry_description.get()

        with open("sheet.csv", "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, amount, date, description])

        self.tree.insert("", tk.END, values=(name, amount, date, description))

        # regen graphs with updated data
        self.graphs = Graphs()
        self.stats = BudgetManager()


class Settings(GUI):
    def __init__(self, parent, controller, userdata):
        super().__init__(parent, controller, userdata)

        self.header_label = ttk.Label(self.main_frame, text="Settings", font=("Segoe UI", 16))
        self.header_label.pack(side="top", pady=(10, 20))

        name_frame = ttk.LabelFrame(self.main_frame, text=" Name ")
        name_frame.pack(padx=10, pady=5, fill="x")

        ttk.Label(name_frame, text="First Name").pack(side="left", padx=10, pady=5)
        self.first_name_var = tk.StringVar(value=userdata.first)
        ttk.Entry(name_frame, textvariable=self.first_name_var).pack(side="left", padx=10, pady=5)

        ttk.Label(name_frame, text="Last Name").pack(side="left", padx=10, pady=5)
        self.last_name_var = tk.StringVar(value=userdata.last)
        ttk.Entry(name_frame, textvariable=self.last_name_var).pack(side="left", padx=10, pady=5)

        # Budgets Section
        budgets_frame = ttk.LabelFrame(self.main_frame, text=" Budgets ")
        budgets_frame.pack(padx=10, pady=5, fill="x")

        budgets = [
            ("Daily Budget", userdata.daily_budget, "daily_budget"),
            ("Weekly Budget", userdata.weekly_budget, "weekly_budget"),
            ("Monthly Budget", userdata.monthly_budget, "monthly_budget")
        ]

        for i, (label, value, key) in enumerate(budgets):
            frame = ttk.Frame(budgets_frame)
            frame.pack(fill="x")
            ttk.Label(frame, text=label).pack(side="left", padx=10, pady=5)
            var = tk.StringVar(value=value)
            ttk.Entry(frame, textvariable=var).pack(side="left", padx=10, pady=5)
            setattr(self, key + "_var", var)

        # Password Section
        pwd_frame = ttk.LabelFrame(self.main_frame, text=" Change Password ")
        pwd_frame.pack(padx=10, pady=5, fill="x")

        ttk.Label(pwd_frame, text="Old Password").pack(side="left", padx=10, pady=5)
        self.old_password_var = tk.StringVar()
        ttk.Entry(pwd_frame, textvariable=self.old_password_var, show="*").pack(side="left", padx=10, pady=5)

        ttk.Label(pwd_frame, text="New Password").pack(side="left", padx=10, pady=5)
        self.new_password_var = tk.StringVar()
        ttk.Entry(pwd_frame, textvariable=self.new_password_var, show="*").pack(side="left", padx=10, pady=5)

        # Save Button
        save_button = ttk.Button(self.main_frame, text="Save", command=self.save_profile_data)
        save_button.pack(pady=10)

    def save_profile_data(self):
        
        if self.old_password_var.get() != self.user_profile.pwd:
            tk.messagebox.showwarning("Error", "Old password is incorrect.")
            return
    
        if self.new_password_var.get():
            self.user_profile.edit_profile_data("password", self.new_password_var.get())

        # Update name and budgets
        self.user_profile.edit_profile_data("first", self.first_name_var.get())
        self.user_profile.edit_profile_data("last", self.last_name_var.get())
        self.user_profile.edit_profile_data("daily_budget", self.daily_budget_var.get())
        self.user_profile.edit_profile_data("weekly_budget", self.weekly_budget_var.get())
        self.user_profile.edit_profile_data("monthly_budget", self.monthly_budget_var.get())

        tk.messagebox.showinfo("Success", "Profile updated successfully.")


if __name__ == "__main__":
    login_page = LoginPage()
    login_page.mainloop()
