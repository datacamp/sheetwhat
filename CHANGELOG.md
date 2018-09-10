# Changelog

All notable changes to the sheetwhat project will be documented in this file.

## 0.1.3

### Added

- `test_exercise()` can now take the `success_msg` argument.
  If it is not specified, it falls back on the default specified in `protowhat.Reporter`.

## 0.1.2

### Fixed/improved

- `test_exercise()` does more strict checking on its input arguments (to aid the web server)
- `test_exercise()` will not fail if an empty `sct` list is passed.

## 0.1.1

- First functioning version with feature parity compared to the JS implementation.

