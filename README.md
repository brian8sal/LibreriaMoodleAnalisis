# LibreriaMoodleAnalisis
Este repositorio busca recoger el trabajo desarrollado para la implementación de una herramienta que permita analizar el contenido de los logs de Moodle. 
Está enlazado con Travis CI para la integración continua y Sonarcloud para el control de calidad, los enlaces a tales herramientas son:

https://travis-ci.com/brian8sal/LibreriaMoodleAnalisis
https://sonarcloud.io/dashboard?id=brian8sal_LibreriaMoodleAnalisis

Los ficheros de configuración de tales herramientas son .travis.yml y sonar-project.properties

El proyecto se desarrolla en el directorio EjerciciosLog, contenedor de lo siguiente:
	-assets: Este directorio contiene el .css que proporcionará el estilo a la web.
	-old: Este directorio contiene los archivos que van perdiendo su vigencia,
	
	-Maadle.py: Este fichero compone la librería para el análisis de logs de cursos de Moodle.
	-Prez.py: Este fichero utiliza Dash y Maadle.py para mostrar la información analizada de un log en un sitio web.
	-Test_Maadle: Este fichero alberga una clase para realizar las pruebas de las funciones de la librería Maadle.
	-setup.py: Este fichero permite configurar la generación de un ejecutable de prez. Para utilizarlo se ha de ejecutar: python setup.py bdist_msi
	-server.py: Este fichero permite configurar el servidor local que requiere Prez.

	-TestingLog99Rows.csv: Este fichero se creó con el fin de poder realizar pruebas. Surge de la anonimización de un log de Moodle, con la intención de mantener
	la privacidad.
	-TestingLog1Row.csv: Este fichero se creó con el fin de poder realizar pruebas. Surge de la anonimización de un log de Moodle, con la intención de mantener
	la privacidad.
	-UsuariosTest.csv: Este fichero se creó con el fin de poder realizar pruebas. Busca albergar el nombre de todos los usuarios de un curso de Moodle. No solo 
	el de los usuarios activos en el curso sino todos en general.