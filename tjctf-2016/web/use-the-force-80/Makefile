all:
	docker build -t usetheforce src/
run:
	docker run -d -p 8012:5000 -t usetheforce
debug:
	docker run -i -p 8012:5000 -t usetheforce
shell:
	docker run -i -p 8012:5000 -t usetheforce /bin/bash
