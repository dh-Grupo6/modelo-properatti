# %%
#from IPython import get_ipython
#get_ipython().magic('reset -sf') 

# %%
%who_ls

# %%
"""
# DESAFIO MODELO PROPERATTI
"""

# %%
import Util as utl
import pandas as pd
import numpy as np

# %%


# %%
data = pd.read_csv('/home/DS-DH/notebooks/digitalHouse/properatti.csv')

# %%
data = utl.limpiarDatos(data,0.055)

# %%
#data = pd.read_csv('/home/DS-DH/notebooks/digitalHouse/data.csv',sep='|')
#data.to_csv('/home/DS-DH/notebooks/digitalHouse/data0_15.csv',sep='|')

# %%
matriz = utl.GenerarMatriz(data)

# %%
modeloMatriz = utl.generarDummies(matriz)

# %%
modeloMatriz.describe()

# %%
modeloMatriz_1=modeloMatriz_1[(modeloMatriz_1.precio_m2>100) & (modeloMatriz_1.precio_m2<5000)]

# %%
modeloMatriz_1.describe()

# %%
modeloMatriz_1.shape

# %%


# %%
modelo = utl.modelo_regresion_lineal(modeloMatriz_1)

# %%
from sklearn.cross_validation import cross_val_score

# %%
xs = modeloMatriz.iloc[:,1:]
y = modeloMatriz.iloc[:,0]
xs = xs.as_matrix()
y = y.as_matrix()
from sklearn import linear_model
from sklearn.model_selection import train_test_split
#PARTICIONAR DATOS DE ENTRENAMIENTO Y TESTING
x_train, x_test, y_train, y_test = train_test_split(xs, y, test_size=0.5)
modelo = linear_model.LinearRegression(fit_intercept=False,normalize=True)
modelo.fit(x_train,y_train)
scores = cross_val_score(modelo, x_train, y_train, cv=5)
print(scores)

# %%
print(scores[0])

