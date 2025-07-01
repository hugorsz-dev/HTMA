
input_path ="demo" 
target_path = "."

# HTMA: HTML Template to Markdown Automator
# v1.4.0

## LICENSE

"""
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

# -----------------------------

import os
import shutil
import re 
import datetime
import markdown2

# Corregir directorios

input_path = os.path.abspath (input_path)
target_path = os.path.abspath (target_path)
if input_path[-1]==os.sep: input_path= input_path[:-1]
if target_path[-1]==os.sep: target_path= target_path[:-1]

#
attributes_separator ="::"
attrubutes_delimiter =";;"
# 

def fix_markdown_indentation(text):

    # Dividir en líneas
    lines = text.split('\n')
    fixed_lines = []
    
    for line in lines:
        # Eliminar espacios al principio y final de cada línea
        stripped = line.strip()
        
        # Si la línea está vacía, mantenerla vacía
        if not stripped: # cadena vacía es = falso
            fixed_lines.append('')
        else:
            fixed_lines.append(stripped)
    
    # Unir las líneas
    return '\n'.join(fixed_lines)

"""
El objetivo de la clase wblock es devolver los bloques HTMA correctamente TEMPLATEeados en TEMPLATEo
de String.
"""
class WBlock ():
    
    """
    Constructor 
    -   Recibe el string (fragmento de código HTMA) y convierte sus variables en un diccionario, para ser manipuladas en los métodos
    """

    def __init__ (self, block):
        self.block = block
        self.attributes = self.block_string_to_attributes (block)

    """
    Bloque en string convertido en atributos. 
    -   Convierte el bloque a un diccionario de python (clave, valor).
    """
        
    def block_string_to_attributes(self, block):
        attributes = {}
        block = block.split(attrubutes_delimiter)
        clean_block = ""
        for trace in block:
            try:
                if "{" in trace:
                    trace = trace.split("{")[0].replace(" ", "") + trace.split("{")[1].strip().replace("}", " ").strip()
                else:
                    trace = trace.split(attributes_separator)[0].replace(" ", "") + attributes_separator + trace.split(attributes_separator)[1].strip()
            except:
                pass  # Omitir registros basura
            clean_block = clean_block + trace + attrubutes_delimiter
        
        block = clean_block.split(attrubutes_delimiter)
        block = [trace for trace in block if trace.strip()]
        
        for trace in block:
            try:
                key = trace.split(attributes_separator)[0].replace("\n", "")
                value = trace.split(attributes_separator)[1]
                attributes[key] = value
            except:
                raise Exception("Formatting error at attribute at:", key, value)
        
        # ATRIBUTOS GLOBALES
        try:
            if "<" not in attributes["MD_TEMPLATE"]:
                with open(attributes["MD_TEMPLATE"], "r", encoding="utf-8") as file:
                    attributes["MD_TEMPLATE"] = file.read().replace("\n", "").replace("\t", "")
        except:
            pass
        
        try:
            if "<" not in attributes["TEMPLATE"]:
                with open(attributes["TEMPLATE"], "r", encoding="utf-8") as file:
                    attributes["TEMPLATE"] = file.read().replace("\n", "").replace("\t", "")
        except:
            pass
        
        try:
            if os.path.exists(attributes["ONLY_MD"]):
                with open(attributes["ONLY_MD"], "r", encoding="utf-8") as file:
                    attributes["ONLY_MD"] = file.read()
        except:
            pass
        
        return attributes

    """
    RETORNA EL CÓDIGO GENERADO de un bloque con REDIR HTMA 
    -   Reemplaza las ids de un TEMPLATE o de archivo HTMA o HTML (atributo TEMPLATE, p.ej: "$HTMA_TITLE$") por las etiquetas identificadas 
        en el fichero HTML introducido por parámetro.
    - Ejemplo de uso: 
        -   Fichero articulos.htma: 
                <html> <head> <title> Funcionamiento teórico de auto-web </title> </head> <body> <header> <h1 id='HTMA_TITLE'	> Sitio web de funcionamiento teorico </h1> <img id="HTMA_IMAGE" src="http://maricones.com"> <h2 id="HTMA_DESCRIPTION"> Esto es un subtítuloa </h2> </header></html> 
        -   Código:
                block = WBlock('DIR: $ROOT$; REDIR: HTMA; TEMPLATE: { <a href="$DIR_LINKS$"> <h3> $HTMA_TITLE$ </h3> <p> $HTMA_DESCRIPTION$ </p> </a> }')
                print (input_path+"/articulos/articulos.htma")
                block.get_format_htm_ids(input_path+"/articulos/articulos.htma")
                print (block.attributes)
        -   Salida:
                {'DIR': '/home/hugo/eclipse-workspace/programacionPyton/autoweb/web_prueba', 'REDIR': 'HTMA', 'TEMPLATE': '<a href="articulos.html"> <h3> Sitio web de funcionamiento teorico </h3> <p> Esto es un subtítuloa </p> </a>'}
    
    Será necesario que para cada bloque se conozca exactamente el fichero al que hace referencia.
    El uso de este método modificará el atributo TEMPLATE, por lo que es fundamental 
    """
    
    def get_format_htm_ids (self, path):  

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
                        if "://" in matches[0].replace("'", "").replace('"', ""):
                            output[htma_id.replace("'", "").replace('"', "")] = matches[0].replace("'", "").replace('"', "")
                        else:
                            output[htma_id.replace("'", "").replace('"', "")] = target_path+os.sep+"target" + os.sep +  os.path.basename(self.attributes["DIR"])  + os.sep + matches[0].replace("'", "").replace('"', "")
                    else:
                        output[htma_id.replace("'", "").replace('"', "")] =  htm[i+1].split("<")[0].strip()
            return output

        output = self.attributes["TEMPLATE"]
        
        # Recorrer el archivo htma para conseguir sus etiquetas
        
        for label in htm_ids(path):
            output = output.replace("$"+label+"$", htm_ids(path)[label]) 
        
        # VARIABLES GLOBALES
        output = self.get_format_global (output, path)
        
        return output

    """
    Atributos markdown
    -   Retorna un diccionario (clave, valor) con cada una de los valores markdown 
    """

    def md_ids (self,md):  
        output = {}

        md_list = md.split ("\n")

        # MD_H1...H6(memoria)
        h_counter = [-1] * 7 

        # MD_IMG... (memoria)
        img_counter = -1

        # MD_URL --- (memoria)
        url_counter = -1

        #MD_QUOTE ... (memoria)
        quote_counter = -1 
        quote_counter_bufer = []

        #MD_TEXT 
        text_counter = -1

        #
        line_counter = -1
        bufer_line_counter = 0 
        
        # Asignación de variables
        for line in md_list:
            line_counter = line_counter +1
            line = line.strip ()
            
            # MD_HEADERS       
            if line [0:1] == "#":
                # Calcula el primer caracter que no es un "#" en la cadena, consecuentemente arrojando en el "index" su valor (1,6)
                match = (re.search(r'[^#]', line))
                index = match.start()
                h_counter[index] = h_counter[index]+1
                output["MD_H"+str(index)+"["+str(h_counter[index])+"]"] = line.replace ("#", "").strip()
                # Array con todos los headers en su interior
                try: 
                    output["MD_H"+str(index)].append (line.replace ("#", "").strip())
                except:
                    output["MD_H"+str(index)] = []
                    output["MD_H"+str(index)].append (line.replace ("#", "").strip())
            # MD_IMG
            elif "![" in line and "](" in line and not r"\!" in line:
                img_counter = img_counter +1
                find = re.findall(r'\(.*?\)', line)
                output ["MD_IMG"+"["+str(img_counter)+"]"] = target_path+os.sep+"target" + os.sep + os.path.basename(self.attributes["DIR"])  + os.sep +  find [0].replace ("(", "").replace(")","")

            # MD_URL
            elif "[" in line and  "](" in line and not r"\[" in line:
                url_counter = img_counter +1
                find = re.findall(r'\(.*?\)', line)
                output ["MD_URL"+"["+str(url_counter)+"]"] =  target_path+os.sep+"target" + os.sep + os.path.basename(self.attributes["DIR"])  + os.sep +  find [0].replace ("(", "").replace(")","").replace(".md", ".html") # Componenda
            
            # MD_QUOTE
            elif line [0:2] == "> " or line ==">":

                if (bufer_line_counter+1) == line_counter or bufer_line_counter==0:
                    quote_counter_bufer.append (line.replace(">", "").strip()) 
                else:
                    # Agregar la línea anterior
                    quote_counter = quote_counter+1 
                    output ["MD_QUOTE"+"["+str(quote_counter)+"]"] = quote_counter_bufer
                    quote_counter_bufer =[] 
                    
                    # Agregar la línea actual 
                    quote_counter_bufer.append (line.replace(">","").strip())
                
                bufer_line_counter = line_counter
            # MD_TEXT
            else:
                if line.strip()!="":
                    text_counter = text_counter +1
                    output ["MD_TEXT"+"["+str(text_counter)+"]"] = line

        # MD_QUOTE Agregar última linea del bufer
        if quote_counter_bufer != []:
            output ["MD_QUOTE"+"["+str(quote_counter)+"]"] = quote_counter_bufer

        # MARKDOWN TO HTML, etiqueta que contiene todo el documento
        
        # TODO: Componenda: sustituir .md por .html para las redirecciones
        md = md.replace(".md)", ".html)")

        output["MARKDOWN_TO_HTML"] = markdown2.markdown(md, extras=["tables", "fenced-code-blocks"])

        return output   

    """
    Sustituye las variables de un string (template) por las variables de md_ids
    """

    def set_format_md (self,template, md):
        
        
        output = template
        
        md_ids_done=self.md_ids(md)
        
        for label in md_ids_done:
            if isinstance(md_ids_done[label], str):
                output = output.replace("$"+label+"$", markdown2.markdown(md_ids_done[label], extras=["break-on-newline"])) 

        # - Los componentes del output que estén dispuestos en un array deben iterarse en etiquetas, p.ej: 
        # "MD_H1:["titulo 1", "titulo 2"
        # Si el usuario escribe: <ul> <li> $MD_H1 </li> </ul> el resultado sería:   
        # <ul> <li> "titulo 1" </li> <li> "titulo 2" </li> </ul> 

        array_labels= re.findall(r'<\w+>\s*\$.*?\$\s*</\w+>',output)
        for label in array_labels:
            try:
                formatted_label = re.findall( r'<(\w+)>\s*\$(.*?)\$\s*</\1>', label)
                bufer =""   
                for content in md_ids_done[formatted_label[0][1]]:
                    bufer = bufer + f"<{formatted_label[0][0]}>{content}</{formatted_label[0][0]}>"
                output = output.replace(label, markdown2.markdown(bufer, extras=["break-on-newline"]))  
            except:
                pass # Las etiquetas que no son especiales de markdown pasarán por aquí
        
        return output
    
    
    def get_format_md (self, path): 

        with open(path, "r",  encoding="utf-8") as file:
            md = file.read()
        
        # Formateo del markdown exportado 
        with open (target_path+os.sep+webname+path[path.find(os.sep):].replace(".md", ".html"), "w", encoding="utf-8") as file:
            formatted_md = self.set_format_md(self.attributes["MD_TEMPLATE"],md)
            formatted_md  = self.get_format_global (formatted_md , path)
            file.write(formatted_md)

        # Formateo del markdown incrustado en el HTMA 

        output = self.set_format_md(self.attributes["TEMPLATE"], md)
        # COMPROBAR TODO: MUY IMPORTANTE, APLICAR LAS VARIABLES GLOBALES TAL COMO ESTABA EN LA FUNCIÓN DE ARRIBA (set_format_md)
        output = self.get_format_global (output, path)
        return output

    def get_format_only_md (self, md):
        formatted_md = self.set_format_md(self.attributes["MD_TEMPLATE"],md)
        formatted_md  = self.get_format_global (formatted_md , ".")
        return formatted_md

    def get_format_other (self, path):
        output = self.attributes["TEMPLATE"]
        
        # VARIABLES GLOBALES
        output = self.get_format_global (output, path)
        return output
        
    """
    Listar archivos del directorio
    -   Lista los archivos que encuentra en la ruta del atributo "DIR"
    -   Admite rutas relativas desde el punto en que se ejecuta el script. 
    """    
    def list_directory_files (self, extension=""):
        output = []
        try:
            self.attributes["DIR"] 
        except:
            print ("\t Error: Directory label is missing in the block")
            quit()


        limit = len(os.listdir(self.attributes["DIR"]))
        self.attributes["TOTAL_REDIRECTIONS"] = limit

        if "REDIR_LIMIT" in self.attributes:
            limit = int(self.attributes["REDIR_LIMIT"])
            self.attributes["TOTAL_REDIRECTIONS"] = limit
        
        for path in os.listdir(self.attributes["DIR"])[:limit]:
            if os.path.isfile(os.path.join(self.attributes["DIR"], path)):
                if extension:
                    if path.split(".")[-1] in extension:
                        output.append(path)
                       
                else:
                    output.append(path)
        
        # Clasificar cadena según el orden
        if "ORDER_BY" in self.attributes:
            if self.attributes["ORDER_BY"]=="ALPHABETICAL":
                output = sorted(output)
            elif self.attributes["ORDER_BY"]=="ALPHABETICAL_REVERSE":
                output = sorted (output, reverse=True)
            elif self.attributes["ORDER_BY"]=="DATE":
                path_date=[]
                for path in output:
                    path_date.append ({"date":os.path.getmtime(self.attributes["DIR"]+os.sep+path), "path":path})
                path_date= sorted (path_date, key= lambda dictionary: dictionary["date"], reverse=False)
                output = []
                for path in path_date:
                    output.append(path["path"])
            elif self.attributes["ORDER_BY"]=="DATE_REVERSE":
                path_date=[]
                for path in output:
                    path_date.append ({"date":os.path.getmtime(self.attributes["DIR"]+os.sep+path), "path":path})
                path_date= sorted (path_date, key= lambda dictionary: dictionary["date"], reverse=True)
                output = []
                for path in path_date:
                    output.append(path["path"])
            elif self.attributes["ORDER_BY"]=="SYSTEM_REVERSE":
                output.reverse()
            elif self.attributes["ORDER_BY"]=="SYSTEM":
                pass
            else:
                print (f"\tWarning: Order method not found at ORDER_BY {self.attributes['ORDER_BY']}")

        return output 

    """
    Sustituye las etiquetas globales, que son comunes a todos los fomatos de archivo
    Algunas de estas pueden ser la fecha, la hora, el nombre del archivo...
    """

    def get_format_global (self, output, path=""):

        if path:
            # Fecha  de creación de cada archivo
            creation_time = os.path.getctime(path)
            creation_time = datetime.datetime.fromtimestamp(creation_time)
            output = output.replace("$CREATION_TIME_FOR_EACH_FILE_IN_DIR$", creation_time.strftime('%Y-%m-%d'))

            # Fecha  de última modificación de cada archivo
            last_modification_time =  os.path.getmtime(path)
            last_modification_time = datetime.datetime.fromtimestamp (last_modification_time)
            output = output.replace("$LAST_MODIFICATION_TIME_FOR_EACH_FILE_IN_DIR$", last_modification_time.strftime('%Y-%m-%d'))

            # Nombre del archivo
            output = output.replace ("$FILE_NAME_FOR_EACH_FILE_IN_DIR$", os.path.basename(path)[:os.path.basename(path).rfind(".")])
            
            # Redirecciones totales
            if "TOTAL_REDIRECTIONS" in self.attributes:
                output = output.replace ("$TOTAL_REDIRECTIONS$", str(self.attributes["TOTAL_REDIRECTIONS"]))
            
            # Enlace para cada archivo.
            if self.attributes["REDIR"] == "MD":
                output = output.replace ("$LINK_FOR_EACH_FILE_IN_DIR$",target_path+os.sep+"target"+path[path.find(os.sep):].replace(".md",".html"))
            elif  self.attributes["REDIR"] == "HTMA":
                 output = output.replace ("$LINK_FOR_EACH_FILE_IN_DIR$",target_path+os.sep+"target"+path[path.find(os.sep):].replace(".htma",".html"))
            else:
                output = output.replace ("$LINK_FOR_EACH_FILE_IN_DIR$",target_path+os.sep+"target"+path[path.find(os.sep):])
            
        # Hora en la ejecución del script.
        output = output.replace("$DATE_OF_TODAY$", str (datetime.date.today()))
        
        return output

    """
    Generar código
    -   Genera el código en base al TEMPLATE del bloque
    """

    def generate_code (self):
        output =""
        if self.attributes["REDIR"] =="HTMA":
            for file in self.list_directory_files(["htma", "html"]):
                htm_file_path = self.attributes["DIR"]+os.sep+file
                output = output + self.get_format_htm_ids(htm_file_path)
        elif self.attributes["REDIR"]=="MD":
            for file in self.list_directory_files(["md", "txt"]):
                md_file_path = self.attributes["DIR"]+os.sep+file
                output = output + self.get_format_md (md_file_path)
        elif self.attributes["REDIR"] =="ONLY_MD":
            self.attributes["DIR"] ="."
            output = self.get_format_only_md ( fix_markdown_indentation(self.attributes["ONLY_MD"])) # TODO
            
        elif self.attributes["REDIR"]=="ALL": 
            pass
        else:
            if "," in self.attributes["REDIR"]:
                extensions = [extension.strip() for extension in self.attributes["REDIR"].split(",")]
            else: 
                extensions = self.attributes["REDIR"].strip()
            for file in self.list_directory_files(extensions):
                other_file_path = self.attributes["DIR"]+os.sep+file
                output = output + self.get_format_other (other_file_path)

        output =  self.get_format_global (output)

        return output
class HTMAFile ():
        
    """
    Constructor 
    -   Recibe el string de la ubicación de un archivo 
    """

    def __init__ (self, htm_path):
        with open(htm_path, "r",  encoding="utf-8") as file:
            self.htm = file.read()#.replace("\n","").replace("\t","")
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

class HTMAProject ():
    def __init__ (self, path, target):
        self.path = path
        self.target = target
    
    """"
    Generar target
    -   Función que se encarga de clonar los ficheros de un proyecto htma
    -   Este es el bucle en torno al que girarán todas las clases del proyecto.
    """

    def generate_target (self):
        if self.target == ".": self.target =""
        else: self.target = self.target+os.sep

        try:
            shutil.rmtree (self.target+"target")
        except: 
            print ("Warning: Directory 'target' does no exist in specified directory, creating...")

        # Generación de los ficheros vacíos, para evitar errores posteriores asociados a format_md

        for root, dirs, files in os.walk(self.path):
            target_directory = root.replace(self.path, self.target+'target')
            os.mkdir (target_directory)

            for file in files:
               file_extension= file.split(".")[-1]
               file_name= file.split(".")[0]
               if file_extension == "htma": #or file_extension =="md":
                with open (target_directory+os.sep+file_name+".html", "w") as file:
                    pass
               elif (file_extension != "md" and file_extension !="template"):
                shutil.copy (root+os.sep+file, target_directory+os.sep+file )
                
        # Introducción de datos en los ficheros vacíos. 
                    
        for root, dirs, files in os.walk(self.path, topdown=False):
            target_directory = root.replace(self.path, self.target+'target')

            for file in files:
               file_extension= file.split(".")[-1]
               file_name= file.split(".")[0]
               if file_extension == "htma": #or file_extension =="md":
                with open (target_directory+os.sep+file_name+".html", "w") as file:
                    print (root+os.sep+file_name+"."+file_extension)
                    htmafile = HTMAFile (root+os.sep+file_name+"."+file_extension)
                    file.write( htmafile.generate_html()) 
            

project = HTMAProject(input_path, target_path)
project.generate_target()

