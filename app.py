from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from models import Hpred
import pickle
from datetime import datetime

state_file = 'db/state.txt'
model_file = 'db/model db.txt'


class App(Tk):
    def __init__(self, start_size):
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
        self.sel_cf_right_label_value  = []

        self.csv_order = []
        self.is_expanded = False
        self.performance_score = None
        self.prediction = None
        self.inputs = {}

        self.id, \
        self.state, \
        self.prediction, \
        self.performance_score, self.num_of_present, self.num_of_absent = self.load_history_model()
        self.previous_id = []
        self.list_hist = []
        self.hist_index = None

        self.is_focus_on_canvas = False
        self.focus_index = 4
        self.focus_arr = []

        # initializing the main window root
        self.title("heart disease prediction system")
        self.geometry(f'{start_size[0]}x{start_size[1]}')
        self.config(bg='white')

        self.header_frame = Frame(self, bg='white', padx=20, pady=10, height=50)

        self.middle_frame = Frame(self, bg='white', padx=10, pady=10)
        self.canvas = Canvas(self.middle_frame, background='grey', height=450)
        self.scrollbar = Scrollbar(self.middle_frame, orient=VERTICAL, command=self.canvas.yview)
        self.canvas_frame = Frame(self.canvas, background='white', padx=20, pady=30)
        self.canvas_frame_wig = Frame(self.canvas_frame, padx=20, pady=30, background='lightgrey')
        self.canvas_frame_wig.columnconfigure(0, weight=1)
        self.canvas_frame_wig.rowconfigure(0, weight=1)

        self.bottom_frame = Frame(self, bg='white', padx=40, pady=10)

        self.config_canvas(self.canvas, self.canvas_frame, self.scrollbar)

        # inner widgets
        self.predict_btn = Button(self.header_frame,
                                  text="Predict",
                                  bg="lightgreen",
                                  fg="white",
                                  font=('sanserif', 10, 'bold'),
                                  border=0, width=10, padx=5, pady=5, command=self.get_prediction)

        self.head_btn_frame = Frame(self.header_frame, background='white')

        self.naive_btn = Button(self.head_btn_frame,
                                text='Naive bayes',
                                bg="skyblue",
                                font=('sanserif', 10, 'bold'),
                                fg="white",
                                border=0,
                                width=10, padx=5, pady=5, command=lambda: self.select_classifier('Naive Bayes'))

        self.SVM_btn = Button(self.head_btn_frame,
                              text='SVM',
                              bg="skyblue",
                              font=('sanserif', 10, 'bold'),
                              fg="white",
                              border=0,
                              width=10, padx=5, pady=5, command=lambda: self.select_classifier('SVM'))

        self.DT_btn = Button(self.head_btn_frame,
                             text='Decision Tree',
                             bg="skyblue", font=('sanserif', 10, 'bold'),
                             fg="white",
                             border=0,
                             width=10, padx=5, pady=5, command=lambda: self.select_classifier('Decision Tree'))

        # drop down menu to import csv file, view model performance and more
        self.options = ttk.Menubutton(self.header_frame, text="Options")
        self.options.config(padding=10)
        self.sub_menu = Menu(self.options, tearoff=False)
        self.sub_menu.add_command(label='Import CSV', command=self.get_prediction_csv)
        self.sub_menu.add_command(label='Change CSV order', command=self.load_history_model)
        self.sub_menu.add_command(label='History', command=self.show_history)
        self.options.configure(menu=self.sub_menu)

        self.cf_left_wig = Frame(self.canvas_frame_wig, padx=20, pady=30, background='lightgrey')
        self.cf_right_wig = Frame(self.canvas_frame_wig, padx=20, pady=30, background='lightgrey')

        self.mid = Frame(self.middle_frame, width=300, background='lightgrey')
        self.canvas_hist = Canvas(self.mid, background='lightgrey')
        self.scrollbar_hist = Scrollbar(self.mid, orient=VERTICAL, command=self.canvas_hist.yview)
        self.canvas_frame_hist = Frame(self.canvas_hist, background='white')
        self.config_canvas(self.canvas_hist, self.canvas_frame_hist, self.scrollbar_hist)

        self.history_frame = Frame(self.canvas_hist, background='lightgrey')
        self.history_label = Label(self.history_frame, text='History', padx=7, pady=7, background='lightgrey')
        self.history_close_btn = Button(self.history_frame, text='X', bg='lightgrey', command=self.close_history)
        self.id_hist = Frame(self.canvas_frame_hist, background='lightgrey')

        self.bottom_frame = Frame(self, bg='white', padx=10, pady=10)

        self.canvas_result = Canvas(self.bottom_frame, background='lightgrey')
        self.scrollbar_result = Scrollbar(self.bottom_frame, orient=VERTICAL, command=self.canvas_result.yview)
        self.canvas_frame_res = Frame(self.canvas_result, background='lightgrey', width=200)
        self.canvas_frame_res_wig = Frame(self.canvas_frame_res, background='lightgrey', padx=20, pady=30)
        self.config_canvas(self.canvas_result, self.canvas_frame_res, self.scrollbar_result)

        self.expand = Button(self.canvas_result,
                             text="expand", bg="grey", fg="white", border=0, width=13, padx=5, pady=5,
                             command=self.expand_collapse)
        self.view_model_per = Button(self.canvas_result,
                                     text="model performance",
                                     bg="grey", fg="white", border=0, width=13, padx=5, pady=5)


        # self.get_id_hist()

        for f in ('Naive Bayes', 'SVM', 'Decision Tree'):
            if f == self.state:
                self.sel_model_btn(f)
            inpt = self.show_input(f)
            inpt.bind('<1>', lambda e: self.focus_on_canvas(e))
            self.inputs[f] = inpt

        self.classifier_inp_controller(self.state)

        self.focus_arr = []
        self.push_to_focus_cat()
        self.make_focus_dynamic()

        # self.reset_result_frame()

        # where to focus on start up
        self.focus_arr[self.focus_index].focus()
        self.bind('<Down>', lambda e: self.change_focus(e))
        self.bind('<Up>', lambda e: self.change_focus(e))

        # function to place focus on canvas anytime area near input is clicked
        self.place_focus_on_canvas()

        # creating performance window
        self.per_root = Toplevel()
        # changing function of close button from destroying second window to hiding second window
        self.per_root.protocol("WM_DELETE_WINDOW", self.hide_performance_gui)
        self.per_root.config(bg='white')
        self.per_root.title('Performance Evaluation')
        # creating a canvas for second window to enable scrolling
        self.canvas_win = Canvas(self.per_root, background='white')
        self.scrollbar_win = Scrollbar(self.per_root, orient=VERTICAL, command=self.canvas_win.yview)
        self.canvas_frame_win = Frame(self.canvas_win, background='white')
        self.config_canvas(self.canvas_win, self.canvas_frame_win, self.scrollbar_win)
        # hide toplevel window
        self.hide_performance_gui()

        # creating order window
        self.order_root = Toplevel()
        self.order_root.protocol("WM_DELETE_WINDOW", self.hide_order_gui)
        self.order_root.config(bg='white')
        self.order_root.title('Performance Evaluation')
        self.hide_order_gui()

    def place_focus_on_canvas(self):
        self.canvas_frame_wig.bind('<1>', lambda e: self.focus_on_canvas(e))

    def focus_on_canvas(self, e):
        self.is_focus_on_canvas = True

    def classifier_inp_controller(self, classifier):
        self.inputs[classifier].tkraise()

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

    def select_classifier(self, classifier):
        self.sel_model_btn(classifier)
        self.classifier_inp_controller(classifier)
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

        input_frame_nd = Frame(self.canvas_frame_wig, background='lightgrey', padx=8)
        input_frame_nd.columnconfigure(0, weight=1)
        input_frame_nd.columnconfigure(1, weight=1)
        input_frame_nd.grid(row=0, column=0, sticky='nwes')

        for i in range(len(self.sel_cf_left_label_value)):
            if i == 0:
                Label(input_frame_nd,
                      text=self.sel_cf_left_label_value[i],
                      background='lightgrey',
                      font=('sanserif', 12), fg='grey').grid(row=i, column=0, sticky='w', padx=10, pady=10)

                input_box = Entry(input_frame_nd, border=0)
                input_box.grid(row=i+1, column=0, sticky='nwes', padx=10, pady=10, ipady=5)

                if mod == 'Naive Bayes':
                    self.cf_left_label_input_n.append(input_box)
                elif mod == 'SVM':
                    self.cf_left_label_input_s.append(input_box)
                elif mod == 'Decision Tree':
                    self.cf_left_label_input_s.append(input_box)
            else:
                Label(input_frame_nd,
                      text=self.sel_cf_left_label_value[i],
                      background='lightgrey',
                      font=('sanserif', 12), fg='grey').grid(row=i+(i+1), column=0, sticky='w', padx=10, pady=10)
                input_box = Entry(input_frame_nd, border=0)
                input_box.grid(row=i+(i+2), column=0, sticky='nwes', padx=10, pady=10, ipady=5)
                if mod == 'Naive Bayes':
                    self.cf_left_label_input_n.append(input_box)
                elif mod == 'SVM':
                    self.cf_left_label_input_s.append(input_box)
                elif mod == 'Decision Tree':
                    self.cf_left_label_input_s.append(input_box)

        for i in range(len(self.sel_cf_right_label_value)):
            if i == 0:
                Label(input_frame_nd,
                      text=self.sel_cf_right_label_value[i],
                      background='lightgrey',
                      font=('sanserif', 12),
                      fg='grey').grid(row=i, column=1, sticky='w', padx=10, pady=10)

                input_box = Entry(input_frame_nd, border=0)
                input_box.grid(row=i+1, column=1, sticky='nwes', padx=10, pady=10, ipady=5)
                if mod == 'Naive Bayes':
                    self.cf_right_label_input_n.append(input_box)
                elif mod == 'SVM':
                    self.cf_right_label_input_s.append(input_box)
                elif mod == 'Decision Tree':
                    self.cf_right_label_input_s.append(input_box)
            else:
                Label(input_frame_nd,
                      text=self.sel_cf_right_label_value[i],
                      background='lightgrey',
                      font=('sanserif', 12), fg='grey').grid(row=i+(i+1), column=1, sticky='w', padx=10, pady=10)

                input_box = Entry(input_frame_nd, border=0)
                input_box.grid(row=i+(i+2), column=1, sticky='nwes', padx=10, pady=10, ipady=5)
                if mod == 'Naive Bayes':
                    self.cf_right_label_input_n.append(input_box)
                elif mod == 'SVM':
                    self.cf_right_label_input_s.append(input_box)
                elif mod == 'Decision Tree':
                    self.cf_right_label_input_s.append(input_box)

        return input_frame_nd

    # method to hide second window
    def close_history(self):
        self.mid.pack_forget()

    def show_history(self):
        self.scrollbar.pack_forget()
        self.mid.pack(fill=Y, side=RIGHT)
        self.mid.pack_propagate(0)
        self.id_hist.pack_forget()
        self.id_hist = Frame(self.canvas_frame_hist, background='lightgrey')
        self.id_hist.pack(fill=BOTH, expand=True)
        self.list_hist = []

        self.scrollbar.pack(side=RIGHT, fill=Y)

        for i in range(len(self.previous_id)):
            if self.previous_id[i] == self.id:
                id_frame = Frame(self.id_hist, background='grey')
                id_frame.pack(fill=X)

                id_label = Button(id_frame, text=self.previous_id[i],
                                  padx=7,
                                  pady=7,
                                  background='grey',
                                  width=30,
                                  border=0, fg='white', command=self.select_id(self.previous_id[i], i))

                id_label.pack(side=LEFT)
                id_del = Button(id_frame, text='del', width=25, padx=7, pady=7, background='grey', border=0, fg='white')
                id_del.pack(side=RIGHT)
                self.list_hist.append(id_label)
                self.hist_index = i
            else:
                id_frame = Frame(self.id_hist, background='lightgrey')
                id_frame.pack(fill=X)

                id_label = Button(id_frame,
                                  text=self.previous_id[i],
                                  padx=7,
                                  pady=7,
                                  background='lightgrey',
                                  width=30,
                                  border=0, command=self.select_id(self.previous_id[i], i))
                id_label.pack(side=LEFT)
                id_del = Button(id_frame, text='del', width=25, padx=7, pady=7, background='lightgrey', border=0)
                id_del.pack(side=RIGHT)
                self.list_hist.append(id_label)

    def get_id_hist(self):
        try:
            with open(model_file, 'rb') as file:
                model_info = pickle.load(file)
        except EOFError:
            self.previous_id = []
        else:
            if len(model_info) > 0:
                for i in range(len(model_info)):
                    self.previous_id.append(model_info[i]["id"])

    # function within a function works when passing parameter to a function in for loop
    def select_id(self, name, ind):
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
                self.previous_id = []
                for i in range(len(model_info)):
                    self.previous_id.append(model_info[i]["id"])

                self.id = name
                self.state = model_info[index]["model"]
                self.prediction = model_info[index]["predictions"]
                self.performance_score = model_info[index]["performance"]
                self.num_of_present = model_info[index]["present"]
                self.num_of_absent = model_info[index]["absent"]

                self.show_input(self.state)
                self.reset_result_frame()
                # self.show_history()
                for j in range(len(self.list_hist)):
                    if j == ind:
                        self.list_hist[j].config(background='grey', width=0, height=0, text='')
                    else:
                        self.list_hist[j].config(background='lightgrey')

                l = Label(text='t')
                l.config()
                with open(model_file, 'wb') as file:
                    pickle.dump(model_info, file)

        return mini

    def hide_performance_gui(self):
        self.per_root.withdraw()

    def hide_order_gui(self):
        self.order_root.withdraw()

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
        print(self.focus_arr)

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

    def show_performance_gui(self):
        self.per_root.deiconify()

    def reset_result_frame(self):
        self.canvas_frame_res_wig.pack_forget()
        self.canvas_frame_res_wig = Frame(self.canvas_frame_res, background='lightgrey', padx=20, pady=3)
        self.canvas_frame_res_wig.pack(side='left', fill=BOTH, expand=1)
        for i in range(len(self.prediction)):
            if self.prediction[i] == 1:
                Label(self.canvas_frame_res_wig,
                      text='p' + str(i) + ': ' + 'this patient have heart disease',
                      background='lightgrey', font=14, ).pack()
                self.num_of_present += 1
            elif self.prediction[i] == 0:
                Label(self.canvas_frame_res_wig,
                      text='p' + str(i) + ': ' + 'this patient does not have heart disease',
                      background='lightgrey', font=14).pack()
                self.num_of_absent += 1
            else:
                Label(self.canvas_frame_res_wig,
                      text=self.prediction[i], background='lightgrey', fg='red', font=14, width=90).pack(pady=50)

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

        # print(model_info)

        with open(model_file, 'wb') as file:
            pickle.dump(model_info, file)

        self.id = obj["id"]
        self.previous_id.append(obj["id"])
        self.show_history()
    # self.performance_of_model(self.state)

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
                    print('ok')
                    should_check_performance = True
                else:
                    should_check_performance = False

                # checking prediction
                predictions = hpred.check_csv_validation(should_check_performance)

                self.prediction = predictions[0]
                self.performance_score = predictions[1]

                # resetting result frame
                self.reset_result_frame()

                self.create_data()

    def get_prediction(self):
        values = {}
        # getting all inputs inputted and putting them in a dictionary
        for i in range(len(self.cf_left_label_input)):
            if self.state == 'Naive Bayes' or self.state == 'Decision Tree':
                values[self.cf_left_label_value[i]] = self.cf_left_label_input[i].get()
            elif self.state == 'SVM':
                values[self.cf_left_label_value_S[i]] = self.cf_left_label_input[i].get()
        for j in range(len(self.cf_right_label_input)):
            if self.state == 'Naive Bayes' or self.state == 'Decision Tree':
                values[self.cf_right_label_value[j]] = self.cf_right_label_input[j].get()
            elif self.state == 'SVM':
                values[self.cf_right_label_value_S[j]] = self.cf_right_label_input[j].get()

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
            self.middle_frame.pack_forget()
            self.expand.config(text='collapse')
            self.is_expanded = True
        else:
            self.bottom_frame.pack_forget()
            self.middle_frame.pack(fill=X)
            self.bottom_frame.pack(fill=BOTH, expand=1, padx=14)
            self.expand.config(text='expand')

            self.scrollbar_result.pack_forget()
            self.scrollbar_result.pack(side='right', fill=Y)
            self.is_expanded = False

    def pack_widget(self):
        # performance window
        self.canvas_win.pack(side=LEFT, fill=BOTH, expand=1)
        self.scrollbar_win.pack(side=RIGHT, fill=Y)

        self.header_frame.pack(fill=X, side='top')
        self.middle_frame.pack(fill=BOTH)

        self.mid.pack_propagate(0)
        self.scrollbar_hist.pack(side=RIGHT, fill=Y)
        self.canvas_hist.pack(fill=BOTH, side=LEFT, expand=True)
        self.history_frame.pack(fill=X)
        self.history_label.pack(anchor='n', side=LEFT)
        self.history_close_btn.pack(anchor='n', side=RIGHT)
        self.id_hist.pack(fill=BOTH, expand=True)

        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.bottom_frame.pack(fill=BOTH, expand=1, padx=14)
        self.canvas_frame_wig.pack(fill=X, expand=True)

        # inner widget for header
        # why use place instead of pack for header frame widget?. Place worked better
        self.predict_btn.place(relx=0.01, rely=0.2)
        self.head_btn_frame.place(relx=0.35, rely=0.2)
        self.naive_btn.pack(side='left', padx=5)
        self.SVM_btn.pack(side='left', padx=5)
        self.DT_btn.pack(side='left', padx=5)
        self.options.place(relx=0.903, rely=0.2)

        # inner widget for middle section
        # self.cf_left_wig.pack(fill=BOTH, expand=True, side='left')
        # self.cf_right_wig.pack(fill=BOTH, expand=True, side='left')

        self.scrollbar.pack(side=RIGHT, fill=Y)

        # inner widget for bottom section
        self.canvas_result.pack(side='left', fill=BOTH, expand=True)
        self.scrollbar_result.pack(side='right', fill=Y)
        self.canvas_frame_res_wig.pack(fill=BOTH, expand=True, anchor='center')
        self.expand.pack(anchor='n', side=RIGHT)
        self.view_model_per.pack(anchor='n', side=LEFT)

        self.mainloop()

    # method to create new performance card any time metrics score button is clicked
    def performance_of_model(self, header):
        per_header = Frame(self.canvas_frame_win, pady=10, padx=10, bg='lightblue')
        head_label = Label(per_header, text=header + 'Performance Score', bg='lightblue',
                           font=('Times', 16, 'bold'), padx=10, pady=10)

        description_frame = Frame(self.canvas_frame_win, padx=10, pady=10, bg='white')

        card_HPresent = Frame(description_frame, width=500, height=100, bg='#c5c6d0', padx=20, pady=20)
        present_label = Label(card_HPresent,
                              text='There are' + str(self.num_of_present) + ' patients with heart disease',
                              bg='#c5c6d0', fg='#373737', font=('sans-serif', 12, 'bold'))
        absence_label = Label(card_HPresent,
                              text='There are' + str(self.num_of_absent) + ' patients without heart disease',
                              bg='#c5c6d0', fg='#373737', font=('sans-serif', 12, 'bold'))

        card_total = Frame(description_frame, width=500, height=100, bg='#c5c6d0')
        total_label = Label(card_total,
                            text='There are' + str(self.num_of_present + self.num_of_absent) + ' patients records',
                            bg='#c5c6d0', fg='#373737', font=('sans-serif', 12, 'bold'), padx=50, pady=50)

        metrics_frame = Frame(self.canvas_frame_win, padx=10, pady=10, bg='white')

        accuracy_card = Frame(metrics_frame, width=322, height=100, bg='#c5c6d0')
        accuracy_title = Label(accuracy_card,
                               text='Accuracy',
                               font=('Times', 16, 'bold'), pady=10, padx=10, bg='#c5c6d0', fg='#373737')
        accuracy_score = Label(accuracy_card,
                               text=str(self.performance_score[0]) + '%',
                               font=('Times', 16, 'bold'), pady=10, padx=10, bg='#c5c6d0', fg='#373737')

        precision_card = Frame(metrics_frame, width=322, height=100, bg='#c5c6d0')
        precision_title = Label(precision_card,
                                text='Precision',
                                font=('Times', 16, 'bold'), pady=10, padx=10, bg='#c5c6d0', fg='#373737')
        precision_score = Label(precision_card,
                                text=str(self.performance_score[1]) + '%',
                                font=('Times', 16, 'bold'), pady=10, padx=10, bg='#c5c6d0', fg='#373737')

        recall_card = Frame(metrics_frame, width=322, height=100, bg='#c5c6d0')
        recall_title = Label(recall_card,
                             text='Recall',
                             font=('Times', 16, 'bold'), pady=10, padx=10, bg='#c5c6d0', fg='#373737')
        recall_score = Label(recall_card,
                             text=str(self.performance_score[2]) + '%',
                             font=('Times', 16, 'bold'), pady=10, padx=10, bg='#c5c6d0', fg='#373737')

        # packing tje widget to the screen
        per_header.pack(fill=X, side=TOP)
        head_label.pack()

        description_frame.pack(fill=BOTH)
        card_HPresent.pack(side=LEFT, padx=10)
        card_HPresent.pack_propagate(0)
        present_label.pack(anchor='w')
        absence_label.pack(anchor='w')

        card_total.pack(side=LEFT, padx=10)
        card_total.pack_propagate(0)
        total_label.pack(anchor='center')

        metrics_frame.pack(fill=BOTH)
        accuracy_card.pack(side=LEFT, padx=10)
        accuracy_card.pack_propagate(0)
        accuracy_title.pack()
        accuracy_score.pack()

        precision_card.pack(side=LEFT, padx=10)
        precision_card.pack_propagate(0)
        precision_title.pack()
        precision_score.pack()

        recall_card.pack(side=LEFT, padx=10)
        recall_card.pack_propagate(0)
        recall_title.pack()
        recall_score.pack()

    @staticmethod
    def config_canvas(canvas, canvas_frame, scrollbar):
        canvas.configure(yscrollcommand=scrollbar.set)
        create_canvas = canvas.create_window((0, 0), window=canvas_frame, anchor='nw')
        canvas_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.bind('<Configure>', lambda e: canvas.itemconfig(create_canvas, width=e.width))

    @staticmethod
    def load_history_model():
        state = None
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
                return state["id"], \
                       state["model"], state["predictions"], state["performance"], state["present"], state["absent"]


App((700, 600)).pack_widget()
