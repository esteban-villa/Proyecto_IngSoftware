from importlib.metadata import requires
from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_mysqldb import MySQL
from flask_login import LoginManager ,login_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect
#from werkzeug.security import check_password_hash, generate_password_hash
from config import config

# MODELS
from models.ModelUser import ModelUser

#  ENTITIES
from models.entities.User import User

##### REGISTRO DE USUARIO ######
from python.registro_usu import registro_usu_proceso, actualizar_datos_proceso

##### CONDICIONES DE SALUD ######
from python.condicion_salud import condicion_salud_proceso, eliminar_cond_proceso, agregar_condicion_proceso, editar_condicion_proceso, actualizar_condicion_proceso


###### EXAMENES ###########
from python.examenes import cargar_examenes, guardar_examen_proceso, eliminar_examen_proceso
app = Flask(__name__)
csrf = CSRFProtect()

db = MySQL(app)
login_manager_app = LoginManager(app)
@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

id_global=""

###### RUTA LOGIN #######
@app.route('/')
def Rutalogin():
    return render_template('plantillas/login.html')

###### RUTA REGISTRO #######
@app.route('/registro')
def registro():
    return render_template('plantillas/registro_usu.html')

####### LOGOUT ########
@app.route('/logout')
def logout():
    logout_user()
    return render_template('plantillas/login.html')

##### REGISTRO DE USUARIO ######
@app.route('/registro_usu', methods=['GET','POST'])
def registro_usu():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    correo = request.form['correo']
    edad = request.form['edad'] 
    genero = request.form['genero']
    img = request.files['img']
    contraseña1 = request.form['contraseña1']
    contraseña2 = request.form['contraseña2']
    
    salida = registro_usu_proceso(db, nombre, apellido, correo, edad, genero, img, contraseña1, contraseña2)
    
    flash (salida)
    return redirect("/registro") 

####### INICIO SESIÓN ########
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = User(0,1,2, request.form['correo'],5,6,7, request.form['password'])
        logged_user = ModelUser.login(db,user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                
                global id_global
                id_global = logged_user.id                  
                
                return redirect(url_for('index'))
            else:
                flash("password incorrecta")
                return render_template('plantillas/login.html')
        else:
            flash("el usuario no existe")
            return render_template('plantillas/login.html')
    else:
        return render_template('plantillas/login.html')


########################################################


########### RUTA DE DATOS DE USUARIO O POR DEFECTO DEL LOGIN #########
#@app.before_request
@app.route('/index')
def index():
    return render_template('plantillas/index.html')


############ RUTA PARA EDITAR PERFIL DE USUARIO ##############
@app.route('/editar_usu')
def editar_usu():
    return render_template('plantillas/editar_usu.html')

################ FUNCION PARA EDITAR EL PERFIL DE USUARIO ###################
@app.route('/actualizar_datos', methods=['POST'])
def actualizar_datos():
    
    nombre = request.form['nombre']
    apellidos = request.form['apellidos']
    correo = request.form['correo']
    edad = request.form['edad']
    genero = request.form['genero']
    img = request.files['img']
    contraseña1 = request.form['contraseña1']
    contraseña2 = request.form['contraseña2']
        
    print(nombre, apellidos, correo, edad, genero, img, contraseña1, contraseña2)
    
    funcion = actualizar_datos_proceso(db, id_global, nombre, apellidos, correo, edad, genero, img, contraseña1, contraseña2)
    flash(funcion)
    return redirect("/editar_usu")
    
################# RUTA DE CONDICIONES DE SALUD #################    
@app.route("/condicion_salud")
def condicion_salud():
    salida = condicion_salud_proceso(db,id_global)
    print(salida) 
    return render_template('plantillas/condiciones_salud.html', salida=salida)

################### ELIMINAR ALGUNA CONDICION DE SALUD #######################
@app.route('/eliminar_cond/<int:id>')
def eliminar_cond(id):
    eliminar_cond_proceso(db,id)
    return redirect("/condicion_salud")


################ RUTA PARA EDITAR UNA CONDICION DE SALUD ################
@app.route('/agregar_condicion')
def agregar_condicion():
    return render_template('plantillas/agregar_cond_salud.html')

################ GUARDAR NUEVAS CONDICIONES DE SALUD ################
@app.route('/guardar_condicion', methods=['POST'])
def guardar_condicion():
    enfermedad = request.form['enfermedad']
    texto = request.form['texto']
    funcion = agregar_condicion_proceso(db, id_global, enfermedad, texto)
    flash(funcion)
    return redirect('/agregar_condicion')

#################### RUTA PARA EDITAR UNA CONDICION DE SALUD ##########################
@app.route('/editar_condicion/<int:id>')
def editar_condicion(id):
    funcion = editar_condicion_proceso(db, id)
    
    print(funcion)
    return render_template('plantillas/editar_condicion.html', funcion=funcion)

######################## GUARDAR ACTULIZACIONES DE CONDICIONES DE SALUD #######################
@app.route('/actualizar_condicion', methods=['POST'])
def actualizar_condicion():
    id = request.form['id']
    enfermedad = request.form['enfermedad']
    texto = request.form['texto']
    
    funcion = actualizar_condicion_proceso(db, id, enfermedad, texto)
    
    flash(funcion)
    return redirect("/condicion_salud")

################# RUTA POR DEFECTO PARA EXAMENES ####################
@app.route('/examenes')
def examenes():
    funcion = cargar_examenes(db, id_global)
    return render_template('plantillas/examenes.html', funcion=funcion)

############# AGREGAR EXAMENES #################
@app.route('/agregar_examen')
def agregar_examen():
    return render_template('plantillas/agregar_examen.html')

############ GUARDAR NUEVOS EXAMENES ##############
@app.route('/guardar_examen', methods=['POST'])
def guardar_examen():
    documento = request.files['documento']
    texto = request.form['texto']
    
    funcion = guardar_examen_proceso(db,id_global, documento, texto)
    flash(funcion)
    return redirect('agregar_examen')

################# ELIMINAR UN EXAMEN ######################
@app.route('/eliminar_examen/<int:id>')
def eliminar_examen(id):
    print(id)
    funcion = eliminar_examen_proceso(db,id)
    
    flash(funcion)
    return redirect("/examenes")



#################### ERROR 404 Y 401 ##########################
def error_401(error):
    return redirect(url_for('index'))

def error_404(error):
    return render_template('plantillas/404.html'), 404

if __name__== '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, error_401)
    app.register_error_handler(404, error_404)
    app.run()