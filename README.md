v8-project
==========

V8 build automation. This project and its CI/CD build the V8 JavaScript engine
whenever a new stable release is published by checking every night
[omahaproxy][1]. The resulting artifacts are then published to [eyeofiles][2].

**The scheduled gitlab job is supposed to fail often: it only succeeds when
a new V8 stable version is available**.


How this works
==============

The main entry point to build V8 is the [Makefile](./Makefile). The three main
targets are:

* **all** - download/sync the V8 source code from the Google repository and
   build the archives in the `build/` folder.

* **update** - checks first if the archives for the latest stable release
   were already uploaded to [eyeofiles][2], if so the job fails, otherwise it
   will execute the `all` target operations and build the archives.

* **clean** - clean up the project by removing the `build/` folder and the V8
   sources in `third_party/`.

The `Makefile` uses internally the following Python scripts:

* [get-revision.py](./get-revision.py) - given a platform and a channel (stable,
  beta, dev, canary), it retrieves the relative V8 commit hash from
  [omahaproxy][1].

* [files-do-not-exist.py](./files-do-not-exist.py) - given a set of urls as
  positional arguments, the program will fail (exit code 1) if the latter are
  all reachable (http status 200) or complete successfully if at least one of
  the urls is not reachable. This is used in the `update` target to make it
  fail in case the latest version of the files were already uploaded (based on
  the file names).

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
