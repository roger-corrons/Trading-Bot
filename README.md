# Evolución de un Algoritmo de Trading en Python

Este repositorio documenta el viaje analítico y de desarrollo para construir un sistema de trading algorítmico rentable. En lugar de buscar un "bot mágico", este proyecto es una autopsia paso a paso de diferentes estrategias cuantitativas, exponiendo los fallos matemáticos ocultos (comisiones, overfitting, riesgo de ruina) y evolucionando el código hasta integrar Machine Learning y Procesamiento de Lenguaje Natural (NLP).

# 1. Tecnologías Utilizadas
- Lenguaje: Python

- Librerías de Datos: yfinance, pandas

- Machine Learning: scikit-learn (Random Forest Classifier)

- Procesamiento de Lenguaje Natural (NLP): nltk (VADER Sentiment Analysis)

# 2. Fases de Desarrollo y Lecciones Aprendidas
- Fase 1: El Espejismo del Scalping y el "Grid Trading"

  La Estrategia: Comprar compulsivamente cada minuto e intentar vender con un beneficio mínimo del +0.5%.
  
  El Resultado: Ganancias teóricas altas, pero destrucción total de la cuenta en el mundo real.
  
  Lección Cuantitativa: Descubrimos los tres enemigos del trader novato:
  
  El Capital Atrapado (Bagholding): Si el mercado cae, te quedas sin liquidez sosteniendo pérdidas latentes ("cuchillos cayendo").
  
  El Fee Drag (Fricción de Comisiones): Operar cientos de veces al día enriquece al bróker. Una comisión fija o porcentual (0.1%) devora los micro-beneficios.
  
  El Riesgo/Beneficio: Introdujimos el Stop Loss (-2.0%) y descubrimos que si arriesgas 4 para ganar 1, la matemática acaba quebrando la cuenta a largo plazo.

- Fase 2: Filtros de Tendencia y Optimización de Parámetros

  La Estrategia: Implementar una Media Móvil Simple (SMA 60) para prohibirle al bot comprar en tendencias bajistas. Además, creamos un Grid Search (bucle de optimización) para encontrar el mejor cruce de Take Profit y Stop Loss.
  
  El Resultado: El bot logró ser rentable en simulaciones cortas (ej. NVDA al +2.0% de ganancia y -2.5% de pérdida).
  
  Lección Cuantitativa: El "ruido" del mercado (Whipsaw) destruye las cuentas. Filtrar la tendencia reduce drásticamente las operaciones perdedoras. Sin embargo, descubrimos el peligro del Overfitting (Sobreajuste): lo que funciona una semana, puede fallar estrepitosamente al mes siguiente.

- Fase 3: El Baño de Realidad (Trend Following vs. Buy & Hold)

  La Estrategia: Un backtest de 2 años operando cruces de medias móviles a largo plazo (SMA 50 vs SMA 200).
  
  El Resultado: El bot fue rentable, pero fue aplastado astronómicamente por la simple estrategia de comprar y mantener (Buy & Hold).
  
  Lección Cuantitativa: Cortar los beneficios demasiado pronto con un Take Profit estático te hace perderte las "corridas alcistas" monumentales. Introdujimos el concepto teórico del Trailing Stop para proteger ganancias sin limitar el crecimiento.

- Fase 4: Inteligencia Artificial Predictiva (Machine Learning)

  La Estrategia: Abandonar las reglas rígidas y usar un RandomForestClassifier para predecir si el S&P 500 subiría al día siguiente. Le inyectamos indicadores como predictores: Rendimiento Diario, SMA 10, SMA 50, Volatilidad, RSI y Volumen.
  
  El Resultado: La IA logró una precisión (Precision Score) de casi el 57% en datos nunca vistos (test set).
  
  Lección Cuantitativa: En bolsa, un acierto del 55-57% es el equivalente a ser un casino: tienes una ventaja matemática real.

- Fase 5: El Bot "Francotirador" (Probabilidades y Hold)

  La Estrategia: Aunque la IA acertaba, las comisiones diarias nos desangraban. Cambiamos la lógica binaria (0 o 1) por el método .predict_proba().
  
  El Resultado: El bot solo operaba si la IA tenía una confianza >60%. Además, aprendió el estado Hold (Mantener) para no pagar comisiones en días consecutivos de subida.
  
  Lección Cuantitativa: Menos es más. Filtrar por el "umbral de confianza" hundió la cantidad de operaciones (reduciendo comisiones al mínimo) y transformó los números rojos en beneficios netos.

- Fase 6: Leyendo las Emociones del Mercado (NLP)

  La Estrategia: El mercado no solo es matemática, es psicología. Usamos NLTK (VADER) para descargar y leer titulares de noticias de Yahoo Finance en tiempo real.
  
  El Resultado: El bot asignó puntuaciones de sentimiento (de -1 a +1) a los titulares, tomando una decisión final (Optimismo, Miedo o Neutralidad) para filtrar operaciones basadas puramente en el pánico o la euforia humana.
  
  Lección Cuantitativa: El procesamiento de lenguaje natural tiene "ruido" (noticias de otras empresas coladas por el sector), por lo que requiere blindaje en la extracción de datos (manejo de KeyErrors en APIs).

# 3. Conclusión del Proyecto
1. El "Santo Grial" del trading algorítmico no es un indicador mágico. Es un Stack Cuantitativo que combina:

2. Machine Learning para la ventaja probabilística.

3. Análisis de Sentimiento para entender el contexto irracional.

4. Gestión de Riesgo (Trailing Stops) para proteger el capital.

5. Optimización de Comisiones (Umbrales de confianza y estados Hold).
