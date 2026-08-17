#!/bin/bash

set -u

script_dir=$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)
repo_root=$(cd -P "$script_dir/.." && pwd -P)
work=$(mktemp -d "${TMPDIR:-/tmp}/references-layout-test.XXXXXX") || exit 1
trap 'rm -rf "$work"' EXIT

passed=0
failed=0

ok() { printf '  ok   %s\n' "$1"; (( passed++ )); }
no() { printf '  FAIL %s\n     %s\n' "$1" "$2"; (( failed++ )); }

validate_tree() {
    local root=$1 errors=0 skill references first_real

    for skill in "$root"/*; do
        [[ -d "$skill" && -f "$skill/SKILL.md" ]] || continue
        references=$skill/references

        if [[ ! -d "$references" ]]; then
            printf 'Missing references directory: %s\n' "${skill##*/}" >&2
            (( errors++ ))
            continue
        fi

        first_real=$(find "$references" -mindepth 1 -type f ! -name .keep -print -quit)
        if [[ -n "$first_real" ]]; then
            if [[ -e "$references/.keep" ]]; then
                printf 'Remove placeholder beside real references: %s/references/.keep\n' \
                    "${skill##*/}" >&2
                (( errors++ ))
            fi
        elif [[ ! -f "$references/.keep" ]]; then
            printf 'Empty references directory: %s/references\n' "${skill##*/}" >&2
            (( errors++ ))
        elif [[ -s "$references/.keep" ]]; then
            printf 'Placeholder must be zero bytes: %s/references/.keep\n' "${skill##*/}" >&2
            (( errors++ ))
        fi
    done

    (( errors == 0 ))
}

printf 'references layout tests\n\n'

if validate_tree "$repo_root"; then
    ok 'every skill exposes real references or a zero-byte placeholder'
else
    no 'every skill exposes real references or a zero-byte placeholder' \
        'one or more skill directories violate the references layout invariant'
fi

fixture=$work/fixture
mkdir -p "$fixture/complete/references" "$fixture/missing"
printf -- '---\nname: complete\n---\n' > "$fixture/complete/SKILL.md"
: > "$fixture/complete/references/.keep"
printf -- '---\nname: missing\n---\n' > "$fixture/missing/SKILL.md"

if validate_tree "$fixture" > "$work/fixture.out" 2>&1; then
    no 'rejects a skill without references' 'the invalid fixture passed validation'
elif grep -q '^Missing references directory: missing$' "$work/fixture.out"; then
    ok 'rejects a skill without references'
else
    no 'rejects a skill without references' "$(cat "$work/fixture.out")"
fi

printf '\n%d passed, %d failed\n' "$passed" "$failed"
(( failed == 0 ))
