# Movify

##  INSTALACIÓN

La aplicación ha sido testeada baja Python3. A continuación se detallan los pasos para su instalación en Ubuntu y Mac OS X y ejecución.

Instalar las herramientas de Python3:

* Ubuntu:
```bash
sudo apt-get update
sudo apt-get -y install python3 python3-pip libffi-dev
sudo pip3 install virtualenv
```
*Nota: Es necesario instalar libffi-dev (usado en el sdk de PayPal)*

* Mac OS X (requiere [brew](http://brew.sh)):
```bash
sudo brew update
brew install python3
sudo pip3 install virtualenv
```

Clonar el repositorio y acceder a él:

```bash
git clone https://github.com/danynab/movify-py.git
cd movify-py
```

Crear el entorno virtual:

```bash
virtualenv venv
```

Activamos el entorno virtual:

```bash
. venv/bin/activate
```

Instalar las dependencias:

```bash
pip3 install -r dependencies
```

Desactivamos el entorno virtual:

```bash
deactivate
```

## Ejecución

A continuación se detallan los pasos a seguir para ejecutar el servidor web.

Activamos el entorno virtual:

```bash
. venv/bin/activate
```

Ejecutar el servidor:
```bash
python3 run.py
```

La activación del entorno virtual será necesaria cada vez que se quiera ejecutar el servidor. Para desactivar el entorno virtual puede utilizarse el comando:

```bash
deactivate
```
