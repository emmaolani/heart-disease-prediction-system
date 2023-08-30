from tkinter import *


class Performance_gui:
    def __init__(self, header, present, absence, metrics, root):
        self.per_root = root
        self.header = header
        self.present = present
        self.absence = absence
        self.metrics = metrics
        self.per_header = Frame(self.per_root, pady=10, padx=10, bg='lightblue')

        self.head_label = Label(self.per_header, text=self.header + 'Performance Score', bg='lightblue',
                                font=('Times', 16, 'bold'), padx=10, pady=10)

        self.description_frame = Frame(self.per_root, padx=10, pady=10, bg='white')

        self.card_HPresent = Frame(self.description_frame, width=500, height=100, bg='#c5c6d0', padx=20, pady=20)
        self.present_label = Label(self.card_HPresent,
                                   text='There are' + str(self.present) + ' patients with heart disease',
                                   bg='#c5c6d0', fg='#373737', font=('sans-serif', 12, 'bold'))
        self.absence_label = Label(self.card_HPresent,
                                   text='There are' + str(self.absence) + ' patients without heart disease',
                                   bg='#c5c6d0', fg='#373737', font=('sans-serif', 12, 'bold'))

        self.card_total = Frame(self.description_frame, width=500, height=100, bg='#c5c6d0')
        self.total_label = Label(self.card_total,
                                 text='There are' + str(self.present + self.absence) + ' patients records',
                                 bg='#c5c6d0', fg='#373737', font=('sans-serif', 12, 'bold'), padx=50, pady=50)

        self.metrics_frame = Frame(self.per_root, padx=10, pady=10, bg='white')

        self.accuracy_card = Frame(self.metrics_frame, width=322, height=100, bg='#c5c6d0')
        self.accuracy_title = Label(self.accuracy_card,
                                    text='Accuracy',
                                    font=('Times', 16, 'bold'), pady=10, padx=10, bg='#c5c6d0', fg='#373737')
        self.accuracy_score = Label(self.accuracy_card,
                                    text=str(self.metrics[0])+ '%',
                                    font=('Times', 16, 'bold'), pady=10, padx=10, bg='#c5c6d0', fg='#373737')

        self.precision_card = Frame(self.metrics_frame, width=322, height=100, bg='#c5c6d0')
        self.precision_title = Label(self.precision_card,
                                     text='Precision',
                                     font=('Times', 16, 'bold'), pady=10, padx=10, bg='#c5c6d0', fg='#373737')
        self.precision_score = Label(self.precision_card,
                                     text=str(self.metrics[1])+ '%',
                                     font=('Times', 16, 'bold'), pady=10, padx=10, bg='#c5c6d0', fg='#373737')

        self.recall_card = Frame(self.metrics_frame, width=322, height=100, bg='#c5c6d0')
        self.recall_title = Label(self.recall_card,
                                  text='Recall',
                                  font=('Times', 16, 'bold'), pady=10, padx=10, bg='#c5c6d0', fg='#373737')
        self.recall_score = Label(self.recall_card,
                                  text=str(self.metrics[2]) + '%',
                                  font=('Times', 16, 'bold'), pady=10, padx=10, bg='#c5c6d0', fg='#373737')

    def pack(self):
        self.per_header.pack(fill=X, side=TOP)
        self.head_label.pack()

        self.description_frame.pack(fill=BOTH)
        self.card_HPresent.pack(side=LEFT, padx=10)
        self.card_HPresent.pack_propagate(0)
        self.present_label.pack(anchor='w')
        self.absence_label.pack(anchor='w')

        self.card_total.pack(side=LEFT, padx=10)
        self.card_total.pack_propagate(0)
        self.total_label.pack(anchor='center')

        self.metrics_frame.pack(fill=BOTH)
        self.accuracy_card.pack(side=LEFT, padx=10)
        self.accuracy_card.pack_propagate(0)
        self.accuracy_title.pack()
        self.accuracy_score.pack()

        self.precision_card.pack(side=LEFT, padx=10)
        self.precision_card.pack_propagate(0)
        self.precision_title.pack()
        self.precision_score.pack()

        self.recall_card.pack(side=LEFT, padx=10)
        self.recall_card.pack_propagate(0)
        self.recall_title.pack()
        self.recall_score.pack()



