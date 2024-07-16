
# "HTML Template to Markdown Automator"
# HTMA

import os
import re 
import markdown

input_path= "/home/hugo/eclipse-workspace/programacionPyton/autoweb/web_prueba"
output_path= "/home/hugo/eclipse-workspace/programacionPyton/autoweb/salida_prueba"

"""
El objetivo de la clase wblock es devolver los bloques HTMA correctamente formateados en formato
de String
"""

class WBlock ():
    
    """
    Constructor 
    -   Recibe el string (fragmento de código HTMA) y convierte sus variables en un diccionario, para ser manipuladas en los métodos
    """

    def __init__ (self, block):
        self.block = block
        self.attributes = self.block_string_to_attributes (block)
        
    # MÉTODOS

    """
    Bloque en string convertido en atributos. 
    -   Convierte el bloque a un diccionario de python (clave, valor).
    """
        
    def block_string_to_attributes (self,block): 

        attributes = {}   

        block = block.split (";")

        clean_block ="" 
        
        for trace in block:
            try: 
                if "FORMAT" in trace: 
                    trace = trace.split("{")[0].replace(" ", "")+ trace.split("{")[1].strip().replace("}", " ").strip() 
                else: 
                    trace = trace.split(":")[0].replace(" ", "")+":"+ trace.split(":")[1].strip()
            except:
                pass # Omitir registros basura
                
            clean_block = clean_block + trace +";"

                
        block = clean_block.replace("[-HTMA=", "").replace("END-]", "").split(";") 
        block =  [trace for trace in block if trace.strip()]

        for trace in block: 
            try:
                key = trace.split (":")[0]
                value= trace.split (":")[1]
                attributes[key]=value; 
            except: 
                raise Exception ("Formatting error at attribute at:", key, value)
            
        return attributes; 

    """
    Dar formato a las htm id
    -   Reemplaza las ids de un formato de archivo HTMA o HTML (atributo format, p.ej: "$HTMA_TITLE$") por las etiquetas identificadas 
        en el fichero HTML introducido por parámetro.
    - Ejemplo de uso: 
        -   Fichero articulos.htma: 
                <html> <head> <title> Funcionamiento teórico de auto-web </title> </head> <body> <header> <h1 id='HTMA_TITLE'	> Sitio web de funcionamiento teorico </h1> <img id="HTMA_IMAGE" src="http://maricones.com"> <h2 id="HTMA_DESCRIPTION"> Esto es un subtítuloa </h2> </header></html> 
        -   Código:
                block = WBlock('DIR: $ROOT$; REDIR: HTMA; FORMAT: { <a href="$DIR_LINKS$"> <h3> $HTMA_TITLE$ </h3> <p> $HTMA_DESCRIPTION$ </p> </a> }')
                print (input_path+"/articulos/articulos.htma")
                block.set_format_htm_ids(input_path+"/articulos/articulos.htma")
                print (block.attributes)
        -   Salida:
                {'DIR': '/home/hugo/eclipse-workspace/programacionPyton/autoweb/web_prueba', 'REDIR': 'HTMA', 'FORMAT': '<a href="articulos.html"> <h3> Sitio web de funcionamiento teorico </h3> <p> Esto es un subtítuloa </p> </a>'}
    
    Será necesario que para cada bloque se conozca exactamente el fichero al que hace referencia.
    El uso de este método modificará el atributo FORMAT, por lo que es fundamental 
    
    """
    
    def set_format_htm_ids (self, path):  
        
        def obtain_name_from_path(path):
            head, tail = os.path.split(path)
            return tail or os.path.basename(head)

        """
        IDs de HTML o HTMA
        -   Retorna un diccionario (clave, valor) con cada una de las etiquetas indicadas en un fichero HTMA
        """
    
        def htm_ids (htm_path): 
            output = {}
            with open(htm_path, "r",  encoding="utf-8") as file:
                htm = file.read().split(">")
                    
            for i in range(len(htm)):
                if 'id="' in htm[i] or "id='" in htm[i]:
                    matches = re.findall(r'id=("[^"]+"|\'[^\']+\')', htm[i])
                    htma_id = matches[0]
                    if 'src="' in htm[i] or "src='" in (htm[i]):
                        matches = re.findall(r'src=("[^"]+"|\'[^\']+\')', htm[i])
                        output[htma_id.replace("'", "").replace('"', "")] = matches[0].replace("'", "").replace('"', "")
                    else:
                        output[htma_id.replace("'", "").replace('"', "")] =  htm[i+1].split("<")[0].strip()
            return output

        output = self.attributes["FORMAT"]
        
        # Recorrer el archivo htma para conseguir sus etiquetas
        
        for label in htm_ids(path):
            output = output.replace("$"+label+"$", htm_ids(path)[label]) 
        output = output.replace ("$LINK_FOR_EACH_FILE_IN_DIR$", obtain_name_from_path(path).replace("htma", "html"))
        self.attributes["FORMAT"] = output
     
    """
    Listar archivos del directorio
    -   Lista los archivos que encuentra en la ruta del atributo "DIR"
    -   Admite rutas relativas desde el punto en que se ejecuta el script. 
    """    
    def list_directory_files (self):
        output = []
        try:
            self.attributes["DIR"] 
        except:
            raise Exception ("Directory label is missing in the block")

        for path in os.listdir(self.attributes["DIR"]):
            if os.path.isfile(os.path.join(self.attributes["DIR"], path)):
                output.append(path)  
        return output 
        
    
block = WBlock('DIR: web_prueba; REDIR: HTMA; FORMAT: { <a href="$LINK_FOR_EACH_FILE_IN_DIR$"> <h3> $HTMA_TITLE$ </h3> <p> $HTMA_DESCRIPTION$ </p> </a> }')
block.set_format_htm_ids(input_path+"/articulos.htma")
print (block.attributes)

class CGenerator ():
    """
    TODO - Antes necesario terminar el list_directory_files
    Generar código
    -   Método del objeto "bloque" que retorna su código HTML generado. 
    """
    
    def generate_code (self):
        output =""
        if self.attributes["REDIR"] == "HTMA": 
            files_to_redir = [link for link in self.list_directory_files() if ".htma" in link ] 
            for link in files_to_redir:
                print (link)

        elif self.attributes["REDIR"] == "MD": 
            pass
        elif self.attributes["REDIR"] == "OTHER": 
            pass


print (block.generate_code())

"""
[HTMA=
    DIR: .;
    REDIR: HTMA; # iteración con todos los ficheros .htma
    FORMAT: {
        <a href="$FOR_EACH_FILE_IN_DIR$"> # para cada fichero htma
            <h3> $HTMLA_TITLE$ </h3> # mostrar sus etiquetas con la id $HTMLA_TITLE$ 
            <p>$DIR_DESCRIPTION$</p>
            <p>$DIR_NAME$</p> 
        </a>
    };
-END]


"""