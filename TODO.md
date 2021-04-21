# TODO

- Add to the `README.md` file (examples, description, etc)
- Changes that will affect the `Command` class:
    - Ability to turn off command output per command (for both standard output and standard error)
    - Ability to turn off command output storage on the `SSHSession`? (for both standard output and
      standard error)
- Why doesn't standard error print in a stream like standard output?
    - If you have a program that prints in a loop every second, if it prints to standard output, it
      will print every second, but if it prints to standard error, it waits for the entire thing to
      finish before printing.
    - Might have to either toggle back and forth between capturing standard output and standard
      error or spin up 2 threads in the `SSHSession` to deal with capturing both simultaneously, and
      use a lock to keep output of the two separated
- Add method called "run_script()` that takes in a path to a script, uploads it, runs it, and
  captures the output.  Will have to make a method for both `SSHSession` and `SSHSessionManager.`
  This will make writing larger commands easier, since it can just be done in a file.
- Add unit tests
    - Either real ones that use a configuration file to connect to real servers and perform real
      actions, or using a mock library to create fake connection objects.
