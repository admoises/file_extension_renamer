import os
from pathlib import Path
from dotenv import load_dotenv 
from datetime import datetime


# Environment Variables:
envars = Path().cwd() / '.env'
load_dotenv(envars)

filepath = os.getenv("FILES_DIRECTORY_PATH")
logPath = os.getenv("LOGS_DIRECTORY_PATH")
srcExtension = os.getenv("SOURCE_FILE_EXTENSION")
destExtension = os.getenv("DESTINATION_FILE_EXTENSION")
files = os.listdir(filepath)

# Verificar se pasta 'Logs' existe, se não, criar
isExist = os.path.exists(logPath)
if not isExist:
  os.makedirs(logPath)

# Program Variables:
errors = []
renamed = []

# Methods:
# Método que instancia e adiciona o item em lista
def reportInstance(originalName, newName, motive, list):
    item = {
        "oldFileName": originalName,
        "newFileName": newName,
        "details": motive
    }
    list.append(str(item))

# Método que instancia e insere informações em log
def createLog(logName, list):
    now = datetime.today().isoformat().replace(':', '_').split('.', 1)[0]
    logFileName =  logName + "_" + now + ".txt"
    log = open(logPath + logFileName, "w+")
    for item in list:
        log.write(item + "\n")
    log.close()

# Verifica se devem ser gerados logs
def validateExecution():
    if len(renamed) != 0:
        createLog("ChangesList", renamed)
    if len(errors) != 0:
        createLog("ErrorList", errors)


# Objects:
statusCode = {
    "sc200": "Arquivo teve a extensão alterada com sucesso",
    "sc400": "Something went wrong"
}

# Main Program:
if len(files) > 0:
    for file in files:
        if file.endswith(srcExtension):
            try:
                newFileName = file.split(".", 1)[0] + destExtension
                os.rename(os.path.join(filepath, file), os.path.join(filepath, newFileName))
                reportInstance(file, newFileName, statusCode["sc200"], renamed)
            except:
                reportInstance(file, "", statusCode["sc400"], errors)
else:
    print("Sem arquivos para modificar")

validateExecution()

    
