all:
	@echo "make sync | local"

sync:
	git stash --include-untracked
	aws s3 sync . s3://tesarek.me --exclude ".git" --exclude "Makefile" --exclude ".git/*" --exclude "*/.DS_Store" --exclude ".DS_Store" --exclude "env/*"
	git stash pop

local:
	python -m http.server 8080
