# ATIS Telecom5G CBOM Validator — Installation and Quick-Use Guide

**Version:** ATIS Telecom5G CBOM 1.0.0  
**Purpose:** Installation and operating instructions for the ATIS Telecom5G CBOM 1.0.0 reference validation environment in the `atis-cbom` repository.

> **Repository location:** this guide belongs to `profiles/3gpp-5g/1.0.0/Documents/`. Commands below are shown from the repository root unless stated otherwise.

> The Python tools in this package are reference tooling. Strict CBOM validation has two layers:
> 1. **CycloneDX 1.7 validation** using the official CycloneDX CLI; and
> 2. **ATIS Telecom5G CBOM profile/taxonomy validation** using the ATIS reference tooling.

A strict validation result is established only when both layers are successfully executed.

## Update 20260831 — follow-up review additions

> **Update 20260831:** The following additions were made after review of the initial revised guide and independent Windows testing of the Version 1.0.0 package. They do **not** change the validator or the two-layer conformance model. They clarify installation, tested versions, executable discovery, package integrity, and the distinction between package self-test and end-user CBOM validation.
>
> The main additions are:
> - use a normal system installation of the CycloneDX CLI where possible, rather than copying a third-party executable into the ATIS package directory;
> - make **Winget + PATH** the preferred Windows workflow;
> - distinguish **tested versions** from minimum/current versions;
> - add Windows PATH / App Execution Alias troubleshooting based on independent QSCII testing; and
> - flag unpublished Version 0.x migration material for removal from the clean public baseline if the team approves that publication approach.

---

## 1. What you need

Install the following before running the validator:

- **Python 3.x** compatible with the supplied dependencies; **Python 3.12 is the QSCII-tested and recommended version for this release**
- The Python package dependencies listed in `requirements.txt`
- The official **CycloneDX CLI 0.30.0 or later** (CycloneDX 1.7 validation support was added in CLI 0.30.0)

The validator package does not include the CycloneDX CLI executable. The current official release at the time of this guide is 0.33.1. QSCII independent release validation of Version 1.0.0 was successfully performed with CycloneDX CLI 0.31.0 and Python 3.12.

> **Update 20260831:** The earlier wording said "Python 3.10 or later." The tooling may work on earlier supported Python 3.x versions, but Version 1.0.0 was independently exercised with Python 3.12. Until QSCII runs CI or explicit tests across 3.10/3.11/3.12, this guide distinguishes the **tested/recommended** version from a broader compatibility claim.

### Install the Python dependency

Open a terminal or PowerShell window at the **repository root** and run:

```text
python -m pip install -r requirements.txt
```

The current package requires:

```text
jsonschema>=4.18,<5
```

If this step is not completed, `test_v1.0.0.py` will fail with:

```text
ModuleNotFoundError: No module named 'jsonschema'
```

---

## 2. Install the CycloneDX CLI

Use the official CycloneDX CLI release repository:

https://github.com/CycloneDX/cyclonedx-cli/releases

The CycloneDX CLI may be installed using an operating-system package manager or by downloading the binary that matches the operating system and processor architecture.

Typical release names include:

| Operating system | Typical binary |
|---|---|
| Windows 64-bit | `cyclonedx-win-x64.exe` |
| Linux 64-bit | `cyclonedx-linux-x64` |
| Linux Alpine/musl 64-bit | `cyclonedx-linux-musl-x64` |
| macOS Intel | `cyclonedx-osx-x64` |
| Other architectures | Select the corresponding ARM/x86 release where available |

### Preferred Windows installation

> **Update 20260831:** On Windows, the preferred workflow is to install the CycloneDX CLI as a normal system tool so that it is available on `PATH`. This avoids modifying the contents of the ATIS/QSCII release package.

Using Winget:

```powershell
winget install -e --id CycloneDX.CLI
```

After installation, **close PowerShell and open a new PowerShell window** so that PATH changes are visible. Then verify:

```powershell
cyclonedx --version
```

If that succeeds, the QSCII runner should locate the CLI automatically:

```powershell
python .\profiles\3gpp-5g\1.0.0\Tests\run_qscii_checks.py --require-cyclonedx
```

A normal user should not need to know the physical location of `cyclonedx.exe` when the CLI is correctly installed on `PATH`.

### Manual binary installation

If a package-manager installation is not available or not desired, download the appropriate binary from the official CycloneDX CLI release repository.

### Do I need to rename the file?

**No.** Renaming is optional.

The most reliable approach for a manually downloaded binary is to leave the official filename unchanged and tell the validator where it is using:

