# Changelog

All notable changes to the sheetwhat project will be documented in this file.

## 0.5.0

- Add `_debug` SCT introspection function
- Normalize conditional format custom formula
- Use `Test` to replace `Rule` in check implementations

## 0.1.5

- Fix setup

## 0.1.4

### Added

- Support checking pivot tables using `has_equal_pivot()`.
- Custom feedback messages can now be templated and use the same parameters as the default messages.

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

