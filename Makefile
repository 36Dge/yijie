.PHONY: bootstrap checkout update-submodules dev-up dev-down lint test generate

bootstrap:
	./scripts/bootstrap.sh

checkout:
	./scripts/checkout-all.sh

update-submodules:
	./scripts/update-submodules.sh

dev-up:
	./scripts/dev-up.sh

dev-down:
	./scripts/dev-down.sh

lint:
	./scripts/lint-all.sh

test:
	./scripts/test-all.sh

generate:
	./scripts/generate-all.sh
