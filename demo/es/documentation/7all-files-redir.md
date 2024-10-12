#  Redirecciones de todo tipo de archivos

Por ahora, solo se han expuesto casos de uso en que se redirigían extensiones `.htma` y `.md`. Cuando, por ejemplo, sea necesario listar archivos alternativos, como `.mp3` o `.pdf`, debe examinarse el `REDIR: extension`. 

A diferencia de `REDIR:MD` y `REDIR:HTMA`, carece de _variables especiales_. Solo podrán usarse las _variables globales_.

## Insertar contenido en cualquier formato

En el proyecto `first_project`, dentro de la carpeta `content`, introduciremos tres imágenes, `img1.gif`, `img2.png` y `img3.jpg`. La estructura de carpetas será la siguiente:

```
myweb/
├── content/
│   ├── doc1.md
│   ├── doc2.md
│   ├── doc3.md
│   ├── htmadoc1.htma
│   ├── htmadoc2.htma
│   ├── htmadoc3.htma
│   ├── img1.gif
│   ├── img2.jpg
│   └── img3.png
└── index.htma
```

## Editar `index.htma`

Y en el fichero `index.htma`, introduciremos un bucle con un `REDIR` que recoja las extensiones de los archivos previos.

```
<HTMA!>
    DIR:: myweb/content;
    REDIR:: png, jpg, gif;
    TEMPLATE:: {
        <h2> $FILE_NAME_FOR_EACH_FILE_IN_DIR$ </h2>
        <img src="$LINK_FOR_EACH_FILE_IN_DIR$">
        <p> <em> $CREATION_TIME_FOR_EACH_FILE_IN_DIR$ </em> </p>
    };
</HTMA>
```

## Resultado

Ejecutado el script `htma.py`, el resultado deberá ser el siguiente:

```
<h2> img2 </h2>
<img src="/home/user/first_project/target/content/img2.jpg">
<p> <em> 2024-10-12 </em> </p>
<h2> img1 </h2>
<img src="/home/user/first_project/target/content/img1.gif">
<p> <em> 2024-10-12 </em> </p>
<h2> img3 </h2>
<img src="/home/user/first_project/target/content/img3.png">
<p> <em> 2024-10-12 </em> </p>
``` 
