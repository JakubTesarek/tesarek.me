all:
	@echo "make sync"

sync:
	aws s3 sync . s3://tesarek.me --exclude ".git" --exclude "Makefile" --include "*.md"
