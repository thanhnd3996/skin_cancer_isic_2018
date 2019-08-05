import numpy as np
import xgboost as xgb
from numpy import sort
from matplotlib import pyplot
from xgboost import plot_importance
from sklearn.metrics import accuracy_score
from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import confusion_matrix

# diagnosis
diagnosis = ['AKIEC', 'BCC', 'BKL', 'DF', 'MEL', 'NV', 'VASC']

# load feature and label from file
X_train = np.load('X_train.npy')
y_train = np.load('y_train.npy')
X_val = np.load('X_val.npy')
y_val = np.load('y_val.npy')

print('Training and making predictions')
clf = xgb.XGBClassifier(max_depth=15, learning_rate=0.1, n_estimators=200)
clf.fit(X_train, y_train)

predictions = clf.predict(X_val)
accuracy = accuracy_score(y_val, predictions)
print("Accuracy: %.2f%%" % (accuracy * 100))

plot_importance(clf)

pyplot.show()
thresh = 50
thresholds = sort(clf.feature_importances_)
selection = SelectFromModel(clf, threshold=thresh, prefit=True)
select_X_train = selection.transform(X_train)
selection_model = xgb.XGBClassifier(max_depth=15, learning_rate=0.1, n_estimators=200)
selection_model.fit(select_X_train, y_train)

select_X_val = selection.transform(X_val)
predictions = clf.predict(select_X_val)

accuracy = accuracy_score(y_val, predictions)
cm = confusion_matrix(y_val, predictions)
cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
cm.diagonal()
print("New_Accuracy: %.2f%%" % (accuracy * 100))
