build:
	docker build -t frame-fetcher:latest .

run:
	 docker run --rm -it -v $(pwd)/frames:/frames frame-fetcher:latest /bin/bash
