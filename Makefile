all:
	@echo "make sync"

sync:
	aws s3 sync . s3://tesarek.me --exclude ".git" --exclude "Makefile" --exclude ".git/*" --exclude "*/.DS_Store" --exclude ".DS_Store" --exclude "env/*"
