#!/usr/bin/env sh

set -eu

REPO_RAW_BASE="https://raw.githubusercontent.com/yoptascript/antigravity-usage-tracker/main"
DEFAULT_INSTALL_DIR="${HOME}/.local/bin"

download_file() {
    url="$1"
    destination="$2"

    if command -v curl >/dev/null 2>&1; then
        curl -fsSL "$url" -o "$destination"
        return
    fi

    if command -v wget >/dev/null 2>&1; then
        wget -qO "$destination" "$url"
        return
    fi

    echo "error: curl or wget is required" >&2
    exit 1
}

choose_install_dir() {
    if [ -n "${INSTALL_DIR:-}" ]; then
        printf '%s\n' "$INSTALL_DIR"
        return
    fi

    case ":$PATH:" in
        *":$HOME/bin:"*)
            printf '%s\n' "$HOME/bin"
            return
            ;;
        *":$HOME/.local/bin:"*)
            printf '%s\n' "$HOME/.local/bin"
            return
            ;;
    esac

    printf '%s\n' "$DEFAULT_INSTALL_DIR"
}

INSTALL_DIR="$(choose_install_dir)"
TARGET_PATH="${INSTALL_DIR}/ag"
TEMP_DIR="$(mktemp -d)"
TEMP_PATH="${TEMP_DIR}/ag"

cleanup() {
    rm -rf "$TEMP_DIR"
}

trap cleanup EXIT INT TERM

mkdir -p "$INSTALL_DIR"
download_file "${REPO_RAW_BASE}/ag" "$TEMP_PATH"
chmod +x "$TEMP_PATH"
mv "$TEMP_PATH" "$TARGET_PATH"

echo "Installed ag to ${TARGET_PATH}"

case ":$PATH:" in
    *":$INSTALL_DIR:"*)
        echo "Running: ag help"
        ag help
        ;;
    *)
        echo "Running: ${TARGET_PATH} help"
        "$TARGET_PATH" help
        echo ""
        echo "Add ${INSTALL_DIR} to PATH to run 'ag' from anywhere."
        ;;
esac
