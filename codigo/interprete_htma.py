
# "HTML Template to Markdown Automator"
# HTMA

import os; 
import re 
import markdown
input_path= "/home/hugo/eclipse-workspace/programacionPyton/autoweb/web_prueba"
output_path= "/home/hugo/eclipse-workspace/programacionPyton/autoweb/salida_prueba"

"""
El objetivo de la clase wblock es devolver los bloques HTMA correctamente formateados en formato
de String
"""

class WBlock ():
    
    #CONSTRUCTOR -> tendrá que recibir el bloque en string
    # El processamiento de la etiqueta debe realizarse en un diccionario
    def __init__ (self, block):
        self.block = block
        self.attributes = self.block_string_to_attributes (block)
        
    # MÉTODOS
    
    """
    Generación de código 
    """
    
    def generate_code (self):
        output =""
        if self.attributes["REDIR"] == "HTMA": 
            files_to_redir = [link for link in self.list_directory_files() if ".htma" in link ] 
            for link in files_to_redir:
                code= ""
                
              
    """
    Obtiene el nombre de un determinado archivo desde la fuente 
    """
    
    def obtener_nombre_archivo_desde_path(self, path):
        head, tail = os.path.split(path)
        return tail or os.path.basename(head)
            
    """
    Reemplaza las ids de un formato de archivo HTMA (atributo format) por las generadas por htm_ids
    """
    
    def set_format_htm_ids (self, path):
        output = self.attributes["FORMAT"]
        
        # Recorrer el archivo htma para conseguir sus etiquetas
        
        for label in self.htm_ids(path):
            output = output.replace("$"+label+"$", self.htm_ids(path)[label]) 
        output = output.replace ("$DIR_LINKS$", self.obtener_nombre_archivo_desde_path(path).replace("htma", "html"))
        self.attributes["FORMAT"] = output
    
    """
    Acceder a un archivo HTMA/L y extraer las ID de sus etiquetas
    """
    
    def htm_ids (self, htm_path): 
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
     
    """
    Lista los archivos de un directorio
    """    
    def list_directory_files (self):
        output = []
        if not self.attributes["DIR"]: 
            return False 
        
        if self.attributes["DIR"] == "$ROOT$":
            self.attributes["DIR"]=input_path 
            
        for path in os.listdir(self.attributes["DIR"]):
            if os.path.isfile(os.path.join(self.attributes["DIR"], path)):
                output.append(path)
                
        return output 
        
    """
    Procesa el bloque de texto y lo devuelve en forma de dicccionario de python, para acceder a las variables introducidas. 
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
                print ("Formatting error at attribute at:", key, value)
            
        return attributes; 
        
    
block = WBlock('DIR: $ROOT$; REDIR: HTMA; FORMAT: { <a href="$DIR_LINKS$"> <h3> $HTMA_TITLE$ </h3> <p> $HTMA_DESCRIPTION$ </p> </a> }')
print (input_path+"/articulos/articulos.htma")
block.set_format_htm_ids(input_path+"/articulos/articulos.htma")
print (block.list_directory_files())
print (block.attributes)
print (block.generate_code())

"""
[HTMA=
    DIR: $THIS$;
    REDIR: HTMA;
    FORMAT: {
        <a href="$DIR-LINKS$">
            <h3> $HTMLA_TITLE$ </h3>
            <p>$DIR_DESCRIPTION$</p>
            <p>$DIR_NAME$</p>
        </a>
    };
-END]


"""