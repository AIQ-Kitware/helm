# AGENT Instructions

## Development environment
- Use **Python 3.10+**.
- Create/activate a venv; `uv` is recommended. Alternatives: `virtualenv`, Conda, `pyenv`.
- Install for dev:
  - `pip install --force-reinstall -e .[dev]` 
  - Or `./install-dev.sh` (pinned deps), then `pip install -e .[all,dev]`
- Core CLI entry points: `helm-run`, `helm-summarize`, `helm-server`, `helm-create-plots`.
- Optional extras (e.g. `[openai]`, `[metrics]`, `[vlm]`, `[heim]`) enable provider/scenario deps; `[all]` aggregates most extras while omitting a few incompatible sets.
- Credentials: `prod_env/credentials.conf` (HOCON). Some providers need extra auth (e.g., `gcloud auth application-default`, `huggingface-cli login`).

## Repository layout
- Benchmark runner + server/static assets: `src/helm/benchmark/`
- Scenarios: `src/helm/benchmark/scenarios/`
- Metrics: `src/helm/benchmark/metrics/`
- Model clients: `src/helm/clients/`
- Common utilities/types/optional-deps/auth helpers: `src/helm/common/`
- Packaged YAML registries (models/tokenizers/etc.): `src/helm/config/`
- Proxy server/CLI: `src/helm/proxy/`
- Frontend (React/Vite/Tailwind): `helm-frontend/`
  - `yarn install`, `yarn dev`, `yarn test`, `yarn build`, `yarn lint`, `yarn format`
- Docs (MkDocs): `docs/` (site config in `mkdocs.yml`)

## Key workflows
- Run evals: `helm-run`
- Summarize: `helm-summarize`
- Local UI: `helm-server` (benchmark server + static assets under `src/helm/benchmark/static*`)

## Testing + linting
- Tests: `python -m pytest`
  - Default `addopts` skip `models` and `scenarios` markers and enable xdoctest.
  - Use `-m models` / `-m scenarios` intentionally (expensive/networked).
- Lint/type checks: `./pre-commit.sh` or run `black` / `flake8` / `mypy`.
  - Install hooks: `pre-commit install`.

## Extending or modifying
- Read first:
  - `docs/adding_new_models.md`
  - `docs/developer_adding_new_models.md`
  - `docs/adding_new_scenarios.md`
  - `docs/adding_new_tokenizers.md`
- New model deployments usually require:
  - YAML updates in `src/helm/config/`
  - client/metadata/registry wiring
  - optional-dependency + credential guards (`helm.common.optional_dependencies`)
- New scenarios/metrics:
  - implement under `benchmark/scenarios/` or `benchmark/metrics/`
  - add tests + ensure run specs reference them
  - avoid hardcoding paths/creds; prefer `--local-path` and `prod_env`

## Documentation pointers
- Developer setup: `docs/developer_setup.md`
- Credentials/provider setup: `docs/credentials.md`
- Quick start: `docs/quick_start.md` (mirrors `README.md`)

## Operational notes
- Default local config path: `./prod_env/` (override with `--local-path`).
- CI: avoid `-m models` / `-m scenarios` unless explicitly needed (external calls + cost).
- UI:
  - **React frontend is the default UI.**
  - `static_build` is a compiled React build for users without Node.
  - Static leaderboard assets: `src/helm/benchmark/static`.
  - Legacy “alternative UI” references may remain from a deleted older frontend.

## Updating this file
AGENTS.md should track repo reality. Update this file when necessary. If legacy wording in docs/code is fixed, update AGENTS.md to remove any temporary caveats.
