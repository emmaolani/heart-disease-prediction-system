from tkinter import *
from tkinter import filedialog
from models import Hpred
from tkinter import messagebox
from performance_gui import Performance_gui


class App(Tk):
    def __init__(self, start_size):
        super().__init__()

        # performance window
        self.per_root = Toplevel()
        # changing function of close button from destroying second window to hiding second window
        self.per_root.protocol("WM_DELETE_WINDOW", self.hide_window_child)
        self.per_root.config(bg='white')
        self.per_root.title('Performance Evaluation')
        # creating a canvas for second window to enable scrolling
        self.canvas_win = Canvas(self.per_root, background='white')
        self.scrollbar_win = Scrollbar(self.per_root, orient=VERTICAL, command=self.canvas_win.yview)
        self.canvas_frame_win = Frame(self.canvas_win, background='white')
        self.config_canvas(self.canvas_win, self.canvas_frame_win, self.scrollbar_win)
        # hide toplevel window
        self.per_root.withdraw()

        self.cf_left_label_input = []
        self.cf_right_label_input = []

        self.cf_left_label_value = ['Age', 'Sex', 'Cp', 'Trestbps', 'Chol', 'Fbs', 'Restecg']
        self.cf_right_label_value = ['Thalch', 'Exang', 'Oldpeak', 'Slope', 'Ca', 'Thal', '']

        self.cf_left_label_value_S = ['Age', 'Cp', 'Trestbps', 'Chol', 'Restecg', 'Thalch']
        self.cf_right_label_value_S = ['Exang', 'Oldpeak', 'Slope', 'Ca', 'Thal', '']

        self.state = 'N'
        self.is_expanded = False
        self.focus_index = 3
        self.focus_arr = []
        self.num_of_present = 0
        self.num_of_absent = 0
        self.performance_score = []

        self.title("heart disease prediction system")
        self.geometry(f'{start_size[0]}x{start_size[1]}')
        self.config(bg='white')

        self.header_frame = Frame(self, bg='white', padx=20, pady=10)

        self.middle_frame = Frame(self, bg='white', padx=10, pady=10)
        self.canvas = Canvas(self.middle_frame, background='grey', height=450)
        self.scrollbar = Scrollbar(self.middle_frame, orient=VERTICAL, command=self.canvas.yview)
        self.canvas_frame = Frame(self.canvas, background='white', padx=20, pady=30)
        self.canvas_frame_wig = Frame(self.canvas_frame, padx=20, pady=30, background='lightgrey')
        self.bottom_frame = Frame(self, bg='white', padx=40, pady=10)

        self.config_canvas(self.canvas, self.canvas_frame, self.scrollbar)

        # inner widgets
        self.header_label = Label(self.header_frame, text='Prediction system', background='white')

        self.head_btn_frame = Frame(self.header_frame, background='white')

        self.naive_btn = Button(self.head_btn_frame, text='Naive bayes', bg="purple",
                                fg="white", border=0, width=13, padx=5, pady=5,
                                command=lambda: self.show_input('N', True))

        self.SVM_btn = Button(self.head_btn_frame, text='SVM',
                              bg="#0080FE", fg="white", border=0, width=13, padx=5, pady=5,
                              command=lambda: self.show_input('S', True))

        self.DT_btn = Button(self.head_btn_frame, text='Decision',
                             bg="#0080FE", fg="white", border=0, width=13, padx=5, pady=5,
                             command=lambda: self.show_input('D', True))

        self.import_btn = Button(self.header_frame,
                                 text="import CSV", bg="purple", fg="white", border=0, width=13, padx=5, pady=5,
                                 command=self.get_file)

        self.cf_left_wig = Frame(self.canvas_frame_wig, padx=20, pady=30, background='lightgrey')
        self.cf_right_wig = Frame(self.canvas_frame_wig, padx=20, pady=30, background='lightgrey')

        self.bottom_frame = Frame(self, bg='white', padx=10, pady=10)

        self.canvas_result = Canvas(self.bottom_frame, background='lightgrey')
        self.scrollbar_result = Scrollbar(self.bottom_frame, orient=VERTICAL, command=self.canvas_result.yview)
        self.canvas_frame_res = Frame(self.canvas_result, background='lightgrey', width=200)
        self.canvas_frame_res_wig = Frame(self.canvas_frame_res, background='lightgrey', padx=20, pady=30)

        self.config_canvas(self.canvas_result, self.canvas_frame_res, self.scrollbar_result)
        self.expand = Button(self.canvas_result,
                             text="expand", bg="grey", fg="white", border=0, width=13, padx=5, pady=5,
                             command=self.expand_collapse)

        self.predict_btn = Button(self.bottom_frame,
                                  text="Predict", bg="#0080FE", fg="white", border=0, width=9, padx=5, pady=5,
                                  command=self.get_prediction)

        self.show_input('N', False)
        self.push_to_focus_cat()

        # where to focus on start up
        self.focus_arr[self.focus_index].focus()

        self.bind('<Down>', lambda e: self.change_focus(e))
        self.bind('<Up>', lambda e: self.change_focus(e))

    # method to hide second window
    def hide_window_child(self):
        self.per_root.withdraw()

    # method to change focus when down or up arrow is pressed
    def change_focus(self, event):
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
        self.focus_arr[self.focus_index].focus_set()

    # creating the catalogue for order up and down button to transverse through widget
    def push_to_focus_cat(self):
        self.focus_arr.append(self.naive_btn)
        self.focus_arr.append(self.SVM_btn)
        self.focus_arr.append(self.DT_btn)
        for i in range(len(self.cf_left_label_input)):
            self.focus_arr.append(self.cf_left_label_input[i])
        for j in range(len(self.cf_right_label_input)):
            self.focus_arr.append(self.cf_right_label_input[j])
        self.focus_arr.append(self.predict_btn)

    def get_response(self):
        response = messagebox.askquestion("Model score", "Do you want to view performance score")
        if response == 'yes':
            if self.state == 'N':
                header = 'Naive Bayes '
            elif self.state == 'S':
                header = 'SVM '
            else:
                header = 'Decision Tree '

            Performance_gui(header,
                            self.num_of_present,
                            self.num_of_absent, self.performance_score, self.canvas_frame_win).pack()
            self.per_root.deiconify()
        else:
            pass

    def get_file(self):
        path = filedialog.askopenfile()
        if path is not None:
            if path.name.endswith('csv'):
                hpred = Hpred(path.name, self.state)
                predictions = hpred.check_csv_validation()

                self.performance_score = predictions[1]

                result = ''
                self.reset_result_frame(result)

                for i in range(len(predictions[0])):
                    if predictions[0][i] == 1:
                        Label(self.canvas_frame_res_wig,
                              text='p' + str(i) + ': ' + 'this patient have heart disease',
                              background='lightgrey', font=14, ).pack()
                        self.num_of_present += 1
                    if predictions[0][i] == 0:
                        Label(self.canvas_frame_res_wig,
                              text='p' + str(i) + ': ' + 'this patient does not have heart disease',
                              background='lightgrey', font=14).pack()
                        self.num_of_absent += 1

                self.get_response()

                self.num_of_present = 0
                self.num_of_absent = 0

    def get_prediction(self):
        values = {}
        # getting all inputs inputed and puting them in a dictionary
        for i in range(len(self.cf_left_label_input)):
            if self.state == 'N' or self.state == 'D':
                values[self.cf_left_label_value[i]] = self.cf_left_label_input[i].get()
            elif self.state == 'S':
                values[self.cf_left_label_value_S[i]] = self.cf_left_label_input[i].get()
        for j in range(len(self.cf_right_label_input)):
            if self.state == 'N' or self.state == 'D':
                values[self.cf_right_label_value[j]] = self.cf_right_label_input[j].get()
            elif self.state == 'S':
                values[self.cf_right_label_value_S[j]] = self.cf_right_label_input[j].get()

        # calling passing the dictionary to heart disease prediction class and training the inputed values
        hpred = Hpred(values, self.state)
        predictions = hpred.check_value_validation()

        # hpred returns an array of [err, index of] or [predictions]
        if predictions[0] == 'val error':
            if self.state == 'S' and predictions[2] > 5:
                predictions[2] = predictions[2] - 6
            if (self.state == 'N' or self.state == 'D') and predictions[2] > 6:
                predictions[2] = predictions[2] - 7

            result = 'incorrect value given at input ' + predictions[1]
            self.reset_result_frame(result)

        elif predictions[0] == 'not in range':
            if self.state == 'S' and predictions[2] > 5:
                predictions[2] = predictions[2] - 6
            if (self.state == 'N' or self.state == 'D') and predictions[2] > 6:
                predictions[2] = predictions[2] - 7

            result = 'value give is not in range at input ' + predictions[1]
            self.reset_result_frame(result)
        else:
            if predictions[0] == 1:
                result = 'this patient have heart disease'
                self.reset_result_frame(result)
            if predictions[0] == 0:
                result = 'this patient does not have heart disease'
                self.reset_result_frame(result)

    def show_input(self, state, is_clicked):
        sel_cf_left_label_value = []
        sel_cf_right_label_value = []
        if is_clicked:
            self.cf_left_label_input = []
            self.cf_right_label_input = []
            self.cf_left_wig.pack_forget()
            self.cf_right_wig.pack_forget()
            self.cf_left_wig = Frame(self.canvas_frame_wig, padx=20, pady=30, background='lightgrey')
            self.cf_right_wig = Frame(self.canvas_frame_wig, padx=20, pady=30, background='lightgrey')
            self.cf_left_wig.pack(fill=BOTH, expand=True, side='left')
            self.cf_right_wig.pack(fill=BOTH, expand=True, side='left')
            if state == 'N':
                self.state = 'N'
                sel_cf_left_label_value = self.cf_left_label_value
                sel_cf_right_label_value = self.cf_right_label_value
                self.naive_btn.config(background='purple')
                self.SVM_btn.config(background="#0080FE")
                self.DT_btn.config(background='#0080FE')
            if state == 'S':
                self.state = 'S'
                sel_cf_left_label_value = self.cf_left_label_value_S
                sel_cf_right_label_value = self.cf_right_label_value_S
                self.naive_btn.config(background='#0080FE')
                self.SVM_btn.config(background='purple')
                self.DT_btn.config(background='#0080FE')
            if state == 'D':
                self.state = 'D'
                sel_cf_left_label_value = self.cf_left_label_value
                sel_cf_right_label_value = self.cf_right_label_value
                self.naive_btn.config(background='#0080FE')
                self.SVM_btn.config(background='#0080FE')
                self.DT_btn.config(background='purple')
        else:
            sel_cf_left_label_value = self.cf_left_label_value
            sel_cf_right_label_value = self.cf_right_label_value

        for i in range(len(sel_cf_left_label_value)):
            cont_frame3 = Frame(self.cf_left_wig, background='lightgrey')
            cont_frame3.pack(fill=X, expand=True)
            Label(cont_frame3, text=sel_cf_left_label_value[i], background='lightgrey').pack(anchor='w', padx=20)
            input_box = Entry(cont_frame3, width=40, border=0)
            input_box.pack(fill=X, expand=True, padx=20, pady=10, ipadx=5, ipady=5)
            self.cf_left_label_input.append(input_box)

        # widget for frame 4
        for i in range(len(sel_cf_right_label_value)):
            cont_frame4 = Frame(self.cf_right_wig, background='lightgrey')
            cont_frame4.pack(fill=X, expand=True)
            Label(cont_frame4, text=sel_cf_right_label_value[i], background='lightgrey').pack(anchor='w', padx=20)
            if i == 5 and self.state == 'S':
                Label(cont_frame4, width=40, border=0, background='lightgrey').pack(fill=X, expand=True, padx=20,
                                                                                    pady=10, ipadx=5, ipady=5)
            elif i == 6:
                Label(cont_frame4, width=40, border=0, background='lightgrey').pack(fill=X, expand=True, padx=20,
                                                                                    pady=10, ipadx=5, ipady=5)
            else:
                input_box = Entry(cont_frame4, width=40, border=0)
                input_box.pack(fill=X, expand=True, padx=20, pady=10, ipadx=5, ipady=5)
                self.cf_right_label_input.append(input_box)

        if is_clicked:
            self.focus_arr = []
            self.push_to_focus_cat()
            self.focus_index = 3

    def reset_result_frame(self, res):
        self.canvas_frame_res_wig.pack_forget()
        self.canvas_frame_res_wig = Frame(self.canvas_frame_res, background='lightgrey', padx=20, pady=3)
        self.canvas_frame_res_wig.pack(side='left', fill=BOTH, expand=True)
        if res != '':
            Label(self.canvas_frame_res_wig, text=res, background='lightgrey', fg='red', font=14).pack()

    def expand_collapse(self):
        if not self.is_expanded:
            self.middle_frame.pack_forget()
            self.expand.config(text='collapse')
            self.is_expanded = True
            self.predict_btn.pack_forget()
        else:
            self.bottom_frame.pack_forget()

            self.middle_frame.pack(fill=X)
            self.bottom_frame.pack(fill=BOTH, expand=1, padx=14)
            self.expand.config(text='expand')

            self.predict_btn.pack(side='right')
            self.scrollbar_result.pack_forget()
            self.scrollbar_result.pack(side='right', fill=Y)
            self.is_expanded = False

    def pack_widget(self):
        # performance window
        self.canvas_win.pack(side=LEFT, fill=BOTH, expand=1)
        self.scrollbar_win.pack(side=RIGHT, fill=Y)

        self.header_frame.pack(fill=X, side='top')
        self.middle_frame.pack(fill=X)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.bottom_frame.pack(fill=BOTH, expand=1, padx=14)
        self.canvas_frame_wig.pack(fill=X, expand=True)

        # inner widget for header
        self.header_label.pack(side='left')
        self.head_btn_frame.pack(side='left', padx=400)
        self.naive_btn.pack(side='left', padx=5)
        self.SVM_btn.pack(side='left', padx=5)
        self.DT_btn.pack(side='left', padx=5)
        self.import_btn.pack(side='right')

        # inner widget for middle section
        self.cf_left_wig.pack(fill=BOTH, expand=True, side='left')
        self.cf_right_wig.pack(fill=BOTH, expand=True, side='left')

        # inner widget for bottom section
        self.predict_btn.pack(side=RIGHT, padx=8)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.canvas_result.pack(side='left', fill=BOTH, expand=True)
        self.scrollbar_result.pack(side='right', fill=Y)
        self.canvas_frame_res_wig.pack(fill=BOTH, expand=True)
        self.expand.pack(anchor='e')

        self.mainloop()

    @staticmethod
    def config_canvas(canvas, canvas_frame, scrollbar):
        canvas.configure(yscrollcommand=scrollbar.set)
        create_canvas = canvas.create_window((0, 0), window=canvas_frame, anchor='nw')
        canvas_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.bind('<Configure>', lambda e: canvas.itemconfig(create_canvas, width=e.width))


App((700, 600)).pack_widget()
