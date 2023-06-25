all: test

.PHONY: test

test:
	ansible-playbook test-callback.yml -v --diff
