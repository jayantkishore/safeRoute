import pandas as pd
import numpy as np

df = pd.read_csv('crime.csv')
#df.describe()

from sklearn.model_selection import train_test_split
train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

X=train_set[['latitude','longitude']]
Y=train_set['cluster']

from sklearn.neighbors import KNeighborsRegressor
import pickle

neigh = KNeighborsRegressor(n_neighbors=5,weights='distance')
neigh.fit(X.values,Y.values)
# save the model to disk
filename = 'finalized_kNN_model.sav'
pickle.dump(neigh, open(filename, 'wb'))



def predict(lat,lng):
  return neigh.predict([[lat,lng]])

# load the model from disk
x_test=test_set[['latitude','longitude']]
y_test=test_set['cluster']
loaded_model = pickle.load(open(filename, 'rb'))
y_pred1 = loaded_model.predict(x_test.values)


from sklearn.metrics import mean_squared_error
mse = mean_squared_error(y_test.values,y_pred1)
rmse = np.sqrt(mse)
print(rmse)