```text
--cyclonedx-exe <path-to-CycloneDX-CLI>
```

This avoids operating-system naming differences.

> **Update 20260831:** Prefer storing a manually downloaded CycloneDX executable in a separate tools location (for example, `C:\Tools\CycloneDX`) rather than inside the ATIS/QSCII CBOM release directory. This preserves the integrity and provenance of the released package and avoids mixing a third-party executable with the ATIS artifacts.

### Windows manual-download example

For example, if the executable is stored at `C:\Tools\CycloneDX\cyclonedx-win-x64.exe`:

```powershell
python .\profiles\3gpp-5g\1.0.0\Tests\run_qscii_checks.py --cyclonedx-exe C:\Tools\CycloneDX\cyclonedx-win-x64.exe --require-cyclonedx
```

You may rename the downloaded executable to `cyclonedx.exe` if preferred, but this is not required.

### Linux example

For a manual installation, store the downloaded binary in a separate tools location rather than in the ATIS/QSCII release directory, then make it executable. For example:

```bash
mkdir -p ~/tools/cyclonedx
mv ./cyclonedx-linux-x64 ~/tools/cyclonedx/
chmod +x ~/tools/cyclonedx/cyclonedx-linux-x64
```

Then run:

```bash
python3 ./profiles/3gpp-5g/1.0.0/Tests/run_qscii_checks.py --cyclonedx-exe ~/tools/cyclonedx/cyclonedx-linux-x64 --require-cyclonedx
```

The Python runner itself is cross-platform. On Linux, the CycloneDX binary must have execute permission.

### macOS example

CycloneDX CLI can be installed through the CycloneDX Homebrew tap on supported macOS/Linux systems:

```bash
brew install cyclonedx/cyclonedx/cyclonedx-cli
```

When installed on `PATH`, verify with `cyclonedx --version` and run the QSCII command without `--cyclonedx-exe`. For a manual download, keep the binary in a separate tools location and use `--cyclonedx-exe <path>`.

---

## 3. Confirm the installation

Check Python:

```text
python --version
```

Check the Python dependency:

```text
python -c "import jsonschema; print(jsonschema.__version__)"
```

Check CycloneDX directly.

Windows, when installed on `PATH` (preferred):

```powershell
cyclonedx --version
```

Windows, manual binary installation:

```powershell
C:\Tools\CycloneDX\cyclonedx-win-x64.exe --version
```

Linux/macOS, manual binary installation:

```bash
./cyclonedx-linux-x64 --version
```

If these commands work, the validator prerequisites are installed.

> **Update 20260831:** On Windows, `where.exe cyclonedx` may be used for troubleshooting if `cyclonedx --version` fails. The physical executable path is a troubleshooting detail, not a normal requirement when PATH is configured correctly.

---

## 4. Run the package self-test

The command below is the recommended full package check when CycloneDX is installed on `PATH`:

```text
python profiles/3gpp-5g/1.0.0/Tests/run_qscii_checks.py --require-cyclonedx
```

For example on Windows:

```powershell
python .\profiles\3gpp-5g\1.0.0\Tests\run_qscii_checks.py --require-cyclonedx
```

For a manual or nonstandard CycloneDX installation, specify the executable explicitly:

```text
python profiles/3gpp-5g/1.0.0/Tests/run_qscii_checks.py --cyclonedx-exe <CycloneDX-CLI> --require-cyclonedx
```

A fully successful run should end with the equivalent of:

```text
ATIS/QSCII VALIDATION: PASS
NATIVE CYCLONEDX 1.7 VALIDATION: PASS
STRICT TWO-LAYER VALIDATION: PASS
QSCII LOCAL QA GATES PASSED
```

### Important: this command is a package QA/self-test

`run_qscii_checks.py` does **not** automatically validate every JSON file in the folder.

In Version 1.0.0 it is hard-coded to run native CycloneDX validation against these three reference CBOMs only:

- `CBOM_AMF_N2_vendor_services_v1.0.0_VALID.json`
- `CBOM_SEPP_N32_deployed_services_v1.0.0_VALID.json`
- `CBOM_UDM_5G_AKA_vendor_v1.0.0_VALID.json`

Therefore, copying an additional CBOM JSON file into the directory will not cause `run_qscii_checks.py` to validate it.

---

## 5. Validate your own CBOM file

For normal end-user validation, run the repository-level validator from the repository root:

```text
python Tools/validate_cbom.py <your-cbom-file>.json
```

