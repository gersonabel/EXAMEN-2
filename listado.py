import psycopg2
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from tkinter import messagebox as mb
from tkinter import scrolledtext as st

class inicio:

    def __init__(self):
        self.abrir_nuevo()
        self.validar()

    def validar(self):

        if self.entrada1.get() == "gerson":
            Listado()
        else:
            mb.showwarning("error", "contraseña incorrecta")

    def abrir_nuevo(self):
        self.ventana = tk.Tk()
        self.ventana.title("VERIFICACIÓN")
        self.ventana.geometry("312x280")
        self.ventana.iconbitmap('unt.ico')

        self.imag4 = PhotoImage(file='fondoUNT.png')
        self.labelimg4 = ttk.Label(self.ventana, image=self.imag4)
        self.labelimg4.place(x=0, y=44)

        self.imag1 = PhotoImage(file='logo.png')
        self.labelimg1 = ttk.Label(self.ventana, image=self.imag1)
        self.labelimg1.place(x=45,y=10)

        self.e2 = tk.Label(self.ventana, text="usuario:", bg="#99CCFF")
        self.e2.place(x=58, y=80)

        self.entrada2 = tk.Entry(self.ventana,bg="#1A2E9C",fg="white")
        self.entrada2.place(x=86, y=120)

        self.e1 = tk.Label(self.ventana, text="contraseña: ", bg="#99CCFF")
        self.e1.place(x=58,y=150)

        self.entrada1 = tk.Entry(self.ventana,bg="#1A2E9C",show="*",fg="white")
        self.entrada1.place(x=86,y=190)

        self.boton = tk.Button(self.ventana, text="VERIFICAR", fg="blue", command=self.validar)
        self.boton.place(x=120,y=230)

        self.ventana.mainloop()

class Conexion_postgres:

    def conexion(self):  #establecemos la conexion que existe entre python y Postgres
        conexion = psycopg2.connect(database="sisalumnos",host="localhost",port="5432",user="postgres", password="gerson1548")
        return conexion

    def llenado(self, datos):      #Con las listas creadas esta funcion reparte a cada columna o fila correspondeiente
        cone=self.conexion()
        cursor=cone.cursor()
        sql="insert into sistema (alumno, dni) values (%s,%s)"
        cursor.execute(sql, datos)
        cone.commit()

    def consulta(self, datos):    #para recopilar los datos se usa la funcion ".fetchall()"
        cone=self.conexion()
        cursor=cone.cursor()
        sql="select alumno, dni from sistema where codigo=%s"
        cursor.execute(sql, datos)
        return cursor.fetchall()

    def recuperacion(self):   # la misma funcion anterior, pero en este caso con al primary key
        cone=self.conexion()
        cursor=cone.cursor()
        sql="select codigo, alumno, dni from sistema"
        cursor.execute(sql)
        return cursor.fetchall()

    def baja(self, datos):  #con la funcion .execute() estamos borrando componentes de las listas, sin embargo con .rowcunt(se borra las filas)
        cone=self.conexion()
        cursor=cone.cursor()
        sql="delete from sistema where codigo=%s"
        cursor.execute(sql, datos)
        cone.commit()
        return cursor.rowcount

    def cambios(self, datos):
        cone=self.conexion()
        cursor=cone.cursor()

        sql="update sistema set alumno=%s, dni=%s where codigo=%s"

        cursor.execute(sql, datos)
        cone.commit()
        return cursor.rowcount



