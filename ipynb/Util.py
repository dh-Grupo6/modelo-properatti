import numpy as np
import pandas as pd
import unidecode as uni
pd.set_option('chained_assignment',None)



def nuevosDatos (p_modeloMatriz, superficie_total, jardin, terraza, ambientes, tipo, barrio):

                            
    modeloMatriz = p_modeloMatriz
    
    ##SUPERFICIE TOTAL
    df0 = pd.DataFrame({'superficie_total':pd.Series(superficie_total)})
    df0_2 = pd.DataFrame({'superficie_total':pd.Series(superficie_total**2)})
    
    ##BARRIOS
    barrios = pd.Series(modeloMatriz.iloc[:,15:].columns)
    barrios = (barrios.str.replace('_',' '))
    df1 = barrios.apply(lambda x: 1 if x==var_barrio else 0)
    df2 = pd.DataFrame(columns=barrios)
    df2 = df2.append({ 'flores' : 0 } , ignore_index=True)
    df2 = df2.fillna(0).astype(int)
    df2.iloc[:,barrios[barrios.str.contains(barrio+'$',regex=True)].index] = '1'
    
    
    ##AMBIENTES Y TIPOS


    
    if jardin=='1':
        var_jardin = 'jardin'
    else:
        var_jardin = ''
    if terraza=='1':
        var_terraza = 'terraza'
    else:
        var_terraza = ''
    if (jardin == '1') & (terraza == '1'):
        var_jardinTerraza = 'jardinTerraza'
    else:
        var_jardinTerraza = ''

    
    df4 = pd.DataFrame({'jardin':pd.Series(0), 'terraza':pd.Series(0),'jardinTerraza':pd.Series(0),'1_AMBIENTE':pd.Series(0),'2_AMBIENTE':pd.Series(0),'3_AMBIENTE':pd.Series(0),'4_AMBIENTE':pd.Series(0),'5_AMBIENTE':pd.Series(0),'6_AMBIENTE':pd.Series(0),'7_AMBIENTE':pd.Series(0),'CASA':pd.Series(0),'PH':pd.Series(0),'DTO':pd.Series(0)})
    indices = df4.columns
    indices = pd.Series(indices).astype(str)
    indices_bool = (indices.apply(lambda x: x==ambientes+'_AMBIENTE')) | (indices.apply(lambda x: x==tipo)) | (indices.apply(lambda x: x==var_jardin)) | (indices.apply(lambda x: x==var_terraza)) | (indices.apply(lambda x: x==var_jardinTerraza))   
    serie_df4 = indices_bool.apply(lambda x : 1 if x else 0)
    
    df4_proc = pd.DataFrame({

        'jardin':[serie_df4[0]], 
        'terraza':[serie_df4[1]],
        'jardinTerraza':[serie_df4[2]],
        '1_AMBIENTE':[serie_df4[3]],
        '2_AMBIENTE':[serie_df4[4]],
        '3_AMBIENTE':[serie_df4[5]],
        '4_AMBIENTE':[serie_df4[6]],
        '5_AMBIENTE':[serie_df4[7]],
        '6_AMBIENTE':[serie_df4[8]],
        '7_AMBIENTE':[serie_df4[9]],
        'CASA':[serie_df4[10]],
        'PH':[serie_df4[11]],
        'DTO':[serie_df4[12]]

        })
    
    
    predecir_data = pd.concat([df0,df4_proc],axis=1)
    predecir_data = pd.concat([predecir_data, df2],axis=1)
    predecir_data = pd.concat([predecir_data,df0_2],axis=1)
    
    return predecir_data






