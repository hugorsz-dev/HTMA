# Los parámetros `ORDER_BY` y `REDIR_LIMIT`

Las iteraciones de los archivos pueden ordenarse según varios criterios, si se introduce el parámetro `ORDER_BY` dentro del bloque HTMA.

Además, también pueden limitarse los bucles a un número de archivos límite, usando `REDIR_LIMIT`.

Ambos parámetros pueden usarse al mismo tiempo para, por ejemplo, solo mostrar _los ultimos cinco artículos publicados_. 

## Ejemplo de uso

En este ejemplo, los archivos de imagen del anterior apartado se organizarán en base a la fecha en que fueron creados. Y en vez de ser tres, solo mostraremos los dos más recientes.

```
<HTMA!>
    DIR:: myweb/content;
    REDIR:: png, jpg, gif;
    ORDER_BY:: DATE
    REDIR_LIMIT::2
    TEMPLATE:: {
        <h2> $FILE_NAME_FOR_EACH_FILE_IN_DIR$ </h2>
        <img src="$LINK_FOR_EACH_FILE_IN_DIR$">
        <p> <em> $CREATION_TIME_FOR_EACH_FILE_IN_DIR$ </em> </p>
    };
</HTMA>
```

> Recuerda que puedes usar `REDIR_LIMIT`y `ORDER_BY` independientemente.

## Criterios de ordenación

### `ALPHABETICAL`

Los archivos se organizarán en orden alfabético, con relación a su nombre original. 

### `ALPHABETICAL_REVERSE`

Los archivos se organizarán en un orden inverso al alfabético, con relación a su nombre original. 

### `DATE`

Los archivos se organizarán en base a la fecha en que fueron creados. 

### `DATE_REVERSE`

Los archivos se organizarán inversamente en base a la fecha en que fueron creados. 

### `SYSTEM`

Es el comportamiento por defecto, ordena los ficheros de la misma forma en que el sistema operativo los muestra. 