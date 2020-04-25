import unidecode as uni
import pandas as pd 
import numpy as np
pd.set_option('chained_assignment',None)





def ejecutar_programa(salida):
    ##DEFINO FUNCIONES LOCALES DEL PROGRAMA
    def f_ambiente (x, palabra) :
        if x.contains("ambiente") :
            return 1
        else :
            return 0


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
        
    def obtengo_dormitorio(x): 
        v_1 = x.lower()             # texto en minuscula
        v_2 = v_1.find('dorm')     # posicion "dormitorio"
        if v_2<0:
            return -1
        else:
            v_3 = v_2-2                     # posicion -2 OBTENGO NUMERO DE AMBIENTES
            v_4 = v_2-1                     # posicion -1 OBTENGO NUMERO DE AMBIENTES
            v_5 = v_1[v_3:v_4]
            return v_5
    
    def obtengo_depto(x): 
        v_1 = x.lower()             # texto en minuscula
        v_2 = v_1.find('dep')     # posicion "amb"
        if v_2<0:
            return -1
        else:
            v_3 = v_2-2                     # posicion -2 OBTENGO NUMERO DE AMBIENTES
            v_4 = v_2-1                     # posicion -1 OBTENGO NUMERO DE AMBIENTES
            v_5 = v_1[v_3:v_4]
            return v_5
    
    def devolver_un_ambiente (x):
        if x :
            return 1
    
    


    
    

  

    
    #LEER ARCHIVO
    data = pd.read_csv('/home/DS-DH/DigitalHouse/desafio/properatti.csv')
    #data = data[data['Unnamed: 0']!=11]
    
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
    
    ##INFERIMOS EL ERROR 
    #inferir_error_superficies_mayores_cu()
    #inferir_error_superficies_menores_cu()
    #inferir_error_superficies_mayores_total()
    #inferir_error_superficies_menores_total()
    #inferir_error_precios_mayores_usd()    
    #inferir_error_precios_menores_usd()    
    
    ##DESISTIMO EL ERROR QUITANDO LAS FILAS CALCULADAS EN EL PASO ANTERI
    #data = data[(data.surface_covered_in_m2>0)|(data.surface_covered_in_m2.isnull())]
    #data = data[(data.surface_total_in_m2>0)|(data.surface_total_in_m2.isnull())]
    #data = data[(data.price_aprox_usd>0)|(data.price_aprox_usd.isnull())]
    
    
    
    #REEMPLAZAR STRING |    
    replace_place = data.place_with_parent_names.str.replace("|",",").str[1:-1].str.split(',')
  
    
    ##AGREGO COLUMNA DE PAIS
    data["pais_2"] = replace_place[:].str[0].str.lower()
    ##AGREGO COLUMNA DE LOCALIDAD
    data["localidad_2"] = replace_place[:].str[1].str.lower()
    ##AGREGO COLUMNA DE BARRIO
    data["barrio_2"] = replace_place[:].str[2].str.lower()
    ##AGREGO COLUMNA BARRIO EXTRA
    data["barrio_2b"] = replace_place[:].str[3].str.lower()
    

    
    ##REEMPLAZO COLUMNAS DESCRIPCION Y TITULO (MINUSCULAS Y ACENTOS)
    data.description = data.description.astype(str).apply(uni.unidecode).str.lower()
    data.title = data.title.astype(str).apply(uni.unidecode).str.lower()
    
    
    ##OBTENGOS JARDINES, TERRAZAS 
    booleanos_jardines =(data.description.str.contains('parquizado'))|(data.description.str.contains('patio'))|(data.description.str.contains('jardin')) 
    booleanos_terraza = (data.description.str.contains('terraza'))|(data.description.str.contains('quincho')) 
    
    
    ##CALCULO SUPERFICIES DE JARDINES (SIN TERRAZA) 
    
    serie_jardines = (booleanos_jardines) & (~booleanos_terraza) & (data.surface_covered_in_m2.notnull()) & (data.surface_total_in_m2.notnull())
    data['superficie_jardin_patio'] = data.surface_total_in_m2[serie_jardines]-data.surface_covered_in_m2[serie_jardines]
    serie_superficie_jardines = pd.DataFrame(data.superficie_jardin_patio[(data.superficie_jardin_patio.notnull()) & (data.superficie_jardin_patio > 0)])
    data['superficies_jardines'] = data.merge(serie_superficie_jardines,how='left',left_on=['Unnamed: 0'],right_index=True)['superficie_jardin_patio_y']

        
    ##CALCULO SUPERFICIES DE TERRAZAS (SIN JARDINES)
    serie_terraza = (booleanos_terraza) & (~booleanos_jardines) & (data.surface_covered_in_m2.notnull()) & (data.surface_total_in_m2.notnull())
    superficie_terraza_indices = pd.DataFrame(data.surface_total_in_m2[serie_terraza]-data.surface_covered_in_m2[serie_terraza],columns=['terraza_y'])    
    columna_superficie_terraza = data.merge(superficie_terraza_indices[superficie_terraza_indices.terraza_y>0],how='left', left_on=['Unnamed: 0'],right_index=True)['terraza_y']
    data['superficie_terraza'] = columna_superficie_terraza
    
    
    ##CALCULO SUPERFICIES DE TERRAZAS CON JARDINES
    serie_terraza_jardin = (booleanos_terraza) & (booleanos_jardines) & (data.surface_covered_in_m2.notnull()) & (data.surface_total_in_m2.notnull())
    superficie_terraza_jardin_indices = pd.DataFrame(data.surface_total_in_m2[serie_terraza_jardin]-data.surface_covered_in_m2[serie_terraza_jardin],columns=['terraza_jardin_y'])
    columna_superficie_terraza_jardin = data.merge(superficie_terraza_jardin_indices[superficie_terraza_jardin_indices.terraza_jardin_y>0],how='left', left_on=['Unnamed: 0'], right_index=True)['terraza_jardin_y']
    data['superficie_terraza_jardin'] = columna_superficie_terraza_jardin
    
        
    ##CONTIENE AMBIENTES EN CAMPO DESCRIPCION 
    un_ambiente = data[data.rooms<=7].description.str.contains("ambiente ") | data.description.str.contains("amb.","amb ") & data.description.str.contains("1 amb")
    dos_o_mas_ambientes = data.description.str.contains("ambientes") | data.description.str.contains("2 amb")
    data["un_ambiente"]=un_ambiente
        

    
    cant_ambientes_old_desc = data[data.rooms<=7].description.astype(str).apply(obtengo_ambiente)
    cant_ambientes_old_title = data[data.rooms<=7].title.astype(str).apply(obtengo_ambiente)
    cant_ambientes_desc = cant_ambientes_old_desc.str.extract(r'(\d+)')
    cant_ambientes_title = cant_ambientes_old_title.str.extract(r'(\d+)')
    
    data['cantidad_ambientes_desc'] = cant_ambientes_desc
    data['cantidad_ambientes_title'] = cant_ambientes_title
    
    data['un_ambiente'] = data.un_ambiente
    data['monoambiente'] = data[data.rooms<=7].description.str.contains('monoambiente') | data.description.str.contains('mono ambiente') | data.title.str.contains('monoambiente') | data.title.str.contains('mono ambiente')  

    
    data['ambientes'] = data.rooms[data.rooms.fillna(100).astype(int)<6].astype(int)
    
    var_un_ambiente = data.un_ambiente.apply(devolver_un_ambiente)
    var_monoambiente = data.monoambiente.apply(devolver_un_ambiente)
    #data.cantidad_ambientes_title.update(data.cantidad_ambientes_desc)
    data.ambientes.update(data.cantidad_ambientes_title)
    data.ambientes.update(data.cantidad_ambientes_desc)
    
    
    
    data['var_un_ambiente'] = var_un_ambiente
    data['var_monoambiente'] = var_monoambiente
    data.var_un_ambiente.update(data.ambientes)
    data.var_monoambiente.update(data.var_un_ambiente)
    
    
    data['nuevos_ambientes'] = data.var_monoambiente 
    
    data['ambientes_ceros'] = data.nuevos_ambientes.fillna(0).astype(int) 
    #data['grupos_ambientes'] = pd.cut(data.ambientes_ceros,[0,4!=0])
    
    
    ##GUARDO COLUMNA TITLE
    data['surface_total'] = data.surface_total_in_m2
    
    data.surface_total_in_m2.update(data.surface_covered_in_m2)
    data['nueva_surface_total_in_m2'] = data.surface_total_in_m2 
        

    ##IMPUTAR AMBIENTES
    data['ambientes_imputados'] = ImputarAmbientes(20)
    data.ambientes_imputados.update(data.nuevos_ambientes)
    
        
    #IMPUTAR FALTANTES CANTIDAD_AMBIENTES CON SUPERFICIES CUBIERTAS
    data['superficie_cubierta_imputada'] = np.nan
    imputar_serie = ImputarSupCubierta(5)
    data.superficie_cubierta_imputada.update(imputar_serie)

    data.superficie_cubierta_imputada.update(data.nueva_surface_total_in_m2)
    data.superficie_cubierta_imputada[(data.superficie_cubierta_imputada<50)&(data.property_type.str.contains('house'))] = np.nan
    
    ##IMPUTAR SUPERFICIE JARDIN
    data['superficie_jardin_imputada'] = ImputarSupJardin(10)
    data.superficie_jardin_imputada.update(data.superficies_jardines)
    
    ##IMPUTAR SUPERFICIE TERRAZA
    data['superficie_terraza_imputada'] = ImputarSupTer(10)
    data.superficie_terraza_imputada.update(data.superficie_terraza)
    
    ##IMPUTAR SUPERFICIE JARDIN/TERRAZA
    data['sup_terraza_jardin_imputada'] = ImputarSupJarTer(10)
    data.sup_terraza_jardin_imputada.update(data.superficie_terraza_jardin)
    
    
    ##IMPUTAR SUPERFICIE TOTAL DE JARDINES TERRAZAS 
    data['superficie_total_imputada'] = ImputarSupTotalJarTer(20)
    data.superficie_total_imputada.update(data.surface_total)
    
    
    
    ##CUANDO LA SUPERFICIE TOTAL < SUPERFICIE CUBIERTA REEMPLAZO CON SUPERFICIE CUBIERTA + JARDIN/TERRAZA
    data['superficie_jardin_imputada_ceros'] = data.superficie_jardin_imputada.fillna(0)
    data['superficie_terraza_imputada_ceros'] = data.superficie_terraza_imputada.fillna(0)
    data['sup_terraza_jardin_imputada_ceros'] = data.sup_terraza_jardin_imputada.fillna(0)
    data.superficie_total_imputada[data.superficie_total_imputada<data.superficie_cubierta_imputada] = data.superficie_cubierta_imputada + data.superficie_jardin_imputada_ceros + data.superficie_terraza_imputada_ceros + data.sup_terraza_jardin_imputada_ceros
    
    
    
    ##IMPUTAR PRECIOS USD
    data['precios_usd_imputados'] = np.nan
    data['categoria_superficie_cubierta_imputada'] = pd.qcut(data[data.superficie_cubierta_imputada>=10].superficie_cubierta_imputada,5)
    
    
    
    #ACTUALIZO POR SUPERFICIE TOTAL
    serie_imputada_sup_total_precios = ImputarPrecioSupTotal(20)
    data.precios_usd_imputados.update(serie_imputada_sup_total_precios)
    
    #ACTUALIZO POR SUPERFICIE CUBIERTA (JARDINES; TERRAZAS; JARDINES Y TERRAZAS)
    serie_imputada_precios = ImputarPrecioJarTer(20)
    data.precios_usd_imputados.update(serie_imputada_precios)
    
    #ACTUALIZO POR COLUMNA PRICE_APROX_USD
    data.precios_usd_imputados.update(data.price_aprox_usd)
    
    
    if salida == 1:
        return data
    
    
    
    #GENERAR MATRIZ
    matriz = pd.DataFrame({ 'id':data['Unnamed: 0'],
                            'tipo':data['operation'],
                            'propiedad':data.property_type,
                            'id_localizacion':data.geonames_id,
                            'pais':data.country_name.astype(str).apply(uni.unidecode).str.lower(),
                            'localidad':data.state_name.astype(str).apply(uni.unidecode).str.lower(),
                            'barrio':data.place_name.astype(str).apply(uni.unidecode).str.lower(),
                            'barrio_2b':data.barrio_2b.astype(str).apply(uni.unidecode).str.lower(),
                            'latitud':data.lat,
                            'longitud':data.lon,
                            'moneda':data.currency.str.lower(),
                            'ambientes':data.ambientes_imputados,
                            'ambientes_ceros':data.ambientes_imputados.fillna(0),
                            'nuevos_ambientes' : data.nuevos_ambientes,
                            'superficie_total':data.superficie_total_imputada,
                            'superficie_cubierta_m2':data.superficie_cubierta_imputada,
                            'precio_aprox_usd':data.precios_usd_imputados       
                   } )
    
    if salida == 0: 
        return matriz
  