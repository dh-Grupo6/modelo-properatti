import pandas as pd
import numpy as np

data = pd.read_csv('properatti.csv')
matriz = pd.read_csv('matriz.csv',sep='|')


#GENERO AMBIENTES DE MATRIZ
#data_['ambientes']=data_.merge(matriz,how='left', left_index=True, right_index=True)['ambientes']

#GENERO DUMMYS DE AMBIENTES
data_['1_AMBIENTE'] = (data_.ambientes>=1)&(data_.ambientes<2)
data_['2_AMBIENTE'] = (data_.ambientes>=2)&(data_.ambientes<3)
data_['3_AMBIENTE'] = (data_.ambientes>=3)&(data_.ambientes<4)
data_['4_AMBIENTE'] = (data_.ambientes>=4)&(data_.ambientes<5)
data_['5_AMBIENTE'] = (data_.ambientes>=5)&(data_.ambientes<6)
data_['6_AMBIENTE'] = (data_.ambientes>=6)&(data_.ambientes<7)
data_['7_AMBIENTE'] = (data_.ambientes>=7)&(data_.ambientes<8)

data_[['1_AMBIENTE','2_AMBIENTE','3_AMBIENTE','4_AMBIENTE', '5_AMBIENTE','6_AMBIENTE','7_AMBIENTE']] = data_[['1_AMBIENTE','2_AMBIENTE','3_AMBIENTE','4_AMBIENTE', '5_AMBIENTE','6_AMBIENTE','7_AMBIENTE']].applymap(lambda x : 1 if (x) else 0)


#GENERO DUMMYS TIPO DE PROPIEDAD 
data_['CASA'] = data_.property_type.str.contains('house')
data_['PH'] =  data_.property_type.str.contains('PH')
data_['DTO'] = data_.property_type.str.contains('apartment')
data_[['CASA','PH','DTO']] = data_[['CASA','PH','DTO']].applymap(lambda x : 1 if x else 0)

#ELIMINO REGISTROS NULOS DE VARIABLES A UTILIZAR EN EL MODELO
data_=data_[data_.price_usd_per_m2.notnull()]
data_=data_[data_.surface_total_in_m2.notnull()]
data_=data_[data_.ambientes.notnull()]


#GENERO DUMMYS DE BARRIOS

#QUITO NULOS DE LA COLUMNA STATE_NAME
data_ = data_[data.place_name.notnull()]


#CREO LISTA DE BARRIOS 
barrios = data_[data_.state_name.str.contains('Capital')].place_name.unique()


#GENERO DUMMYS
for barrio in barrios:
    indices_barrios = (data_.index[data_.place_name.str.contains(barrio)])
    barrio = barrio.lower().replace(' ','_')
    df = data_
    df.place_name = df.place_name.apply(lambda x : x.lower().replace(' ','_'))
    df[barrio] = df.place_name.str.contains(barrio)


numero_barrios = len(data_.place_name[data_.state_name.str.contains('Capital')].unique())
indices_dummys_barrios = data_.shape[1]-numero_barrios

#CREO EL DATAFRAME CON LAS DUMMYS DE BARRIOS
dummys_barrios = data_.iloc[:,indices_dummys_barrios:]


dummys_barrios = dummys_barrios.applymap(lambda x : 1 if (x) else 0)

#GENERO DUMMYS DE BARRIOS EN EL DATAFRAME
data_.iloc[:,indices_dummys_barrios:] = dummys_barrios



