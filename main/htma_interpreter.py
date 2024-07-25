
# "HTML Template to Markdown Automator"
# HTMA

import os
import re 
import markdown2

input_path= "/home/hugo/eclipse-workspace/programacionPyton/autoweb/web_prueba"
output_path= "/home/hugo/eclipse-workspace/programacionPyton/autoweb/salida_prueba"


        
def obtain_name_from_path(path):
    head, tail = os.path.split(path)
    return tail or os.path.basename(head)

"""
El objetivo de la clase wblock es devolver los bloques HTMA correctamente TEMPLATEeados en TEMPLATEo
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
                if "{" in trace: 
                    trace = trace.split("{")[0].replace(" ", "")+ trace.split("{")[1].strip().replace("}", " ").strip() 
                else: 
                    trace = trace.split(":")[0].replace(" ", "")+":"+ trace.split(":")[1].strip()
            except:
                pass # Omitir registros basura
                
            clean_block = clean_block + trace +";"

                
        block = clean_block.split(";") 
        block =  [trace for trace in block if trace.strip()]

        for trace in block: 
            try:
                key = trace.split (":")[0]
                value= trace.split (":")[1]
                attributes[key]=value; 
            except: 
                raise Exception ("Formatting error at attribute at:", key, value)

        # ATRIBUTOS GLOBALES 
        try: 
            if "<" not in attributes ["MD_TEMPLATE"]:
                with open(attributes ["MD_TEMPLATE"], "r",  encoding="utf-8") as file:
                    attributes ["MD_TEMPLATE"] = file.read().replace("\n","").replace("\t","")
        except:
            pass
        try: 
            if "<" not in attributes ["TEMPLATE"]:
                with open(attributes ["TEMPLATE"], "r",  encoding="utf-8") as file:
                    attributes ["TEMPLATE"] = file.read().replace("\n","").replace("\t","")
        except:
            pass

            
        return attributes; 

    """
    Dar formato a las htm id
    -   Reemplaza las ids de un TEMPLATEo de archivo HTMA o HTML (atributo TEMPLATE, p.ej: "$HTMA_TITLE$") por las etiquetas identificadas 
        en el fichero HTML introducido por parámetro.
    - Ejemplo de uso: 
        -   Fichero articulos.htma: 
                <html> <head> <title> Funcionamiento teórico de auto-web </title> </head> <body> <header> <h1 id='HTMA_TITLE'	> Sitio web de funcionamiento teorico </h1> <img id="HTMA_IMAGE" src="http://maricones.com"> <h2 id="HTMA_DESCRIPTION"> Esto es un subtítuloa </h2> </header></html> 
        -   Código:
                block = WBlock('DIR: $ROOT$; REDIR: HTMA; TEMPLATE: { <a href="$DIR_LINKS$"> <h3> $HTMA_TITLE$ </h3> <p> $HTMA_DESCRIPTION$ </p> </a> }')
                print (input_path+"/articulos/articulos.htma")
                block.set_format_htm_ids(input_path+"/articulos/articulos.htma")
                print (block.attributes)
        -   Salida:
                {'DIR': '/home/hugo/eclipse-workspace/programacionPyton/autoweb/web_prueba', 'REDIR': 'HTMA', 'TEMPLATE': '<a href="articulos.html"> <h3> Sitio web de funcionamiento teorico </h3> <p> Esto es un subtítuloa </p> </a>'}
    
    Será necesario que para cada bloque se conozca exactamente el fichero al que hace referencia.
    El uso de este método modificará el atributo TEMPLATE, por lo que es fundamental 
    
    """
    
    def set_format_htm_ids (self, path):  

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

        output = self.attributes["TEMPLATE"]
        
        # Recorrer el archivo htma para conseguir sus etiquetas
        
        for label in htm_ids(path):
            output = output.replace("$"+label+"$", htm_ids(path)[label]) 
        output = output.replace ("$LINK_FOR_EACH_FILE_IN_DIR$", obtain_name_from_path(path).replace("htma", "html"))
        
        self.attributes["TEMPLATE"] = output
     
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


    """
    Generar código
    -   Genera el código en base al TEMPLATE del bloque
    """

    def generate_code (self):
        output =""
        if self.attributes["REDIR"] =="HTMA":
            for file in self.list_directory_files():
                self.set_format_htm_ids(self.attributes["DIR"]+os.sep+file)
                output = output + self.attributes["TEMPLATE"]
                self.attributes["TEMPLATE"] = self.attributes["TEMPLATE"].replace (obtain_name_from_path(self.attributes["DIR"]+os.sep+file).replace("htma","html"),"$LINK_FOR_EACH_FILE_IN_DIR$",1)
        elif self.attributes["REDIR"]=="MD":
            # TODO: La generación de código en markdown es diferente, porque se bifurca en "MD_TEMPLATE". Hay que ver cómo trabajar con esto
            for file in self.list_directory_files():
                with open(self.attributes["DIR"]+os.sep+file, "r",  encoding="utf-8") as mfile:
                    markdown_html= markdown2.markdown(mfile.read(), extras=["tables", "fenced-code-blocks"])
            # Código que tendría que corresponder a otros1.html 
            markdown_html_output = self.attributes["MD_TEMPLATE"].replace("$MARKDOWN$",markdown_html)
            print (markdown_html_output)

        elif self.attributes["REDIR"]=="OTHER":
            pass


        
        return output
        
block = WBlock('     DIR: web_prueba; REDIR: HTMA; TEMPLATE: { <a href="$LINK_FOR_EACH_FILE_IN_DIR$"> <h3> $HTMA_TITLE$ </h3> <p> $HTMA_DESCRIPTION$ </p> </a> }')
#block.set_format_htm_ids(input_path+"/articulos.htma")
#print (block.attributes)
#print (block.generate_code())

class HTMAFile ():
        
    """
    Constructor 
    -   Recibe el string de la ubicación de un archivo 
    """

    def __init__ (self, htm_path):
        with open(htm_path, "r",  encoding="utf-8") as file:
            self.htm = file.read().replace("\n","").replace("\t","")
        self.blocks = self.file_to_blocks()
    
    """
    Archivo a bloques
    -   Utilidad del constructor, retorna un array de bloques (clase WBlock) con la que operará toda la clase
    -   Recorre todo el archivo y extrae los bloques HTMA entre las etiquetas <HTMA!> y </HTMA>
    """
    
    def file_to_blocks (self):
        output = []
        

        htm_blocks = (re.split("<HTMA|</HTMA>", self.htm))
        string_blocks = [block for block in htm_blocks if "!>" in block]
        string_blocks = [block.replace("!>","") for block in string_blocks]

        for block in string_blocks: 
            output.append(WBlock(block))

        return output

    """
    Generar HTML
    -   Genera un documento HTML, sustituyendo los bloques HTMA por su correspondiente código, recogido de cada objeto bloque. 
    """

    def generate_html (self):
        output = []
        htm_blocks = (re.split("<HTMA|</HTMA>", self.htm))

        counter = 0
        for i in range(len(htm_blocks)):
            if "!>" in htm_blocks[i]:
                output.append(self.blocks[counter].generate_code())
                counter = counter +1
            else:
                output.append(htm_blocks[i])
        return ' '.join(output);             


                                    









file = HTMAFile ("web_prueba/index.htma")

#for block in file.blocks:
#    print (block.attributes) 

print (file.generate_html())
"""
[HTMA=
    DIR: .;
    REDIR: HTMA; # iteración con todos los ficheros .htma
    TEMPLATE: {
        <a href="$FOR_EACH_FILE_IN_DIR$"> # para cada fichero htma
            <h3> $HTMLA_TITLE$ </h3> # mostrar sus etiquetas con la id $HTMLA_TITLE$ 
            <p>$DIR_DESCRIPTION$</p>
            <p>$DIR_NAME$</p> 
        </a>
    };
-END]


"""
