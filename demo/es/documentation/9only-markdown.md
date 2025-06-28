# Utilizar solamente markdown

## Incrustar markdown sin iteraciones 
En algunos casos, no cabe la necesidad de realizar iteraciones, porque solo existe un fichero markdown para incrustar directamente en el documento. 
La redirección `REDIR:: ONLY_MD` permite incrustar o referenciar un único archivo markdown, para facilitar la creación de documentos HTML sin la necesidad de usar las tediosas etiquetas nativas. 

## Ejemplo de uso

El atributo `DIR` no procederá, dado que no hay carpeta en la que iterar los archivos, y solo será necesario introducir en la variable `ONLY_MD` el contenido o ruta del markdown, y en `MD_TEMPLATE` el contenido formateado con las **variables especiales de MD**, 

```
<HTMA!>
    REDIR::ONLY_MD;;
    ONLY_MD:: {
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
    };;
    MD_TEMPLATE:: {
        $MARKDOWN_TO_HTML$
    };;

</HTMA>
```

El resultado de este bloque será:

```
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
 
```
