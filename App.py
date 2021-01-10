from flask import Flask, render_template,request,redirect,url_for,flash # retornar los templates
# redirect url_for para direccionar a la url 
from flask_mysqldb import MySQL

app=Flask(__name__) # 


# conexion a la BD
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='123456'
app.config['MYSQL_DB']='notas_flask'
mysql= MySQL(app)

# sesion 
app.secret_key= 'mysecretkey123'

# rutas 
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM categoria')
    data = cur.fetchall()
    cur.close()
    cur1 = mysql.connection.cursor()
    cur1.execute('SELECT \
                  notas.idnota,\
                  notas.titulo_nota,\
                  categoria.nombre_categoria, \
                  notas.url_nota,\
                  notas.comentario  \
                  from notas       \
                  inner join categoria on notas.idcategoria = categoria.idcategoria\
                  ORDER BY notas.idnota DESC LIMIT 2 ')
    data1 = cur1.fetchall()
    cur1.close()
    #print(data)
    return render_template('index.html', notas = data1 ,categorias=data) # solo se da el nombre de tu archivo 

@app.route('/listanotas')
def Lista_notas():
    cur1 = mysql.connection.cursor()
    cur1.execute('SELECT \
                  notas.idnota,\
                  notas.titulo_nota,\
                  categoria.nombre_categoria, \
                  notas.url_nota,\
                  notas.comentario  \
                  from notas       \
                  inner join categoria on notas.idcategoria = categoria.idcategoria')
    data1 = cur1.fetchall()
    cur1.close()
    #print(data)
    return render_template('ListaNotas.html', notas = data1) # solo se da el nombre de tu arch

@app.route('/add_nota',methods=['POST'])
def add_nota():
    if request.method == 'POST':
        titulo =request.form['titulo'] # almacenando el dato
        idcategoria =request.form['idcategoria'] 
        url = request.form['url']
        comentario =request.form['comentario']
        cur = mysql.connection.cursor()
        cur.execute(' INSERT INTO notas (titulo_nota,idcategoria,url_nota,comentario) VALUES (%s,%s,%s,%s)' , (titulo,idcategoria,url,comentario))
        mysql.connection.commit() # se ejecuta el script 
        flash('Nota agregado sastifactoriamente')
        return redirect(url_for('Index'))
      

@app.route('/edit_nota/<id>', methods = ['POST', 'GET'])
def get_nota(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM notas WHERE idnota = %s',[id])
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-nota.html', nota= data[0])
 
@app.route('/update/<id>' ,methods=['POST'])
def nota_update(id):
    if request.method == 'POST':
        titulo = request.form['titulo']
        url= request.form['url']
        comentario = request.form['comentario']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE notas
            SET titulo_nota = %s,
                url_nota = %s,
                comentario = %s
            WHERE idnota = %s
        """, (titulo, url, comentario, id))
        flash('Nota actualizada sastifactoriamente')
        mysql.connection.commit()
        return redirect(url_for('Index'))


@app.route('/delete/<string:id>')
def delete_nota(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM notas WHERE idnota = {0}'.format(id))
    mysql.connection.commit()
    flash('Nota Eliminada Sastifactoriamente')
    return redirect(url_for('Index'))


@app.route('/categoria')
def Categoria():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM categoria')
    data = cur.fetchall()
    cur.close()
    return render_template('categoria.html',categorias=data) # solo se da el nombre de tu archivo 


@app.route('/add_categoria',methods=['POST'])
def add_categoria():
    if request.method == 'POST':
        nombrecategoria =request.form['nombrecategoria'] #
        descripcioncategoria =request.form['descripcioncategoria'] # almacenando el dato
        cur = mysql.connection.cursor()
        cur.execute(' INSERT INTO categoria (nombre_categoria,descripcion) VALUES (%s,%s)' , (nombrecategoria,descripcioncategoria))
        mysql.connection.commit() # se ejecuta el script 
        flash('Categoria agregado sastifactoriamente')
        return redirect(url_for('Categoria'))

@app.route('/edit_categoria/<id>',  methods = ['POST', 'GET']) # pasando los datos 
def edit_categoria(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM categoria WHERE idcategoria = %s',(id))
    data = cur.fetchall()
    print(data)
    return render_template('edit-categoria.html', categoria = data[0])  

@app.route('/update_categoria/<id>' ,methods=['POST'])
def categoria_update(id):
    if request.method == 'POST':
        nombrecategoria =request.form['nombrecategoria'] #
        descripcioncategoria =request.form['descripcioncategoria'] # almacenando el dato
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE categoria
            SET nombre_categoria = %s,
                descripcion = %s
            WHERE idcategoria = %s
        """, (nombrecategoria,descripcioncategoria,id))
        flash('Categoria actualizada sastifactoriamente')
        mysql.connection.commit()
        return redirect(url_for('Categoria'))

@app.route('/delete_categoria/<string:id>')
def delete_categoria(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM categoria WHERE idcategoria = {0}'.format(id))
    mysql.connection.commit()
    flash('Categoria Eliminada Sastifactoriamente')
    return redirect(url_for('Categoria'))

# cada vez que se hace cambio se reinicia el servidor
if __name__ == '__main__':
    app.run(port=3000,debug=True)