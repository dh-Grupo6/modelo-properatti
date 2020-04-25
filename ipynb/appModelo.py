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
