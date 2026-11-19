# Third-party license review — acadrust comparison pilot

Two implementations are compared in this isolated experiment:

1. **Stable release:** crates.io package `acadrust = 0.6.8`, exact version pin, declared MPL-2.0.
2. **Upstream source snapshot:** Git repository `https://github.com/hakanaktt/acadrust`, exact revision `52034a673ff59bf6936ebf01ec794b07a97df246`, declared MPL-2.0. This revision is 581 commits beyond the v0.6.8 release tag; its Cargo package version string remains 0.6.8.

Both dependencies are optional Cargo features and are tested separately. No acadrust source files are vendored or copied into this repository.

- Use in this branch: isolated optional pilot tool only.
- Production runtime: unchanged; neither implementation is added to `requirements.txt` or any production Python dependency manifest.
- The upstream Git dependency requires network access during initial Cargo resolution unless the repository and dependencies are cached/vendored. This matters for deployment and for users with restricted or unstable connectivity.
- The workflow generates Cargo.lock, which pins the registry checksum and exact Git revision for the run, and uploads it with the evidence artifact. The lockfile is not yet committed. It must be committed and reviewed before any production adoption.
- Do not distribute a bundled binary or ship either dependency in a customer installer until a separate compliance review verifies the exact lockfile, applicable MPL-2.0 notices/source obligations, and the project's final packaging model.
- This note is an engineering inventory, not legal advice.

No third-party code is copied, modified, or redistributed by this pilot change.
