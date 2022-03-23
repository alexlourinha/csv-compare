import tkinter as tk
from tkinter.filedialog import askopenfilename
import os
import csv
import tempfile

script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
image_path = os.path.join(script_dir, "looking_glass.png")


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        root.geometry("400x400")
        self.file1 = ''
        self.file2 = ''
        self.pack()
        self.master = master
        self.create_ui()
        self.results_btn = tk.Button(self, text="Open results", fg="orange")
        self.results = ''
        self.results_color = ''
        self.results_label = tk.Label(self, text='')
        self.browse_label1_file = tk.Label(self, text="")
        self.browse_label2_file = tk.Label(self, text="")

    def open_results(self):
        os.system(f"open -a 'Microsoft Excel.app' {self.results}")

    def browse_file1(self):
        filename1 = askopenfilename()
        self.file1 = filename1
        self.browse_label1_file.destroy()
        self.browse_label1_file = tk.Label(self, text=filename1)
        self.browse_label1_file.place(relx=.5, rely=.3, anchor="c")

    def browse_file2(self):
        filename2 = askopenfilename()
        self.file2 = filename2
        self.browse_label2_file.destroy()
        self.browse_label2_file = tk.Label(self, text=filename2)
        self.browse_label2_file.place(relx=.5, rely=.5, anchor="c")

    def generate_op(self):

        self.results_label.destroy()
        diff_lines = []

        with open(self.file1, 'r') as t1, open(self.file2, 'r') as t2:
            file_one = t1.readlines()
            file_two = t2.readlines()

        handle, fn = tempfile.mkstemp(suffix='.csv')
        with os.fdopen(handle, "w", encoding='utf8') as f:
            writer = csv.writer(f)
            reader1 = csv.reader(file_one)
            reader2 = csv.reader(file_two)
            for row in reader2:
                if row not in reader1:
                    diff_lines.append(row)
                    writer.writerow(row)
            for row in reader1:
                if row not in reader2:
                    diff_lines.append(row)
                    writer.writerow(row)

        self.results = fn

        error = "Files are not identical. There are " + str(len(diff_lines)) + \
                " different lines"
        success = "Files are identical"

        if len(diff_lines) > 0:
            self.results_btn = tk.Button(self, text="Open results", fg="orange")
            self.results_btn.place(relx=.5, rely=.8, anchor="c")
            self.results_btn["command"] = self.open_results
            self.results_label = tk.Label(self, text=error, fg='red')
            self.results_label.place(relx=.5, rely=.7, anchor="c")
        else:
            self.results_btn.destroy()
            self.results_label = tk.Label(self, text=success, fg='green')
            self.results_label.place(relx=.5, rely=.7, anchor="c")

    def create_ui(self):
        browse_label1 = tk.Label(self, text="Original CSV File:")
        browseb1 = tk.Button(self)
        browseb1["text"] = "Browse File"
        browseb1["command"] = self.browse_file1
        browseb1.grid(row=3, column=1)
        # second file
        browse_label2 = tk.Label(self, text="New CSV File:")
        browseb2 = tk.Button(self)
        browseb2["text"] = "Browse File"
        browseb2["command"] = self.browse_file2
        # submit button
        submit = tk.Button(self, text="Compare", fg="blue")
        submit["command"] = self.generate_op
        browse_label1.place(relx=.3, rely=.2, anchor="c")
        browse_label2.place(relx=.3, rely=.4, anchor="c")
        browseb1.place(relx=.6, rely=.2, anchor="c")
        browseb2.place(relx=.6, rely=.4, anchor="c")
        submit.place(relx=.5, rely=.6, anchor="c")


root = tk.Tk(className=" Compare CSV Files")
app = Application(master=root)
app.pack(fill="both", expand=True)
app.mainloop()
