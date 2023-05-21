# zhs-marketplace-crawler

## Installation for dev

Works with python 3.8.
Create new env with mangager of your choice. Mine is conda:

```sh
conda create --name zhs python=3.8
pip install -r requirements.txt
```

## Build for productivity

```sh
git clone <repo>
cd <repoPath>
docker build -t zhs-checker .
```

## Run

```sh
docker run -v $PWD:/etc/zhs zhs-checker
```