def generarDummies(p_matriz):

	matriz = p_matriz

	# TRANSFORMO A FLOAT PARA QUE PUEDA COMPARAR EL PROXIMO PROCESO
	matriz.ambientes = matriz.ambientes.astype(float)

	#GENERO DUMMYS DE AMBIENTES
	matriz['1_AMBIENTE'] = (matriz.ambientes>=1)&(matriz.ambientes<2)
	matriz['2_AMBIENTE'] = (matriz.ambientes>=2)&(matriz.ambientes<3)
	matriz['3_AMBIENTE'] = (matriz.ambientes>=3)&(matriz.ambientes<4)
	matriz['4_AMBIENTE'] = (matriz.ambientes>=4)&(matriz.ambientes<5)
	matriz['5_AMBIENTE'] = (matriz.ambientes>=5)&(matriz.ambientes<6)
	matriz['6_AMBIENTE'] = (matriz.ambientes>=6)&(matriz.ambientes<7)
	matriz['7_AMBIENTE'] = (matriz.ambientes>=7)&(matriz.ambientes<8)

	matriz[['1_AMBIENTE','2_AMBIENTE','3_AMBIENTE','4_AMBIENTE', '5_AMBIENTE','6_AMBIENTE','7_AMBIENTE']] = matriz[['1_AMBIENTE','2_AMBIENTE','3_AMBIENTE','4_AMBIENTE', '5_AMBIENTE','6_AMBIENTE','7_AMBIENTE']].applymap(lambda x : 1 if (x) else 0)


	#GENERO DUMMYS TIPO DE PROPIEDAD 
	matriz['CASA'] = matriz.propiedad.str.contains('house')
	matriz['PH'] =  matriz.propiedad.str.contains('PH')
	matriz['DTO'] = matriz.propiedad.str.contains('apartment')
	matriz[['CASA','PH','DTO']] = matriz[['CASA','PH','DTO']].applymap(lambda x : 1 if x else 0)

	#ELIMINO REGISTROS NULOS DE VARIABLES A UTILIZAR EN EL MODELO
	matriz=matriz[matriz.precio_m2.notnull()]
	matriz=matriz[matriz.superficie_total.notnull()]
	matriz=matriz[matriz.ambientes.notnull()]

	#GENERO DUMMYS DE BARRIOS


	#QUITO NULOS DE LA COLUMNA STATE_NAME
	matriz = matriz[matriz.barrio.notnull()]


	#CREO LISTA DE BARRIOS 
	barrios = matriz[matriz.localidad.str.contains('capital')].barrio.unique()


	#GENERO DUMMYS

	for barrio in barrios:
	    indices_barrios = (matriz.index[matriz.barrio.str.contains(barrio)])
	    barrio = barrio.lower().replace(' ','_')
	    df = matriz
	    df.barrio = df.barrio.apply(lambda x : x.lower().replace(' ','_'))
	    df[barrio] = df.barrio.str.contains(barrio)


	numero_barrios = len(matriz.barrio[matriz.localidad.str.contains('capital')].unique())
	indices_dummys_barrios = matriz.shape[1]-numero_barrios

	#CREO EL DATAFRAME CON LAS DUMMYS DE BARRIOS
	dummys_barrios = matriz.iloc[:,indices_dummys_barrios:]


	dummys_barrios = dummys_barrios.applymap(lambda x : 1 if (x) else 0)

	#GENERO DUMMYS DE BARRIOS EN EL DATAFRAME
	matriz.iloc[:,indices_dummys_barrios:] = dummys_barrios


	matriz = matriz.loc[matriz.localidad.str.contains('capital')]


	#SKLEARN
	nuevos_feactures = matriz[['superficieJardines','superficieTerrazas','superficieJardinesTerrazas']].applymap(lambda x: 1 if x>0 else 0)	#GENERO VARIABLES INDEPENDIENTES
	x_feactures=matriz.iloc[:,16:]
	df1 = pd.concat([matriz['superficie_total'],nuevos_feactures],axis=1)
	xs = pd.concat([df1,x_feactures],axis=1)
	#GENERO VARIABLE DEPENDIENTE
	y = matriz.precio_m2

	matriz = pd.concat([y,xs],axis=1)

	return matriz


