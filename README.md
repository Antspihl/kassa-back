# Soveldaja kassa backend

### Make a .exe file

- To make a new version into a .exe file:
    - You have to have PyInstaller installed
    - ``pip install pyinstaller``
    - ``python -m PyInstaller app.py``

### Make a docker image and push it to docker hub

- To make a new version into a docker image:
    - You have to have docker installed
    - You have to have a docker hub account
    - Replace [latest] with the version number
```bash
docker build -t antspihl/kassa-app:[latest] .
```
```bash
docker login
```
```bash
docker tag antspihl/kassa-app:latest antspihl/kassa-app:[latest]
```
```bash
docker push antspihl/kassa-app:[latest]
```

### Run the image
- Replace [latest] with the version number or just use latest
```bash
docker run -it -p 5000:5000 --rm --name kassa-app antspihl/kassa-app:[latest]
```
