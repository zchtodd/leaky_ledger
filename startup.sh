#!/usr/bin/env bash

set -euo pipefail

# trap sigint (ctrl-c) and exit gracefully
trap 'echo "SIGINT received, exiting..."; exit 0' SIGINT

# set up virtual environment
if [ "$(uname -s)" = "Darwin" ]; then
	export VENV=".venv"
else
	export VENV="/opt/venv"
fi
export PATH="${VENV}/bin:$HOME/.asdf/bin:$HOME/.asdf/shims:$PATH"

# get the top-level directory
if [ -d ".git" ] && [ $(command -v brew >/dev/null 2>&1; echo $?) -eq 0 ]; then
	TLD="$(git rev-parse --show-toplevel)"
else
	TLD="$(dirname "$(readlink -f "$0")")"
fi

# source .env file skipping commented lines
if [ -f "${TLD}/.env" ]; then
	export $(grep -v '^#' .env | xargs)
else
	# ! relies on docker env vars (more succinct)
	echo "No .env file found. Filling in with defaults..."
	cat <<-EOF >"${TLD}/.env"
		POSTGRES_DB="${POSTGRES_DB}"
		POSTGRES_USER="${POSTGRES_USER}"
		POSTGRES_PASSWORD="${POSTGRES_PASSWORD}"
		POSTGRES_HOST="${POSTGRES_HOST}"
		POSTGRES_PORT="${POSTGRES_PORT}"
	EOF
	export $(grep -v '^#' .env | xargs)
fi

# check if port is listening
is_listening() {
	local port_return="$(lsof -i :$1 | grep LISTEN | awk '{print $2; exit}')"
	echo "$port_return"
}

# short circuit if postgres isn't running
db_check() {
	if [ "$(uname -s)" = "Darwin" ]; then
		running=$(is_listening "$POSTGRES_PORT")
		if [ -z "$running" ]; then
			echo "Postgres is not running. Exiting"
			exit 1
		fi
	elif [ "$(uname -s)" = "Linux" ]; then
		running=$(ping "$POSTGRES_HOST" -c 1 | grep "1 received")
		if [ -z "$running" ]; then
			echo "Postgres is not running. Exiting"
			exit 1
		fi
	fi
}

# move server port
move_port() {
	echo "Port $1 is in use, trying $PORT"
	while [ -n "$(is_listening "$PORT")" ]; do
		echo "Port $PORT is in use, trying $((PORT+1))"
		PORT=$((PORT+1))
	done
	echo "Port $PORT is available. Using it instead of $1"
}

# check if port is available
port_check() {
	if [ $# -eq 1 ]; then
		PORT="$1"
	else
		PORT=8000
	fi
	[ -z "$(is_listening "$PORT")" ] || move_port "$PORT"
}

# generate self-signed certs
gen_cert() {
	if [ -n "$1" ]; then
		base_url=$1
	else
		base_url="leakyledger.com"
	fi
	priv_key="${TLD}/certs/localhost.key"
	pub_key="${TLD}/certs/localhost.crt"
	csr_file="${TLD}/certs/localhost.csr"
	subj="/CN=leakyledger.com"
	ext="subjectAltName=DNS:${base_url},DNS:www.${base_url},IP:127.0.0.1"
	if [ ! -f "$priv_key" ] || [ ! -f "$pub_key" ]; then
		echo "Generating self-signed certs..."
		mkdir -p "${TLD}/certs"
		openssl genrsa -out "$priv_key" 4096
		openssl req -new -sha256 -out "$csr_file" \
			-key "$priv_key" -nodes -subj "$subj"
		openssl x509 -req -sha256 -in "$csr_file" \
			-signkey "$priv_key" \
			-out "$pub_key" \
			-days 365 \
			-extfile <(echo -n "$ext")
		rm -f "$csr_file"
		echo "Successfully generated self-signed certs! Exiting..."
	else
		echo "Self-signed certs already exist. Skipping..."
		return 0
	fi
}

# run server after checks
server() {
	# rewrite host env var for macos
	if [ "$(uname -s)" = "Darwin" ]; then
		POSTGRES_HOST="localhost"
	fi

	# asgi server
	asgi_app="${TLD}/leaky_ledger_bank_and_company/asgi.py"

	# transform absolute path to dirname.asgi without suffix
	asgi_app="${asgi_app%/*}"
	asgi_app="${asgi_app##*/}.asgi"

	if [ -n "$1" ]; then
		case "$1" in
			"check")
				python "${TLD}/manage.py" "$1" "$2"
				;;
			"collectstatic")
				if [ -d "${TLD}/staticfiles" ]; then
					return 0
				else
					python "${TLD}/manage.py" "$1" "--noinput"
				fi
				;;
			"makemigrations")
				python "${TLD}/manage.py" "$1"
				;;
			"migrate")
				python "${TLD}/manage.py" "$1"
				;;
			"runserver")
				python "${TLD}/manage.py" "$1" "0.0.0.0:${PORT}"
				;;
			"gunicorn")
				gunicorn -w 2 -k uvicorn.workers.UvicornWorker \
				"$asgi_app" -b "0.0.0.0:${PORT}" --log-file -
				;;
			*)
				echo "Invalid command: $1"
				exit 1
				;;
		esac
	else
		# runserver is the default command
		python "${TLD}/manage.py" "$1" "$2"
	fi
}

main() {
	db_check								# check if postgres is running
	port_check "$@"							# default port is 8000
	gen_cert "leakyledger.com"				# dev self-signed certs
	# server "check" "--deploy"				# check for any issues
	server "collectstatic"					# collect static files
	server "makemigrations"
	server "migrate"
	# server "runserver"					# run the server (django)
	server "gunicorn"						# run the server (gunicorn)
}
main "$@"

exit 0