def matriz(p_data):

    data = p_data

    #GENERAR MATRIZ
    matriz = pd.DataFrame({ 'id':data['Unnamed: 0'],
                            'tipo':data['operation'],
                            'propiedad':data.property_type,
                            'id_localizacion':data.geonames_id,
                            'pais':data.country_name.astype(str).apply(uni.unidecode).str.lower(),
                            'localidad':data.state_name.astype(str).apply(uni.unidecode).str.lower(),
                            'barrio':data.place_name.astype(str).apply(uni.unidecode).str.lower(),
                            'moneda':data.currency.str.lower(),
                            'ambientes':data.imputar_ambientes,
                            'superficie_total':data.surface_total_in_m2,
                            'superficie_cubierta_m2':data.surface_covered_in_m2,
                            'precio_aprox_usd':data.price_aprox_usd,
                            'precio_m2':data.price_usd_per_m2,
                            'superficieJardines':data.superficieJardines,
                            'superficieTerrazas':data.superficieTerraza,
                            'superficieJardinesTerrazas':data.superficieJarTer
                           })

    return matriz

def imputarAmbientes(p_data):

	data = p_data

	##IMPUTANDO AMBIENTES
	data.ambientesImputados = ImputarAmbientesProceso(data,10)
	data.ambientesImputados.update(data.ambientes)

	return data.ambientesImputados


def ImputarSupCubierta(p_data):


    data = p_data

    #IMPUTAR FALTANTES CANTIDAD_AMBIENTES CON SUPERFICIES CUBIERTAS
    data['superficie_cubierta_imputada'] = np.nan
    imputar_serie = ImputarSupCubiertaProceso(data,5)
    data.superficie_cubierta_imputada.update(imputar_serie)
    data.superficie_cubierta_imputada.update(data.surface_total_in_m2)
    data.superficie_cubierta_imputada.update(data.surface_covered_in_m2)
    

    return data.superficie_cubierta_imputada



def ImputarSupTotal(p_data):

    data = p_data


    data['superficie_total_imputada_Cubierta'] = ImputarSupTotalCubierta(data,10)
    data['superficie_total_imputada_Ambientes'] = ImputarSupTotalAmbientes(data,5)

    data.superficie_total_imputada_Ambientes.update(data.superficie_total_imputada_Cubierta)
    data.superficie_total_imputada_Ambientes.update(data.surface_total_in_m2)

    return data.superficie_total_imputada_Ambientes



def ImputarTotalMenorCubierta(p_data):

	data = p_data
	
	#CUANDO LA SUPERFICIE TOTAL < SUPERFICIE CUBIERTA REEMPLAZO CON SUPERFICIE CUBIERTA + JARDIN/TERRAZA
	superficie_jardin_imputada_ceros = data.superficieJardines.fillna(0)
	superficie_terraza_imputada_ceros = data.superficieTerraza.fillna(0)
	sup_terraza_jardin_imputada_ceros = data.superficieJarTer.fillna(0)
	data.surface_total_in_m2.loc[data.surface_total_in_m2-data.surface_covered_in_m2<0] = data.surface_covered_in_m2 + superficie_jardin_imputada_ceros + superficie_terraza_imputada_ceros + sup_terraza_jardin_imputada_ceros
	data['surface_total_in_m2'] = data.surface_total_in_m2

	return data.surface_total_in_m2


def generarSupJardines(p_data):
	
	data = p_data

	##OBTENGOS JARDINES, TERRAZAS 
	booleanos_jardines =(data.description.str.contains('parquizado'))|(data.description.str.contains('patio'))|(data.description.str.contains('jardin')) 
	booleanos_terraza = (data.description.str.contains('terraza'))|(data.description.str.contains('quincho')) 

	##CALCULO SUPERFICIES DE JARDINES (SIN TERRAZA) 
	serie_jardines = (booleanos_jardines) & (~booleanos_terraza) & (data.surface_covered_in_m2.notnull()) & (data.surface_total_in_m2.notnull())
	data['superficie_jardin_patio'] = data.surface_total_in_m2[serie_jardines]-data.surface_covered_in_m2[serie_jardines]
	serie_superficie_jardines = pd.DataFrame(data.superficie_jardin_patio[(data.superficie_jardin_patio.notnull()) & (data.superficie_jardin_patio > 0)])
	data['superficies_jardines'] = data.merge(serie_superficie_jardines,how='left',left_on=['Unnamed: 0'],right_index=True)['superficie_jardin_patio_y']

	return data.superficies_jardines 


