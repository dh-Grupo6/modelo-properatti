def outliers(p_data, Feacture1, Feacture2, Feacture3, Objetivo, Desviacion):


    data_modificada = p_data

    # GENERO CULUMNA DE MEDIAS AGRUPANDO POR PCIA, BARRIO, TIPO DE PROPIEDAD
    media__ = data_modificada.groupby([Feacture1,Feacture2,Feacture3])[Objetivo].transform('mean')

    #GENERO COLUMNA DE STD AGRUPANDO POR PCIA, BARRIO, TIPO DE PROPIEDAD
    str__ = data_modificada.groupby([Feacture1,Feacture2,Feacture3])[Objetivo].transform('std')

    #GENERO COLUMNA CON LA FORMULA DE CHEUVENET PARA EL CALCULO DE OUTLIERS
    criterio_cheuvenet__ = (abs(data_modificada.Objetivo-media__))/(str__)
    data_modificada.Objetivo.loc[criterio_cheuvenet__>Desviacion] = np.nan
    
    
    return data_modificada 