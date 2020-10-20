v8-project
==========

V8 build automation. This project and its CI/CD build the V8 JavaScript engine
whenever a new stable release is published by checking every night
[omahaproxy][1]. The resulting artifacts are then published to [eyeofiles][2].

**The scheduled gitlab job is supposed to fail often: it only succeeds when
a new V8 stable version is available**.


How this works
==============

The main entry point to build V8 is the [Makefile](./Makefile). The main
targets are:

* **all** - download/sync the V8 source code from the Google repository and
   build the archives in the `build/` folder.

* **clean** - clean up the project by removing the `build/` folder and the V8
   sources in `third_party/`.

GitLab CI and the configuration in .gitlab-ci.yml is used to automate the
updates.  There are extra targets in the Makefile to support building the
Docker images used in the CI process and make sure idempotency is
maintained:

* **check_up_to_date** - checks if the archives for the latest stable release
   were already uploaded to [eyeofiles][2].  If this fails, CI will execute
   the `all` target operations and build the archives.

* **foo_prerequisites** (where foo is "check" or "build") - makes sure the
   Debian/Ubuntu prerequisite packages are installed in the same
   environment, in order for the build to succeed.

The `Makefile` uses internally the following Python scripts:

* [get-revision.py](./get-revision.py) - given a platform and a channel (stable,
  beta, dev, canary), it retrieves the relative V8 commit hash from
  [omahaproxy][1].

* [remote-files-exist.py](./remote-files-exist.py) - given a set of urls as
  positional arguments, the program will fail (with error output and exit
  code 1) if any of the latter are unreachable (if the HTTP HEAD status is
  not successful) or complete successfully if all of the urls are reachable.
  This is used in the `needs_update` target, so CI will skip further work in
  case the latest version of the files were already uploaded (based on the
  file names).

* [sync.py](./sync.py) - given a revision (a commit hash), it ensures that V8
  source gets downloaded together with all the dependencies.

* [build.py](./build.py) - given a target platform, a target architecture and
  a build mode chosen between debug and release, it performs the library build.

All the scripts support the traditional `--help` flag to get a brief
description of their usage as standalone script.


Git commits
===========

This repo uses [pre-commit][3] to maintain agreed conventions in the repo. It
should be [installed][4] (tldr; `pip install pre-commit` then
`pre-commit install`) before making any new commits to the repo.


[1]: https://omahaproxy.appspot.com/
[2]: https://v8.eyeofiles.com/
[3]: https://pre-commit.com
[4]: https://pre-commit.com/#installation