def generarSupTerrazas(p_data):
	
	data = p_data

	##OBTENGOS JARDINES, TERRAZAS 
	booleanos_jardines =(data.description.str.contains('parquizado'))|(data.description.str.contains('patio'))|(data.description.str.contains('jardin')) 
	booleanos_terraza = (data.description.str.contains('terraza'))|(data.description.str.contains('quincho')) 

	##CALCULO SUPERFICIES DE TERRAZAS (SIN JARDINES)
	serie_terraza = (booleanos_terraza) & (~booleanos_jardines) & (data.surface_covered_in_m2.notnull()) & (data.surface_total_in_m2.notnull())
	superficie_terraza_indices = pd.DataFrame(data.surface_total_in_m2[serie_terraza]-data.surface_covered_in_m2[serie_terraza],columns=['terraza_y'])    
	columna_superficie_terraza = data.merge(superficie_terraza_indices[superficie_terraza_indices.terraza_y>0],how='left', left_on=['Unnamed: 0'],right_index=True)['terraza_y']
	data['superficie_terraza'] = columna_superficie_terraza

	return data.superficie_terraza


def generarSupJarTer(p_data):

	data = p_data

	##OBTENGOS JARDINES, TERRAZAS 
	booleanos_jardines =(data.description.str.contains('parquizado'))|(data.description.str.contains('patio'))|(data.description.str.contains('jardin')) 
	booleanos_terraza = (data.description.str.contains('terraza'))|(data.description.str.contains('quincho')) 


	##CALCULO SUPERFICIES DE TERRAZAS CON JARDINES
	serie_terraza_jardin = (booleanos_terraza) & (booleanos_jardines) & (data.surface_covered_in_m2.notnull()) & (data.surface_total_in_m2.notnull())
	superficie_terraza_jardin_indices = pd.DataFrame(data.surface_total_in_m2[serie_terraza_jardin]-data.surface_covered_in_m2[serie_terraza_jardin],columns=['terraza_jardin_y'])
	columna_superficie_terraza_jardin = data.merge(superficie_terraza_jardin_indices[superficie_terraza_jardin_indices.terraza_jardin_y>0],how='left', left_on=['Unnamed: 0'], right_index=True)['terraza_jardin_y']
	data['superficie_terraza_jardin'] = columna_superficie_terraza_jardin

	return data.superficie_terraza_jardin


def quitarMayusculasAcentos(p_data):
	
	data = p_data

	##REEMPLAZO COLUMNAS DESCRIPCION Y TITULO (MINUSCULAS Y ACENTOS)
	data.description = data.description.astype(str).apply(uni.unidecode).str.lower()
	data.title = data.title.astype(str).apply(uni.unidecode).str.lower()
	
	return data



def generoAmbientes(p_data):

	data = p_data

	##CONTIENE AMBIENTES EN CAMPO DESCRIPCION 
	un_ambiente = data[data.rooms<=7].description.str.contains("ambiente ") | data.description.str.contains("amb.","amb ") & data.description.str.contains("1 amb")
	dos_o_mas_ambientes = data.description.str.contains("ambientes") | data.description.str.contains("2 amb")
	data["un_ambiente"]=un_ambiente

	##CONTIENE AMBIENTES DE CAMPOS TITULO Y DESCRIPCION
	cant_ambientes_old_desc = data[data.rooms<=7].description.astype(str).apply(obtengo_ambiente)
	cant_ambientes_old_title = data[data.rooms<=7].title.astype(str).apply(obtengo_ambiente)
	cant_ambientes_desc = cant_ambientes_old_desc.str.extract(r'(\d+)')
	cant_ambientes_title = cant_ambientes_old_title.str.extract(r'(\d+)')

	data['cantidad_ambientes_desc'] = cant_ambientes_desc
	data['cantidad_ambientes_title'] = cant_ambientes_title

	##CONTIENE AMBIENTES DE DESCIPCIONES CON 1 AMBIENTE
	data['un_ambiente'] = data.un_ambiente
	data['monoambiente'] = data[data.rooms<=7].description.str.contains('monoambiente') | data.description.str.contains('mono ambiente') | data.title.str.contains('monoambiente') | data.title.str.contains('mono ambiente')  
	data['ambientes'] = data.rooms[data.rooms.fillna(100).astype(int)<6].astype(int)

	##LO AGREGO LOS DE 1 AMBIENTES A LOS QUE YA TENGO
	var_un_ambiente = data.un_ambiente.apply(devolver_un_ambiente)
	var_monoambiente = data.monoambiente.apply(devolver_un_ambiente)
	#data.cantidad_ambientes_title.update(data.cantidad_ambientes_desc)
	data.ambientes.update(data.cantidad_ambientes_title)
	data.ambientes.update(data.cantidad_ambientes_desc)

	##SUMARIZO TODOS LOS AMBIENTES
	data['var_un_ambiente'] = var_un_ambiente
	data['var_monoambiente'] = var_monoambiente
	data.var_un_ambiente.update(data.ambientes)
	data.var_monoambiente.update(data.var_un_ambiente)

	##GUARDO LA COLUMNA DE AMBIENTES EN DATA.NUEVOS_AMBIENTES
	data['nuevos_ambientes'] = data.var_monoambiente 
	data['ambientes_ceros'] = data.nuevos_ambientes.fillna(0).astype(int) 

	return data.nuevos_ambientes