# %%
 xs = modeloMatriz.iloc[:,1:]
    y = modeloMatriz.iloc[:,0]
    
    #for 
    #xs = xs.apply(lambda x: normalizar(x))
    #TRANSFORMO VARIABLES INDEPENDIENTES EN FORMATO MATRIZ
    xs = xs.as_matrix()
    #TRANSFORMO VARIABLE DEPENDIENTE EN FORMATO MATRIZ
    y = y.as_matrix()
    #IMPORTAR LIBRERIAS DE SKLEARN
    from sklearn import linear_model
    from sklearn.model_selection import train_test_split
    #PARTICIONAR DATOS DE ENTRENAMIENTO Y TESTING
    x_train, x_test, y_train, y_test = train_test_split(xs, y, test_size=0.4)
    #FIT 

  
    modelo = linear_model.LinearRegression(normalize=True)
    modelo.fit(x_train,y_train)
    #PREDECIR DATOS "Y" DE "X" TEST 
    y_predict = modelo.predict(x_test)
    #PENDIENTES
    pendientes = modelo.coef_
    #ORDENADA 
    ordenada = modelo.intercept_
    #R2
    #'EL RESULTADO DEL MODELO ES DE {}'.format(modelo.score(x_train,y_train))
    import matplotlib.pyplot as plt
    #GENERO EJE X -> SUPERFICIE TOTAL
    x1 = x_test[:,0]
    #GENERO EJE Y -> PRECIO M2 DE TEST
    x2 = y_test
    # EJE Y -> PRECIO M2 PREDICHO
    x3 = y_predict

    #PLOT
    plt.scatter(x1,x2,label='test modelo', color='blue')
    plt.scatter(x1,x3,label='prediccion modelo', color='red')
    plt.title('grafico modelo')
    plt.show()

    from sklearn import metrics
    import numpy as np
    print ('MAE:', metrics.mean_absolute_error(y_test, y_predict))
    print ('MSE:', metrics.mean_squared_error(y_test, y_predict))
    print ('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, y_predict)))
    print('EL R2 TRAIN ES DE: ', modelo.score(x_train,y_train))   
    print('EL R2 TEST ES DE: ', metrics.r2_score(y_test, y_predict))
    #print ('R2:', metrics.r2_score(y_test, y_predict))

# %%


# %%


# %%


# %%


# %%


# %%
"""
## PARAMETROS A PREDECIR
###### PARA LA PREDICCION DE PRECIOS POR M2 DE ALQUILERES EN CAPITAL FEDERAL
"""

# %%
SUPERFICIE_TOTAL = 50           ##  [0,600]
JARDIN = '1'                      ##  0,1
TERRAZA = '1'                     ##  0,1
CANTIDAD_DE_AMBIENTES = '3'       ##  1,2,3,4,4,5,6,7
TIPO_DE_PROPIEDAD = 'DTO'        ##  CASA, PH, DTO
BARRIO = 'caballito'               ##  barrios de CABA, en minusculas

nuevos_Feactures = utl.nuevosDatos(modeloMatriz, SUPERFICIE_TOTAL, JARDIN, TERRAZA, CANTIDAD_DE_AMBIENTES, TIPO_DE_PROPIEDAD, BARRIO)
y_predict = modelo.predict(nuevos_Feactures)

'EL RESULTADO DEL MODELO PARA LAS VARIABLES INGRESADAS ES DE {} U$D POR M2'.format(y_predict[0].astype(int))


# %%
SUPERFICIE_TOTAL = 200           ##  [0,600]
JARDIN = '1'                      ##  0,1
TERRAZA = '0'                     ##  0,1
CANTIDAD_DE_AMBIENTES = '1'       ##  1,2,3,4,4,5,6,7
TIPO_DE_PROPIEDAD = 'CASA'        ##  CASA, PH, DTO
BARRIO = 'avellaneda'               ##  barrios de CABA, en minusculas

nuevos_Feactures = utl.nuevosDatos(modeloMatriz, SUPERFICIE_TOTAL, JARDIN, TERRAZA, CANTIDAD_DE_AMBIENTES, TIPO_DE_PROPIEDAD, BARRIO)


# %%


# %%
"""
## CROSS VALIDATION
"""

# %%
"""
###### REGRESION LINEAL PARA MEDICION DE R2
"""

# %%
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.model_selection import cross_val_score

# %%


# %%
xs = modeloMatriz.iloc[:,1:]
y = modeloMatriz.iloc[:,0]

# %%
from sklearn import preprocessing
X_train, X_test, y_train, y_test = train_test_split(xs, y, test_size=0.4, random_state=10)

# %%


# %%
scaler = preprocessing.StandardScaler().fit(X_train)

# %%


# %%


# %%


# %%


# %%


# %%
"""
## LIMPIEZA DE OUTLIERS 
"""

# %%
data_original = pd.read_csv('/home/DS-DH/notebooks/digitalHouse/properatti.csv')

# %%
import matplotlib.pyplot as plt

#GENERO EJE X -> SUPERFICIE TOTAL
x1 = data_original.surface_total_in_m2

#GENERO EJE Y -> PRECIO M2 DE TEST
x2 = data_original.price_aprox_usd

# EJE Y -> PRECIO M2 PREDICHO
x3 = data.surface_total_in_m2

x4 = data.price_aprox_usd

#PLOT
plt.scatter(x1,x2,label='original', color='blue')
plt.scatter(x3,x4,label='limpiado', color='red')
plt.title('grafico limpieza')
plt.show()

# %%


# %%


# %%


# %%


# %%


# %%


# %%


# %%


# %%
"""
## DESCENSO GRADIENTE 
"""

# %%
%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import datasets, preprocessing

# %%
for x in xs:
    print (x.applymap(lambda x: x+1))

# %%
mean = np.mean(xs)
std = np.std(xs)

# %%
xs = [(x - mean) / std for x in xs]

# %%
mean = np.mean(y)
std = np.std(y)
y = [(y - mean) / std for y in y]

# %%


# %%


# %%


# %%
"""
# REGRESION MULTIPLE
"""

# %%



# %%


# %%


# %%


# %%
%matplotlib inline

from matplotlib import pyplot as plt
plt.rcParams['figure.figsize'] = 10, 10

import numpy as np
import pandas as pd
from scipy import stats
import seaborn as sns
from sklearn import datasets
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.linear_model import LinearRegression, Lasso, LassoCV, Ridge, RidgeCV
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.metrics import mean_squared_error, r2_score

# %%
xs = modeloMatriz.iloc[:,1:]
y = modeloMatriz.iloc[:,0]

# %%
X_train, X_test, y_train, y_test = train_test_split(xs, y, test_size=0.4)

# %%
X_train, X_test, y_train, y_test = train_test_split(xs, y, test_size=0.4)
print(X_train.shape, y_train.shape)
print(X_test.shape, y_test.shape)

# %%
al_ridge = np.linspace(0.001, 0.3, 300)
#al_lasso = np.linspace(0.1, 0.5, 300)
kf = KFold(n_splits=5, shuffle=True, random_state=12)

# %%


# %%
#lm = LinearRegression(normalize=True)
lm_ridge_cv= RidgeCV(alphas=al_ridge, cv=kf, normalize=True)
#lm_lasso_cv = LassoCV(alphas=al_lasso, cv=kf, normalize=True)

# %%
# Hacemos los fits respectivos
#lm.fit(X_train, y_train)
lm_ridge_cv.fit(X_train, y_train)
#lm_lasso_cv.fit(X_train, y_train)

# %%
print('Alpha Ridge:',lm_ridge_cv.alpha_,'\n')
      #'Alpha LASSO:',lm_lasso_cv.alpha_,'\n')

# %%
# Calculamos el R2

print(#" Score Train Lineal: %.2f\n" % lm.score(X_train, y_train),
      " Score Train Ridge : %.2f\n" % lm_ridge_cv.score(X_train, y_train))
      #" Score Train Lasso : %.2f\n" %  lm_lasso_cv.score(X_train, y_train))


# %%


# %%
import matplotlib.pyplot as plt

#GENERO EJE X -> SUPERFICIE TOTAL
x1 = X_test[:,0]

#GENERO EJE Y PARA TESTING DE RL
#x2 = lm.predict(y_train)

#GENERO EJE Y -> PRECIO M2 DE TEST
x3 = lm_ridge_cv.predict(y_test)

# EJE Y -> PRECIO M2 PREDICHO
x4 = lm_lasso_cv.predict(y_test)


#PLOT
plt.scatter(x1,x2,label='lineal multiple', color='blue')
plt.scatter(x1,x3,label='ridge', color='red')
plt.scatter(x1,x4,label='lasso', color='yellow')
plt.title('grafico comparacion regresiones lineal')
plt.show()

# %%


# %%


# %%
