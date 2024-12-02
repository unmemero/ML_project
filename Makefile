run: 
	python3 project.py
test:
	python3 test.py
gui:
	python3 project_gui.py
pull:
	git pull origin main --rebase
push:
	@read -p "Enter commit message: " message; \
	git add -A; \
	git commit -m "$message" ;\
	git pull origin main --rebase; \
	git push origin main
pdf:
	pandoc ./docs/\[F24-ML\]Project\ Report\ -\ Rafael\ Garcia\ and\ Fernando\ Muñoz.md -o ./docs/\[F24-ML\]Project\ Report\ -\ Rafael\ Garcia\ and\ Fernando\ Muñoz.pdf