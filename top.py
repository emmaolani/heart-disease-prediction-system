from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox


class TopSection:
    def __init__(self, root):
        self.root = root

        self.header_frame = Frame(self.root, bg='#F5F5F5', padx=20, pady=10, )
        self.header_frame.place(relx=0.0, rely=0.0, relwidth=1, relheight=0.1)

        # frame used to hold buttons in the top frame
        self.head_btn_frame = Frame(self.header_frame, background='#F5F5F5')
        self.head_btn_frame.place(relx=0.35, rely=0.2)

        self.naive_btn = Button(self.head_btn_frame,
                                text='Naive bayes',
                                bg="skyblue",
                                font=('sanserif', 10, 'bold'),
                                fg="white",
                                border=0,
                                width=10, padx=5, pady=5)
        self.naive_btn.pack(side='left', padx=5)

        self.SVM_btn = Button(self.head_btn_frame,
                              text='SVM',
                              bg="skyblue",
                              font=('sanserif', 10, 'bold'),
                              fg="white",
                              border=0,
                              width=10, padx=5, pady=5)
        self.SVM_btn.pack(side='left', padx=5)

        self.DT_btn = Button(self.head_btn_frame,
                             text='Decision Tree',
                             bg="skyblue", font=('sanserif', 10, 'bold'),
                             fg="white",
                             border=0,
                             width=10, padx=5, pady=5)
        self.DT_btn.pack(side='left', padx=5)

        # drop down menu to import csv file, view model performance and more
        self.options = ttk.Menubutton(self.header_frame, text="Options")
        self.options.place(relx=0.903, rely=0.2)
        # option menu configuration to initiate import csv and view log drop down menue
        self.options.config(padding=10)
        self.sub_menu = Menu(self.options, tearoff=False)
        self.sub_menu.add_command(label='Import CSV')
        self.sub_menu.add_command(label='View logs')
        self.options.configure(menu=self.sub_menu)

    def render(self, classifier, update_classifier, open_log, get_prediction_csv):
        self.naive_btn.configure(command=lambda: update_classifier('Naive Bayes'))
        self.SVM_btn.configure(command=lambda: update_classifier('SVM'))
        self.DT_btn.configure(command=lambda: update_classifier('Decision Tree'))

        self.sub_menu.delete(0, 1)
        self.sub_menu.add_command(label='Import CSV', command=get_prediction_csv)
        self.sub_menu.add_command(label='View logs', command=open_log)

        if classifier == 'Naive Bayes':
            self.naive_btn.config(background='#0080FE')
            self.SVM_btn.config(background="skyblue")
            self.DT_btn.config(background='skyblue')
        if classifier == 'SVM':
            self.naive_btn.config(background='skyblue')
            self.SVM_btn.config(background='#0080FE')
            self.DT_btn.config(background='skyblue')
        if classifier == 'Decision Tree':
            self.naive_btn.config(background='skyblue')
            self.SVM_btn.config(background='skyblue')
            self.DT_btn.config(background='#0080FE')


