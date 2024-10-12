# Redirecciones entre plantillas

Hasta este punto, la documentación solo ha abordado el uso de `REDIR: MD`. Sin embargo, no podemos hacer una página web compleja usando un unico nodo entre archivos HTMA y markdown: si es necesario disponer más de una página, será necesario contar con las herramientas para interconectar varios documentos HTMA entre sí. 

**`REDIR:HTMA`** permite iterar como en los ejemplos anteriores, pero sobre ficheros HTMA en lugar de markdown. 

## Crear contenido en HTMA

En el proyecto `first_project`, dentro de la carpeta `content`, crearemos tres documentos, `htmadoc1.htma`, `htmadoc2.htma` y `htmadoc3.htma`. La estructura de carpetas será la siguiente:

```
└── myweb/
    ├── content/
    │   ├── doc1.md
    │   ├── doc2.md
    │   ├── doc3.md
    │   ├── htmadoc1.htma
    │   ├── htmadoc2.htma
    │   └── htmadoc3.htma
    └── index.htma
```

Dentro de los los ficheros `htma`, podemos introducir algún documento HTML sencillo. Y aunque pudieran emplearse iteraciones, este caso el ejemplo no las contendrá para que el ejemplo sea más fácilmente comprensible.

``` html
<html>
   <head>
      <title> 
         First sample HTMA document
      </title>
   </head>
   <body>
      <header>
         <h2 id='title'> This is the first sample HTMA document </h1>
         <p id="description"> This is a description  <p>
         <img id="image" src="https://upload.wikimedia.org/wikipedia/commons/0/0e/Urgub_-_Texier_Charles_F%C3%A9lix_Marie_-_1882.jpg"> 
         <a id="url" href="http://google.es"> Link </a>
      </header>
</html>
```

## Editar el archivo `index.htma`

Y en el fichero `index.htma`, será necesario añadir el siguiente fragmento de código: 

```html
<HTMA!>
    DIR:: myweb/content;
    REDIR:: HTMA;
    TEMPLATE:: {
        <a href="$url$"> Link </a>
        <img src="$image$">
        <li> <a href="$LINK_FOR_EACH_FILE_IN_DIR$"> $title$  </a> 
        <p> $description$ </p>
    };
</HTMA>
```
## Explicación del archivo `index.htma`

- **`DIR`**: Como ya se ha visto, este campo recoge todos los archivos de un determinado directorio.
- **`REDIR`**: Ahora, la extensión recogida del directorio será `.htma`.

## Variables especiales

Las variables especiales para `REDIR:HTMA` corresponden a las que el usuario referencie en los atributos `id` del documento de origen. Por ejemplo, `id=description` en una etiqueta HTML significará que automaticamente se creará una variable `$description$` referenciable en el HTMA. 

Si la `id` se señala en etiquetas que usan el campo `src` o `href`, no se capturará el contenido entre etiquetas, sino el enlace. 

## Resultado

Ejecutado el script `htma.py`, el resultado deberá ser el siguiente:

```html
<html>
    <header>
        <title>My first page with HTMA</title>
    </header>
    <body>
        <p>This are the markdown documents in the <code> content </code> directory:</p>
        <li><a href="/home/user/first_project/target/content/doc1.html"> Page Title</a></li>
        <li><a href="/home/user/first_project/target/content/doc2.html"> Page Title</a></li>
        <li>
            <a href="/home/user/first_project/target/content/doc3.html"> Page Title</a>
            <p>This are the HTMA documents in the <code> content </code> directory:</p>
            <a href="Link"> Link </a> <img src="https://upload.wikimedia.org/wikipedia/commons/0/0e/Urgub_-_Texier_Charles_F%C3%A9lix_Marie_-_1882.jpg" />
        </li>

        <li>
            <a href="/home/user/first_project/target/content/htmadoc1.html"> This is the first sample HTMA document </a>
            <p>This is a description</p>
            <a href="Link"> Link </a> <img src="https://upload.wikimedia.org/wikipedia/commons/0/0e/Urgub_-_Texier_Charles_F%C3%A9lix_Marie_-_1882.jpg" />
        </li>

        <li>
            <a href="/home/user/first_project/target/content/htmadoc2.html"> This is the second sample HTMA document </a>
            <p>This is a description</p>
            <a href="Link"> Link </a> <img src="https://upload.wikimedia.org/wikipedia/commons/0/0e/Urgub_-_Texier_Charles_F%C3%A9lix_Marie_-_1882.jpg" />
        </li>

        <li>
            <a href="/home/user/first_project/target/content/htmadoc3.html"> This is the third sample HTMA document </a>
            <p>This is a description</p>
        </li>
    </body>
</html>
``` 


