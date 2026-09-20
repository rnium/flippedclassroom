COMPOSE    := docker compose
WEB        := $(COMPOSE) exec web
DB         := $(COMPOSE) exec db
BACKUP_DIR := backups
STAMP      := $(shell date +%Y%m%d-%H%M%S)

# Baked into the image so the container user owns the bind-mounted media/static.
APP_UID ?= $(shell id -u)
APP_GID ?= $(shell id -g)
export APP_UID
export APP_GID

.DEFAULT_GOAL := help
.PHONY: help dirs env build up down restart ps logs logs-web logs-db logs-nginx \
        shell dbshell manage migrate makemigrations collectstatic createsuperuser \
        check backup loaddata pg-dump pg-restore fix-perms destroy

help: ## Show this help
	@grep -hE '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) \
		| awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

# Docker creates a missing bind-mount source as root, which the app user then cannot write.
dirs:
	@mkdir -p $(BACKUP_DIR) media static

env:
	@test -f .env || { cp .env.example .env; echo "created .env from .env.example - fill it in"; }

##@ Docker

build: dirs env ## Build the web image
	$(COMPOSE) build

up: dirs env ## Start the stack in the background
	$(COMPOSE) up -d

down: ## Stop the stack (keeps the database)
	$(COMPOSE) down

restart: ## Recreate containers with the current image
	$(COMPOSE) up -d --force-recreate

ps: ## Show container status
	$(COMPOSE) ps

logs: ## Follow logs from all services
	$(COMPOSE) logs -f --tail=100

logs-web: ## Follow the gunicorn/Django log
	$(COMPOSE) logs -f --tail=100 web

logs-db: ## Follow the postgres log
	$(COMPOSE) logs -f --tail=100 db

logs-nginx: ## Follow the nginx log
	$(COMPOSE) logs -f --tail=100 nginx

shell: ## Open a shell in the web container
	$(WEB) bash

dbshell: ## Open psql on the application database
	$(DB) sh -c 'psql -U "$$POSTGRES_USER" -d "$$POSTGRES_DB"'

##@ Django

manage: ## Run any manage.py command: make manage ARGS="showmigrations"
	@test -n "$(ARGS)" || { echo 'usage: make manage ARGS="showmigrations"'; exit 1; }
	$(WEB) python manage.py $(ARGS)

migrate: ## Apply database migrations
	$(WEB) python manage.py migrate

makemigrations: ## Generate new migrations
	$(WEB) python manage.py makemigrations

collectstatic: ## Rebuild the static root served by nginx
	$(WEB) python manage.py collectstatic --noinput --clear

createsuperuser: ## Create a Django admin user
	$(WEB) python manage.py createsuperuser

check: ## Run Django's deployment checks
	$(WEB) python manage.py check --deploy

##@ Backups

backup: dirs ## Dump app data to backups/backup-<stamp>.json
	$(WEB) python manage.py dumpdata \
		--natural-foreign --natural-primary \
		--exclude contenttypes --exclude auth.permission --exclude sessions.session \
		--indent 2 --output backups/backup-$(STAMP).json
	@echo "wrote $(BACKUP_DIR)/backup-$(STAMP).json"

loaddata: ## Load a fixture from anywhere on the host: make loaddata FILE=backups/backup-x.json
	@test -n "$(FILE)" || { echo 'usage: make loaddata FILE=backups/backup-x.json'; exit 1; }
	@test -f "$(FILE)" || { echo "no such file: $(FILE)"; exit 1; }
	$(COMPOSE) cp "$(FILE)" web:/tmp/fixture.json
	$(WEB) python manage.py loaddata /tmp/fixture.json
	$(WEB) rm -f /tmp/fixture.json

pg-dump: dirs ## Full SQL dump to backups/pg-<stamp>.sql
	$(COMPOSE) exec -T db sh -c 'pg_dump -U "$$POSTGRES_USER" -d "$$POSTGRES_DB" --clean --if-exists' \
		> $(BACKUP_DIR)/pg-$(STAMP).sql
	@echo "wrote $(BACKUP_DIR)/pg-$(STAMP).sql"

pg-restore: ## Restore a SQL dump: make pg-restore FILE=backups/pg-x.sql
	@test -n "$(FILE)" || { echo 'usage: make pg-restore FILE=backups/pg-x.sql'; exit 1; }
	@test -f "$(FILE)" || { echo "no such file: $(FILE)"; exit 1; }
	$(COMPOSE) exec -T db sh -c 'psql -U "$$POSTGRES_USER" -d "$$POSTGRES_DB"' < "$(FILE)"

##@ Maintenance

fix-perms: dirs ## Give media/static back to the container user (runs as root in a throwaway container)
	docker run --rm \
		-v "$(CURDIR)/media:/t/media" \
		-v "$(CURDIR)/static:/t/static" \
		alpine:3.20 sh -c \
		'chown -R $(APP_UID):$(APP_GID) /t/media /t/static && \
		 chmod -R u=rwX,go=rX /t/media /t/static'
	@echo "media/ and static/ now owned by $(APP_UID):$(APP_GID)"

destroy: ## Stop the stack AND delete the postgres volume
	@printf 'This deletes the database volume. Type yes to continue: '; \
	read ans; [ "$$ans" = yes ] || { echo aborted; exit 1; }
	$(COMPOSE) down -v
