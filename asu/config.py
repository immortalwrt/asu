from pathlib import Path
from typing import Union

from pydantic_settings import BaseSettings, SettingsConfigDict

package_changes_list = [
    {"source": "firewall", "target": "firewall4", "revision": 18611},
    {"source": "kmod-nft-nat6", "revision": 20282, "mandatory": True},
    {"source": "luci-app-diag-core", "revision": 28021, "mandatory": True},
    {"source": "auc", "target": "owut", "revision": 30931},
    {"source": "ipv6helper", "revision": 31953, "mandatory": True},
    {
        "source": "luci-app-opkg",
        "target": "luci-app-package-manager",
        "revision": 32211,
    },
    {"source": "opkg", "target": "apk-openssl", "revision": 32382},
]


def package_changes(before=None):
    changes = []
    for change in package_changes_list:
        if before is None or change["revision"] <= before:
            changes.append(change)
    return changes


def release(branch_off_rev, enabled=True):
    return {
        "path": "releases/{version}",
        "enabled": enabled,
        "snapshot": False,
        "path_packages": "DEPRECATED",
        "branch_off_rev": branch_off_rev,
        "package_changes": package_changes(branch_off_rev),
    }


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    public_path: Path = Path.cwd() / "public"
    redis_url: str = "redis://localhost:6379"
    feeds_url: str = ""
    upstream_url: str = "https://downloads.immortalwrt.org"
    allow_defaults: bool = False
    async_queue: bool = True
    branches_file: Union[str, Path, None] = None
    max_custom_rootfs_size_mb: int = 1024
    max_defaults_length: int = 20480
    repository_allow_list: list = []
    base_container: str = "ghcr.io/openwrt/imagebuilder"
    container_socket_path: str = ""
    container_identity: str = ""
    branches: dict = {
        "SNAPSHOT": {
            "path": "snapshots",
            "enabled": True,
            "snapshot": True,
            "path_packages": "DEPRECATED",
            "package_changes": package_changes(),
        },
        "24.10": release(32308),
        "23.05": release(26397),
    }
    server_stats: str = ""
    log_level: str = "INFO"
    squid_cache: bool = True
    build_ttl: str = "3h"
    build_defaults_ttl: str = "30m"
    build_failure_ttl: str = "10m"
    max_pending_jobs: int = 200

    cache_path: Path = Path.cwd() / "cache"
    misc_path: Path = Path.cwd() / "misc"
    keys_path: Path = Path.cwd() / "keys"

settings = Settings()
