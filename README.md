Pour deployer:
Utiliser docker avec : heroku container:push web
-> Attention: Il faut que le fichier Dockerfile soit présent et avec un f minuscule
Sinon il y aura une erreur No image to push

Projet3: il faut créer les csv dmatrix_f.csv et info_f.csv avant grâce à webapp/app/main.py build_cache()

Projet4: il faut importer le csv database du Google Drive
data_flight_delay_2016.csv
heroku ps:scale web=1
heroku ps:scale web=0


Pour les test en local:
la racine des csv et le dossier actif du terminal dans lequel on lance le script python
