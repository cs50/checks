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

### `Child`

* `stdin(line, prompt=True, timeout=3)`
  * Passes in the `line` of input (or passes `EOF` if `line` is `EOF`)
  * If prompt is `True`, asserts that some textual prompt should be displayed first before passing in `stdin`, and will wait up to `timeout` seconds for the prompt
* `stdout(output=None, str_output=None, timeout=3)`
  * If output is `None`, waits `timeout` seconds for program to terminate, and then returns the output (`stdout` and `stderr`)
  * Otherwise, asserts that the program’s output will match the regex output
  * If output is a file, rather than a regex, then the method asserts that the output matches the file exactly
  * `str_output` is the human-friendly version of the output regex which will be displayed in error messages to the student
* `reject(timeout=3)`
  * Asserts that the student’s program will reject the previously provided input; in other words, asserts that the program provides a textual prompt (within `timeout` seconds) and then waits for `stdin`
* `exit(code=None, timeout=3)`
  * waits `timeout` seconds for the program to terminate
  * If code is `None`, returns the exit code
  * If code isn’t `None`, asserts that the program exits with code code
* `wait(timeout=3)`
  * Waits `timeout` seconds for program to terminate, raises an error if it doesn’t
* `kill()`
  * Terminates the process
  
### Error

* `__init__(rationale=None, helpers=None, result=Checks.FAIL)`
  * When raised, the check ends with the `result`
  * `rationale` is the reason why the check failed (and should be either a `str` or a `Mismatch`)
  * `helpers` is a line of advice for how the student might be able to fix their problem
  * `result` can be `PASS`, `FAIL`, or `SKIP`
  
### Mismatch

* `__init__(expected, actual)`
  * Represents a type of `rationale` that can be passed to an `Error`. Used to indicate that we expected output `expected`, but got output `actual`
  
### File

* `__init__(filename)`
  * Represents a file whose name is `filename`
* `read()`
  * Returns the contents of the file
  
### Decorators

* `@check(dependency)`
  * Defines a check to run: will only run if dependency passes, and will use its side-effects
* `@valgrind`
  * Checks for memory errors during check
