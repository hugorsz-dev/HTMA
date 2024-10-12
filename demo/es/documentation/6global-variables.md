# Variables globales

## ¿Qué es una "variable global"?

Las _variables globales_ son un conjunto de valores comunes a todos los formatos de archivo. En los ejemplos anteriores, se ha usado la variable `$LINK_FOR_EACH_FILE_IN_DIR$`: se trata de una variable global, porque se puede usar en todos los casos, independientemente del tipo de `REDIR`.

## Variables globales

### **`LINK_FOR_EACH_FILE_IN_DIR`**
Para cada archivo iterado, retorna su enlace directo.

### **`LAST_MODIFICATION_TIME_FOR_EACH_FILE_IN_DIR`**
Para cada archivo iterado, retorna la fecha de su última modificación.

### **`CREATION_TIME_FOR_EACH_FILE_IN_DIR`**
Para cada archivo iterado, retorna la fecha de su creación.

### **`FILE_NAME_FOR_EACH_FILE_IN_DIR`**
Para cada archivo iterado, retorna el nombre de archivo.

### **`DATE_OF_TODAY`**
Devuelve la fecha en el momento en que se ejecutó el script.


