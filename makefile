deploy-latest:
	git pull
	hugo

debug:
	hugo --buildDrafts