def TransformacionData(p_data):

	data = p_data

	#QUITO LAS FILAS REPETIDAS DEL CAMPO DESCRIPCION
	data = data.drop_duplicates(subset=['description'], keep='first')
	#QUITO LAS FILAS CON SUPERFICIE CUBIERTA MENOR A 16
	data = data[(data.surface_covered_in_m2>16)|(data.surface_covered_in_m2.isnull())]
	#QUITO LAS FILAS CON SUPERFICIE TOTAL MENOR A 16
	data = data[(data.surface_total_in_m2>16)|(data.surface_total_in_m2.isnull())]
	#QUITO LAS FILAS CON SUPERFICIES CUBIERTAS MENOR 50 DE CASAS 
	data = data[(~((data.surface_covered_in_m2<50)&(data.property_type.str.contains('house'))))]
	#QUITO LAS FILAS CON SUPERFICIE TOTAL MENOR 50 DE CASAS 
	data = data[(~((data.surface_total_in_m2<50)&(data.property_type.str.contains('house'))))]
	#PONGO NULOS LOS VALORES DE SUPERFICIE CUBIERTA CUANDO SUPERFICIE_CUBIERTA>SUPERFICIE_TOTAL
	data.surface_covered_in_m2[data.surface_covered_in_m2>data.surface_total_in_m2] = np.nan 
	#data.surface_total_in_m2.update(data.surface_covered_in_m2)

	return data


def devolver_un_ambiente (x):
    if x :
        return 1


def obtengo_ambiente(x): 
    v_1 = x.lower()             # texto en minuscula
    v_2 = v_1.find('amb')     # posicion "amb"
    if v_2<0:
        return -1
    else:
        v_3 = v_2-2                     # posicion -2 OBTENGO NUMERO DE AMBIENTES
        v_4 = v_2-1                     # posicion -1 OBTENGO NUMERO DE AMBIENTES
        v_5 = v_1[v_3:v_4]
        return v_5


def OutliersSupTotal(p_data, Desviacion):


    data_modificada = p_data

    # GENERO CULUMNA DE MEDIAS AGRUPANDO POR PCIA, BARRIO, TIPO DE PROPIEDAD
    media__ = data_modificada.groupby(['state_name', 'place_name', 'property_type'])['surface_total_in_m2'].transform('mean')

    #GENERO COLUMNA DE STD AGRUPANDO POR PCIA, BARRIO, TIPO DE PROPIEDAD
    str__ = data_modificada.groupby(['state_name','place_name','property_type'])['surface_total_in_m2'].transform('std')

    #GENERO COLUMNA CON LA FORMULA DE CHEUVENET PARA EL CALCULO DE OUTLIERS
    criterio_cheuvenet__ = (abs(data_modificada.surface_total_in_m2-media__))/(str__)
    data_modificada.surface_total_in_m2.loc[criterio_cheuvenet__>Desviacion] = np.nan
    
    
    return data_modificada 



