run: 
	python3 projext.py
pull:
	git pull origin main --rebase
push:
	@read -p "Enter commit message: " message; \
	git add -A; \
	git commit -m "$message" ;\
	git pull origin main --rebase; \
	git push origin main