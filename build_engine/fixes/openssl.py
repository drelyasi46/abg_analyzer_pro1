from pathlib import Path
import os
import tarfile
import shutil


OPENSSL_VERSION = "1.1.1w"
ARCHIVE_NAME = f"openssl-{OPENSSL_VERSION}.tar.gz"


def repair_openssl(engine):
    engine.log("=== OPENSSL REPAIR ===")

    source = Path.home() / "p4a-local" / "openssl"

    if not (source / "Configure").exists():
        engine.log(f"OPENSSL REPAIR FAILED: Configure not found: {source}")
        return False

    engine.log(f"LOCAL OPENSSL SOURCE: {source}")

    # P4A packages path
    packages_path = Path(
        os.environ.get(
            "PACKAGES_PATH",
            str(Path.home() / ".buildozer" / "android" / "packages")
        )
    )

    openssl_package = packages_path / "openssl"
    openssl_package.mkdir(parents=True, exist_ok=True)

    archive = openssl_package / ARCHIVE_NAME
    marker = openssl_package / f".mark-{ARCHIVE_NAME}"

    engine.log(f"P4A PACKAGES PATH: {packages_path}")
    engine.log(f"OPENSSL PACKAGE DIR: {openssl_package}")

    # If a valid cached archive already exists, don't rebuild it.
    if archive.exists() and archive.stat().st_size > 100000:
        engine.log(f"OPENSSL ARCHIVE EXISTS: {archive}")
    else:
        engine.log("CREATING LOCAL OPENSSL ARCHIVE")

        temp_root = engine.cache / f"openssl-{OPENSSL_VERSION}"

        if temp_root.exists():
            shutil.rmtree(temp_root)

        temp_root.mkdir(parents=True)

        extracted_source = temp_root / f"openssl-{OPENSSL_VERSION}"

        shutil.copytree(
            source,
            extracted_source,
            symlinks=True
        )

        temp_archive = temp_root / ARCHIVE_NAME

        with tarfile.open(temp_archive, "w:gz") as tar:
            tar.add(
                extracted_source,
                arcname=f"openssl-{OPENSSL_VERSION}"
            )

        shutil.copy2(temp_archive, archive)

        engine.log(
            f"LOCAL OPENSSL ARCHIVE CREATED: "
            f"{archive} ({archive.stat().st_size} bytes)"
        )

    # The marker is what recipe.py uses to trust the cached archive.
    marker.touch()

    engine.log(f"OPENSSL CACHE MARKER: {marker}")

    # Keep the environment variable as an additional safety mechanism.
    os.environ["P4A_OPENSSL_DIR"] = str(source)

    engine.log(f"P4A_OPENSSL_DIR={source}")

    # Verify archive integrity.
    try:
        with tarfile.open(archive, "r:gz") as tar:
            names = tar.getnames()

        expected_root = f"openssl-{OPENSSL_VERSION}"

        if not any(
            name == expected_root or name.startswith(expected_root + "/")
            for name in names
        ):
            engine.log("OPENSSL REPAIR FAILED: invalid archive root")
            return False

    except Exception as exc:
        engine.log(
            f"OPENSSL REPAIR FAILED: archive validation error: {exc}"
        )
        return False

    engine.log("OPENSSL REPAIR: CACHE SEEDED SUCCESSFULLY")

    return True
