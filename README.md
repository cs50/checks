# checks

## `check50` API

### `Checks`

* `diff(f1, f2)`
  * Checks two files against each other; returns a boolean, True if the two files are different
* `require(paths)`
  * Asserts that all paths passed into the function exist, raises an Error otherwise
* `hash(filename)`
  * Returns the SHA-256 hash of the file
* `spawn(cmd, env=None)`
  * Runs the command `cmd` with environment variables specified by `env`, returns a `Child`
* `add(cmd, paths)`
  * Includes each of paths in checks directory
* `append_code(filename, codefile)`
  * Appends the contents of `filename` to the end of `codefile`
* `replace_fn(old_fn, new_fn, filename)`
  * Replaces C function calls to `old_fn` with function calls to `new_fn` in assembly file `filename`
