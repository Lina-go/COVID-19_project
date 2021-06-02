import numpy as np
import matplotlib.pyplot as plt # manipulacion de graficas
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk) # graficas y toolbar de graficas
from matplotlib.backend_bases import key_press_handler
from matplotlib.font_manager import FontProperties    # Esto es para modificar el estilo de fuente de los gráficos.
import matplotlib
import tkinter as tk
from tkinter import *               # wild card import para evitar llamar tk cada vez

from tkinter import filedialog      # elegir archivos
from tkinter import messagebox      # mensaje de cerrar
from PIL import ImageTk ,Image      # insersion de imagenes
import datetime as dt               # fecha para que la carpeta de datos tenga un nombres bonito
import tkinter.font as font         # mas fuentes
import struct as st
from pathlib import Path
from time import time
#from Logica import *                # importo todos los metodos implementados en la logica
from model import * 

# parametros iniciales de matplotlib
matplotlib.use("TkAgg")


class Interfaz:
    ''' Clase que modela toda la interfaz del app, por comodidad y orden se define asi y se llama en la llave main al final del script
    '''

    def __init__(self, ventanta):
        # algunas variables que se usaran a lo largo de la aplicacion
        self.ventana = ventanta
        self.ventana.title('Epidemiología de distintos países')
        self.fuente_ppal = font.Font(family='math')
        self.fuente_sec = ('math', 15, 'bold italic')
        self.fuente_param = ('math', 12, 'bold italic')
        self.fuente_text = ('math', 14, 'bold italic')
        self.fuente_title = ("Our Arcade Games Regular",30)
        self.directorioActual = Path(__file__).parent
        # Colores
        self.color_1 = '#2b2c2f'
        self.color_2 = '#615d62'
        self.color_3 = '#414044'
        self.color_4 = '#8e858b'
        self.color_blanco = '#fff'
        self.color_negro = '#000'
        self.color_efor = 'red'
        self.color_eback = '#fbb901'
        self.color_emod = 'darkgreen'
        self.color_rk2 = 'blue'
        self.color_rk4 = 'purple'
        self.color_scipy = 'black'
        # =================== Lista de ejecuciones de cada algoritmo para guardar ==========================
        # guardo tuplas de los listados de x y y de la ejecucion de cada algoritmo mientras no se limpie la grafica
        self.eForSet = []
        self.eBackSet = []
        self.eModSet = []
        self.RK2Set = []
        self.RK4Set = []
        self.scipySet = []
        

        # ================================================= toolbar =================================================
        self.frameHerramientas = Frame(self.ventana, bd=5 , bg=self.color_1)
        # genero los objetos imagen para la toolbox
        abrir_img = Image.open(self.directorioActual.joinpath('abrir.png').absolute())
        guardar_img = Image.open(self.directorioActual.joinpath('Imagen4.png').absolute())
        cerrar_img = Image.open(self.directorioActual.joinpath('exit.png').absolute())
        abrir_icon = ImageTk.PhotoImage(abrir_img)
        guardar_icon = ImageTk.PhotoImage(guardar_img)
        cerrar_icon = ImageTk.PhotoImage(cerrar_img)
        
        # creo los botones con las imagenes definidas ateriormente
        self.abrir_btn = Button(self.frameHerramientas, image=abrir_icon, command=self.cargarDatos ,border="0",bg=self.color_1)
        self.guardar_btn = Button(self.frameHerramientas, image=guardar_icon, command=self.guardarDatos, border="0",bg=self.color_1)
        self.cerrar_btn = Button(self.frameHerramientas, image=cerrar_icon, command=self.cerrarAplicacion, border="0",bg=self.color_1)

        self.abrir_btn.image = abrir_icon
        self.guardar_btn.image = guardar_icon
        self.cerrar_btn.image = cerrar_icon
        # posiciono los botones y el frame de herramientas
        self.abrir_btn.pack(side=LEFT, padx =1,pady=2)
        self.guardar_btn.pack(side=LEFT, padx =2,pady=2)
        self.cerrar_btn.pack(side=RIGHT, padx =2,pady=2)
        self.frameHerramientas.pack(side=TOP,fill=X)

        # =================================================  frame de contenido y subframes =================================================

        self.frameContenido = Frame(self.ventana, bd=5 , bg=self.color_1)
        # hago que el frame ocupe todo el espacio sobrante ya que este sera sobre el que dibuje el resto de widgets
        self.frameContenido.pack(expand=True, fill=BOTH)
        
        #defino los 2 frames que usara para que la interfaz quede bonita
        # el frame de la izquierda donde ira la grafica y los parametros de corriente
        self.frameLeft = Frame(self.frameContenido, bd=5, width=600 , bg=self.color_4)
        # hago que el frame ocupe todo el espacio sobrante ya que este sera sobre el que dibuje el resto de widgets
        self.frameLeft.pack(side=LEFT, fill=Y)
        # el frame de la derecha donde iran los demas parametros y los metodos de solucion
        self.frameRight = Frame(self.frameContenido, bd=5, width=300 , bg=self.color_4)
        # hago que el frame ocupe todo el espacio sobrante ya que este sera sobre el que dibuje el resto de widgets
        self.frameRight.pack(side=RIGHT, fill=Y)
        
        # Creo los contenedores de los botones, graficas y demas

        # frame de la grafica
        self.frameGrafica = Frame(self.frameLeft, bd = 5, height=450, width=585 , bg=self.color_2) 
        self.frameGrafica.place(x=0,y=0)
        # frame del apartado para la corriente
        self.frameCorriente = Frame(self.frameLeft, bd = 5, height=75, width=585 , bg=self.color_2)
        self.frameCorriente.place(x=0,y=530)
        # frame del apartado para la corriente
        self.frametiempo = Frame(self.frameLeft, bd = 5, height=70, width=585 , bg=self.color_2)
        self.frametiempo.place(x=0,y=455)
        # frame de los metodos
        self.frameMetodos = Frame(self.frameRight, bd = 5, height=300, width=285 , bg=self.color_2) 
        self.frameMetodos.place(x=0,y=0)
        # frame del los parametros
        self.frameParametros = Frame(self.frameRight, bd = 5, height=300, width=285 , bg=self.color_2)
        self.frameParametros.place(x=0,y=305)
        # ================================ Grafica ===========================================
        plt.style.use('bmh')
        self.fig = plt.Figure(figsize=(5.75, 4.0)) # figura principal
        self.plot = self.fig.add_subplot(1,1,1) # plto principal donde se dibujara todos los datos
        grafFont = FontProperties()
        grafFont.set_family('serif')   # Define que las fuentes usadas en el gráfico son serifadas.
        self.plot.set_xlabel(r'$t\ \ [tiempo]$',fontsize='x-large', fontproperties=grafFont)       # Título secundario del eje x
        self.plot.set_ylabel(r'$population\ [porcentaje]$ ',fontsize='large', fontproperties=grafFont)        # Título secundario del eje y
        

        self.plot.set_title('Análisis epidemiológico COVID-19', fontsize='x-large', fontproperties=grafFont) # Titulo Principal
        self.fig.tight_layout()
        self.imagenGrafica = FigureCanvasTkAgg(self.fig, master=self.frameGrafica)  # canvas que dibujara la grafica en la interfaz
        self.imagenGrafica.get_tk_widget().place(x=0,y=0)                           # le asigno su posicion
        self.herramientasGrafica = NavigationToolbar2Tk(self.imagenGrafica, self.frameGrafica, pack_toolbar=False) # creo la barra de herramientas que manipularan la grafica
        self.herramientasGrafica.update()                                                                           # lo añada a la interfaz
        self.herramientasGrafica.place(x=0, y=400)                                                                  # le pongo su lugar

        # boton que se encargara de limpiar las ejecuciones de algoritmos en la grafica
        self.limpiar_btn = Button(master=self.frameGrafica, text="limpiar",  command = self.limpiarGrafica, bg=self.color_3, fg = self.color_blanco,  width=20, height=1, font=self.fuente_ppal,border="0")
        self.limpiar_btn.place(x=350,y=410)
    	# ================================ Variables para las formulas ================================
        
        self.sbutton =  IntVar()
        self.ebutton =  IntVar()
        self.ibutton =  IntVar()
        self.rbutton =  IntVar()
        self.pbutton =  IntVar()

        self.k = StringVar()
        self.a_e = StringVar()
        self.a_i = StringVar()
        self.beta = StringVar()
        self.rho = StringVar()
        self.miu = StringVar()
        self.gamma = StringVar()
        self.tiempo_inicial = StringVar()
        self.tiempo_final = StringVar()
        self.tiempo4 = StringVar()
        self.intensidad1 = StringVar()
        self.intensidad2 = StringVar()
        # ================================ Valores Defecto ==================================
        
        self.k.set('0.05')
        self.a_e.set('0.65')
        self.a_i.set('0.005')
        self.beta.set('0.1')
        self.rho.set('0.08')
        self.miu.set('0.02')
        self.gamma.set("0.005")
        self.tiempo_inicial.set('0.0')
        self.tiempo_final.set('150.0')
        self.tiempo4.set('200.0')
        self.intensidad1.set('20.0')
        self.intensidad2.set('-15.0')
        
        

        # ================================ Contenido ==================================

        # -----------------------------contenido de corriente--------------------------

        # radio button de corriente constate el cual llama a la funcion que habilita las entradas de datos
        self.s = Checkbutton(text='S(t)', variable=self.sbutton, bg=self.color_2,font=self.fuente_sec)
        self.s.place(x=30,y=544)

        
        # radio button de corriente variable el cual llama a la funcion que habilita las entradas de datos adicionales
        self.e = Checkbutton(master=self.frametiempo, text='E(t)', variable=self.ebutton, bg=self.color_2,font=self.fuente_sec)
        self.e.place(x=140,y=10)

        # radio button de corriente variable el cual llama a la funcion que habilita las entradas de datos adicionales
        self.i = Checkbutton(master=self.frametiempo, text='I(t)',  variable=self.ibutton, bg=self.color_2,font=self.fuente_sec)
        self.i.place(x=250,y=10)

        self.r = Checkbutton(master=self.frametiempo, text='R(t)',  variable=self.rbutton, bg=self.color_2,font=self.fuente_sec)
        self.r.place(x=360,y=10)

        self.p = Checkbutton(master=self.frametiempo, text='P(t)',  variable=self.pbutton, bg=self.color_2,font=self.fuente_sec)
        self.p.place(x=470,y=10)
        
        # titulo de los parametros de tiempo 
        self.titulo_tiempo = Label(self.frameCorriente, text='Tiempo de Simulación', font=self.fuente_sec,fg = self.color_blanco, bg =self.color_1)
        self.titulo_tiempo.place(x=5,y=20)

        # entradas de tiempo para corriente constante, el separador entre entradas y sus respectivas unidades

        self.tiempo0_in = Entry(master=self.frameCorriente, textvariable=self.tiempo_inicial, width=5, font=self.fuente_sec)
        self.tiempo0_in.place(x=270,y=20)

        self.sep1 =  Label(self.frameCorriente,width=2, text='-', font=self.fuente_sec,fg = self.color_blanco, bg =self.color_2) 
        self.sep1.place(x=330,y=20)

        self.tiempo_final_in = Entry(master=self.frameCorriente, textvariable=self.tiempo_final, width=5, font=self.fuente_sec)
        self.tiempo_final_in.place(x=370,y=20)

        self.ms_decor1 =  Label(self.frameCorriente,width=11, text='t en días', font=self.fuente_sec,fg = self.color_blanco, bg =self.color_2) 
        self.ms_decor1.place(x=430,y=20)

        

        # entradas de tiempo adicionales para corriente variable,  el separador entre entradas y sus respectivas unidades
        

        self.miu_in = Entry(master=self.frameCorriente, textvariable=self.miu, width=5, font=self.fuente_sec)
        self.miu_in.place(x=250,y=90)

        self.sep2 =  Label(self.frameCorriente,width=2, text='-', font=self.fuente_sec,fg = self.color_blanco, bg =self.color_2) 
        self.sep2.place(x=315,y=90)

        self.tiempo4_in = Entry(master=self.frameCorriente, textvariable=self.tiempo4, width=5, font=self.fuente_sec)
        self.tiempo4_in.place(x=350,y=90)


        # intensidad corriente para corriente variable, con borde amarillo y su respectiva etiqueta de unidades
        self.intensidad2_in = Entry(master=self.frameCorriente, textvariable=self.intensidad2, width=5, font=self.fuente_sec, highlightthickness=2, highlightbackground = "yellow", highlightcolor= "yellow")
        self.intensidad2_in.place(x=470,y=90)


        # desactivo las entradas de intesidad variable hasta que se seleccione dicha opcion y le cambio el bg para que se vea cool

        
        self.tiempo4_in.configure(state="disabled", disabledbackground=self.color_3)
        self.intensidad2_in.configure(state="disabled", disabledbackground=self.color_3)

        # ----------------------------------------------contenido de metodos de solucion ------------------------------------
        # titulo del apartado de metodos de solcion
        self.title =  Label( text='PROYECTO FINAL', font=self.fuente_title,fg = self.color_blanco, bg =self.color_1)
        self.title.place(x=255,y=12)
        
        
        # titulo del apartado de metodos de solcion
        self.metodos_lbl =  Label(self.frameMetodos, text='Métodos de solución', font=self.fuente_sec,fg = self.color_blanco, bg =self.color_1)
        self.metodos_lbl.place(x=35,y=10)

        # boton para el metodo euler for y su respectivo color
        self.metodos_decor1 =  Label(self.frameMetodos,width=2, text='', font=self.fuente_ppal,fg = self.color_blanco, bg =self.color_efor) 
        self.metodos_decor1.place(x=20,y=61)

        self.eulerfw_btn = Button(master=self.frameMetodos, text="Euler Adelante",  command = self.llamadoEulerFor, bg=self.color_3, fg = self.color_blanco,  width=20,height=1, font=self.fuente_ppal,border="0")
        self.eulerfw_btn.place(x=45,y=60)

        # boton para el metodo euler back y su respectivo color

        self.metodos_decor2 =  Label(self.frameMetodos,width=2, text='', font=self.fuente_ppal,fg = self.color_blanco, bg =self.color_eback) 
        self.metodos_decor2.place(x=20,y=101)

        self.eulerbk_btn = Button(master=self.frameMetodos, text="Euler Atrás",  command = self.llamadoEulerBack, bg=self.color_3, fg = self.color_blanco,  width=20, height=1, font=self.fuente_ppal,border="0")
        self.eulerbk_btn.place(x=45,y=100)

        # boton para el metodo euler modificado y su respectivo color
        self.metodos_decor3 =  Label(self.frameMetodos,width=2, text='', font=self.fuente_ppal,fg = self.color_blanco, bg =self.color_emod) 
        self.metodos_decor3.place(x=20,y=141)

        self.eulermod_btn = Button(master=self.frameMetodos, text="Euler Mod",  command = self.llamadoEulerMod, bg=self.color_3, fg = self.color_blanco,  width=20, height=1, font=self.fuente_ppal,border="0")
        self.eulermod_btn.place(x=45,y=140)

        # boton para el metodo rk2 y su respectivo color
        self.metodos_decor4 =  Label(self.frameMetodos,width=2, text='', font=self.fuente_ppal,fg = self.color_blanco, bg =self.color_rk2) 
        self.metodos_decor4.place(x=20,y=181)

        self.rk2_btn = Button(master=self.frameMetodos, text="Runge-Kutta 2",  command = self.llamadoRK2, bg=self.color_3, fg = self.color_blanco,  width=20, height=1, font=self.fuente_ppal,border="0")
        self.rk2_btn.place(x=45,y=180)

        # boton para el metodo rk4 y su respectivo color
        self.metodos_decor5 =  Label(self.frameMetodos,width=2, text='', font=self.fuente_ppal,fg = self.color_blanco, bg =self.color_rk4) 
        self.metodos_decor5.place(x=20,y=221)

        self.rk4_btn = Button(master=self.frameMetodos, text="Runge-Kutta 4",  command = self.llamadoRK4, bg=self.color_3, fg = self.color_blanco,  width=20, height=1, font=self.fuente_ppal,border="0")
        self.rk4_btn.place(x=45,y=220)

        # boton para el metodo scipy y su respectivo color
        self.metodos_decor6 =  Label(self.frameMetodos,width=2, text='', font=self.fuente_ppal,fg = self.color_blanco, bg =self.color_scipy) 
        self.metodos_decor6.place(x=20,y=261)

        self.scipy_btn = Button(master=self.frameMetodos, text="Scipy",  command = self.llamadoScipy, bg=self.color_3, fg = self.color_blanco,  width=20, height=1, font=self.fuente_ppal,border="0")
        self.scipy_btn.place(x=45,y=260)

        # ------------------------------------------------- contenido de parametros -----------------------------------------------
        # titulo del apartadode parametros
        self.metodos_lbl =  Label(self.frameParametros, text='Parámetros', font=self.fuente_text,fg = self.color_blanco, bg =self.color_1)

        self.metodos_lbl.place(x=70,y=10)
        # Parámetros
        # etiqueta para el parametro a_e y su respectiva entrada para cambiar el parametro

        self.k_lbl =  Label(self.frameParametros,width=5, text='k:', font=self.fuente_param,fg = self.color_blanco, bg =self.color_1)
        self.k_lbl.place(x=30,y=50)

        self.k_in = Entry(master=self.frameParametros, textvariable=self.k, width=8, font=self.fuente_param)
        self.k_in.place(x=120,y=50)

        self.k_lbl_units =  Label(self.frameParametros,width=3, text='%', font=self.fuente_param,fg = self.color_blanco, bg =self.color_2)
        self.k_lbl_units.place(x=220,y=50)
        # etiqueta para el parametro a_e y su respectiva entrada para cambiar el parametro

        self.a_e_lbl =  Label(self.frameParametros,width=5, text='a'+u"\u2091"+":", font=self.fuente_param,fg = self.color_blanco, bg =self.color_1)
        self.a_e_lbl.place(x=30,y=85)

        self.a_e_in = Entry(master=self.frameParametros, textvariable=self.a_e, width=8, font=self.fuente_param)
        self.a_e_in.place(x=120,y=85)

        self.a_e_lbl_units =  Label(self.frameParametros,width=3, text='%', font=self.fuente_param,fg = self.color_blanco, bg =self.color_2)
        self.a_e_lbl_units.place(x=220,y=85)
        
        # etiqueta para el parametro n_0 y su respectiva entrada para cambiar el parametro

        self.a_i_lbl =  Label(self.frameParametros,width=5, text='a'+u"\u1D62"+":", font=self.fuente_param,fg = self.color_blanco, bg =self.color_1)
        self.a_i_lbl.place(x=30,y=120)

        self.a_i_in = Entry(master=self.frameParametros, textvariable=self.a_i, width=8, font=self.fuente_param)
        self.a_i_in.place(x=120,y=120)

        self.a_i_lbl_units =  Label(self.frameParametros,width=3, text='%', font=self.fuente_param,fg = self.color_blanco, bg =self.color_2)
        self.a_i_lbl_units.place(x=220,y=120)

        # etiqueta para el parametro m_0 y su respectiva entrada para cambiar el parametro
        self.beta_lbl =  Label(self.frameParametros,width=5, text=u"\u03B2"+":", font=self.fuente_param,fg = self.color_blanco, bg =self.color_1)
        self.beta_lbl.place(x=30,y=155)

        self.beta_in = Entry(master=self.frameParametros, textvariable=self.beta, width=8, font=self.fuente_param)
        self.beta_in.place(x=120,y=155)

        self.beta_lbl_units =  Label(self.frameParametros,width=3, text='%', font=self.fuente_param,fg = self.color_blanco, bg =self.color_2)
        self.beta_lbl_units.place(x=220,y=155)
        # etiqueta para el parametro h_0 y su respectiva entrada para cambiar el parametro
        self.rho_lbl =  Label(self.frameParametros,width=5, text=u"\u03C1"+":", font=self.fuente_param,fg = self.color_blanco, bg =self.color_1)
        self.rho_lbl.place(x=30,y=190)

        self.rho_in = Entry(master=self.frameParametros, textvariable=self.rho, width=8, font=self.fuente_param)
        self.rho_in.place(x=120,y=190)

        self.rho_lbl_units =  Label(self.frameParametros,width=3, text='%', font=self.fuente_param,fg = self.color_blanco, bg =self.color_2)
        self.rho_lbl_units.place(x=220,y=190)
        # etiqueta para el parametro miu y su respectiva entrada para cambiar el parametro
        self.miu_lbl =  Label(self.frameParametros,width=5, text=u"\u03BC"+":", font=self.fuente_param,fg = self.color_blanco, bg =self.color_1) 
        self.miu_lbl.place(x=30,y=225)

        self.miu_in = Entry(master=self.frameParametros, textvariable=self.miu, width=8, font=self.fuente_param)
        self.miu_in.place(x=120,y=225)

        self.miu_lbl_units =  Label(self.frameParametros,width=3, text="%", font=self.fuente_param,fg = self.color_blanco, bg =self.color_2)
        self.miu_lbl_units.place(x=220,y=225)
        
        # etiqueta para el parametro gamma y su respectiva entrada para cambiar el parametro

        self.gamma_lbl =  Label(self.frameParametros,width=5, text=u"\u03B3"+":", font=self.fuente_param,fg = self.color_blanco, bg =self.color_1)
        self.gamma_lbl.place(x=30,y=260)

        self._gamma = Entry(master=self.frameParametros, textvariable=self.gamma, width=8, font=self.fuente_param)
        self._gamma.place(x=120,y=260)

        self.gamma_lbl_units =  Label(self.frameParametros,width=3, text='%', font=self.fuente_param,fg = self.color_blanco, bg =self.color_2)
        self.gamma_lbl_units.place(x=220,y=260)
    
    def limpiarGrafica(self):
        ''' Funcion que limpia las grafica y las listas donde se guardan los datos para los metodos de persistencia
        '''
        self.plot.cla() # lipio toda la grafica, esto elimina incluso los titulos por lo que debo volver a ponerlos despues de esto
        grafFont = FontProperties()
        grafFont.set_family('serif')                                                           # Define que las fuentes usadas en el gráfico son serifadas.
        self.plot.set_xlabel(r'$t\ \ [tiempo]$',fontsize='x-large', fontproperties=grafFont)       # Título secundario del eje x
        self.plot.set_ylabel(r'$population\ [porcentaje]$ ',fontsize='large', fontproperties=grafFont)        # Título secundario del eje y
        self.plot.set_title('Análisis epidemiológico COVID-19', fontsize='x-large', fontproperties=grafFont) # titulo principal
        self.imagenGrafica.draw()                                                              # Una vez agregado todo dibujo la grafica en la interfaz
        # vuelvo a poner el valor vacio en las listas que guardan los datos para los metodos de persistencia
        self.eForSet = []
        self.eBackSet = []
        self.eModSet = []
        self.RK2Set = []
        self.RK4Set = []
        self.scipySet = []

    def actualizarParametros(self):
        ''' Metodo que sera llamado cada vez que se desee ejecutar un algoritmo, esto con el fin de siempre tener los parametros actualizados
        '''
        # obtengo los valores de cada entrada de las varibales en la interfaz
        pgamma = float(self.gamma.get())
        pk = float(self.k.get())
        pa_e = float(self.a_e.get())
        pa_i = float(self.a_i.get())
        pbeta = float(self.beta.get())
        prho = float(self.rho.get())
        pmiu = float(self.miu.get())

        pOpcion_s = int(self.sbutton.get())

        pTiempo_inicial=float(self.tiempo_inicial.get())
        pTiempo_final=float(self.tiempo_final.get())
        pTiempo3=0
        pTiempo4=0
        pIntensidad1=float(self.intensidad1.get())
        pIntensidad2=0
        # si la opcion es corriente variable entonces obtengo los valores adicionales si no estos permanecen como 0
        return (pa_e,pa_i,pbeta,prho,pmiu,pOpcion_s,pTiempo_inicial,pTiempo_final,pTiempo3,pTiempo4,pIntensidad1,pIntensidad2,pgamma,pk)


    def llamadoEulerFor(self):
        ''' Metodo que llamara la funcion definida en la logica para el metodo euler forward con los parametros que tenga la interfaz en este momento
        '''
        # se piden los parametros a la interfaz
        parametro = self.actualizarParametros()
        t0= parametro[6]
        tf = parametro[7]
        a_e= parametro[0]
        a_i = parametro[1]
        k= parametro[13]
        gamma= parametro[12]
        B= parametro[2]
        phi= parametro[3] 
        u= parametro[4]
        t, ys_EulerFor, ye_EulerFor, yi_EulerFor, yr_EulerFor, yp_EulerFor= eulerforward(t0, tf, a_e, a_i, k, gamma, B, phi, u)
        # llamo la funcion de la logica para el metodo y obtengo los valores de x y y a graficar
        if self.sbutton.get():
            self.eForSet.append((t,ys_EulerFor))
            self.plot.plot(t,ys_EulerFor,color="#F58731",label="s(t)_Efor")
        
        if self.ebutton.get():
            self.eForSet.append((t,ye_EulerFor))
            self.plot.plot(t,ye_EulerFor,color="#3DF53F",label="e(t)_Efor")
            
        if self.ibutton.get():
            self.eForSet.append((t,yi_EulerFor))
            self.plot.plot(t,yi_EulerFor,color="#F54425",linestyle='dashed',label="i(t)_Efor")
            
        if self.rbutton.get():
            self.eForSet.append((t,yr_EulerFor))
            self.plot.plot(t,yr_EulerFor,color="#0CD6F5",label="r(t)_Efor")
            
        if self.pbutton.get():
            self.eForSet.append((t,yp_EulerFor))
            self.plot.plot(t,yp_EulerFor,color="#F51883",label="p(t)_Efor")
        
        self.plot.legend(loc="upper right")
        self.imagenGrafica.draw()
        # agregro los valores como una tupla en la variable que guarda las ejecuciones para los metodos de persistencia
        
        
        
        
        
        # grafico los puntos con el respectivo color asignado para el metodo, variable que se puede cambiar en el ini
        # una vez se añade todo al plot procedo a mostrarlo en la interfaz con el metodo draw del canvas definido para la grafica
        


    def llamadoEulerBack(self):
        ''' Metodo que llamara la funcion definida en la logica para el metodo euler back con los parametros que tenga la interfaz en este momento
        '''
        # se piden los parametros a la interfaz
        parametro = self.actualizarParametros()
        t0= parametro[6]
        tf = parametro[7]
        a_e= parametro[0]
        a_i = parametro[1]
        k= parametro[13]
        gamma= parametro[12]
        B= parametro[2]
        phi= parametro[3] 
        u= parametro[4]
        t, ys_EulerBack, ye_EulerBack, yi_EulerBack, yr_EulerBack, yp_EulerBack= eulerbackward(t0, tf, a_e, a_i, k, gamma, B, phi, u)
        
        print(self.sbutton.get())
        if self.sbutton.get():
            self.eBackSet.append((t,ys_EulerBack))
            self.plot.plot(t,ys_EulerBack,color="#4A2AA8",label="s(t)_Eback")
        
        if self.ebutton.get():
            self.eBackSet.append((t,ye_EulerBack))
            self.plot.plot(t,ye_EulerBack,color="#6331F5",label="e(t)_Eback")
            
        if self.ibutton.get():
            self.eBackSet.append((t,yi_EulerBack))
            self.plot.plot(t,yi_EulerBack,color="#A3F525",linestyle='dashed',label="i(t)_Eback")
            
        if self.rbutton.get():
            self.eBackSet.append((t,yr_EulerBack))
            self.plot.plot(t,yr_EulerBack,color="#A80843",label="r(t)_Eback")
            
        if self.pbutton.get():
            self.eBackSet.append((t,yp_EulerBack))
            self.plot.plot(t,yp_EulerBack,color="#F51869",label="p(t)_Eback")
        
        self.plot.legend(loc="upper right")
        self.imagenGrafica.draw()
        # llamo la funcion de la logica para el metodo y obtengo los valores de x y y a graficar
        
        # agregro los valores como una tupla en la variable que guarda las ejecuciones para los metodos de persistencia
        # grafico los puntos con el respectivo color asignado para el metodo, variable que se puede cambiar en el init
    


    def llamadoEulerMod(self):
        ''' Metodo que llamara la funcion definida en la logica para el metodo euler modificado con los parametros que tenga la interfaz en este momento
        '''
        # se piden los parametros a la interfaz
        parametro = self.actualizarParametros()
        t0= parametro[6]
        tf = parametro[7]
        a_e= parametro[0]
        a_i = parametro[1]
        k= parametro[13]
        gamma= parametro[12]
        B= parametro[2]
        phi= parametro[3] 
        u= parametro[4]
        t, ys_EulerMod, ye_EulerMod, yi_EulerMod, yr_EulerMod, yp_EulerMod = eulermodificado(t0, tf, a_e, a_i, k, gamma, B, phi, u)
        if self.sbutton.get():
            self.eModSet.append((t,ys_EulerMod))
            self.plot.plot(t,ys_EulerMod,color="#0A38C2",label="s(t)_EMod")
        
        if self.ebutton.get():
            self.eModSet.append((t,ye_EulerMod))
            self.plot.plot(t,ye_EulerMod,color="#5C698F",label="e(t)_EMod")
            
        if self.ibutton.get():
            self.eModSet.append((t,yi_EulerMod))
            self.plot.plot(t,yi_EulerMod,color="#25C6F5",linestyle='dashed',label="i(t)_EMod")
            
        if self.rbutton.get():
            self.eModSet.append((t,yr_EulerMod))
            self.plot.plot(t,yr_EulerMod,color="#F69662",label="r(t)_EMod")
            
        if self.pbutton.get():
            self.eModSet.append((t,yp_EulerMod))
            self.plot.plot(t,yp_EulerMod,color="#C22F0A",label="p(t)_EMod")
        
        self.plot.legend(loc="upper right")
        self.imagenGrafica.draw()
        
    


    def llamadoRK2(self):
        ''' Metodo que llamara la funcion definida en la logica para el metodo runge-kutta 2 con los parametros que tenga la interfaz en este momento
        '''
        # se piden los parametros a la interfaz
        parametro = self.actualizarParametros()
        t0= parametro[6]
        tf = parametro[7]
        a_e= parametro[0]
        a_i = parametro[1]
        k= parametro[13]
        gamma= parametro[12]
        B= parametro[2]
        phi= parametro[3] 
        u= parametro[4]
        # llamo la funcion de la logica para el metodo y obtengo los valores de x y y a graficar
        
        t, ys_RK2, ye_RK2, yi_RK2, yr_RK2, yp_RK2= rk2(t0, tf, a_e, a_i, k, gamma, B, phi, u)
        if self.sbutton.get():
            self.RK2Set.append((t,ys_RK2))
            self.plot.plot(t,ys_RK2,color="#D6D0F2",label="s(t)_RK2")
        
        if self.ebutton.get():
            self.RK2Set.append((t,ye_RK2))
            self.plot.plot(t,ye_RK2,color="#F53D50",label="e(t)_RK2")
            
        if self.ibutton.get():
            self.RK2Set.append((t,yi_RK2))
            self.plot.plot(t,yi_RK2,color="#25C6F5",linestyle='dashed',label="i(t)_RK2")
            
        if self.rbutton.get():
            self.RK2Set.append((t,yr_RK2))
            self.plot.plot(t,yr_RK2,color="#F5EB9E",label="r(t)_RK2")
            
        if self.pbutton.get():
            self.RK2Set.append((t,yp_RK2))
            self.plot.plot(t,yp_RK2,color="#18F54A",label="p(t)_RK2")
        
        self.plot.legend(loc="upper right")
        self.imagenGrafica.draw()
        # agregro los valores como una tupla en la variable que guarda las ejecuciones para los metodos de persistencia
        
    

    def llamadoRK4(self):
        ''' Metodo que llamara la funcion definida en la logica para el metodo runge-kutta 4 con los parametros que tenga la interfaz en este momento
        '''
        # se piden los parametros a la interfaz
        parametro = self.actualizarParametros()
        t0= parametro[6]
        tf = parametro[7]
        a_e= parametro[0]
        a_i = parametro[1]
        k= parametro[13]
        gamma= parametro[12]
        B= parametro[2]
        phi= parametro[3] 
        u= parametro[4]
        # llamo la funcion de la logica para el metodo y obtengo los valores de x y y a graficar
        
        t, ys_RK4, ye_RK4, yi_RK4, yr_RK4, yp_RK4= rk4(t0, tf, a_e, a_i, k, gamma, B, phi, u)
        if self.sbutton.get():
            self.RK4Set.append((t,ys_RK4))
            self.plot.plot(t,ys_RK4,color="#A80011",label="s(t)_RK4")
        
        if self.ebutton.get():
            self.RK4Set.append((t,ye_RK4))
            self.plot.plot(t,ye_RK4,color="#F56170",label="e(t)_RK4")
            
        if self.ibutton.get():
            self.RK4Set.append((t,yi_RK4))
            self.plot.plot(t,yi_RK4,color="#5B86F5",linestyle='dashed',label="i(t)_RK4")
            
        if self.rbutton.get():
            self.RK4Set.append((t,yr_RK4))
            self.plot.plot(t,yr_RK4,color="#3AA82D",label="r(t)_RK4")
            
        if self.pbutton.get():
            self.RK4Set.append((t,yp_RK4))
            self.plot.plot(t,yp_RK4,color="#5FF54E",label="p(t)_RK4")
        
        self.plot.legend(loc="upper right")
        self.imagenGrafica.draw()
        
        # agregro los valores como una tupla en la variable que guarda las ejecuciones para los metodos de persistencia
        
        
        
        # grafico los puntos con el respectivo color asignado para el metodo, variable que se puede cambiar en el init
        

    
    def llamadoScipy(self):
        ''' Metodo que llamara la funcion definida en la logica para el metodo implementado con scipy con los parametros que tenga la interfaz en este momento
        '''
        # se piden los parametros a la interfaz
        parametro = self.actualizarParametros()
        t0= parametro[6]
        tf = parametro[7]
        a_e= parametro[0]
        a_i = parametro[1]
        k= parametro[13]
        gamma= parametro[12]
        B= parametro[2]
        phi= parametro[3] 
        u= parametro[4]
        t, y_0,  y_1, y_2, y_3, y_4 = scipy(t0, tf, a_e, a_i, k, gamma, B, phi, u,h = 0.01)
        if self.sbutton.get():
            self.RK4Set.append((t,y_0))
            self.plot.plot(t,y_0,color="#F06F6C",label="s(t)_RK45")
        
        if self.ebutton.get():
            self.RK4Set.append((t,y_1))
            self.plot.plot(t,y_1,color="#F5CA20",label="e(t)_RK45")
            
        if self.ibutton.get():
            self.RK4Set.append((t,y_2))
            self.plot.plot(t,y_2,color="#F50500",linestyle='dashed',label="i(t)_RK45")
            
        if self.rbutton.get():
            self.RK4Set.append((t,y_3))
            self.plot.plot(t,y_3,color="#00F550",label="r(t)_RK45")
            
        if self.pbutton.get():
            self.RK4Set.append((t,y_4))
            self.plot.plot(t,y_4,color="#000CF5",label="p(t)_RK45")
        
        self.plot.legend(loc="upper right")
        self.imagenGrafica.draw()
        
        # llamo la funcion de la logica para el metodo y obtengo los valores de x y y a graficar
        
        # agregro los valores como una tupla en la variable que guarda las ejecuciones para los metodos de persistencia
        
        
        # grafico los puntos con el respectivo color asignado para el metodo, variable que se puede cambiar en el init


    def cerrarAplicacion(self):
        ''' Funcion que es llamada al hacer click en el boton cerrar, pregunta si realmente se desea cerrar o retornar a la aplicacion
        '''
        # creo la caja de mensaje y su valor
        MsgBox =  messagebox.askquestion ('Cerrar Aplicación','¿Está seguro que desea cerrar la aplicación?', icon = 'warning')
        # si el valor es yes entonces cierro la apliacion
        if MsgBox == 'yes':
            self.ventana.destroy()     
            self.ventana.quit()
        # en caso contrario se notifica el retorono a la aplicacion
        else:
            messagebox.showinfo('Retornar','Será retornado a la aplicación')
    
    def auxGuardar(self, directorio, extencion, listaDatos):
        ''' Metodo auxiliar que ayudara al guardado de archivos, es definido para evitar redundacia en codigo
        '''
         
        # genero un proceso iterativo para leer todas las lineas graficadas en el listado de datos el cual tiene en cada posicion un conjunto (X,Y)
        for i,val in enumerate(listaDatos):
            # obtengo el listado de datos de X 
            x_data = val[0]
            # obtengo el listado de datos deY
            y_data = val[1]
            # las empaqueto en formatodouble
            x_packed = st.pack('d'*len(x_data),*x_data)
            y_packed = st.pack('d'*len(y_data),*y_data)
            # creo el archivo con el nombre i.extencion para hacer la lectura despues de forma facil ejemplo 0.efor
            with open(directorio.joinpath(str(i)+extencion).absolute(),'wb') as f:
                # escribo los datos de X en el archivo
                f.write(x_packed)
                # escribo los datos de Y en el archivo
                f.write(y_packed)
                # Nota: el orden es importante ya que en la lectura se obtendra un set completo por lo que la primera mitad sera X y la segunda mitad sera Y

    def guardarDatos(self):
        ''' Funcion que abre un dialogo para ingresar el nombre de un archivo para guardar el resultado de una ejecucion de algoritmo en formato double
        '''
        ahora = time() # obtengo el timestamp actual
        fecha = dt.datetime.utcfromtimestamp(ahora).strftime("%Y-%m-%d_%H-%M-%S") # genero la fecha actual con el time stamp obtenido previamente
        nombreCarpetaDatos = 'Datos_' + fecha # contruyo el nombre de la carpeta donde se guardaran los archivos con el nombre Datos_Fecha
        # pido el directorio donde se creara la carpeta en la que se guardaran los datos
        directorioNombre = filedialog.askdirectory(parent = self.ventana,initialdir=self.directorioActual,title="Directorio de guardado de datos") 
        # si el directorio es vacio quiere decir que se cerro la ventana sin escojer por lo que la funcion no hara nada y se retorna
        if directorioNombre == '':
            return
        # si hay algo en el directorio se procede a crear una clase path con el parametro obtenido en el dialog para asi manejar de manera mas simple el path
        directorioDatos = Path(directorioNombre)
        # se crea el path a la carpeta nueva con el nombre previamente generaro y se manda el comando al sistema para que la cree como carpeta
        carpetaDatos = directorioDatos.joinpath(str(nombreCarpetaDatos))
        carpetaDatos.mkdir(parents=True, exist_ok=True)
        # llamo a la funcion auxiliar con el la carpeta donde se guardaran los datos, la extencion con la que se guardaran y el listado del que leera los datos a guardar
        self.auxGuardar(carpetaDatos,'.efor',self.eForSet)
        self.auxGuardar(carpetaDatos,'.eback',self.eBackSet)
        self.auxGuardar(carpetaDatos,'.emod',self.eModSet)
        self.auxGuardar(carpetaDatos,'.rk2',self.RK2Set)
        self.auxGuardar(carpetaDatos,'.rk4',self.RK4Set)
        self.auxGuardar(carpetaDatos,'.scipy',self.scipySet)
        
    def auxCargar(self, directorio, extencion, color_grafica):
        ''' Metodo auxiliar que ayudara a la carga de archivos, es definido para evitar redundacia en codigo
        retorna una lista con los valores leidos de X y Y de los archivos que encuentre en el path especificado con la extencion especificada
        '''
        # obtengo el nombre de todos los arvhicos con la extencion deseada
        ext = '*'+extencion
        files = [f.absolute() for f in directorio.glob(ext) if f.is_file()]
        tmpSet = [] # variable donde se guardaran los conjuntos
        # proceso iterativo que lee cada archivo
        for tmpF in files:
            with open(tmpF,'rb') as f:
                # leo el contenido del archivo
                data = f.read()
                # desempaqueto el contenido del arvhivo y lo convierto en lista para manipularlo
                unpacked = list(st.unpack('d'*(len(data)//8),data))
                # obtengo la mitad del tamaño para poder partir el array
                tam = len(unpacked)//2
                # genero los valores de X con la mitad de los datos y lo vuelvo un array de numpy
                t = np.array(unpacked[:tam])
                # genero los valores de Y con la segunda mitad de los datos y lo vuelvo un array de numpy
                V = np.array(unpacked[tam:])
                # grafico la linea con el color que debe ir
                self.plot.plot(t,V,color=color_grafica)
                # guardo los valore de X y Y en la lista temporal que se retornara al final de este metodo
                tmpSet.append((t,V))
        # retorno la lista resultante de la lectura de los archivos con la extencion
        return tmpSet


    def cargarDatos(self):
        ''' Funcion que abre un dialogo para seleccionar un archivo del cual se cargaran los datos de una ejecucion previa en formato double
        '''
        # pido el directorio donde se encuentran los datos previamente generados
        directorioNombre = filedialog.askdirectory(parent = self.ventana,initialdir=self.directorioActual,title="Directorio de datos generados")
        # si el directorio es vacio quiere decir que se cerro la ventana sin escojer por lo que la funcion no hara nada y se retorna
        if directorioNombre == '':
            return
        # si hay algo en el directorio se procede a crear una clase path con el parametro obtenido en el dialog para asi manejar de manera mas simple el path
        directorioDatos = Path(directorioNombre)
        # se llama a la funcion auxiliar que lee los archivos con la extencion y añade los datos a la grafica
        tmpSetEfor = self.auxCargar(directorioDatos,'.efor', self.color_efor)
        tmpSetEback = self.auxCargar(directorioDatos,'.eback', self.color_eback)
        tmpSetEmod = self.auxCargar(directorioDatos,'.emod', self.color_emod)
        tmpSetRK2 = self.auxCargar(directorioDatos,'.rk2', self.color_rk2)
        tmpSetRK4 = self.auxCargar(directorioDatos,'.rk4',self.color_rk4)
        tmpSetScipy = self.auxCargar(directorioDatos,'.scipy', self.color_scipy)
        # agrego los datos cargados a los existentes en las listas que almacenan estos para la persistencia
        self.eForSet+=tmpSetEfor
        self.eBackSet+=tmpSetEback
        self.eModSet+=tmpSetEmod
        self.RK2Set+=tmpSetRK2
        self.RK4Set+=tmpSetRK4
        self.scipySet+=tmpSetScipy
        # despues de todo lo anterior actualizo el grafico en la interfaz con el metodo draw definido para un canvas
        self.imagenGrafica.draw()


    def iniciar(self):
        ''' Metodo que inicia la interfaz con el main loop, este metodo se define por tener orden en toda la clase y no hacer accesos externos al parametro de ventana
        '''
        self.ventana.mainloop()




# proceso que inicia la ventana y carga el app proceso que solo se llamara si se ejecuta este archivo y no si se lo importa
if __name__ == '__main__':
    # configuracion inicaial de la ventana
    ventana =  Tk()                  # Definimos la ventana con nombre ventana porque es una ventana
    ventana.geometry('900x700')      # Tamaño de la ventana
    ventana.config(cursor="arrow")   # Cursor de flecha
    ventana.resizable(False, False)  # Hago que la ventana no sea ajustable en su tamaño
    app = Interfaz(ventana)          # Genero el objeto interfaz
    app.iniciar()                    # Main loop AKA EL LOOP