def OutliersSupCubierta(p_data, Desviacion):


    data_modificada = p_data

    # GENERO CULUMNA DE MEDIAS AGRUPANDO POR PCIA, BARRIO, TIPO DE PROPIEDAD
    media__ = data_modificada.groupby(['state_name', 'place_name', 'property_type'])['surface_covered_in_m2'].transform('mean')

    #GENERO COLUMNA DE STD AGRUPANDO POR PCIA, BARRIO, TIPO DE PROPIEDAD
    str__ = data_modificada.groupby(['state_name','place_name','property_type'])['surface_covered_in_m2'].transform('std')

    #GENERO COLUMNA CON LA FORMULA DE CHEUVENET PARA EL CALCULO DE OUTLIERS
    criterio_cheuvenet__ = (abs(data_modificada.surface_covered_in_m2-media__))/(str__)
    data_modificada.surface_covered_in_m2.loc[criterio_cheuvenet__>Desviacion] = np.nan
    
    
    return data_modificada 


def OutliersPrecioUSD(p_data, Desviacion):


    data_modificada = p_data

    # GENERO CULUMNA DE MEDIAS AGRUPANDO POR PCIA, BARRIO, TIPO DE PROPIEDAD
    media__ = data_modificada.groupby(['state_name', 'place_name', 'property_type'])['price_aprox_usd'].transform('mean')

    #GENERO COLUMNA DE STD AGRUPANDO POR PCIA, BARRIO, TIPO DE PROPIEDAD
    str__ = data_modificada.groupby(['state_name','place_name','property_type'])['price_aprox_usd'].transform('std')

    #GENERO COLUMNA CON LA FORMULA DE CHEUVENET PARA EL CALCULO DE OUTLIERS
    criterio_cheuvenet__ = (abs(data_modificada.price_aprox_usd-media__))/(str__)
    data_modificada.price_aprox_usd.loc[criterio_cheuvenet__>Desviacion] = np.nan
    
    
    return data_modificada



def OutliersPrecioM2(p_data, Desviacion):


    data_modificada = p_data

    # GENERO CULUMNA DE MEDIAS AGRUPANDO POR PCIA, BARRIO, TIPO DE PROPIEDAD
    media__ = data_modificada.groupby(['state_name', 'place_name', 'property_type'])['price_usd_per_m2'].transform('mean')

    #GENERO COLUMNA DE STD AGRUPANDO POR PCIA, BARRIO, TIPO DE PROPIEDAD
    str__ = data_modificada.groupby(['state_name','place_name','property_type'])['price_usd_per_m2'].transform('std')

    #GENERO COLUMNA CON LA FORMULA DE CHEUVENET PARA EL CALCULO DE OUTLIERS
    criterio_cheuvenet__ = (abs(data_modificada.price_usd_per_m2-media__))/(str__)
    data_modificada.price_usd_per_m2.loc[criterio_cheuvenet__>Desviacion] = np.nan
    
    
    return data_modificada





def ImputarAmbientesProceso(p_data, rango):

	data = p_data

	data['imputar_ambientes'] = np.nan
	
	for i in range(1,rango): 
	
		#GENERAR GRUPOS DE SUPERFICIES
		data['categorias_sup_cubierta_por_m2'] = pd.qcut(data[data.surface_covered_in_m2>10].surface_covered_in_m2,i)
		#CALCULAR MEDIAS CANTIDAD_AMBIENTES 
		dfImputacionesAmbientes = pd.DataFrame(data[data.ambientes_ceros!=0].groupby(['state_name','place_name','categorias_sup_cubierta_por_m2'])['ambientes_ceros'].mean())
		serie_imputaciones_ambientes = data.merge(dfImputacionesAmbientes,how='left',left_on=['state_name','place_name','categorias_sup_cubierta_por_m2'],right_on=['state_name','place_name','categorias_sup_cubierta_por_m2'])['ambientes_ceros_y']   
		data.imputar_ambientes.update(serie_imputaciones_ambientes)
		
		break


	data.rooms[data.rooms>7] = np.nan 
	data.imputar_ambientes.update(data.rooms)	
		
	return data.imputar_ambientes


	
