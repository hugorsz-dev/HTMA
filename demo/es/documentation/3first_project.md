# Primer proyecto en HTMA

## Estructura de directorios

Crea una carpeta de proyecto (`first_project`), ubícate dentro de ella y crea una nueva carpeta (`myweb`). 

``` 
mkdir first_project
cd first_project
mkdir myweb
```

Luego, copia el script `htma.py` dentro de la raíz del proyecto. 

Como resultado, el árbol de directorios debería de ser igual al siguiente:

```
first_project
├── myweb/
└── htma.py
```

> Es preciso mantener el script `htma.py` fuera de las carpetas que va a recorrer. 

## Editar las variables de input y target

Abre `htma.py` y modifica las dos variables siguientes:

- `input_path`: Ruta de la carpeta donde se encuentra el contenido de tu proyecto (`first_project/myweb`)
- `target_path`: Ruta de la carpeta donde se generará el directorio `target`  que contendrá el proyecto generado en formato HTML (p.ej, `first_project`)

Es recomendable que en ambas variables se introduzcan rutas absolutas. Si introduces rutas relativas, deberán apuntar respecto a la localización de `htma.py`.

Las variables habrían de ser: 

```
input_path ="/home/user/first_project/myweb"
target_path = "/home/user/first_project/"
```

> No utilices la misma ruta para `input_path` y `target_path`. 

## Crear contenido en markdown

En `myweb`, crea una carpeta `content`  (aunque servirá cualquier otro nombre) y guarda en ella algunos documentos markdown, en los que introducirás algún texto de ejemplo. 

Por ejemplo, `doc1.md`, `doc2.md` y `doc3.md`:

````
# Page Title

This is how you write *italic text*.
This is how you write **bold text**.
This is how you write [a link](https://google.com).
This is how you write `code`.

```
This is a block of code
```

> This is a quote

- This is a list.
- This is a list.

1. This is a numbered list.
2. This is a numbered list.
````

## Crear un archivo index.htma

En la raíz de tu proyecto, crea un archivo `index.htma`, en el que introducirás lo siguiente:

``` html
<html>
    <header>
        <title> My first page with HTMA </title>
    </header>

    <body>

        <p> This are the markdown documents in the <code> content </code> directory: </p> 

        <HTMA!>
            DIR:: content;
            REDIR:: MD;
            TEMPLATE:: {
                <li> <a href="$LINK_FOR_EACH_FILE_IN_DIR$"> $MD_H1[0]$</a> 
            };
            MD_TEMPLATE {
                <html>
                    <header>
                        <title> $MD_H1[0]$ </title>
                    </header>
                    
                    <body>
                        $MARKDOWN_TO_HTML$
                    </body>
                </html>
            }
        </HTMA>

    </body> 

</html>
```

Y ejecútalo desde el directorio raíz, usando `python htma.py`.

El resultado será semejante al siguiente:

```
├── myweb/
│   ├── content/
│   │   ├── doc1.md
│   │   ├── doc2.md
│   │   └── doc3.md
│   └── index.htma
├── target/
│   ├── content/
│   │   ├── doc1.html
│   │   ├── doc2.html
│   │   └── doc3.html
│   └── index.html
└── htma.py*
``` 


## Explicación del archivo index.htma

A partir de este ejercicio básico, resulta comprensible el funcionamiento de las etiquetas `<HTMA!>`. Gracias a estas, será posible referenciar un directorio (`DIR`) e insertar su contenido en la web usando plantillas (`TEMPLATE`, `MD_TEMPLATE`), que utilizarán variables (`$VARIABLE$`) para enlazar el contenido entre ambos documentos.

- **`DIR`**: Es el directorio donde se ubican los archivos redireccionados (en este caso, los markdowns).
- **`REDIR`**: Es la extensión del archivo a procesar (puesto que se trata de archivos markdown, su `REDIR` será `MD`).
- **`TEMPLATE`**: Es el formato que se sustituirá en el documento `index.html` generado. 
    - **`LINK_FOR_EACH_FILE_IN_DIR`**: Es la ruta de archivo para cada uno de los markdowns. 
    - **`MD_H1[0]`**: Es el array de encabezados de primer nivel recogidos en el markdown, donde se especifica el primer elemento del mismo `[0]`
- **`MD_TEMPLATE`**: Es el formato en el que se generará la conversión de `.md` a `.html`.
    **`MARKDOWN_TO_HTML`**: El archivo markdown se sustituirá por esta etiqueta, convertido a HTML

## Resultado

Ejecutado el script `htma.py`, el resultado deberá ser el siguiente:

``` html

<html>
<header>
  <title> Page Title </title>
</header>

<body>
  <h1>Page Title</h1>

  <p>This is how you write <em>italic text</em>.
    This is how you write <strong>bold text</strong>.
    This is how you write <a href="https://google.com">a link</a>.
    This is how you write <code>code</code>.</p>

  <pre><code>This is a block of code
</code></pre>

  <blockquote>
    <p>This is a quote</p>
  </blockquote>

  <ul>
    <li>This is a list.</li>
    <li>This is a list.</li>
  </ul>

  <ol>
    <li>This is a numbered list.</li>
    <li>This is a numbered list.</li>
  </ol>
</body>

</html>

```


