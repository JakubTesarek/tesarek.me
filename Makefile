all:
	@echo "make run.local"


run.local:
	gunicorn tesarek_me:app --bind localhost:8080 --worker-class aiohttp.GunicornWebWorker