def ImputarSupCubiertaProceso(p_data, rango):

    data = p_data
    data['imputando_superficies_cubiertas'] = np.nan
    data.imputar_ambientes = data.imputar_ambientes.fillna(0).astype(int)
    for i in range(1,rango): 

        #GENERAR GRUPOS DE AMBIENTES EN PESOS
        data['ambientes_imputados_ceros'] = data.ambientesImputados.fillna(0).astype(float)
        data['categorias_ambientes'] = pd.qcut(data.imputar_ambientes,i)
        #CALCULAR MEDIAS SUPERFICIES CUBIERTAS
        df_superficies_imput = pd.DataFrame(data[data.ambientes_imputados_ceros>=1].groupby(['state_name','place_name','property_type','categorias_ambientes'])['surface_covered_in_m2'].mean())
        imputar_serie = data.merge(df_superficies_imput,how='left',left_on=['state_name','place_name','property_type','categorias_ambientes'],right_on=['state_name','place_name','property_type','categorias_ambientes'])['surface_covered_in_m2_y']
        data.imputando_superficies_cubiertas.update(imputar_serie)

        break

    
    for i in range (1,rango):

        #GENERAR GRUPOS DE SUPERFICIES TOTAL
        data['categorias_sup_total'] = pd.qcut(data.surface_total_in_m2,rango)
        imputar_serie_Cubierta_con_total = data.groupby(['state_name','place_name','property_type','categorias_sup_total'])['surface_covered_in_m2'].transform('mean')
        data.imputando_superficies_cubiertas.update(imputar_serie_Cubierta_con_total)

        break

    return data.imputando_superficies_cubiertas


def ImputarSupTotalCubierta(p_data, rango):


    data = p_data
    data['imputando_superficies_total'] = np.nan
    

    for i in range(1,rango): 
    
        #GENERAR GRUPOS DE SUPERFICIES
        data['categorias_sup_cubierta_por_m2'] = pd.qcut(data.surface_covered_in_m2,i)
        #CALCULAR MEDIAS CANTIDAD_AMBIENTES 
        dfImputarTotal = pd.DataFrame(data.groupby(['state_name','place_name','categorias_sup_cubierta_por_m2'])['surface_total_in_m2'].mean())
        serie_imputaciones_ambientes = data.merge(dfImputarTotal,how='left',left_on=['state_name','place_name','categorias_sup_cubierta_por_m2'],right_on=['state_name','place_name','categorias_sup_cubierta_por_m2'])['surface_total_in_m2_y']   
        data.imputando_superficies_total.update(serie_imputaciones_ambientes)

        break

    return data.imputando_superficies_total 


def ImputarSupTotalAmbientes(p_data, rango):

    data = p_data

    data['imputando_superficies_total'] = np.nan

    data.imputar_ambientes = data.imputar_ambientes.fillna(0).astype(int)


    for i in range(1, rango):

        data['categorias_ambientes'] = pd.qcut(data.imputar_ambientes,i)
        #CALCULAR MEDIAS AGRUPANDO POR AMBIENTES
        dfImputarTotal = pd.DataFrame(data.groupby(['state_name','place_name','categorias_ambientes'])['surface_total_in_m2'].mean())
        serie_imputaciones_ambientes = data.merge(dfImputarTotal,how='left',left_on=['state_name','place_name','categorias_ambientes'],right_on=['state_name','place_name','categorias_ambientes'])['surface_total_in_m2_y']   
        data.imputando_superficies_total.update(serie_imputaciones_ambientes)

        break

    return data.imputando_superficies_total 





def imputarPrecio(p_data):

    data = p_data

    data['imputandoPrecioSupTotalJarTer'] = ImputarPrecioJarTer(data)
    data['imputandoPrecioSupTotal'] = ImputarPrecioSupTotal(data)

    data.imputandoPrecioSupTotalJarTer.update(data.imputandoPrecioSupTotal)
    data.imputandoPrecioSupTotalJarTer.update(data.price_aprox_usd)

    return data.imputandoPrecioSupTotalJarTer





