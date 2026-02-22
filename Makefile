.PHONY: format format-check lint test

format:
	docker run --rm -v "$$(pwd):/workdir" -w /workdir node:20 npx --yes prettier@3.2.5 --write "**/*.{md,yml,yaml}"

format-check:
	docker run --rm -v "$$(pwd):/workdir" -w /workdir node:20 npx --yes prettier@3.2.5 --check "**/*.{md,yml,yaml}"

lint:
	docker run --rm -v "$$(pwd):/workdir" -w /workdir node:20 npx --yes markdownlint-cli2@0.13.0 "**/*.md" "#node_modules"

test: format-check lint
