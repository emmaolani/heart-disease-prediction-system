from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from models import Hpred
import pickle
from datetime import datetime
from performance_gui import Performance_gui
from csv_gui import Csv_gui

state_file = 'db/state.txt'
model_file = 'db/model db.txt'


class App(Tk):
    def __init__(self):
        super().__init__()

        self.cf_left_label_input_n = []
        self.cf_right_label_input_n = []

        self.cf_left_label_input_s = []
        self.cf_right_label_input_s = []

        self.cf_left_label_input_d = []
        self.cf_right_label_input_d = []

        self.cf_left_label_value = ['Age', 'Sex', 'Cp', 'Trestbps', 'Chol', 'Fbs', 'Restecg']
        self.cf_right_label_value = ['Thalch', 'Exang', 'Oldpeak', 'Slope', 'Ca', 'Thal']

        self.cf_left_label_value_S = ['Age', 'Cp', 'Trestbps', 'Chol', 'Restecg', 'Thalch']
        self.cf_right_label_value_S = ['Exang', 'Oldpeak', 'Slope', 'Ca', 'Thal']

        self.sel_cf_left_label_value = []
        self.sel_cf_right_label_value = []

        self.csv_order = []
        self.is_expanded = False
        self.inputs = {}
        self.list_hist = []
        self.hist_index = None

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
        self.prev_btn = None
        self.next_btn = None

        self.is_focus_on_canvas = False
        self.focus_index = 4
        self.focus_arr = []

        # creating performance window
        self.root_per = Toplevel()
        self.performance_gui = Performance_gui(self.root_per)

        self.root_csv = Toplevel()
        self.csv_gui = Csv_gui(self.root_csv)

        # initializing the main window root
        self.title("heart disease prediction system")
        self.geometry('500x500+200+200')

        self.header_frame = Frame(self, bg='#F5F5F5', padx=20, pady=10, )
        self.header_frame.place(relx=0.0, rely=0.0, relwidth=1, relheight=0.1)

        self.middle_frame = Frame(self, bg='#F5F5F5')
        self.middle_frame.place(relx=0.0, rely=0.1, relwidth=1, relheight=0.6)

        self.input_frame = Frame(self.middle_frame, bg='white')
        self.input_frame.pack(side=LEFT, fill=BOTH, expand=True)

        self.canvas = Canvas(self.input_frame, background='grey', height=450)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

        self.scrollbar = Scrollbar(self.input_frame, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.canvas_frame = Frame(self.canvas, background='white', border=0)

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

        self.head_btn_frame = Frame(self.header_frame, background='#F5F5F5')
        self.head_btn_frame.place(relx=0.35, rely=0.2)

        self.naive_btn = Button(self.head_btn_frame,
                                text='Naive bayes',
                                bg="skyblue",
                                font=('sanserif', 10, 'bold'),
                                fg="white",
                                border=0,
                                width=10, padx=5, pady=5, command=lambda: self.select_classifier('Naive Bayes', False))
        self.naive_btn.pack(side='left', padx=5)

        self.SVM_btn = Button(self.head_btn_frame,
                              text='SVM',
                              bg="skyblue",
                              font=('sanserif', 10, 'bold'),
                              fg="white",
                              border=0,
                              width=10, padx=5, pady=5, command=lambda: self.select_classifier('SVM', False))
        self.SVM_btn.pack(side='left', padx=5)

        self.DT_btn = Button(self.head_btn_frame,
                             text='Decision Tree',
                             bg="skyblue", font=('sanserif', 10, 'bold'),
                             fg="white",
                             border=0,
                             width=10, padx=5, pady=5, command=lambda: self.select_classifier('Decision Tree', False))
        self.DT_btn.pack(side='left', padx=5)

        # drop down menu to import csv file, view model performance and more
        self.options = ttk.Menubutton(self.header_frame, text="Options")
        self.options.place(relx=0.903, rely=0.2)

        self.options.config(padding=10)
        self.sub_menu = Menu(self.options, tearoff=False)
        self.sub_menu.add_command(label='Import CSV', command=self.get_prediction_csv)
        self.sub_menu.add_command(label='Setting', command=self.csv_gui.show_csv_gui)
        self.sub_menu.add_command(label='View logs', command=self.show_history_widget)
        self.options.configure(menu=self.sub_menu)

        self.history_frame = Frame(self.middle_frame, width=300, background='lightgrey')
        self.history_frame.pack(fill=Y, side=RIGHT)
        self.history_frame.pack_propagate(0)

        self.canvas_hist = Canvas(self.history_frame, background='lightgrey')
        self.scrollbar_hist = Scrollbar(self.history_frame, orient=VERTICAL, command=self.canvas_hist.yview)
        self.scrollbar_hist.pack(side=RIGHT, fill=Y)

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

        self.id_hist = Frame(self.canvas_frame_hist, background='lightgrey')
        self.id_hist.pack(fill=BOTH, expand=True, pady=30)

        self.config_canvas(self.canvas_hist, self.canvas_frame_hist, self.scrollbar_hist)

        # Bottom frame for widgets
        self.bottom_frame = Frame(self, bg='#F5F5F5', pady=10)
        self.bottom_frame.place(relx=0.0, rely=1, relwidth=1, anchor='sw', relheight=0.3)

        self.canvas_result = Canvas(self.bottom_frame, background='lightgrey')
        self.canvas_result.pack(side='left', fill=BOTH, expand=True)

        self.scrollbar_result = Scrollbar(self.bottom_frame, orient=VERTICAL, command=self.canvas_result.yview)
        self.scrollbar_result.pack(side='right', fill=Y)

        self.canvas_frame_res = Frame(self.canvas_result, background='lightgrey', width=200)

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

        self.canvas_frame_res_wig = Frame(self.canvas_frame_res, background='lightgrey', padx=20, pady=30)
        self.canvas_frame_res_wig.pack(fill=BOTH, expand=True, anchor='center')
        self.canvas_frame_res_wig.columnconfigure(0, weight=1)
        self.canvas_frame_res_wig.rowconfigure(0, weight=1)
        self.result_val = []

        self.result_frame = Frame(self.canvas_frame_res_wig, background='lightgrey')
        self.result_frame.columnconfigure(0, weight=1)
        self.result_frame.columnconfigure(1, weight=1)
        self.create_result_labels()

        self.prev_btn = Button(self.canvas_result,
                               text='<',
                               padx=7,
                               pady=7,
                               border=0,
                               font=('sanserif', 11, 'bold'),
                               command=lambda: self.fill_result_label(self.prediction, -1))
        self.prev_btn.place(relx=0.01, rely=1, anchor='sw')
        self.next_btn = Button(self.canvas_result,
                               text='>',
                               padx=7,
                               pady=7,
                               border=0,
                               font=('sanserif', 11, 'bold'),
                               command=lambda: self.fill_result_label(self.prediction, 1))
        self.next_btn.place(relx=0.99, rely=1, anchor='se')

        self.config_canvas(self.canvas_result, self.canvas_frame_res, self.scrollbar_result)

        self.load_model_from_db()
        self.focus_arr = []
        self.push_to_focus_cat()
        self.make_focus_dynamic()
        # where to focus on start up
        self.focus_arr[self.focus_index].focus()
        self.bind('<Down>', lambda e: self.change_focus(e))
        self.bind('<Up>', lambda e: self.change_focus(e))

        # function to place focus on canvas anytime area near input is clicked
        self.place_focus_on_canvas()

    def place_focus_on_canvas(self):
        self.canvas_frame_wig.bind('<1>', lambda e: self.focus_on_canvas(e))

    def focus_on_canvas(self, e):
        self.is_focus_on_canvas = True

    def classifier_inp_controller(self, classifier):
        self.inputs[classifier].tkraise()

    def display_model_per(self):
        if self.performance_score is not None:
            self.view_model_per.config(background='#0080FE',
                                       fg='white', command=self.performance_gui.show_performance_gui)
        else:
            self.view_model_per.config(background='grey', fg='white', command=self.no_performance)
            self.performance_gui.hide_performance_gui()

    @staticmethod
    def no_performance():
        messagebox.showinfo('Info', 'No performance score recorded')

    def sel_model_btn(self, state):
        self.state = state

        # function to place focus on canvas anytime area near input is clicked
        self.place_focus_on_canvas()
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

    def select_classifier(self, classifier, is_state_changed):
        self.sel_model_btn(classifier)
        self.classifier_inp_controller(classifier)
        if is_state_changed:
            self.track_res_diag = 0
            self.fill_result_label(self.prediction, 0)
            self.display_model_per()
            if self.performance_score is not None:
                self.performance_gui.update_performance_gui(self.result_model,
                                                            self.num_of_present,
                                                            self.num_of_absent, self.performance_score)

        self.focus_arr = []
        self.push_to_focus_cat()
        self.make_focus_dynamic()

    def show_input(self, mod):
        if mod == 'Naive Bayes':
            self.sel_cf_left_label_value = self.cf_left_label_value
            self.sel_cf_right_label_value = self.cf_right_label_value
        if mod == 'SVM':
            self.sel_cf_left_label_value = self.cf_left_label_value_S
            self.sel_cf_right_label_value = self.cf_right_label_value_S
        if mod == 'Decision Tree':
            self.sel_cf_left_label_value = self.cf_left_label_value
            self.sel_cf_right_label_value = self.cf_right_label_value

        input_frame_nd = Frame(self.canvas_frame_wig, background='lightgrey')
        input_frame_nd.columnconfigure(0, weight=1)
        input_frame_nd.columnconfigure(1, weight=1)
        input_frame_nd.grid(row=0, column=0, sticky='nwes')

        for i in range(len(self.sel_cf_left_label_value)):
            if i == 0:
                Label(input_frame_nd,
                      text=self.sel_cf_left_label_value[i],
                      background='lightgrey',
                      font=('sanserif', 11), fg='grey').grid(row=i, column=0, sticky='w', padx=50, pady=10)

                input_box = Entry(input_frame_nd, border=0)
                input_box.grid(row=i + 1, column=0, sticky='nwes', padx=50, pady=10, ipady=5)

                if mod == 'Naive Bayes':
                    self.cf_left_label_input_n.append(input_box)
                elif mod == 'SVM':
                    self.cf_left_label_input_s.append(input_box)
                elif mod == 'Decision Tree':
                    self.cf_left_label_input_d.append(input_box)
            else:
                Label(input_frame_nd,
                      text=self.sel_cf_left_label_value[i],
                      background='lightgrey',
                      font=('sanserif', 11), fg='grey').grid(row=i + (i + 1), column=0, sticky='w', padx=50, pady=10)
                input_box = Entry(input_frame_nd, border=0)
                input_box.grid(row=i + (i + 2), column=0, sticky='nwes', padx=50, pady=10, ipady=5)
                if mod == 'Naive Bayes':
                    self.cf_left_label_input_n.append(input_box)
                elif mod == 'SVM':
                    self.cf_left_label_input_s.append(input_box)
                elif mod == 'Decision Tree':
                    self.cf_left_label_input_d.append(input_box)

        for i in range(len(self.sel_cf_right_label_value)):
            if i == 0:
                Label(input_frame_nd,
                      text=self.sel_cf_right_label_value[i],
                      background='lightgrey',
                      font=('sanserif', 11),
                      fg='grey').grid(row=i, column=1, sticky='w', padx=50, pady=10)

                input_box = Entry(input_frame_nd, border=0)
                input_box.grid(row=i + 1, column=1, sticky='nwes', padx=50, pady=10, ipady=5)
                if mod == 'Naive Bayes':
                    self.cf_right_label_input_n.append(input_box)
                elif mod == 'SVM':
                    self.cf_right_label_input_s.append(input_box)
                elif mod == 'Decision Tree':
                    self.cf_right_label_input_d.append(input_box)
            else:
                Label(input_frame_nd,
                      text=self.sel_cf_right_label_value[i],
                      background='lightgrey',
                      font=('sanserif', 11), fg='grey').grid(row=i + (i + 1), column=1, sticky='w', padx=50, pady=10)

                input_box = Entry(input_frame_nd, border=0)
                input_box.grid(row=i + (i + 2), column=1, sticky='nwes', padx=50, pady=10, ipady=5)
                if mod == 'Naive Bayes':
                    self.cf_right_label_input_n.append(input_box)
                elif mod == 'SVM':
                    self.cf_right_label_input_s.append(input_box)
                elif mod == 'Decision Tree':
                    self.cf_right_label_input_d.append(input_box)

        return input_frame_nd

    # method to hide second window
    def close_history_widget(self):
        self.history_frame.pack_forget()

    def show_history_widget(self):
        self.history_frame.pack(fill=Y, side=RIGHT)
        self.history_frame.pack_propagate(0)

    # function within a function works when passing parameter to a function in for loop
    def select_hist_id(self, name):
        def mini():
            index = None
            with open(model_file, 'rb') as file:
                model_info = pickle.load(file)

            for j in range(len(model_info)):
                if model_info[j]["id"] == name:
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
                    if name == self.list_hist[j]["hist_id"]:
                        self.list_hist[j]["hist_f"].config(background='grey')
                        self.list_hist[j]["his_but"].config(background='grey', fg='white')
                        self.list_hist[j]["hist_del"].config(background='grey', fg='white')
                    else:
                        self.list_hist[j]["hist_f"].config(background='lightgrey')
                        self.list_hist[j]["his_but"].config(background='lightgrey', fg='black')
                        self.list_hist[j]["hist_del"].config(background='lightgrey', fg='black')

                self.select_classifier(self.state, True)
                if self.performance_score is not None:
                    self.performance_gui.update_performance_gui(self.result_model,
                                                                self.num_of_present,
                                                                self.num_of_absent, self.performance_score)

                with open(model_file, 'wb') as file:
                    pickle.dump(model_info, file)

        return mini

    def create_history_widget(self):
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
                                      command=self.select_hist_id(model_info[i]["id"]))

                    id_label.pack(side=LEFT)
                    id_del = Button(id_frame, text='del', width=25, padx=7, pady=7, background='grey', border=0,
                                    fg='white')
                    id_del.pack(side=RIGHT)

                    self.list_hist.append({})
                    self.list_hist[i]["hist_id"] = model_info[i]["id"]
                    self.list_hist[i]["hist_f"] = id_frame
                    self.list_hist[i]["his_but"] = id_label
                    self.list_hist[i]["hist_del"] = id_del

                    self.hist_index = i
                else:
                    id_frame = Frame(self.id_hist, background='lightgrey')
                    id_frame.pack(fill=X)

                    id_label = Button(id_frame,
                                      text=model_info[i]["id"],
                                      padx=7,
                                      pady=7,
                                      background='lightgrey',
                                      width=30,
                                      border=0, command=self.select_hist_id(model_info[i]["id"]))
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
                if self.focus_index < len(self.focus_arr) - 1:
                    self.focus_index += 1
                else:
                    self.focus_index = 0
            else:
                if self.focus_index > 0:
                    self.focus_index -= 1
                else:
                    self.focus_index = len(self.focus_arr) - 1
        else:
            if event.keysym == 'Down':
                self.canvas.yview_scroll(1, "units")
                if self.scrollbar.get()[1] == 1.0:
                    self.is_focus_on_canvas = False
            else:
                self.canvas.yview_scroll(-1, "units")
                if self.scrollbar.get()[0] == 0.0:
                    self.is_focus_on_canvas = False
        self.focus_arr[self.focus_index].focus_set()

    # creating the catalogue for order up and down button to transverse through widget
    def push_to_focus_cat(self):
        arr_l = []
        arr_r = []

        if self.state == 'Naive Bayes':
            arr_l = self.cf_left_label_input_n
            arr_r = self.cf_right_label_input_n
        if self.state == 'SVM':
            arr_l = self.cf_left_label_input_s
            arr_r = self.cf_right_label_input_s
        if self.state == 'Decision Tree':
            arr_l = self.cf_left_label_input_d
            arr_r = self.cf_right_label_input_d

        self.focus_arr.append(self.predict_btn)
        self.focus_arr.append(self.naive_btn)
        self.focus_arr.append(self.SVM_btn)
        self.focus_arr.append(self.DT_btn)
        self.focus_arr.append(self.options)

        for i in range(len(arr_l)):
            self.focus_arr.append(arr_l[i])
        for j in range(len(arr_r)):
            self.focus_arr.append(arr_r[j])

    def make_focus_dynamic(self):
        for i in range(len(self.focus_arr)):
            self.focus_arr[i].bind('<1>', lambda e: self.change_num_focus_clicked(e.widget))

    def change_num_focus_clicked(self, wid):
        num = 0
        for elements in self.focus_arr:
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
            inputs_l = self.cf_left_label_input_n
            inputs_r = self.cf_right_label_input_n
        elif self.state == 'SVM':
            inputs_l = self.cf_left_label_input_s
            inputs_r = self.cf_right_label_input_s
        elif self.state == 'Decision Tree':
            inputs_l = self.cf_left_label_input_d
            inputs_r = self.cf_right_label_input_d

        # getting all inputs collected and putting them in a dictionary
        for i in range(len(inputs_l)):
            if self.state == 'Naive Bayes' or self.state == 'Decision Tree':
                values[self.cf_left_label_value[i]] = inputs_l[i].get()
            elif self.state == 'SVM':
                values[self.cf_left_label_value_S[i]] = inputs_l[i].get()
        for j in range(len(inputs_r)):
            if self.state == 'Naive Bayes' or self.state == 'Decision Tree':
                values[self.cf_right_label_value[j]] = inputs_r[j].get()
            elif self.state == 'SVM':
                values[self.cf_right_label_value_S[j]] = inputs_r[j].get()

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
                    self.sel_model_btn(f)
                inpt = self.show_input(f)
                inpt.bind('<1>', lambda e: self.focus_on_canvas(e))
                self.inputs[f] = inpt

            self.fill_result_label(self.prediction, 0)
            self.classifier_inp_controller(self.state)
            self.display_model_per()
            self.create_history_widget()

    def create_result_labels(self):
        for i in range(51):
            index_diag = Label(self.result_frame,
                               text='',
                               background='lightgrey', font=('Times', 11), padx=5, pady=5)
            index_diag.grid(row=i, column=0)

            diag = Label(self.result_frame,
                         text='',
                         background='lightgrey', font=('sanserif', 11, 'bold'), padx=5, pady=5)
            diag.grid(row=i, column=1, sticky='w')

            self.result_val.append({})
            self.result_val[i]['diag'] = diag
            self.result_val[i]['index'] = index_diag

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
                self.result_val[i]['diag'].configure(text=diagnosis)
                self.result_val[i]['index'].configure(text=str(index))
            else:
                self.result_val[i]['diag'].configure(text='')
                self.result_val[i]['index'].configure(text='')
            index = index + 1

    @staticmethod
    def config_canvas(canvas, canvas_frame, scrollbar):
        canvas.configure(yscrollcommand=scrollbar.set)
        create_canvas = canvas.create_window((0, 0), window=canvas_frame, anchor='nw')
        canvas_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.bind('<Configure>', lambda e: canvas.itemconfig(create_canvas, width=e.width))


App().pack_widget()
