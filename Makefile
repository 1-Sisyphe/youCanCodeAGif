.PHONY: docker-build docker-run

docker-build:
	docker build -t codeagif .
docker-run:
	docker run --rm -ti -v `pwd`:/usr/src/app codeagif:latest "/usr/local/bin/python /usr/src/app/main_script_en.py"
