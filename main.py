import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2


def val_for_defected_row(dfr, null):
    temp_df = dfr
    for i in range(len(null[0])):
        temp_df = temp_df.drop(null[0][i])

    value = np.array([])

    for j in range(len(null[1])):
        min_value = dfr.iloc[:, null[1][j]].min()
        value = np.append(value, min_value)

    return value


def add_missing_val(dfr, nul_val, rep_val):
    for i in range(len(rep_val)):
        dfr.iat[nul_val[0][i], nul_val[1][i]] = rep_val[i]
    return dfr


data = pd.read_csv("processed.cleveland.csv", header=None)
columns = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca',
           'thal', 'target']
data.columns = columns
null_val = np.where(data == '?')
replace_value = val_for_defected_row(data, null_val)
data = add_missing_val(data, null_val, replace_value)

data.loc[data['target'] > 1, 'target'] = 1

print(null_val)
print(data)
print('value: ', replace_value)

data = data.astype(float)
df = data.to_numpy()
print('array', df)

# feature selection
x = data.iloc[:, 0:13]
y = data.iloc[:, -1]

# apply SelectKBest class to extract top 5 feature
best_features = SelectKBest(score_func=chi2, k=13)
fit = best_features.fit(x, y)

df_scores = pd.DataFrame(fit.scores_)
df_columns = pd.DataFrame(x.columns)

features_scores = pd.concat([df_columns, df_scores], axis=1)
features_scores.columns = ['specs', 'scores']
print(features_scores)

# logistic regression gradient descent

y = data["target"].to_numpy()

row = x.to_numpy()
target = data.iloc[:, -1].to_numpy()
weights = np.transpose(row)

for i in range(0, len(weights)):
    mean = np.mean(weights[i])
    maxi = np.max(weights[i])
    mini = np.min(weights[i])
    weights[i] = (weights[i] - mean) / (maxi - mini)

scaled_row = np.transpose(weights)
slopes = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=float)
sub_slop = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=float)
intercept = 0
sub_intercept = 0
learning_rate = 0.01
jw = np.array([])
iterations = np.array([])


def lin_regression():
    sub_reg = np.dot(scaled_row, slopes.reshape(-1, 1))
    reg = sub_reg.ravel() + intercept
    return reg


def lo():
    linear_reg = lin_regression()
    expon = np.exp(-1 * linear_reg)
    expon = expon + 1
    g = 1 / expon
    return g


def loss_function():
    linear_reg = lin_regression()
    expon = np.exp(-1 * linear_reg)
    g = 1 / (expon + 1)
    # calculate (f(x)-y)x
    loss_funct = g - y
    return loss_funct


def logistic_regression():
    loss_funct = loss_function()
    for j in range(0, len(sub_slop)):
        derived = loss_funct * weights[j]
        derived = derived.sum() / len(y)
        sub_slop[j] = derived


for i in range(200000):
    logistic_regression()
    loss_int = loss_function()
    sub_intercept = loss_int.sum() / len(y)

    l = lo()
    sub_jw = -y * np.log(l) - (1 - y) * np.log(1 - l)
    jw = np.append(jw, sub_jw.sum() / len(y))
    iterations = np.append(iterations, i)

    slopes = slopes - (learning_rate * sub_slop)
    intercept = intercept - (learning_rate * sub_intercept)

    print(slopes)
    print(intercept)

print(jw)
print(iterations)
plt.scatter(iterations, jw, c="blue")
plt.show()

