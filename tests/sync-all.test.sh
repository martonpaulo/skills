#!/bin/bash
#
# Regression tests for sync-all.
#
# Runs the real script against a throwaway repository and a throwaway HOME. Touches nothing
# outside its own temporary directory. No dependencies beyond bash and coreutils.
#
#     tests/sync-all.test.sh

set -u

script_dir=$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)
sync_all=$script_dir/../sync-all

if [[ ! -f "$sync_all" ]]; then
    printf 'Cannot find sync-all next to %s\n' "$script_dir" >&2
    exit 1
fi

passed=0
failed=0
work=$(mktemp -d "${TMPDIR:-/tmp}/sync-all-test.XXXXXX") || exit 1
trap 'rm -rf "$work"' EXIT

ok() { printf '  ok   %s\n' "$1"; (( passed++ )); }
no() { printf '  FAIL %s\n     %s\n' "$1" "$2"; (( failed++ )); }

# Builds a fresh case: $case_repo holds the skills, $case_home stands in for HOME, and
# $case_links is the directory sync-claude manages.
new_case() {
    case_dir=$work/$1
    case_repo=$case_dir/Repo
    case_home=$case_dir/home
    case_links=$case_home/.claude/skills
    mkdir -p "$case_repo" "$case_links"
    cp "$sync_all" "$case_repo/sync-all"
    ln -s "$case_repo/sync-all" "$case_repo/sync-claude"
}

add_skill() {
    mkdir -p "$case_repo/$1"
    printf -- '---\nname: %s\n---\n' "$1" > "$case_repo/$1/SKILL.md"
}

# Runs sync-claude against the case's HOME and captures stdout plus the summary counters.
run_sync() {
    output=$(HOME=$case_home "$case_repo/sync-claude" "$@" 2>&1)
}

count() {
    local label=$1
    printf '%s\n' "$output" | sed -n "s/^  $label: \([0-9]*\)$/\1/p"
}

# The whole point of these tests is a path that reaches the same directory under a different
# spelling, which only exists on a case-insensitive filesystem. Detect it rather than assume it.
new_case detect
if [[ -d "${case_dir}/repo" ]]; then
    case_insensitive=1
else
    case_insensitive=0
fi

printf 'sync-all regression tests\n\n'

# --- The reported regression -------------------------------------------------------------------
# A stale link created through a differently-cased path to the repository must still be pruned.
# Before the fix this compared paths as strings, the two spellings never matched, and the link
# survived every run while the summary reported "Removed: 0".
if (( case_insensitive )); then
    new_case stale_other_case
    add_skill keeper
    ln -s "$case_dir/repo/keeper" "$case_links/keeper"   # lowercase r, same directory
    ln -s "$case_dir/repo/gone" "$case_links/gone"       # lowercase r, skill no longer exists
    run_sync --dry-run
    if [[ "$(count Removed)" == 1 ]] && printf '%s' "$output" | grep -q 'Would remove.*gone'; then
        ok 'prunes a stale link written with a different path case'
    else
        no 'prunes a stale link written with a different path case' "$(printf '%s' "$output" | tail -8)"
    fi

    # The same defect made every correctly-pointing link look wrong, so each run rewrote all of
    # them and reported Updated instead of Already correct.
    if [[ "$(count 'Already correct')" == 1 && "$(count Updated)" == 0 ]]; then
        ok 'treats a correct link written with a different path case as already correct'
    else
        no 'treats a correct link written with a different path case as already correct' \
           "Already correct=$(count 'Already correct') Updated=$(count Updated)"
    fi
else
    printf '  skip case-spelling tests: filesystem is case-sensitive\n'
fi

# --- Baseline behaviour that must not regress ---------------------------------------------------
new_case stale_same_case
add_skill keeper
ln -s "$case_repo/keeper" "$case_links/keeper"
ln -s "$case_repo/gone" "$case_links/gone"
run_sync --dry-run
if [[ "$(count Removed)" == 1 && "$(count 'Already correct')" == 1 ]]; then
    ok 'prunes a stale link written with the canonical path'
else
    no 'prunes a stale link written with the canonical path' "$(printf '%s' "$output" | tail -8)"
fi

new_case dry_run_writes_nothing
add_skill keeper
ln -s "$case_repo/gone" "$case_links/gone"
run_sync --dry-run
if [[ -L "$case_links/gone" && ! -e "$case_links/keeper" ]]; then
    ok 'dry run changes nothing on disk'
else
    no 'dry run changes nothing on disk' 'the dry run created or removed a link'
fi

new_case removal_is_real
add_skill keeper
ln -s "$case_repo/gone" "$case_links/gone"
run_sync
if [[ ! -L "$case_links/gone" && -L "$case_links/keeper" ]]; then
    ok 'a real run removes the stale link and creates the missing one'
else
    no 'a real run removes the stale link and creates the missing one' "$(ls -l "$case_links")"
fi

# --- Links this script does not own must survive -------------------------------------------------
new_case foreign_link
add_skill keeper
mkdir -p "$case_dir/elsewhere/thing"
ln -s "$case_dir/elsewhere/thing" "$case_links/thing"
run_sync --dry-run
if [[ "$(count Removed)" == 0 ]]; then
    ok 'leaves a link pointing outside the repository alone'
else
    no 'leaves a link pointing outside the repository alone' "$(printf '%s' "$output" | tail -8)"
fi

# Only direct children of the repository root are managed here, so a link reaching deeper into
# the repository belongs to someone else.
new_case nested_link
add_skill keeper
mkdir -p "$case_repo/keeper/inner"
ln -s "$case_repo/keeper/inner" "$case_links/inner"
run_sync --dry-run
if [[ "$(count Removed)" == 0 ]]; then
    ok 'leaves a link reaching deeper into the repository alone'
else
    no 'leaves a link reaching deeper into the repository alone' "$(printf '%s' "$output" | tail -8)"
fi

# A directory that is not a symlink is someone's real data. It is reported, never replaced.
new_case real_directory_conflict
add_skill keeper
mkdir -p "$case_links/keeper"
printf 'mine\n' > "$case_links/keeper/notes.md"
run_sync
if [[ "$(count Conflicts)" == 1 && -f "$case_links/keeper/notes.md" ]]; then
    ok 'reports a real directory as a conflict and leaves it untouched'
else
    no 'reports a real directory as a conflict and leaves it untouched' "$(printf '%s' "$output" | tail -8)"
fi

# A dangling link whose target directory is gone entirely cannot be attributed to this repository,
# so it is left in place rather than guessed at.
new_case unresolvable_link
add_skill keeper
ln -s "$work/vanished/thing" "$case_links/thing"
run_sync --dry-run
if [[ "$(count Removed)" == 0 && "$(count Errors)" == 0 ]]; then
    ok 'leaves a link whose parent directory no longer exists alone'
else
    no 'leaves a link whose parent directory no longer exists alone' "$(printf '%s' "$output" | tail -8)"
fi

printf '\n%d passed, %d failed\n' "$passed" "$failed"
(( failed == 0 ))
