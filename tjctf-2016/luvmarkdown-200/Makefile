all:
			nodejs setup.js
	        docker build -t luvmarkdown src/
run:
	        docker run -d -p 8010:3000 -t luvmarkdown
debug:
			docker run -i -p 8010:3000 -t luvmarkdown
shell:
			docker run -i -p 8010:3000 -t luvmarkdown /bin/bash
