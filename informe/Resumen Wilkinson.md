---
fecha: 2025-06-17
materia: Electronica Analogica II
tipo: Resumen
---
Diseñamos un divisor de potencia de Wilkinson balanceado.
# Principio de funcionamiento
Se trata de dividir una señal de entrada en dos señales cada una con una fracción de la potencia usando dos transformadores de $\frac 1 4$ de onda para adaptar la impedancia de entrada al circuito. La relación entre la potencia de entrada $P_1$ y las potencias de salida de cada puerto $P_2$ y $P_3$ viene dada por la razón de división de potencia $k = \sqrt{P_2/P_3}$  resultando en $Z_{01} = Z_0 \sqrt{1 + k^2}$ y $Z_{02} = Z_0\sqrt{1 + \frac 1 {k^2}}$ . En nuestro caso usamos $P_2 = P_3 = \frac {P_1}{2}$ resultando en $Z_{01} = Z_{02} = Z_0 \cdot \sqrt{2}$.
Entonces cada salida debe reflejar un 50% de la potencia de entrada quedando $P_2 = P_3 = P_1 / 2 \Rightarrow 10\log\left(\frac{P_2}{P_1}\right) = -3\text{dB}$ 
# Proceso de diseño
## Materiales y equipamiento
El proyecto se va a imprimir sobre una placa para radiofrecuencia con las siguientes características:

| Parámetro               | Valor               |     |
| ----------------------- | ------------------- | --- |
| Constante dieléctrica   | $2.00 \pm 0.04$     |     |
| Espesor del dieléctrico | $0.05 \text{ inch}$ |     |
| Espesor del cobre ($t$) | $35 \mu m$          |     |
La impresión sobre el PCB se hace con un router CNC marca Wegstr con una precisión de $4\mu m$ por paso.
![[Pasted image 20250727162128.png]]
Las mediciones sobre el proyecto final con un Analizador de redes de dos puertos marca Rohde & Schwarz modelo ZNC3-2Port

## Diseño ideal
Primero hicimos un diagrama funcional y simulamos las relaciones entre entrada y salida.
El esquemático se diseña en ADS y se pone a continuación
![[ideal.jpg]]
Iniciando desde el puerto uno (desde la izquierda) se tienen:
- Un tramo calculado para que a $1\text{GHz}$ tenga $1\lambda$ de forma tal de ganar distancia entre el conector y la entrada a los dos transformadores de $\frac 1 4 \lambda$ sin que haya desfasaje
- Dos arcos con un radio calculado de manera tal que su longitud sea $\frac 1 4 \lambda$. Su ancho de pista se calcula con line calc para que su impedancia sea $Z = \sqrt 2 Z_0 \approx 70.7\Omega$
- Dos puertos con una resistencia en el medio de $90 \Omega$. Se elige este valor por limitaciones de stock en laboratorio (ideal sería $100\Omega = 2 Z_0$)
- Luego el resto hacia la derecha son parámetros necesarios únicamente para ejecutar la simulación

Como se ve en la sección de parámetros $S$ del esquemático, la simulación se hace con un barrido de frecuencias entre $0.5$ y $1.5 \text{ GHz}$. Se simula y los resultados se exportan al formato s3p para ser procesados luego con scikit rf en Python (análisis completo en los anexos).
Las líneas verticales gruesas en cada ploteo indican la frecuencia objetivo $1\text{GHz}$ y las líneas punteadas indican el máximo o mínimo encontrado programáticamente a partir de los datos
![[Análisis desde simulacion ideal.png]]
## Diseño físico
Luego se diseña el bloque físico en ADS a partir del esquemático

![[simulado.jpg]]
La optimización de los objetivos de aislación y transferencia se logra mediante una disposición estratégica de las piezas. La selección de dos semi-círculos en lugar de tramos rectos se justifica por dos ventajas técnicas fundamentales:  
1. **Maximización de la aislación** entre los tramos, reduciendo interferencias.  
2. **Eliminación de ángulos agudos** en el recorrido de las pistas, lo que mejora el rendimiento electromagnético del diseño.  
La separación en la salida del transformador hacia los puertos viene dada por el tamaño máximo de una resistencia de radiofrecuencia que conseguimos.
Una vez definido el bloque físico, se realizan simulaciones en ADS para evaluar las transferencias. Los resultados se exportan en formato de parámetros *s3p* y se analizan mediante la metodología previamente establecida. Los datos obtenidos se presentan a continuación
![[Analisis de red simulada.png]]
Si bien hay un claro desfasaje hacia frecuencias más altas por limitaciónes de tiempo se determina que se mantiene el diseño

## Construcción física  
Los datos del diseño se exportan en formato Gerber para su fabricación mediante el router especificado previamente. Durante el ensamblado, los puertos SMA se sueldan manualmente para permitir la conexión con el analizador de redes.
Se añaden conexiónes entre el cobre que rodea a las pistas (por dentro y por fuera) y la tierra (placa de cobre inferior) evitando acoplamientos parásitos

![[real.jpg]]
![[IMG-20250618-WA0002.jpg]]
![[IMG-20250618-WA0003.jpg]]
### Resultado:  
A continuación, se procede a realizar las mediciones utilizando el analizador de redes vectoriales (VNA) previamente especificado. Los resultados obtenidos se presentan a continuación
![[Analisis de red real.png]]
## Resultados obtenidos vs esperados
Los resultados muestran que el divisor cumple su función ya que en la frecuencia objetivo se tiene una relación entre entrada y salida de $\approx -3\text{dB}$ y la aislación entre los puertos de salida y las adaptaciones de los tres puertos están todas por debajo de $-20\text{dB}$. Se observa mucho ripple no deseado en la transferencia. Para determinar si el ripple se debía al divisor o a los cables del VNA hicimos una medición del through entre los dos cables. En el análisis anexo se hace la prueba de multiplicar los parámetros $S$ de la transferencia por la inversa del through de los cables (siempre respetando el orden de conexiones original para que los datos sean válidos) pero esto no mejora de manera sustancial el ripple si no que parece simplemente desfasarlo.
A futuro sería bueno implementar:

- Mayor itración en las simulaciónes del bloque en el software, antes de construírlo. Si se observan las mediciones simuladas vs las reales se ve que la tendencia en el corrimiento de la máxima transferencia y máxima aislación se mantiene (se podría haber evitado)
- Pruebas con más puertos para medir las salidas en distintos puntos y tratar de entender a qué se debe el ripple


# Anexos
CNC Wegster https://wegstr.com/CNC-Wegstr/CNC-Wegstr-LIGHT