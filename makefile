APP_NAME=jardim_gis
PORT=4141

VENV_PYTHON=.venv/bin/python
VENV_PIP=.venv/bin/pip


# Valida .env.deploy (v2.0.0)
.PHONY: validate
validate:
	@echo "Validando .env.deploy..."
	@python3 tools/validate-env.py


# Cria a venv e instala as dependências
.PHONY: setup
setup: validate
	python -m venv .venv
	./$(VENV_PIP) install -r requirements.txt
	./$(VENV_PIP) install .


# Executa o projeto
run:
	./.venv/bin/waitress-serve --host 127.0.0.1 --port $(PORT) $(APP_NAME):app


# Apaga a venv
clear_venv:
	@if [ -d ".venv" ]; then rm -r .venv; fi



# Configurações de Deploy
# ----------------------------

# Realiza o deploy
deploy:
	if [ ! -x "./scripts/deploy.sh" ]; then sudo chmod +x ./scripts/deploy.sh; fi
	./scripts/deploy.sh

undeploy:
	if [ ! -x "./scripts/undeploy.sh" ]; then sudo chmod +x ./scripts/undeploy.sh; fi
	./scripts/undeploy.sh


# Configurações do Servico
# ----------------------------
SERVICE_NAME=jardim_gis

service-reload:
	sudo systemctl daemon-reload

service-restart:
	sudo setenforce 0
	sudo systemctl restart $(SERVICE_NAME)
	sudo setenforce 1

service-status:
	systemctl status $(SERVICE_NAME)

log:
	sudo journalctl -u $(SERVICE_NAME)

print_log:
	sudo journalctl -u $(SERVICE_NAME) > service.log
