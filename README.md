# MOB
Mobiles Emissions. </br>
Programing in python 2.7 import directories xlrd, json, csv, sys. </br>
To import xlrd preview install pip: 
<ul>
<li>$ sudo apt-get install pip 
<li>$ pip install xlrd
</ul>

Execute for mobiles archive in folder src/main.py 
<ul>
<li>$ python main.py
</ul>

##Run the program

```python
  cd src
  python main.py 
```

#CMB - TBW ()
Este sub-modulo corresponde a Fuentes Móviles; su estructura consiste en:
<ul>
    <li>data: Archivos de entrada y salida</li>
        <ul>
            <li>in: archivos de entrada</li></li>
                <ul>
                    <li>constants: Aloja las constantes las cuales no cambian durante las corridas</li>
                        <ul>
                            <li>DAYS_2014.xlsx: Días hábiles y no hábiles 2014</li>
                            <li>DAYS_2030.xlsx: Días hábiles y no hábiles 2030</li>
                        </ul>

                    <li>missionFactors: Aloja los archivos de factores de emisión, con los cuales se operan las emisiones.</li>
                        <ul>
                            <li>FactoresEmision_2014.xlsx: Contiene los factores de emisión para 2014, en una estructura matricial; se pueden agregar datos verticalmente conservando la estructura horizontal y nombres de la filas superior.</li>
                            <li>FactoresEmision_2030.xlsx: Contiene los factores de emisión para 2030, en una estructura matricial; se pueden agregar datos verticalmente conservando la estructura horizontal y nombres de la fila superior.</li>
                            <li>FEBrake_2014.xlsx: Contiene los factores de emisión BRAKE y TIRE para 2014, en una estructura matricial; se pueden agregar datos verticalmente conservando la estructura horizontal y nombres de la fila superior.</li>
                            <li>FEBrake_2030.xlsx: Contiene los factores de emisión BRAKE y TIRE para 2030, en una estructura matricial; se pueden agregar datos verticalmente conservando la estructura horizontal y nombres de la fila superior.</li>
                        </ul>

                    <li>Flows: Aloja los flujos vehiculares que salen del módulo PRE > FLX se identifican por la fecha.</li>
                        <ul>
                            <li>MOB_2014.csv: Archivo .csv que aloja los datos de los flujos vehiculares, este es el resultado del módulo PRE > FLX.</li>
                            <li>MOB_2030.csv: Archivo .csv que aloja los datos de los flujos vehiculares 2030, este es el resultado del módulo PRE > FLX.</li>
                        </ul>

                    <li>Link: Aloja los links correspondientes que provienen de ArcGis. </li>
                        <ul>
                            <li>PRINCIPAL: Aloja los links de vías principales, con los datos a procesar, y/o combinar operacionalmente con los flujos vehiculares. </li>
                                <ul>
                                    <li>PRINCIPALES_2014.xlsx: Archivo que contiene la información de links para las vías principales al año 2014; se pueden agregar datos verticalmente conservando la estructura horizontal y nombres de la fila superior.</li>
                                    <li>PRINCIPALES_2030.xlsx: Archivo que contiene la información de links para las vías principales al año 2030; se pueden agregar datos verticalmente conservando la estructura horizontal y nombres de la fila superior.</li>
                                </ul>

                            <li>SECUNDARIAS: Aloja los links de vías secundarias, con los datos a procesar, y/o combinar operacionalmente con los flujos vehiculares. </li>
                                <ul>
                                    <li>SECUNDARIAS_2014.xlsx: Archivo que contiene la información de links para las vías secundarias al año 2014; se pueden agregar datos verticalmente conservando la estructura horizontal y nombres de la fila superior.</li>
                                    <li>SECUNDARIAS_2030.xlsx: Archivo que contiene la información de links para las vías secundarias al año 2030; se pueden agregar datos verticalmente conservando la estructura horizontal y nombres de la fila superior.</li>
                                </ul>
                        </ul>

                    <li>speciation: Aloja los archivos con los datos para el proceso de especiación de las emisiones BRAKE y TIRE, procesadas. </li>
                        <ul>
                            <li>BRAKE_SCP_PROF_PM25_2014.xlsx: contiene los perfiles de especiación para BRAKE del año 2014; se pueden agregar datos verticalmente conservando la estructura horizontal y nombres de la fila superior.</li>
                            <li>TIRE_SCP_PROF_PM25_2014.xlsx: contiene los perfiles de especiación para TIRE del año 2014; se pueden agregar datos verticalmente conservando la estructura horizontal y nombres de la fila superior.</li>
                            <li>BRAKE_SCP_PROF_PM25_2030.xlsx: contiene los perfiles de especiación para BRAKE del año 2030; se pueden agregar datos verticalmente conservando la estructura horizontal y nombres de la fila superior.</li>
                            <li>TIRE_SCP_PROF_PM25_2030.xlsx: contiene los perfiles de especiación para TIRE del año 2030; se pueden agregar datos verticalmente conservando la estructura horizontal y nombres de la fila superior.</li>
                        </ul>
                </UL>

            <li> out: archivos de salida.</li>
                <ul>
                    <li> carburant: Contienen los resultados por link y grilla de las emisiones por tipo de combustible.</li>
                    <li> category: Contienen los resultados por link y grilla de las emisiones por categoría vehicular. </li>
                    <li> departure: Esta es una salida parcial, que guarda los datos para sacar de aquí los resultados por tipo de combustible, y categoría vehicular.</li>
                    <li>emissions: Contiene los resultados de las emisiones, por link y por grilla, adicional, contiene los unidos de estos. Tanto de combustión como de wear.</li>
                    <li>speciation: Contiene los archivos resultantes del proceso de especiación, donde se divide por combustión y wear, estos se entregan g/s</li>
                    <li>TotalEmisions: Contiene los totales de las emisiones, por contaminante. </li>
                    <li>Principales_vkt_xxxx.csv: Contiene los VKT de vías principales</li>
                    <li>Secundarias_vkt_xxxx.csv: Contiene los VKT de vías Secundarias</li>
                    <li>suma_vkt_xxxx.csv: Contiene la suma de los VKT Principales y Secundarias.</li>
                </ul>
        </ul>    
        
    <li>src: Códigos de programación, y su ejecutable main.py</li>
        <ul>
            <li>core: Aloja los códigos que se reutilizan en todos los módulos. Es decir que se encuentran escritos como funciones generales.</li>
                <ul>
                    <li>binding.py: Se encarga de unir los flujos con los links, de la misma forma que de unir algunos datos intermedios.  </li>
                    <li>clear.py: Realiza una limpieza de la carpeta y subcarpetas out para tener más confianza en los resultados de salida. </li>
                    <li>matriz.py: Realiza las operaciones de pasar de Excel a csv y también de convertir de csv a matriz para realizar operaciones. </li>
                    <li>PMC.py: Calcula el PMC, donde es la resta de PM10 – PM2.5</li>
                    <li>wcsv.py: Realiza la escritura de los datos, o resultados.</li>
                </ul>
            
            <li>emition.py: Calcula las emisiones de fuentes móviles. </li>
            <li>speciation.py: Realiza el cálculo de especiación</li>
            <li>main.py: Ejecutable, el cual contiene las instrucciones y rutas, para realizar las operaciones </li>
            <li>totalEmissions.py: Realiza el cálculo de sacar el total de las emisiones, por contaminante. </li>
            <li>vkt.py: Realiza la suma de las emisiones por hora. </li>
        </ul>
</ul>