class Listado(Conexion_postgres):

    def __init__(self):

        self.principal=Conexion_postgres()
        self.ventana1=tk.Toplevel()
        self.ventana1.geometry('510x320')
        self.ventana1.resizable(0, 0)   #con esto fijamos la ventana para no ser extendida
        self.ventana1.title("SISTEMA DE ALUMNOS")

        self.hoja1 = ttk.Notebook(self.ventana1)
        self.ventana1.iconbitmap('unt.ico')
        self.ventana1['bg'] = '#40D'  # para darle un toque pintoresco el color es en sistema hexadecimal

        self.llenar_lista()
        self.consultar_alumno()
        self.mostrar_lista()
        self.borrado()
        self.modificar()
        self.hoja1.grid(column=0, row=0, padx=25, pady=10)
        self.ventana1.mainloop()


    def llenar_lista(self):
        self.pagina1 = ttk.Frame(self.hoja1)
        self.hoja1.add(self.pagina1, text="creación")

        #se crea la primera venta con tkk.Frame()

        self.labelframe1=ttk.LabelFrame(self.pagina1,text="Inicio")
        self.labelframe1.pack(fill="both", expand="yes")
        self.labelframe1.grid(column=0, row=0, padx=90, pady=20)

        #una sub ventana que se crea con ttk.labelFrame()

        self.label1=ttk.Label(self.labelframe1, text="Alumno:")
        self.label1.grid(column=0, row=0, padx=4, pady=4)

        # los label son muestras de texto en pantalla

        self.alumno=tk.StringVar()
        self.entrydescripcion=ttk.Entry(self.labelframe1, textvariable=self.alumno)
        self.entrydescripcion.grid(column=1, row=0, padx=4, pady=4)

        #tk.StringVar() es para recolectar variables y entry para crear una entrada de texto

        self.label2=ttk.Label(self.labelframe1, text="DNI:")
        self.label2.grid(column=0, row=1, padx=4, pady=4)

        self.infoalum=tk.StringVar()
        self.g_Alumno=ttk.Entry(self.labelframe1, textvariable=self.infoalum)
        self.g_Alumno.grid(column=1, row=1, padx=4, pady=4)

        self.img = PhotoImage(file='check.png')
        self.boton1=ttk.Button(self.labelframe1,image=self.img,command=self.agregar)
        self.boton1.grid(column=1, row=2)

        # con una imagen redimensionada, con PhotoImage podemos crear una imagen y ponerla como icono de un boton

        self.imag = PhotoImage(file='logo.png')
        self.labelimg=ttk.Label(self.labelframe1,image=self.imag)
        self.labelimg.grid(column=1, row=3)

        # es una simple imagen para adornar un poco, es un label.


    def agregar(self):
        datos=(self.alumno.get(), self.infoalum.get())
        self.principal.llenado(datos)
        mb.showinfo("Información", "Alumno correctamente añadido")
        self.alumno.set("")
        self.infoalum.set("")


    def consultar_alumno(self):
        self.pagina2 = ttk.Frame(self.hoja1)
        self.hoja1.add(self.pagina2, text="Consulta")

        self.labelframe1=ttk.LabelFrame(self.pagina2, text="consultas por codigo",width=20, height=10)
        self.labelframe1.grid(column=0, row=0, padx=90, pady=20)

        self.label1=ttk.Label(self.labelframe1, text="Código:")
        self.label1.grid(column=0, row=0, padx=4, pady=4)

        self.codigo=tk.StringVar()
        self.meterDNI=ttk.Entry(self.labelframe1, textvariable=self.codigo)
        self.meterDNI.grid(column=1, row=0, padx=4, pady=4)

        self.label2=ttk.Label(self.labelframe1, text="Alumno:")
        self.label2.grid(column=0, row=1, padx=4, pady=4)

        self.descripcion=tk.StringVar()
        self.entrydescripcion=ttk.Entry(self.labelframe1, textvariable=self.descripcion, state="readonly")
        self.entrydescripcion.grid(column=1, row=1, padx=4, pady=4)

        self.label3=ttk.Label(self.labelframe1, text="DNI:")
        self.label3.grid(column=0, row=2, padx=4, pady=4)

        self.precio=tk.StringVar()
        self.g_Alumno=ttk.Entry(self.labelframe1, textvariable=self.precio, state="readonly")
        self.g_Alumno.grid(column=1, row=2, padx=4, pady=4)

        self.img2 = PhotoImage(file='lupa.png')
        self.boton1=ttk.Button(self.labelframe1, text="Consultar",image=self.img2, command=self.consultar)
        self.boton1.grid(column=1, row=3)

    def consultar(self):
        datos=(self.codigo.get(), )
        respuesta=self.principal.consulta(datos)
        if len(respuesta)>0:
            self.descripcion.set(respuesta[0][0])
            self.precio.set(respuesta[0][1])
        else:
            self.descripcion.set('')
            self.precio.set('')
            mb.showinfo("Información", "No existe un alumno con dicho código")

    def mostrar_lista(self):
        self.pagina3 = ttk.Frame(self.hoja1)
        self.hoja1.add(self.pagina3, text="Listado")

        self.labelframe1=ttk.LabelFrame(self.pagina3, text="lista completa",width=70, height=20)
        self.labelframe1.grid(column=0, row=0, padx=90, pady=20)

        self.boton1=ttk.Button(self.labelframe1, text="generar lista", command=self.listar)
        self.boton1.grid(column=0, row=0, padx=4, pady=4)

        self.scrolledtext1=st.ScrolledText(self.labelframe1, width=30, height=10)
        self.scrolledtext1.grid(column=0,row=1, padx=10, pady=10)

    def listar(self):

        respuesta=self.principal.recuperacion()
        self.scrolledtext1.delete("1.0", tk.END)

        for fila in respuesta:
            self.scrolledtext1.insert(tk.END, "código:"+str(fila[0])+
                                              "\nalumno:"+fila[1]+
                                              "\nDNI:"+str(fila[2])+"\n\n")

    def borrado(self):
        self.pagina4 = ttk.Frame(self.hoja1)
        self.hoja1.add(self.pagina4, text="Borrado")

        self.labelframe1=ttk.LabelFrame(self.pagina4, text="Artículo")
        self.labelframe1.grid(column=0, row=0, padx=90, pady=20)

        self.label1=ttk.Label(self.labelframe1, text="Código:")
        self.label1.grid(column=0, row=0, padx=4, pady=4)

        self.codigoborra=tk.StringVar()
        self.entryborra=ttk.Entry(self.labelframe1, textvariable=self.codigoborra)
        self.entryborra.grid(column=1, row=0, padx=4, pady=4)

        self.img3 = PhotoImage(file='tacho.png')
        self.boton1=ttk.Button(self.labelframe1, text="Borrar",image=self.img3, command=self.mensaje_borrar)
        self.boton1.grid(column=1, row=1 )

    def mensaje_borrar(self):
        datos=(self.codigoborra.get(), )
        cantidad=self.principal.baja(datos)
        if cantidad==1:
            mb.showinfo("Información", "Se borró el alumno con dicho código")
        else:
            mb.showinfo("Información", "No existe un alumno con dicho código")

    def modificar(self):
        self.pagina5 = ttk.Frame(self.hoja1)
        self.hoja1.add(self.pagina5, text="Modificar")

        self.labelframe1=ttk.LabelFrame(self.pagina5, text="Correcion de datos")
        self.labelframe1.grid(column=0, row=0, padx=90, pady=30)

        self.label1=ttk.Label(self.labelframe1, text="Código:")
        self.label1.grid(column=0, row=0, padx=4, pady=4)

        self.nuevoDNI=tk.StringVar()
        self.meterDNI=ttk.Entry(self.labelframe1, textvariable=self.nuevoDNI)
        self.meterDNI.grid(column=1, row=0, padx=4, pady=4)

        self.label2=ttk.Label(self.labelframe1, text="Alumno:")
        self.label2.grid(column=0, row=1, padx=4, pady=4)

        self.nuevoAlumno=tk.StringVar()
        self.entrydescripcion=ttk.Entry(self.labelframe1, textvariable=self.nuevoAlumno)
        self.entrydescripcion.grid(column=1, row=1, padx=4, pady=4)

        self.label3=ttk.Label(self.labelframe1, text="DNI:")
        self.label3.grid(column=0, row=2, padx=4, pady=4)

        self.modificado=tk.StringVar()
        self.g_Alumno=ttk.Entry(self.labelframe1, textvariable=self.modificado)
        self.g_Alumno.grid(column=1, row=2, padx=4, pady=4)

        self.boton1=ttk.Button(self.labelframe1, text="Consultar", command=self.nuevasconsultas)
        self.boton1.grid(column=1, row=3, padx=4, pady=4)

        self.label4 = ttk.Label(self.labelframe1, text="Y")
        self.label4.grid(column=1, row=4, padx=4, pady=4)

        self.boton1=ttk.Button(self.labelframe1, text="Modificar", command=self.modifica)
        self.boton1.grid(column=1, row=5, padx=4, pady=4)

    def modifica(self):
        datos=(self.nuevoAlumno.get(), self.modificado.get(), self.nuevoDNI.get())
        cantidad=self.principal.cambios(datos)

        if cantidad==1:
            mb.showinfo("Información", "Se modificó la informacion del alumno")
        else:
            mb.showinfo("Información", "No existe un alumno con ese código")

    def nuevasconsultas(self):
        datos=(self.nuevoDNI.get(), )
        respuesta=self.principal.consulta(datos)

        if len(respuesta)>0:
            self.nuevoAlumno.set(respuesta[0][0])
            self.modificado.set(respuesta[0][1])
        else:
            self.nuevoAlumno.set('')
            self.modificado.set('')
            mb.showinfo("Información", "No existe un alumno con ese código")

if __name__ == "__main__":
    inicio()