The tool identifies the declared ATIS profile, locates the corresponding profile-specific taxonomy and validation support, runs native CycloneDX validation, runs the ATIS profile/taxonomy validation layer, and returns one combined result. The user does **not** supply a taxonomy filename.

A successful result ends with:

```text
NATIVE CYCLONEDX VALIDATION: PASS
ATIS PROFILE VALIDATION: PASS
STRICT TWO-LAYER VALIDATION: PASS
```

The command exits nonzero if either required layer fails or cannot be executed.

### Low-level / diagnostic validation

Advanced users may still execute either layer independently. For the ATIS 3GPP-5G 1.0.0 layer:

```text
python profiles/3gpp-5g/1.0.0/Validation/validate_atis_cbom.py \
  profiles/3gpp-5g/1.0.0/atis-telecom5g-taxonomy-1.0.0.json \
  <your-cbom-file>.json
```

Expected status: `PASS ATIS-LAYER`. This alone does not establish strict two-layer validation.

For native CycloneDX 1.7 validation:

```text
cyclonedx validate --input-file <your-cbom-file>.json --input-format json --input-version v1_7 --fail-on-errors
```

Both layers must pass for strict conformance.

### Validate more than one CBOM

The global validator accepts one or more explicit CBOM filenames:

```text
python Tools/validate_cbom.py cbom-1.json cbom-2.json cbom-3.json
```

Each file is validated independently against the profile it declares.

## 6. `run_qscii_checks.py` options

| Option | What it does | When to use it |
|---|---|---|
| `--require-cyclonedx` | Makes the run fail if the CycloneDX CLI cannot be found or native validation cannot be completed successfully. | Recommended for release, CI, and formal validation checks. |
| `--cyclonedx-exe <path>` | Specifies the CycloneDX executable directly. This overrides the environment variable and PATH lookup. | Use for manual, pinned, or nonstandard CycloneDX installations, or for troubleshooting PATH lookup. |
| `--quiet-cyclonedx` | Suppresses detailed CycloneDX CLI stdout/stderr and shows the summarized PASS/FAIL result. | Useful for compact CI or automated logs. |
| `--version` | Displays the runner version. | Troubleshooting/version confirmation. |

**Note:** the option is `--quiet-cyclonedx`; there is no `--silent-cyclonedx` option in Version 1.0.0.

The runner searches for CycloneDX in this order:

1. `--cyclonedx-exe`
2. `CYCLONEDX_CLI` environment variable
3. a command named `cyclonedx` on the system `PATH`

When CycloneDX is correctly installed on `PATH`, no explicit executable path is required. Use `--cyclonedx-exe` when a manual/pinned installation is desired or PATH lookup fails.

> **Update 20260831:** This makes executable discovery a fallback/troubleshooting mechanism rather than a prerequisite for normal use.

---

## 7. `validate_atis_cbom.py` options

Basic syntax:

```text
python profiles/3gpp-5g/1.0.0/Validation/validate_atis_cbom.py [options] <taxonomy> <cbom> [<cbom> ...]
```

| Option / argument | What it does |
|---|---|
| `<taxonomy>` | Machine-readable ATIS taxonomy. For Version 1.0.0 use `atis-telecom5g-taxonomy-1.0.0.json`. |
| `<cbom>` | One or more CBOM JSON files to validate. |
| `--legacy-compat` | Allows deprecated Version 0.x migration properties with warnings. This is diagnostic/migration mode and is **not** strict Version 1.0.0 conformance. |
| `--show-scope-closure` | Prints the calculated inventory scope closure when `inventoryScopeRef` is present. |
| `--cyclonedx-schema <file>` | Also validates against a supplied CycloneDX JSON schema using Python `jsonschema`. This requires an appropriate official schema and referenced schemas to be available. |
| `--version` | Displays the ATIS validator version. |

For normal use, the independently installed CycloneDX CLI is the simpler native CycloneDX validation method.

> **Update 20260831 — publication cleanup note:** If QSCII approves publication of Version 1.0.0 as the **initial public baseline**, references to unpublished Version 0.x migration behavior (including `--legacy-compat`) should be removed from the public-facing quick-use guide. The capability may remain available for internal/developer diagnostics if desired, but it should not burden first-time public users with unpublished drafting history.

---

## 8. Tool and test organization