def ImputarPrecioSupTotal(p_data, rango=5):
	
	data = p_data

	data['imputar_precios_usd'] = np.nan
	
	for i in range(1,rango):
		
		data['categorias_superficie_total_m2'] = pd.qcut(data.surface_total_in_m2,i)
		df_precio_sup_total = pd.DataFrame(data.groupby(['state_name','place_name','property_type','categorias_superficie_total_m2'])['price_aprox_usd'].mean())
		serie_imputada_precio_sup_total = data.merge(df_precio_sup_total,how='left',left_on=['state_name','place_name','property_type','categorias_superficie_total_m2'], right_on=['state_name','place_name','property_type','categorias_superficie_total_m2'])['price_aprox_usd_y']            
		data.imputar_precios_usd.update(serie_imputada_precio_sup_total)            
	
		break


	return data.imputar_precios_usd



def ImputarPrecioJarTer(p_data, rango=5):

    data = p_data
    data['imputar_precios_usd'] = np.nan
    data['categoria_superficie_cubierta_imputada'] = pd.qcut(data.surface_covered_in_m2,5)
    
    for i in range(1,rango): 

        data['categorias_superficie_terraza'] = pd.qcut(data.superficieTerraza,i)
        ##IMPUTAR PRECIOS DE SUPERFICIES CON TERRAZA
        df_terraza = pd.DataFrame(data[data.categorias_superficie_terraza.notnull()].groupby(['state_name','place_name','property_type','categoria_superficie_cubierta_imputada','categorias_superficie_terraza'])['price_aprox_usd'].mean()) 
        data['imputar_precios_terraza'] = data.merge(df_terraza, how='left', left_on=['state_name','place_name','property_type','categoria_superficie_cubierta_imputada','categorias_superficie_terraza'],right_on=['state_name','place_name','property_type','categoria_superficie_cubierta_imputada','categorias_superficie_terraza'])['price_aprox_usd_y']
        data.imputar_precios_usd.update(data.imputar_precios_terraza)

        data['categorias_superficie_jardines']  = pd.qcut(data.superficieJardines,i)
        ##IMPUTAR PRECIOS DE SUPERFICIES CON JARDINES
        df_jardin = pd.DataFrame(data[data.categorias_superficie_jardines.notnull()].groupby(['state_name','place_name','property_type','categoria_superficie_cubierta_imputada','categorias_superficie_jardines'])['price_aprox_usd'].mean())
        data['imputar_precios_jardines'] = data.merge(df_jardin,how='left',left_on=['state_name','place_name','property_type','categoria_superficie_cubierta_imputada','categorias_superficie_jardines'], right_on=['state_name','place_name','property_type','categoria_superficie_cubierta_imputada','categorias_superficie_jardines'])['price_aprox_usd_y']
        data.imputar_precios_usd.update(data.imputar_precios_jardines)

        data['categorias_superficie_terraza_jardin'] = pd.qcut(data.superficieJarTer,i)
        ##IMPUTAR PRECIOS DE SUPERFICIES CON TERRAZAS Y JARDINES 
        df_terraza_jardin = pd.DataFrame(data[data.categorias_superficie_terraza_jardin.notnull()].groupby(['state_name','place_name','property_type','categoria_superficie_cubierta_imputada','categorias_superficie_terraza_jardin'])['price_aprox_usd'].mean())
        data['imputar_precios_terraza_jardin'] = data.merge(df_terraza_jardin, how='left', left_on=['state_name','place_name','property_type','categoria_superficie_cubierta_imputada','categorias_superficie_terraza_jardin'], right_on=['state_name','place_name','property_type','categoria_superficie_cubierta_imputada','categorias_superficie_terraza_jardin'])['price_aprox_usd_y']
        data.imputar_precios_usd.update(data.imputar_precios_terraza_jardin)


        break 


    return data.imputar_precios_usd




def imputarPrecioM2(p_data):

	data = p_data

	serie_precio_m2 = data.price_aprox_usd/data.surface_total_in_m2
	serie_precio_m2.update(data.price_usd_per_m2)

	return serie_precio_m2

