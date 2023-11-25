from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from models import Hpred
import pickle
from datetime import datetime
from performance_gui import Performance_gui

model_file = 'db/model db.txt'


class App(Tk):
    def __init__(self):
        super().__init__()

        # arrays that store input field from respective classifier
        self.inputs_naive_bayes = []
        self.inputs_svm = []
        self.inputs_dt = []

        self.attribute_field_left = ['Age', 'Sex', 'Cp', 'Trestbps', 'Chol', 'Fbs', 'Restecg']
        self.attribute_field_right = ['Thalch', 'Exang', 'Oldpeak', 'Slope', 'Ca', 'Thal']

        self.attribute_field_left_svm = ['Age', 'Cp', 'Trestbps', 'Chol', 'Restecg', 'Thalch']
        self.attribute_field_right_svm = ['Exang', 'Oldpeak', 'Slope', 'Ca', 'Thal']

        self.csv_order = []
        self.is_expanded = False
        self.classifiers = {}
        self.list_hist = []
        self.diagnosis_labels = []

        self.id = None
        self.state = None
        self.result_model = None
        self.prediction = []
        self.performance_score = None
        self.num_of_present = None
        self.num_of_absent = None
        self.track_res_diag = 0
        self.len_predictions = 0
        self.result_widget = None

        self.is_focus_on_canvas = False
        self.focus_index = 4
        self.focus_widget = []

        # creating performance window
        self.root_per = Toplevel()
        self.performance_gui = Performance_gui(self.root_per)

        # initializing the main window root
        self.title("Heart Disease Prediction System")
        self.geometry('500x500+200+200')

        # top section**********************************************
        self.header_frame = Frame(self, bg='#F5F5F5', padx=20, pady=10, )
        self.header_frame.place(relx=0.0, rely=0.0, relwidth=1, relheight=0.1)

        # middle section *******************************************
        self.middle_frame = Frame(self, bg='#F5F5F5')
        self.middle_frame.place(relx=0.0, rely=0.1, relwidth=1, relheight=0.6)

        self.input_frame = Frame(self.middle_frame, bg='white')
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

        # inner widgets
        self.predict_btn = Button(self.header_frame,
                                  text="Predict",
                                  bg="lightgreen",
                                  fg="white",
                                  font=('sanserif', 10, 'bold'),
                                  border=0, width=10, padx=5, pady=5, command=self.get_prediction)
        self.predict_btn.place(relx=0.01, rely=0.2)
        # frame used to hold buttons in the top frame
        self.head_btn_frame = Frame(self.header_frame, background='#F5F5F5')
        self.head_btn_frame.place(relx=0.35, rely=0.2)

        self.naive_btn = Button(self.head_btn_frame,
                                text='Naive bayes',
                                bg="skyblue",
                                font=('sanserif', 10, 'bold'),
                                fg="white",
                                border=0,
                                width=10, padx=5, pady=5, command=lambda: self.select_classifier('Naive Bayes'))
        self.naive_btn.pack(side='left', padx=5)

        self.SVM_btn = Button(self.head_btn_frame,
                              text='SVM',
                              bg="skyblue",
                              font=('sanserif', 10, 'bold'),
                              fg="white",
                              border=0,
                              width=10, padx=5, pady=5, command=lambda: self.select_classifier('SVM'))
        self.SVM_btn.pack(side='left', padx=5)

        self.DT_btn = Button(self.head_btn_frame,
                             text='Decision Tree',
                             bg="skyblue", font=('sanserif', 10, 'bold'),
                             fg="white",
                             border=0,
                             width=10, padx=5, pady=5, command=lambda: self.select_classifier('Decision Tree'))
        self.DT_btn.pack(side='left', padx=5)

        # drop down menu to import csv file, view model performance and more
        self.options = ttk.Menubutton(self.header_frame, text="Options")
        self.options.place(relx=0.903, rely=0.2)
        # option menu configuration to initiate import csv and view log drop down menue
        self.options.config(padding=10)
        self.sub_menu = Menu(self.options, tearoff=False)
        self.sub_menu.add_command(label='Import CSV', command=self.get_prediction_csv)
        self.sub_menu.add_command(label='View logs', command=self.show_history_widget)
        self.options.configure(menu=self.sub_menu)

        # frame for side section to view history tab
        self.history_frame = Frame(self.middle_frame, width=300, background='lightgrey')
        self.history_frame.pack(fill=Y, side=RIGHT)
        self.history_frame.pack_propagate(0)
        # canvas for history frame to enable scrolling
        self.canvas_hist = Canvas(self.history_frame, background='lightgrey')
        self.scrollbar_hist = Scrollbar(self.history_frame, orient=VERTICAL, command=self.canvas_hist.yview)
        self.scrollbar_hist.pack(side=RIGHT, fill=Y)
        # canvas for history frame to enable scrolling
        self.canvas_frame_hist = Frame(self.canvas_hist, background='lightgrey')
        self.canvas_hist.pack(fill=BOTH, side=LEFT, expand=True)

        self.history_header_frame = Frame(self.canvas_hist, background='lightgrey')
        self.history_header_frame.pack(fill=X)

        self.history_label = Label(self.history_header_frame,
                                   text='History',
                                   padx=7,
                                   pady=7,
                                   font=('sanserif', 9, 'bold'), background='lightgrey')
        self.history_label.pack(side=LEFT)

        self.history_close_btn = Button(self.history_header_frame,
                                        text='X',
                                        bg='lightgrey',
                                        font=('sanserif', 10),
                                        border=0,
                                        command=self.close_history_widget)
        self.history_close_btn.pack(side=RIGHT, ipadx=2)
        # frame that holds history list
        self.id_hist = Frame(self.canvas_frame_hist, background='lightgrey')
        self.id_hist.pack(fill=BOTH, expand=True, pady=30)
        # scrolling configuration for history frame
        self.config_canvas(self.canvas_hist, self.canvas_frame_hist, self.scrollbar_hist)

        # Bottom frame for widgets *****************************
        self.bottom_frame = Frame(self, bg='#F5F5F5', pady=10)
        self.bottom_frame.place(relx=0.0, rely=1, relwidth=1, anchor='sw', relheight=0.3)

        # Canvas use to create scrollable frame for prediction results
        self.canvas_result = Canvas(self.bottom_frame, background='lightgrey')
        self.canvas_result.pack(side='left', fill=BOTH, expand=True)
        # scrollbar for result frame
        self.scrollbar_result = Scrollbar(self.bottom_frame, orient=VERTICAL, command=self.canvas_result.yview)
        self.scrollbar_result.pack(side='right', fill=Y)
        self.canvas_frame_res = Frame(self.canvas_result, background='lightgrey', width=200)

        # frame holding model performance and expand button
        self.stat_bar_res_frame = Frame(self.canvas_result, background='lightgrey')
        self.stat_bar_res_frame.place(relx=0.0, rely=0.0, relwidth=1)
        self.expand = Button(self.stat_bar_res_frame,
                             text="expand", bg="grey", fg="white", border=0, width=13, padx=5, pady=5,
                             command=self.expand_collapse)
        self.expand.pack(anchor='n', side=RIGHT)

        self.view_model_per = Button(self.stat_bar_res_frame,
                                     text="model performance",
                                     bg="grey", fg="white", border=0, width=13, padx=9, pady=5)
        self.view_model_per.pack(anchor='n', side=LEFT)
        # widget holding the frame holding prediction result
        self.canvas_frame_res_wig = Frame(self.canvas_frame_res, background='lightgrey', padx=20, pady=30)
        self.canvas_frame_res_wig.pack(fill=BOTH, expand=True, anchor='center')
        self.canvas_frame_res_wig.columnconfigure(0, weight=1)
        self.canvas_frame_res_wig.rowconfigure(0, weight=1)

        #  widget holding prediction result
        self.result_frame = Frame(self.canvas_frame_res_wig, background='lightgrey')
        self.result_frame.columnconfigure(0, weight=1)
        self.result_frame.columnconfigure(1, weight=1)
        # creating 51 labels that holds individual heart disease input this label exists
        # within result_frame
        self.create_result_labels()

        # previous button in result button
        self.prev_btn = Button(self.canvas_result,
                               text='<',
                               padx=7,
                               pady=7,
                               border=0,
                               font=('sanserif', 11, 'bold'),
                               command=lambda: self.fill_result_label(self.prediction, -1))
        self.prev_btn.place(relx=0.01, rely=1, anchor='sw')

        # next button in result button
        self.next_btn = Button(self.canvas_result,
                               text='>',
                               padx=7,
                               pady=7,
                               border=0,
                               font=('sanserif', 11, 'bold'),
                               command=lambda: self.fill_result_label(self.prediction, 1))
        self.next_btn.place(relx=0.99, rely=1, anchor='se')
        # configuring the canvas for result widget to make it scrollable
        self.config_canvas(self.canvas_result, self.canvas_frame_res, self.scrollbar_result)

        # load everything from database
        self.load_model_from_db()

        # An array which arrange all widget in the order they will be focused on when the down button or up
        # button is pressed
        self.focus_widget = []
        # function that push widget to focus_array
        self.push_widget_to_focus_arr()
        # this function binds a function th all input in the input array which change the focus index
        # to the index of the widget clicked
        self.make_focus_dynamic()
        # where to focus on start up
        self.focus_widget[self.focus_index].focus()
        self.bind('<Down>', lambda e: self.change_focus(e))
        self.bind('<Up>', lambda e: self.change_focus(e))

        # function that binds a function to middle section scrollable
        # frame to place focus on canvas anytime area near input is clicked
        self.place_focus_on_canvas()

    def place_focus_on_canvas(self):
        self.canvas_frame_wig.bind('<1>', lambda e: self.focus_on_canvas(e))

    def focus_on_canvas(self, e):
        self.is_focus_on_canvas = True

    def select_classifier_input(self, classifier):
        self.classifiers[classifier].tkraise()

    def display_performance_btn(self):
        # if performance score exist the model performance button turns blue, if no performance was calculated
        # the button is color is grey
        if self.performance_score is not None:
            self.view_model_per.config(background='#0080FE',
                                       fg='white', command=self.performance_gui.show_performance_gui)
        else:
            self.view_model_per.config(background='grey', fg='white', command=self.no_performance)
            self.performance_gui.hide_performance_gui()

    @staticmethod
    def no_performance():
        messagebox.showinfo('Info', 'No performance score recorded')

    def select_model_btn(self, state):
        # Here the color of the classifier button in the top section change colors according
        # to the new state value blue indicate the active button
        self.state = state

        # # function to place focus on canvas anytime area near input is clicked
        # self.place_focus_on_canvas()
        if self.state == 'Naive Bayes':
            self.naive_btn.config(background='#0080FE')
            self.SVM_btn.config(background="skyblue")
            self.DT_btn.config(background='skyblue')
        if self.state == 'SVM':
            self.naive_btn.config(background='skyblue')
            self.SVM_btn.config(background='#0080FE')
            self.DT_btn.config(background='skyblue')
        if self.state == 'Decision Tree':
            self.naive_btn.config(background='skyblue')
            self.SVM_btn.config(background='skyblue')
            self.DT_btn.config(background='#0080FE')

    def reset_focus(self):
        self.focus_widget = []
        self.push_widget_to_focus_arr()
        self.make_focus_dynamic()

    def select_classifier(self, classifier):
        self.select_model_btn(classifier)
        self.select_classifier_input(classifier)
        self.reset_focus()

    # create input field in the middle section
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

    # method to hide second window
    def close_history_widget(self):
        self.history_frame.pack_forget()

    def show_history_widget(self):
        self.history_frame.pack(fill=Y, side=RIGHT)
        self.history_frame.pack_propagate(0)

    # function within a function works when passing parameter to a function in for loop
    def select_prediction(self, selected_id):

        def mini():
            index = None
            with open(model_file, 'rb') as file:
                model_info = pickle.load(file)

            for j in range(len(model_info)):
                if model_info[j]["id"] == selected_id:
                    model_info[j]["selected"] = True
                    index = j
                else:
                    model_info[j]["selected"] = False

            if len(model_info) > 0:
                self.id = model_info[index]["id"]
                self.state = model_info[index]["model"]
                self.result_model = model_info[index]["model"]
                self.prediction = model_info[index]["predictions"]
                self.performance_score = model_info[index]["performance"]
                self.num_of_present = model_info[index]["present"]
                self.num_of_absent = model_info[index]["absent"]

                for j in range(len(self.list_hist)):
                    if selected_id == self.list_hist[j]["hist_id"]:
                        self.list_hist[j]["hist_f"].config(background='grey')
                        self.list_hist[j]["his_but"].config(background='grey', fg='white')
                        self.list_hist[j]["hist_del"].config(background='grey', fg='white')
                    else:
                        self.list_hist[j]["hist_f"].config(background='lightgrey')
                        self.list_hist[j]["his_but"].config(background='lightgrey', fg='black')
                        self.list_hist[j]["hist_del"].config(background='lightgrey', fg='black')

                self.reset_widgets()

                with open(model_file, 'wb') as file:
                    pickle.dump(model_info, file)

        return mini

    def reset_widgets(self):
        self.select_classifier(self.state)
        self.track_res_diag = 0
        self.fill_result_label(self.prediction, 0)
        self.display_performance_btn()
        if self.performance_score is not None:
            self.performance_gui.update_performance_gui(self.result_model,
                                                        self.num_of_present,
                                                        self.num_of_absent, self.performance_score)

    def fill_history_widget(self):
        # we load all the history from the file db and create button for each prediction
        try:
            with open(model_file, 'rb') as file:
                model_info = pickle.load(file)
        except EOFError:
            self.list_hist = []
        if len(model_info) > 0:
            for i in range(len(model_info)):
                if model_info[i]["id"] == self.id:
                    id_frame = Frame(self.id_hist, background='grey')
                    id_frame.pack(fill=X)

                    id_label = Button(id_frame, text=model_info[i]["id"],
                                      padx=7,
                                      pady=7,
                                      background='grey',
                                      width=30,
                                      border=0, fg='white',
                                      command=self.select_prediction(model_info[i]["id"]))

                    id_label.pack(side=LEFT)
                    id_del = Button(id_frame, text='del', width=25, padx=7, pady=7, background='grey', border=0,
                                    fg='white')
                    id_del.pack(side=RIGHT)

                else:
                    id_frame = Frame(self.id_hist, background='lightgrey')
                    id_frame.pack(fill=X)

                    id_label = Button(id_frame,
                                      text=model_info[i]["id"],
                                      padx=7,
                                      pady=7,
                                      background='lightgrey',
                                      width=30,
                                      border=0, command=self.select_prediction(model_info[i]["id"]))
                    id_label.pack(side=LEFT)
                    id_del = Button(id_frame, text='del', width=25, padx=7, pady=7, background='lightgrey',
                                    border=0)
                    id_del.pack(side=RIGHT)

                self.list_hist.append({})
                self.list_hist[i]["hist_id"] = model_info[i]["id"]
                self.list_hist[i]["hist_f"] = id_frame
                self.list_hist[i]["his_but"] = id_label
                self.list_hist[i]["hist_del"] = id_del

        self.close_history_widget()

    # method to change focus when down or up arrow is pressed
    def change_focus(self, event):
        if not self.is_focus_on_canvas:
            if event.keysym == 'Down':
                if self.focus_index < len(self.focus_widget) - 1:
                    self.focus_index += 1
                else:
                    self.focus_index = 0
            else:
                if self.focus_index > 0:
                    self.focus_index -= 1
                else:
                    self.focus_index = len(self.focus_widget) - 1
        else:
            if event.keysym == 'Down':
                self.canvas.yview_scroll(1, "units")
                if self.scrollbar.get()[1] == 1.0:
                    self.is_focus_on_canvas = False
            else:
                self.canvas.yview_scroll(-1, "units")
                if self.scrollbar.get()[0] == 0.0:
                    self.is_focus_on_canvas = False
        self.focus_widget[self.focus_index].focus_set()

    # creating the catalogue for order up and down button to transverse through widget
    def push_widget_to_focus_arr(self):
        selected_array = []

        if self.state == 'Naive Bayes':
            selected_array = self.inputs_naive_bayes
        if self.state == 'SVM':
            selected_array = self.inputs_svm
        if self.state == 'Decision Tree':
            selected_array = self.inputs_dt

        self.focus_widget.append(self.predict_btn)
        self.focus_widget.append(self.naive_btn)
        self.focus_widget.append(self.SVM_btn)
        self.focus_widget.append(self.DT_btn)
        self.focus_widget.append(self.options)

        for i in range(len(selected_array)):
            self.focus_widget.append(selected_array[i])

    def make_focus_dynamic(self):
        for i in range(len(self.focus_widget)):
            self.focus_widget[i].bind('<1>', lambda e: self.change_num_focus_clicked(e.widget))

    def change_num_focus_clicked(self, wid):
        num = 0
        for elements in self.focus_widget:
            if elements == wid:
                self.focus_index = num
                elements.focus_set()
            num += 1

        self.is_focus_on_canvas = False

    def create_data(self):
        try:
            with open(model_file, 'rb') as file:
                model_info = pickle.load(file)
        except EOFError:
            with open(model_file, 'wb') as file:
                pickle.dump([], file)

            with open(model_file, 'rb') as file:
                model_info = pickle.load(file)

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        obj = {
            "id": dt_string + " " + str(len(model_info)),
            "model": self.state,
            "predictions": self.prediction,
            "performance": self.performance_score,
            "present": self.num_of_present,
            "absent": self.num_of_absent,
            "selected": True
        }

        # resetting all stored model selected attributes to false
        for i in range(len(model_info)):
            if model_info[i]["selected"]:
                model_info[i]["selected"] = False

        model_info.append(obj)

        with open(model_file, 'wb') as file:
            pickle.dump(model_info, file)

        self.id = obj["id"]
        self.show_history_widget()

    def get_prediction_csv(self):
        # resetting number of patient with and without heart disease
        self.num_of_present = 0
        self.num_of_absent = 0
        path = filedialog.askopenfile()
        if path is not None:
            if path.name.endswith('csv'):
                hpred = Hpred(path.name, self.state)

                que = messagebox.askquestion('check performance', 'Do you want to check performance')
                if que == 'yes':
                    should_check_performance = True
                else:
                    should_check_performance = False

                # checking prediction
                predictions = hpred.check_csv_validation(should_check_performance)

                self.prediction = predictions[0]
                self.len_predictions = len(predictions)
                self.performance_score = predictions[1]

                # resetting result frame
                self.track_res_diag = 0
                self.fill_result_label(self.prediction, 0)

                self.create_data()

    def get_prediction(self):
        values = {}
        inputs_l = []
        inputs_r = []

        if self.state == 'Naive Bayes':
            inputs_l = self.left_inputs_naive_bayes
            inputs_r = self.right_inputs_naive_bayes
        elif self.state == 'SVM':
            inputs_l = self.left_inputs_svm
            inputs_r = self.right_inputs_svm
        elif self.state == 'Decision Tree':
            inputs_l = self.left_inputs_dt
            inputs_r = self.right_inputs_dt

        # getting all inputs collected and putting them in a dictionary
        for i in range(len(inputs_l)):
            if self.state == 'Naive Bayes' or self.state == 'Decision Tree':
                values[self.attribute_field_left[i]] = inputs_l[i].get()
            elif self.state == 'SVM':
                values[self.attribute_field_left_svm[i]] = inputs_l[i].get()
        for j in range(len(inputs_r)):
            if self.state == 'Naive Bayes' or self.state == 'Decision Tree':
                values[self.attribute_field_right[j]] = inputs_r[j].get()
            elif self.state == 'SVM':
                values[self.attribute_field_right_svm[j]] = inputs_r[j].get()

        # calling passing the dictionary to heart disease prediction class and training the inputed values
        hpred = Hpred(values, self.state)
        predictions = hpred.check_value_validation()
        # hpred returns an array of [err, index of] or [predictions]
        if predictions[0] == 'val error':
            if self.state == 'SVM' and predictions[2] > 5:
                predictions[2] = predictions[2] - 6
            if (self.state == 'Naive Bayes' or self.state == 'Decision Tree') and predictions[2] > 6:
                predictions[2] = predictions[2] - 7

            self.prediction = ['incorrect value given at input ' + predictions[1]]
            self.reset_result_frame()

        elif predictions[0] == 'not in range':
            if self.state == 'SVM' and predictions[2] > 5:
                predictions[2] = predictions[2] - 6
            if (self.state == 'Naive Bayes' or self.state == 'Decision Tree') and predictions[2] > 6:
                predictions[2] = predictions[2] - 7

            self.prediction = ['value give is not in range at input ' + predictions[1]]
            self.reset_result_frame()
        else:
            self.prediction = predictions[0]
            self.performance_score = predictions[1]

            if self.prediction == 1:
                self.num_of_present = 1
                self.num_of_absent = 0
            if self.prediction == 0:
                self.num_of_absent = 1
                self.num_of_present = 0

            self.reset_result_frame()
            self.create_data()

    def expand_collapse(self):
        if not self.is_expanded:
            self.expand.config(text='collapse')
            self.is_expanded = True
            self.bottom_frame.place_configure(relheight=1.0)
        else:
            self.expand.config(text='expand')
            self.is_expanded = False
            self.bottom_frame.place_configure(relheight=0.3)

    def pack_widget(self):
        self.mainloop()

    def load_model_from_db(self):
        try:
            with open(model_file, 'rb') as file:
                model_info = pickle.load(file)
        except EOFError:
            return None, 'Naive Bayes', None, None, None, None
        else:
            if len(model_info) == 0:
                return None, 'Naive Bayes', None, None, None, None
            else:
                for i in range(len(model_info)):
                    if model_info[i]["selected"]:
                        state = model_info[i]
                        self.id = state["id"]
                        self.state = state["model"]
                        self.result_model = state["model"]
                        self.prediction = state["predictions"]
                        self.len_predictions = len(self.prediction)
                        self.performance_score = state["performance"]
                        self.num_of_present = state["present"]
                        self.num_of_absent = state["absent"]

            if self.performance_score is not None:
                self.performance_gui.update_performance_gui(self.result_model,
                                                            self.num_of_present,
                                                            self.num_of_absent, self.performance_score)

            for f in ('Naive Bayes', 'SVM', 'Decision Tree'):
                if f == self.state:
                    self.select_model_btn(f)
                inpt = self.create_classifier_input_field(f)
                inpt.bind('<1>', lambda e: self.focus_on_canvas(e))
                self.classifiers[f] = inpt

            self.fill_result_label(self.prediction, 0)
            self.select_classifier_input(self.state)
            self.display_performance_btn()

            self.reset_widgets()
            self.fill_history_widget()

    def create_result_labels(self):
        # creating empty 51 labels in result frame that holds the diagnosis of th patient
        for i in range(51):
            index_diag = Label(self.result_frame,
                               text='',
                               background='lightgrey', font=('Times', 11), padx=5, pady=5)
            index_diag.grid(row=i, column=0)

            diag = Label(self.result_frame,
                         text='',
                         background='lightgrey', font=('sanserif', 11, 'bold'), padx=5, pady=5)
            diag.grid(row=i, column=1, sticky='w')

            # pushing labels to an array to input values after loading diagnosis from db
            self.diagnosis_labels.append({})
            self.diagnosis_labels[i]['diag'] = diag
            self.diagnosis_labels[i]['index'] = index_diag

        self.result_frame.grid(column=0, row=0, sticky='nwes')

    def fill_result_label(self, predictions, should_next):
        if should_next == 0:
            self.track_res_diag = 0
        elif should_next == 1:
            if (self.track_res_diag + 50) < self.len_predictions:
                self.track_res_diag = self.track_res_diag + 50
        elif should_next == -1:
            if (self.track_res_diag - 50) >= 0:
                self.track_res_diag = self.track_res_diag - 50
            else:
                self.track_res_diag = 0

        index = self.track_res_diag
        for i in range(50):
            if index < self.len_predictions:
                if predictions[index] == 1:
                    diagnosis = 'This Patient have heart disease'
                else:
                    diagnosis = 'This patients does not have heart disease'
                self.diagnosis_labels[i]['diag'].configure(text=diagnosis)
                self.diagnosis_labels[i]['index'].configure(text=str(index))
            else:
                self.diagnosis_labels[i]['diag'].configure(text='')
                self.diagnosis_labels[i]['index'].configure(text='')
            index = index + 1

    @staticmethod
    def config_canvas(canvas, canvas_frame, scrollbar):
        canvas.configure(yscrollcommand=scrollbar.set)
        create_canvas = canvas.create_window((0, 0), window=canvas_frame, anchor='nw')
        canvas_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.bind('<Configure>', lambda e: canvas.itemconfig(create_canvas, width=e.width))


App().pack_widget()
