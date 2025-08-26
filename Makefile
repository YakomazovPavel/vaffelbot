push:
	git add .
	git commit --allow-empty-message -m ""
	git push origin main

run:
	gunicorn app:app --log-level debug