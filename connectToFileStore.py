import pickle

model_file = 'db/model db.txt'


def getLog(start, end):
    try:
        with open(model_file, 'rb') as file:
            model_info = pickle.load(file)
    except EOFError:
        return []
    else:
        logs = {
            'logs': [],
            'Tlength': 0
        }
        if len(model_info) > 0:
            TLength = len(model_info) / 10
            logs['Tlength'] = TLength
            for i in range(start, end):
                if i <= len(model_info) - 1:
                    sid = model_info[i]['id']
                    logs['logs'].append(sid)

        return logs


def getPredictions(sid):
    try:
        with open(model_file, 'rb') as file:
            model_info = pickle.load(file)
    except EOFError:
        return []
    else:
        diagnosis = {
            'diagnosis': [],
            'Tlength': 0
        }
        performance = [],
        classifier = ''

        if len(model_info) > 0:
            for data in model_info:
                if data['id'] == sid:
                    TLength = len(data['predictions']) / 50
                    diagnosis['Tlength'] = TLength
                    diagnosis['diagnosis'] = data['predictions']
                    performance = data['performance']
                    classifier = data['model']

        return [diagnosis, performance, classifier]


def insertData(data):
    try:
        with open(model_file, 'rb') as file:
            model_info = pickle.load(file)
    except EOFError:
        return []
    else:
        model_info.append(data)
        with open(model_file, 'wb') as file:
            pickle.dump(model_info, file)


def deleteData(sid):
    try:
        with open(model_file, 'rb') as file:
            model_info = pickle.load(file)
    except EOFError:
        return []
    else:
        del_index = None
        for i in range(len(model_info)):
            if model_info[i]['id'] == sid:
                del_index = i

        model_info.pop(del_index)
        with open(model_file, 'wb') as file:
            pickle.dump(model_info, file)