| Script | Purpose | User options |
|---|---|---|
| `Tests/normative_audit.py` | Checks normative text and human/machine alignment for this profile. | None |
| `Tests/sdo_reviewer_audit.py` | Runs publication/readiness checks for this profile. | `--fail-on blocker|major|minor|info|none` |
| `Tests/test_v1.0.0.py` | Runs the profile/package regression suite. | None |
| `Validation/generate_overlay.py` | Regenerates the derived ATIS schema overlay. | None |
| `Tests/run_qscii_checks.py` | Runs the integrated profile/package QA self-test. | See Section 6 |
| `Validation/validate_atis_cbom.py` | Runs the 3GPP-5G profile-specific ATIS validation layer. | See Section 7 |

Most end users only need `Tools/validate_cbom.py`. QSCII developers/reviewers use the profile-specific `Tests/run_qscii_checks.py` entry point for package assurance.

---

## 9. Understanding PASS and FAIL messages

There are several different PASS messages in the output. They do not all mean the same thing.

### `NORMATIVE AUDIT PASSED`

The normative/package audit passed. This does not mean the CBOM validation process as a whole passed.

### `PASS ATIS-LAYER`

The CBOM passed the ATIS reference profile/taxonomy validation only.

### `NATIVE CYCLONEDX 1.7 VALIDATION: PASS`

The CBOM/reference CBOMs passed native CycloneDX 1.7 validation.

### `STRICT TWO-LAYER VALIDATION: PASS`

This is the important full result. Both required validation layers were successfully established.

Always use the final combined status rather than an earlier individual `PASSED` message when assessing the complete run.

---

## 10. Troubleshooting

### `CycloneDX CLI: NOT FOUND`

Use the explicit executable option:

```text
--cyclonedx-exe <path-to-downloaded-binary>
```

### Windows cannot find `cyclonedx`

> **Update 20260831:** First close and reopen PowerShell after installation, then run:

```powershell
cyclonedx --version
where.exe cyclonedx
```

If `cyclonedx --version` still fails but `where.exe cyclonedx` shows an executable, use the explicit `--cyclonedx-exe` option. If no executable is found, reinstall the CLI or use the manual-download method in Section 2.

### Windows says Python was not found or opens the Microsoft Store

This can occur when Windows has an **App Execution Alias** for `python.exe` but no real Python interpreter is installed. Verify with:

```powershell
where.exe python
where.exe py
```

If Python is not installed, a tested Windows installation path is:

```powershell
winget install -e --id Python.Python.3.12
```

Then close and reopen PowerShell and verify:

```powershell
python --version
```

If `python` still resolves only to `...\Microsoft\WindowsApps\python.exe`, disable the `python.exe` / `python3.exe` **App Execution Aliases** in Windows Settings and reopen PowerShell.

### `ModuleNotFoundError: No module named 'jsonschema'`

Run:

```text
python -m pip install -r requirements.txt
```

### I copied a new CBOM into the folder but it was not checked

This is expected with Version 1.0.0. `run_qscii_checks.py` contains a fixed list of the three reference CBOMs and does not scan the directory.

Validate the new file explicitly using the commands in Section 5.

### Linux reports permission denied for CycloneDX

Run `chmod +x` on the downloaded CycloneDX binary, for example:

```bash
chmod +x ~/tools/cyclonedx/cyclonedx-linux-x64
```

and use `--cyclonedx-exe` with the corresponding path.

### The native CBOMs show PASS but the final run does not pass

Check the ATIS/QSCII test output as well. A missing Python dependency or failure in the reference QA/regression layer prevents the complete package check from succeeding.

---

## 11. End-user and package-self-test entry points

The repository intentionally provides two separate entry points with different responsibilities:

1. **`Tools/validate_cbom.py`** — profile-independent end-user validation. It determines the declared profile, runs native CycloneDX validation and the appropriate ATIS profile-specific validation layer, and returns one combined result.
2. **`profiles/3gpp-5g/1.0.0/Tests/run_qscii_checks.py`** — profile/package self-test. It validates the supplied reference fixtures and runs the profile-specific QA and regression gates.

This separation keeps the end-user validation workflow independent of the internal release/package self-test workflow.

## Update 20260831 — verification notes

The 20260831 additions were based on:

- independent QSCII Windows validation of ATIS Telecom5G CBOM Version 1.0.0 using **Python 3.12** and **CycloneDX CLI 0.31.0**, which achieved `STRICT TWO-LAYER VALIDATION: PASS`;
- the CycloneDX CLI documentation confirming native `v1_7` validation support; and
- follow-up usability review focused on making first-time installation and executable discovery more obvious.

These additions are documentation/usability clarifications only. They do not modify the normative profile, taxonomy, or validation semantics.
