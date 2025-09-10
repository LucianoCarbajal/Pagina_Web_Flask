from flask import Flask, render_template, request,url_for,redirect,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config.from_pyfile('config.py')

from models import db
from models import Trabajador, registro_horario



@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/menu_empleado', methods=['GET','POST'])
def menu_empleado():
    return render_template('menu_empleado.html')

@app.route('/listar_dependencia', methods=['POST'])
def listar_dependencia():
    dependencia = request.form['dependecia']
    session['dependencia'] = dependencia
    return render_template(dependencia = dependencia)

@app.route('/registrar_entrada', methods=['GET', 'POST'])
def registrar_entrada():
    if request.method == 'POST':
        legajo = request.form['legajo']
        digdni = request.form['dni']
        dependencia = request.form['dependencia']

        # Validar que los campos no estén vacíos
        if not legajo or not digdni or not dependencia:
            return render_template('error.html', error='Por favor complete bien los campos.')

        # Buscar trabajador por legajo y que los últimos 4 dígitos del DNI coincidan
        trabajador = Trabajador.query.filter(Trabajador.legajo == int(legajo)).first()
        if trabajador and str(trabajador.dni)[-4:] == digdni:
            # Verificar si ya existe un registro de entrada para hoy
            hoy = datetime.now().date()
            registro_existente = registro_horario.query.filter(registro_horario.idtrabajador == trabajador.id,registro_horario.fecha == hoy).first()
            if registro_existente:
                return render_template('error.html', error='Ya se ha registrado una entrada para este trabajador hoy.')
            nueva_entrada = registro_horario(
                fecha = hoy,
                HoraEntrada = datetime.now().time().replace(microsecond=0),
                HoraSalida = None,
                dependencia = dependencia,
                idtrabajador = trabajador.id
            )#aca se crea un nuevo registro de entrada
            db.session.add(nueva_entrada)
            db.session.commit()#Esto guarda el registro de entrada en la base de datos
            return redirect(url_for('registro_exitoso'))
        else: 
            return render_template('error.html', error='No se encontró un trabajador con ese legajo y últimos 4 dígitos de DNI.')
    else:
        return render_template('registrar_entrada.html')

@app.route('/registrar_salida', methods=['GET', 'POST'])
def registrar_salida():
    if request.method == 'POST':
        legajo = request.form['legajo']
        digdni = request.form['dni']
        if not legajo or not digdni:
            #el render_template crea una vinculacion dinamica entre el html y python
            return render_template('error.html', error='Por favor complete bien los campos.')
        
        # Buscar trabajador por legajo y que los últimos 4 dígitos del DNI coincidan
        trabajador = Trabajador.query.filter(Trabajador.legajo == int(legajo)).first()
        if trabajador and str(trabajador.dni)[-4:] == digdni:
            # Verificar si ya existe un registro de entrada para hoy
            hoy = datetime.now().date()
            hora = datetime.now().time().replace(microsecond=0)
            registro_existente = registro_horario.query.filter(registro_horario.idtrabajador == trabajador.id,registro_horario.fecha == hoy).first()
            if not registro_existente:
                return render_template('error.html', error='No se ha registrado una entrada para este trabajador hoy.')

            registro_existente.HoraSalida = hora
            db.session.commit()
            return redirect(url_for('registro_salida_exitoso'))
        else: 
            return render_template('error.html', error='No se encontró un trabajador con ese legajo y últimos 4 dígitos de DNI.')
    else:
        return render_template('registrar_salida.html')

@app.route('/registro_exitoso', methods=['GET'])
def registro_exitoso():
    return render_template('registro_exitoso.html')

@app.route('/registro_salida_exitoso', methods=['GET'])
def registro_salida_exitoso():
    return render_template('registro_salida_exitoso.html')


@app.route('/menu_administrativo', methods=['GET','POST'])
def menu_administrativo():
    return render_template('menu_administrativo.html')

@app.route('/lista_registros', methods=['GET', 'POST'])
def lista_registros():
    if request.method == 'POST':
        legajo = request.form['legajo']
        digdni = request.form['dni']
        fechaInicio = request.form['fechaInicial']
        fechaFinal = request.form['fechaFinal']
        if not legajo or not digdni or not fechaInicio or not fechaFinal:
            return render_template('error.html', error='Ingrese bien los datos...')
        trabajador = Trabajador.query.filter(Trabajador.legajo == int(legajo)).first()
        if trabajador:
            fecha_inicio_obj = datetime.strptime(fechaInicio, "%Y-%m-%d").date()
            fecha_final_obj = datetime.strptime(fechaFinal, "%Y-%m-%d").date()
            registros = registro_horario.query.filter(
                registro_horario.idtrabajador == trabajador.id,
                registro_horario.fecha >= fecha_inicio_obj,
                registro_horario.fecha <= fecha_final_obj).order_by(registro_horario.fecha).all()
            return render_template('listar_registros.html', registros=registros, trabajador=trabajador)
        else:
            return render_template('error.html', error='No se encontraron datos asociados a ese empleado.')
    return render_template('consultar_registro.html')

@app.route('/informe_general', methods=['GET', 'POST'])
def informe_general():
    if request.method == 'POST':
        legajo = request.form.get('legajo')
        digdni = request.form.get('dni')
        trabajador = Trabajador.query.filter(Trabajador.legajo == int(legajo)).first()
        if not trabajador or str(trabajador.dni)[-4:] != digdni:
            return render_template('error2.html', error='Datos incorrectos o no es administrativo.')
        if trabajador.funcion != 'AD':
            return render_template('error2.html', error='El usuario no es administrativo.')
        # Si es correcto, mostrar el formulario de filtros
        return render_template('formulario_b_informe.html')
    else:
        return render_template('Ingrese_datos_informe.html')


@app.route('/listar', methods=['GET', 'POST'])
def listar():
    if request.method == 'POST':
        fechaInicio = request.form.get('fechaInicial')
        fechaFinal = request.form.get('fechaFinal')
        funcion = request.form.get('funcion')
        dependencia = request.form.get('dependencia')

        if not fechaInicio or not fechaFinal or not funcion or not dependencia:
            return render_template('error2.html', error='Ingrese bien los datos...')
        query = registro_horario.query.join(Trabajador).filter()

        # Solo filtra si no es "todas"
        if funcion != "todas":
            query = query.filter(Trabajador.funcion == funcion)
        if dependencia != "todas":
            query = query.filter(registro_horario.dependencia == dependencia)
        registros = query.order_by(Trabajador.apellido).all()

        resultados = []
        for xreg in registros:
            totalhoras = None
            if xreg.HoraEntrada and xreg.HoraSalida:
                #el combine une la fecha con la hora
                h1 = datetime.combine(xreg.fecha, xreg.HoraEntrada)
                h2 = datetime.combine(xreg.fecha, xreg.HoraSalida)
                totalhoras = h2 - h1
            apellido = xreg.trabajador.apellido
            nombre = xreg.trabajador.nombre
            fecha = xreg.fecha
            Hentrada = xreg.HoraEntrada
            Hsalida = xreg.HoraSalida
            # cargamos los datos en la lista de resultados
            resultados.append({
                "apellido": apellido,
                "nombre": nombre,
                "fecha": fecha,
                "entrada": Hentrada,
                "salida": Hsalida,
                "horas": totalhoras
            })
        return render_template('listar.html', registros=resultados)
    else:
        return render_template('formulario_b_informe.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)