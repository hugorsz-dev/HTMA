
# Redirecciones de markdown

## ¿Qué es una "variable especial"?

Como se ha visto en el [tema previo](3first_project.md), el campo `REDIR` predispone a la lectura de una extensión: Si es `MD`, solo leerá los archivos `.md` del directorio al que apunta el campo `DIR`.  

Pero el campo `REDIR` entraña una importancia radical en la interpretación del `TEMPLATE`, en el uso de las denominadas **variables especiales**. Las **variables especiales** son aquellas variables (`$VARIABLE$`) asociadas a una extensión en específico.

Por ejemplo, para `REDIR: MD`, el script tendrá acceso a la variable especial `MARKDOWN_TO_HTML`.

## Las variables especiales de `REDIR:MD`

Anteriormente, también se ejemplificó un empleo sencillo de la etiqueta `<HTMA!>` junto con `REDIR: MD`, orientado a las redirecciones de archivos markdown. 

**No se trataba un ejemplo sencillo**, sino que, en realidad, comprende toda la sintaxis que existe en `HTMA`, y sus posibilidades con respecto a las redirecciones de archivos markdown. Entenderlo implica tener presente la totalidad de las funciones que esta herramienta propone para presentar documentos markdown convertidos a formato HTML.

Sobre este punto, solo será preciso aprender cuales son las *variables especiales* para este tipo de `REDIR`.

### `MARKDOWN_TO_HTML`

Esta variable introducirá el archivo `.md` iterado, pero en formato HTML. La página previa presenta su sencillo funcionamiento,

### **`MD_H1...MD_H6`**

Los encabezados del markdown se referencian usando la variable `MD_Hn[i]`. 

Por ejemplo, para mostrar el séptimo encabezado de tercer nivel que aparece en un documento, habría de llamarse a `MD_H3[6]`.

Especialmente los encabezados tienen la capacidad de iterarse, como se vio en el ejemplo de la página anterior, mediante la etiqueta `MD_Hn`

### **`MD_IMG`**

Las imágenes del markdown se referencian usando la variable `MD_IMG[i]`. 

Esta arrojará el enlace absoluto de la imagen en cuestión o, si se tratase de una página externa, su enlace correspondiente. 

### **`MD_URL`**

Los enlaces del markdown se referencian usando la variable `MD_URL[i]`. 

Esta arrojará el enlace absoluto del enlace en cuestión o, si se tratase de una página externa, su enlace correspondiente. 

### **`MD_QUOTE`**

Las citas del markdown se referencian usando la variable `MD_QUOTE[i]`. 

### **`MD_TEXT`**

El resto del texto del markdown que no es depositado en las variables anteriores - párrafos -, se introduce en `MD_TEXT[i]`

## `MD_TEMPLATE` en archivos separados

Al tratarse de una plantilla, el contenido de `MD_TEMPLATE` quizás deba ser el mismo en varias ocasiones. 

``` html
<html>
    <header>
        <title> $MD_H1[0]$ </title>
    </header>
    
    <body>
        $MARKDOWN_TO_HTML$
    </body>
</html>
```

Para evitar repetir el contenido de una misma plantilla, es recomendable guardar `MD_TEMPLATE` en un archivo con la extensión `.htma.template`, como por ejemplo, `example.md.template`, y referenciar el archivo en su lugar.

```
MD_TEMPLATE: {path/to/example.md.template}
```

