from tkinter import *


class Performance_gui:
    def __init__(self, root):
        self.root = root
        # changing function of close button from destroying second window to hiding second window
        self.root.protocol("WM_DELETE_WINDOW", self.hide_performance_gui)
        self.root.config(bg='white')
        self.root.title('Performance Evaluation')

        # creating header frame
        self.header = Frame(self.root, pady=10, padx=10, bg='lightblue')
        self.header.pack(fill=X, side=TOP)

        self.head_label = Label(self.header, text='', bg='lightblue',
                                font=('Times', 16, 'bold'), padx=10, pady=10)
        self.head_label.pack()

        # creating a frame that shows stats like the number of patients, number of patients with or without heart
        # disease
        self.description_frame = Frame(self.root, padx=10, pady=10, bg='white')
        self.description_frame.pack(fill=BOTH)

        # creating a frame that holds 2 label with number of patients with or without heart disease respectively
        self.card_HPresent = Frame(self.description_frame, width=500, height=100, bg='#c5c6d0', padx=20, pady=20)
        self.card_HPresent.pack(side=LEFT, padx=10)
        self.card_HPresent.pack_propagate(0)

        # label showing number of patients with heart disease
        self.present_label = Label(self.card_HPresent,
                                   text='',
                                   bg='#c5c6d0', fg='#373737', font=('sans-serif', 12, 'bold'))
        self.present_label.pack(anchor='w')

        # label showing number of patients without heart disease
        self.absence_label = Label(self.card_HPresent,
                                   text='',
                                   bg='#c5c6d0', fg='#373737', font=('sans-serif', 12, 'bold'))
        self.absence_label.pack(anchor='w')

        # A frame that holds a label that shows the total number of patients
        self.card_total = Frame(self.description_frame, width=500, height=100, bg='#c5c6d0')
        self.card_total.pack(side=LEFT, padx=10)
        self.card_total.pack_propagate(0)

        # label that shows the total number of patients
        self.total_label = Label(self.card_total,
                                 text='',
                                 bg='#c5c6d0', fg='#373737', font=('sans-serif', 12, 'bold'), padx=50, pady=50)
        self.total_label.pack(anchor='center')

        self.metrics_frame = Frame(self.root, padx=10, pady=10, bg='white')
        self.metrics_frame.pack(fill=BOTH)

        self.accuracy_card = Frame(self.metrics_frame, width=322, height=100, bg='#c5c6d0')
        self.accuracy_card.pack(side=LEFT, padx=10)
        self.accuracy_card.pack_propagate(0)

        self.accuracy_title = Label(self.accuracy_card,
                                    text='Accuracy',
                                    font=('Times', 16, 'bold'), pady=10, padx=10, bg='#c5c6d0', fg='#373737')
        self.accuracy_title.pack()

        self.accuracy_score = Label(self.accuracy_card,
                                    text='',
                                    font=('Times', 16, 'bold'), pady=10, padx=10, bg='#c5c6d0', fg='#373737')
        self.accuracy_score.pack()

        self.precision_card = Frame(self.metrics_frame, width=322, height=100, bg='#c5c6d0')
        self.precision_card.pack(side=LEFT, padx=10)
        self.precision_card.pack_propagate(0)

        self.precision_title = Label(self.precision_card,
                                     text='Precision',
                                     font=('Times', 16, 'bold'), pady=10, padx=10, bg='#c5c6d0', fg='#373737')
        self.precision_title.pack()

        self.precision_score = Label(self.precision_card,
                                     text='',
                                     font=('Times', 16, 'bold'), pady=10, padx=10, bg='#c5c6d0', fg='#373737')
        self.precision_score.pack()

        self.recall_card = Frame(self.metrics_frame, width=322, height=100, bg='#c5c6d0')
        self.recall_card.pack(side=LEFT, padx=10)
        self.recall_card.pack_propagate(0)

        self.recall_title = Label(self.recall_card,
                                  text='Recall',
                                  font=('Times', 16, 'bold'), pady=10, padx=10, bg='#c5c6d0', fg='#373737')
        self.recall_title.pack()

        self.recall_score = Label(self.recall_card,
                                  text='',
                                  font=('Times', 16, 'bold'), pady=10, padx=10, bg='#c5c6d0', fg='#373737')
        self.recall_score.pack()

        # hiding window on start up
        self.hide_performance_gui()

    def hide_performance_gui(self):
        self.root.withdraw()

    def update_performance_gui(self, model, presence, absence, performance):
        self.head_label.configure(text=model)
        self.present_label.configure(text='There are ' + str(presence) + ' patients with heart disease')
        self.absence_label.configure(text='There are ' + str(absence) + ' patients without heart disease')
        self.total_label.configure(text='There are a total of ' + str(absence + presence) + ' patients')
        self.accuracy_score.configure(text=str(performance[0]) + '%')
        self.precision_score.configure(text=str(performance[1]) + '%')
        self.recall_score.configure(text=str(performance[2]) + '%')

    def show_performance_gui(self):
        self.root.deiconify()
