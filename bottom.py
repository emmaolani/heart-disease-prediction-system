from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox


class BottomSection:
    def __init__(self, root):
        self.root = root
        self.diagnosis_labels = []
        self.is_expanded = False

        self.bottom_frame = Frame(self.root, bg='#F5F5F5', pady=10)
        self.bottom_frame.place(relx=0.0, rely=1, relwidth=1, anchor='sw', relheight=0.3)
        # Canvas use to create scrollable frame for prediction results
        self.canvas = Canvas(self.bottom_frame, background='lightgrey')
        self.canvas.pack(side='left', fill=BOTH, expand=True)
        # scrollbar for result frame
        self.scrollbar = Scrollbar(self.bottom_frame, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side='right', fill=Y)
        self.canvas_frame = Frame(self.canvas, background='lightgrey', width=200)
        # frame holding model performance and expand button
        self.stat_bar_frame = Frame(self.canvas, background='lightgrey')
        self.stat_bar_frame.place(relx=0.0, rely=0.0, relwidth=1)

        self.view_model_per = Button(self.stat_bar_frame,
                                     text="model performance",
                                     bg="grey", fg="white", border=0, width=13, padx=9, pady=5)
        self.view_model_per.pack(side=LEFT)

        self.expand = Button(self.stat_bar_frame,
                             text="expand", bg="grey", fg="white", border=0, width=13, padx=5, pady=5,
                             command=self.expand_collapse)
        self.expand.pack(side=RIGHT)
        self.diag_classifier = Label(self.stat_bar_frame,
                                     text='',
                                     background='lightgrey', font=('Times', 11), padx=5, pady=5)
        self.diag_classifier.pack(anchor='center', side=TOP)

        # widget holding the frame holding prediction result
        self.canvas_frame_wig = Frame(self.canvas_frame, background='lightgrey', padx=20, pady=30)
        self.canvas_frame_wig.pack(fill=BOTH, expand=True, anchor='center')
        self.canvas_frame_wig.columnconfigure(0, weight=1)
        self.canvas_frame_wig.rowconfigure(0, weight=1)
        #  widget holding prediction result
        self.result_frame = Frame(self.canvas_frame_wig, background='lightgrey')
        self.result_frame.columnconfigure(0, weight=1)
        self.result_frame.columnconfigure(1, weight=1)
        # creating 51 labels that holds individual heart disease input this label exists
        # within result_frame
        self.create_result_labels()

        # previous button in result button
        self.prev_btn = Button(self.canvas,
                               text='<',
                               padx=7,
                               pady=7,
                               border=0,
                               font=('sanserif', 11, 'bold'))
        self.prev_btn.place(relx=0.01, rely=1, anchor='sw')

        # next button in result button
        self.next_btn = Button(self.canvas,
                               text='>',
                               padx=7,
                               pady=7,
                               border=0,
                               font=('sanserif', 11, 'bold'))
        self.next_btn.place(relx=0.99, rely=1, anchor='se')
        # configuring the canvas for result widget to make it scrollable
        self.config_canvas(self.canvas, self.canvas_frame, self.scrollbar)

    def expand_collapse(self):
        if not self.is_expanded:
            self.expand.config(text='collapse')
            self.is_expanded = True
            self.bottom_frame.place_configure(relheight=1.0)
        else:
            self.expand.config(text='expand')
            self.is_expanded = False
            self.bottom_frame.place_configure(relheight=0.3)

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

    def render(self,
               diag,
               diag_index,
               increase_ndex_diagnosis, reduce_index_diagnosis, diagnosis_classifier, performance_score, update_show_per):
        index = diag_index
        diagnosis = diag['diagnosis']
        self.diag_classifier.configure(text=diagnosis_classifier)
        self.next_btn.configure(command=increase_ndex_diagnosis)
        self.prev_btn.configure(command=reduce_index_diagnosis)
        if performance_score is not None:
            self.view_model_per.configure(background='#0080FE')
            self.view_model_per.configure(command=lambda: update_show_per(True))
        else:
            self.view_model_per.configure(background='grey')
            self.view_model_per.configure(command='')

        for i in range(50):
            if index < len(diagnosis):
                if diagnosis[index] == 1:
                    result = 'This Patient have heart disease'
                else:
                    result = 'This patients does not have heart disease'
                self.diagnosis_labels[i]['diag'].configure(text=result)
                self.diagnosis_labels[i]['index'].configure(text=str(index))
            else:
                self.diagnosis_labels[i]['diag'].configure(text='')
                self.diagnosis_labels[i]['index'].configure(text='')
            index = index + 1

        HMI = index / 50

        if index <= 50:
            self.prev_btn.place_forget()
        else:
            self.prev_btn.place(relx=0.01, rely=1, anchor='sw')

        if HMI > diag['Tlength']:
            self.next_btn.place_forget()
        else:
            self.next_btn.place(relx=0.99, rely=1, anchor='se')

    @staticmethod
    def config_canvas(canvas, canvas_frame, scrollbar):
        canvas.configure(yscrollcommand=scrollbar.set)
        create_canvas = canvas.create_window((0, 0), window=canvas_frame, anchor='nw')
        canvas_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.bind('<Configure>', lambda e: canvas.itemconfig(create_canvas, width=e.width))
