## Deployment
### Deploy web server
Make sure to authenticate with `gcloud` CLI beforehand.

1. Build gcloud-compatible docker image:
```shell
docker build -t europe-north1-docker.pkg.dev/fun-finder-12/fun-finder/fun-finder-backend:latest . --platform linux/amd64
```
2. Push docker image to GCP Artifact Registry:
```shell
docker push europe-north1-docker.pkg.dev/fun-finder-12/fun-finder/fun-finder-backend:latest
```
3. Deploy the web server to Cloud Run:
```shell
gcloud run deploy fun-finder-backend --image europe-north1-docker.pkg.dev/fun-finder-12/fun-finder/fun-finder-backend:latest --platform=managed --region=europe-north1
```

### Deploy cronjob to fetch data
1. Build gcloud-compatible docker image:
```shell
docker build -t europe-north1-docker.pkg.dev/fun-finder-12/fun-finder/fun-finder-cron:latest -f Dockerfile.cronjob --platform linux/amd64 .
```

2. Push docker image to GCP Artifact Registry:
```shell
docker push europe-north1-docker.pkg.dev/fun-finder-12/fun-finder/fun-finder-cron:latest
```

3. Deploy a new version of the cronjob to Cloud Run:
```shell
gcloud run jobs deploy cron-fetch-available-tennis-slots --image=europe-north1-docker.pkg.dev/fun-finder-12/fun-finder/fun-finder-cron:latest
```

4. Trigger the job manually:
```shell
gcloud run jobs execute cron-fetch-available-tennis-slots
```

## Local development - Docker
```shell
docker-compose up --build
```

## Local development - Python virtual environment
### 1. Manage python version with `asdf`:
```shell
$ brew install asdf
$ asdf current
python          3.11.2          Not installed. Run "asdf install python 3.11.2"
```

The python version is specified in `.tool-versions`.

Next, install the python version using `asdf`:
```shell
$ asdf install
...
Installed Python-3.11.2 to /Users/vinhle/.asdf/installs/python/3.11.2

$ asdf current
python          3.11.2          /Users/vinhle/dev/apps/tennis-reservation/.tool-versions
```

### 2. Create a new virtual environment using `virtualenv`:
First install `virtualenv` if it is not installed on your local machine:
```shell
$ brew install virtualenv
$ virtualenv --version
virtualenv 20.21.0 from /opt/homebrew/lib/python3.11/site-packages/virtualenv/__init__.py
```

Create a virtual environment, having python version installed by `asdf`:
```shell 
$ virtualenv --python=$(asdf which python) fun_finder
```

### 3. Activate the virtual environment
```shell
$ source fun_finder/bin/activate
```

After this step, we should use correct python version in the virtual environment:
```shell
$ python --version
Python 3.11.2

$ which python
/Users/vinhle/dev/projects/fun_finder/fun_finder/bin/python
```

### 4. Install dependencies
```shell
$ pip3 install -r requirements.txt
```