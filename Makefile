GIT_TOP=$(shell git rev-parse --show-toplevel 2>/dev/null)
UNAME := $(shell uname)
USER = $(shell id -u -n)

install:
	if [ '$(UNAME)' = 'Linux' ] || [ '$(UNAME)' = 'Darwin' ]; then echo "installing for ${USER}"; \
	chmod 755 ${GIT_TOP}/jq-repl.py;\
	ln -s ${GIT_TOP}/jq-repl.py /usr/local/bin/jq-repl; chown -R ${USER} /usr/local/bin/jq-repl; fi

clean:
	if [ '$(UNAME)' = 'Linux' ]; then echo "cleaning for ${USER}"; rm -f /usr/local/bin/jq-repl;\
	fi
