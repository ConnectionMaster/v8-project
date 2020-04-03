v8-project
==========

A set of tools to work with V8 JavaScript engine. In particular it takes care of all platform specific peculiarities when one has to obtain a new version of V8 or build it for a particular platform.

Getting the help
================

For a brief description of the available functionality run `build.py` without parameters.
For a comprehensive overview of available commands and their options run `build.py --help`.
Use `--help` to get detailed explaination of a command.


Getting V8
==========

In order to get V8 run `build.py sync`, one can optionally specify the revision of V8 by adding `--revision SOME_REVISION`.


Building V8
===========

In order to build V8 use the corresponding `build` command, e.g. `build.py build windows x64 debug`. The output is in the `{path to build.py}/build` directory.

Git commits
===========

This repo uses [pre-commit](https://pre-commit.com) to maintain agreed conventions in the repo. It should
be [installed](https://pre-commit.com/#installation) (tldr; `pip install pre-commit` then `pre-commit install`)
before making any new commits to the repo.

Gitlab Merge Requests
=====================

The *master* branch reflects a stable (production-ready) state.

In order to navigate between the stable states one can go over first parent commits.

In order to ensure that any results obtained during the CI of a merge request are actually for the commit which is going to be considered stable there are several rules
* only Fast-forward merge requests are allowed
* CI firstly ensures that the changes are already properly merged onto the master branch

What it means on practice
-------------------------

If there is a relatively small change and no additional reviewing rounds, e.g. only updating of the todays default V8 version, or the everything is squashed into a single commit, then the merging is basically the adavancing of the *master* branch and artifacts obtained for the commit will be considered ready for use.

If the reviewing of a merge request requires several rounds and/or an author decided to keep changes in small self-contained commits, then before sending an update of the merge request the author should perform the merging locally. If the author wants to keep the history of the merge request cleaner, namely without intermediate merge commits, then one may use force push to the feature branch of the merge request.
