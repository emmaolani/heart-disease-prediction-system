from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox


class InputField:
    def __init__(self, root):
        self.root = root
        self.classifiers = {}
        self.inputs_naive_bayes = []
        self.inputs_svm = []
        self.inputs_dt = []

        self.attribute_field_left = ['Age', 'Sex', 'Cp', 'Trestbps', 'Chol', 'Fbs', 'Restecg']
        self.attribute_field_right = ['Thalch', 'Exang', 'Oldpeak', 'Slope', 'Ca', 'Thal']

        self.attribute_field_left_svm = ['Age', 'Cp', 'Trestbps', 'Chol', 'Restecg', 'Thalch']
        self.attribute_field_right_svm = ['Exang', 'Oldpeak', 'Slope', 'Ca', 'Thal']

        self.input_frame = Frame(self.root, bg='white')
        self.input_frame.pack(side=LEFT, fill=BOTH, expand=True)
        # canvas is used to enable scrolling for input field
        self.canvas = Canvas(self.input_frame, background='grey', height=450)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.scrollbar = Scrollbar(self.input_frame, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        # frame in canvas used to hold input fields
        self.canvas_frame = Frame(self.canvas, background='white', border=0)
        # frame in canvas frame used to hold input fields
        self.canvas_frame_wig = Frame(self.canvas_frame, padx=50, pady=30, background='lightgrey')
        self.canvas_frame_wig.pack(fill=X, expand=True)

        self.canvas_frame_wig.columnconfigure(0, weight=1)
        self.canvas_frame_wig.rowconfigure(0, weight=1)

        self.config_canvas(self.canvas, self.canvas_frame, self.scrollbar)

        # create input field in the middle section
        self.createInputs()

    def render(self, state):
        self.classifiers[state].tkraise()

    def create_classifier_input_field(self, classifier):
        selected_left_attribute_field = []
        selected_right_attribute_field = []

        if classifier == 'Naive Bayes':
            selected_left_attribute_field = self.attribute_field_left
            selected_right_attribute_field = self.attribute_field_right
        if classifier == 'SVM':
            selected_left_attribute_field = self.attribute_field_left_svm
            selected_right_attribute_field = self.attribute_field_right_svm
        if classifier == 'Decision Tree':
            selected_left_attribute_field = self.attribute_field_left
            selected_right_attribute_field = self.attribute_field_right

        input_frame = Frame(self.canvas_frame_wig, background='lightgrey')
        input_frame.columnconfigure(0, weight=1)
        input_frame.columnconfigure(1, weight=1)
        input_frame.grid(row=0, column=0, sticky='nwes')

        for i in range(len(selected_left_attribute_field)):
            if i == 0:
                Label(input_frame,
                      text=selected_left_attribute_field[i],
                      background='lightgrey',
                      font=('sanserif', 11), fg='grey').grid(row=i, column=0, sticky='w', padx=50, pady=10)

                input_box = Entry(input_frame, border=0)
                input_box.grid(row=i + 1, column=0, sticky='nwes', padx=50, pady=10, ipady=5)

                if classifier == 'Naive Bayes':
                    self.inputs_naive_bayes.append(input_box)
                elif classifier == 'SVM':
                    self.inputs_svm.append(input_box)
                elif classifier == 'Decision Tree':
                    self.inputs_dt.append(input_box)
            else:
                Label(input_frame,
                      text=selected_left_attribute_field[i],
                      background='lightgrey',
                      font=('sanserif', 11), fg='grey').grid(row=i + (i + 1), column=0, sticky='w', padx=50, pady=10)
                input_box = Entry(input_frame, border=0)
                input_box.grid(row=i + (i + 2), column=0, sticky='nwes', padx=50, pady=10, ipady=5)
                if classifier == 'Naive Bayes':
                    self.inputs_naive_bayes.append(input_box)
                elif classifier == 'SVM':
                    self.inputs_svm.append(input_box)
                elif classifier == 'Decision Tree':
                    self.inputs_dt.append(input_box)

        for i in range(len(selected_right_attribute_field)):
            if i == 0:
                Label(input_frame,
                      text=selected_right_attribute_field[i],
                      background='lightgrey',
                      font=('sanserif', 11),
                      fg='grey').grid(row=i, column=1, sticky='w', padx=50, pady=10)

                input_box = Entry(input_frame, border=0)
                input_box.grid(row=i + 1, column=1, sticky='nwes', padx=50, pady=10, ipady=5)
                if classifier == 'Naive Bayes':
                    self.inputs_naive_bayes.append(input_box)
                elif classifier == 'SVM':
                    self.inputs_svm.append(input_box)
                elif classifier == 'Decision Tree':
                    self.inputs_dt.append(input_box)
            else:
                Label(input_frame,
                      text=selected_right_attribute_field[i],
                      background='lightgrey',
                      font=('sanserif', 11), fg='grey').grid(row=i + (i + 1), column=1, sticky='w', padx=50, pady=10)

                input_box = Entry(input_frame, border=0)
                input_box.grid(row=i + (i + 2), column=1, sticky='nwes', padx=50, pady=10, ipady=5)
                if classifier == 'Naive Bayes':
                    self.inputs_naive_bayes.append(input_box)
                elif classifier == 'SVM':
                    self.inputs_svm.append(input_box)
                elif classifier == 'Decision Tree':
                    self.inputs_dt.append(input_box)

        return input_frame

    def createInputs(self):
        for i in ('Naive Bayes', 'SVM', 'Decision Tree'):
            classifier = self.create_classifier_input_field(i)
            self.classifiers[i] = classifier

    @staticmethod
    def config_canvas(canvas, canvas_frame, scrollbar):
        canvas.configure(yscrollcommand=scrollbar.set)
        create_canvas = canvas.create_window((0, 0), window=canvas_frame, anchor='nw')
        canvas_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.bind('<Configure>', lambda e: canvas.itemconfig(create_canvas, width=e.width))
