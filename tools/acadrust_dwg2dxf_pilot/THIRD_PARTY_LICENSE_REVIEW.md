# Third-party license review — acadrust pilot

- Dependency: `acadrust`
- Exact crate version requested: `=0.6.8`
- Upstream repository: https://github.com/hakanaktt/acadrust
- Declared upstream license: MPL-2.0 (confirmed in the v0.6.8 Cargo.toml and upstream repository).
- Use in this branch: isolated optional pilot tool only. No acadrust source files are vendored or copied into this repository.
- Production runtime: unchanged; acadrust is not added to `requirements.txt` or any production Python dependency manifest.
- Distribution: do not distribute a bundled binary or ship this dependency in a customer installer until a separate compliance review verifies the exact Cargo.lock checksum, applicable MPL-2.0 notices/source obligations, and the project's final packaging model.
- The CI workflow generates Cargo.lock and uploads it with the evidence artifact. The lockfile checksum is the dependency integrity record for that run; it must be committed/pinned before any production adoption.
- This note is an engineering inventory, not legal advice.

No third-party code is copied, modified, or redistributed by this pilot change.
