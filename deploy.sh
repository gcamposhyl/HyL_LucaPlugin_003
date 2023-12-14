#npm install -g firebase-tools
firebase login

# configuración proyecto backend
cd cloud_functions

# configurar proyecto para deploy
firebase use --add

# Preguntar al usuario si está en Windows o Linux
read -p "¿Estás en Windows o Linux? (w/l): " sistema_operativo

# Deploy cloud functions

directorios=$(ls -d */)

# Configuración de variables
if [ "$sistema_operativo" == "w" ]; then
    create_venv="python -m venv venv"
    activate_venv="source venv/Scripts/activate"
else
    create_venv="python3.11 -m venv venv"
    activate_venv="source venv/bin/activate"
fi

install_python_dependencies="pip install -r requirements.txt"

# Configuración de variables node
install_node_dependencies="npm install"

# instalo dependencias de functions por defecto
cd functions
$install_node_dependencies
cd ..


# Carpetas a ignorar
carpetas_ignoradas=("functions")

# configuración firebase deploy
deploy_functions="firebase deploy --only functions:"

# Iterar sobre cada directorio
for dir in $directorios; do
    # Verificar si el directorio está en la lista de carpetas ignoradas
    if [[ " ${carpetas_ignoradas[@]} " =~ " ${dir%/} " ]]; then
        echo "Ignorando directorio: $dir"
    else
        echo "Procesando directorio: $dir"
        
        # Entrar en el directorio
        cd $dir

        # Verificar la existencia de main.py o index.js
        if [ -e "main.py" ]; then
            echo "Detectado main.py, instalando dependencias de Python"
            $create_venv
            $activate_venv
            $install_python_dependencies
            $deploy_functions${dir%/} -m "Deploy cloud functions from repository script: ${dir%/}"
            deactivate
        elif [ -e "index.js" ]; then
            echo "Detectado index.js, instalando dependencias de Node.js"
            $install_node_dependencies
            $deploy_functions${dir%/} -m "Deploy cloud functions from repository script: ${dir%/}"
        else
            echo "No se detectó main.py ni index.js en ${dir%/}"
        fi

        # Volver al directorio raíz
        cd ..
    fi
done