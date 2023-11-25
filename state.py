from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from top import TopSection
from middle import MiddleSection
from bottom import BottomSection
from performance_gui import Performance_gui
from connectToFileStore import getPredictions, getLog, insertData, deleteData
from models import Hpred
from datetime import datetime


class State(Tk):
    def __init__(self):
        super().__init__()

        self.id = None
        self.classifier = 'Naive Bayes'
        self.index_diagnosis = 0
        self.diagnosis = {
            'diagnosis': [],
            'Tlength': 0
        }
        self.diagnosis_classifier = ''
        self.performance_score = None
        self.show_logs = False
        self.show_per_page = False
        self.index_logs = 0
        self.logs = {}

        # initializing the main window root
        self.title("Heart Disease Prediction System")
        self.geometry('500x500+200+200')
        self.root_per = Toplevel()
        self.TopSection = TopSection(self)
        self.MiddleSection = MiddleSection(self)
        self.BottomSection = BottomSection(self)
        self.Performance_gui = Performance_gui(self.root_per, self.updateShowPer)

        self.updateLog()
        self.mainloop()

    def renderComponent(self):
        self.TopSection.render(self.classifier, self.updateClassifier, self.openLog, self.get_prediction_csv)
        self.MiddleSection.render(self.classifier,
                                  self.logs['logs'],
                                  self.index_logs,
                                  self.show_logs,
                                  self.id,
                                  self.logs['Tlength'],
                                  self.closeLog, self.changeState, self.moveUp, self.moveDown, self.delete_data)
        self.BottomSection.render(self.diagnosis,
                                  self.index_diagnosis,
                                  self.increaseIndexDiagnosis,
                                  self.reduceIndexDiagnosis,
                                  self.diagnosis_classifier, self.performance_score, self.updateShowPer)
        self.Performance_gui.render(self.diagnosis_classifier,
                                    self.performance_score, self.diagnosis, self.show_per_page, self.updateShowPer)

    def closeLog(self):
        self.show_logs = False
        self.renderComponent()

    def openLog(self):
        self.show_logs = True
        self.renderComponent()

    def updateShowPer(self, boolean):
        self.show_per_page = boolean
        self.renderComponent()

    def changeState(self, sid):
        self.id = sid
        self.index_diagnosis = 0
        predictions = getPredictions(self.id)
        self.diagnosis = predictions[0]
        self.performance_score = predictions[1]
        self.diagnosis_classifier = predictions[2]
        self.renderComponent()

    def moveUp(self):
        self.index_logs = self.index_logs - 10
        self.updateLog()

    def moveDown(self):
        self.index_logs = self.index_logs + 10
        self.updateLog()

    def updateClassifier(self, classifier):
        self.classifier = classifier
        self.renderComponent()

    def increaseIndexDiagnosis(self):
        self.index_diagnosis = self.index_diagnosis + 50
        self.renderComponent()

    def reduceIndexDiagnosis(self):
        self.index_diagnosis = self.index_diagnosis - 50
        self.renderComponent()

    def updateLog(self):
        start = self.index_logs
        if start == 0:
            end = 10
        else:
            end = start * 2

        self.logs = getLog(start, end)
        self.renderComponent()

    def get_prediction_csv(self):
        # resetting number of patient with and without heart disease
        path = filedialog.askopenfile()
        if path is not None:
            if path.name.endswith('csv'):
                hpred = Hpred(path.name, self.classifier)

                info = messagebox.askquestion('check performance', 'Do you want to check performance')
                if info == 'yes':
                    should_check_performance = True
                else:
                    should_check_performance = False

                # checking prediction
                result = hpred.check_csv_validation(should_check_performance)
                data = self.create_data(result)
                insertData(data)
                self.changeState(data['id'])
                self.updateLog()

    def create_data(self, result):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        obj = {
            "id": dt_string + " " + str(1),
            "model": self.classifier,
            "predictions": result[0],
            "performance": result[1],
        }
        return obj

    def delete_data(self, sid):
        deleteData(sid)
        if sid == self.id:
            self.id = None
            self.classifier = 'Naive Bayes'
            self.index_diagnosis = 0
            self.diagnosis = {
                'diagnosis': [],
                'Tlength': 0
            }
            self.diagnosis_classifier = ''
            self.performance_score = None
            self.show_logs = False
            self.show_per_page = False
            self.index_logs = 0
            self.logs = {}

        self.updateLog()


State()
