.PHONY: bootstrap checkout dev-up dev-down lint test generate

bootstrap:
	./scripts/bootstrap.sh

checkout:
	./scripts/checkout-all.sh

dev-up:
	./scripts/dev-up.sh

dev-down:
	./scripts/dev-down.sh

lint:
	pnpm lint
	./scripts/lint-all.sh

test:
	pnpm test
	./scripts/test-all.sh

generate:
	./scripts/generate-all.sh
