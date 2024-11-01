from pathlib import Path
from typing import Union

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    public_path: Path = Path.cwd() / "public"
    json_path: Path = public_path / "json" / "v1"
    redis_url: str = "redis://localhost:6379"
    upstream_url: str = "https://downloads.immortalwrt.org"
    allow_defaults: bool = False
    async_queue: bool = True
    branches_file: Union[str, Path, None] = None
    max_custom_rootfs_size_mb: int = 1024
    max_defaults_length: int = 20480
    repository_allow_list: list = []
    base_container: str = "ghcr.io/openwrt/imagebuilder"
    update_token: Union[str, None] = "foobar"
    container_host: str = "localhost"
    container_identity: str = ""
    branches: dict = {
        "SNAPSHOT": {
            "path": "snapshots",
            "enabled": True,
            "path_packages": "DEPRECATED",
            "package_changes": [
                {
                    "source": "luci-app-opkg",
                    "target": "luci-app-package-manager",
                    "revision": 32211,
                },
                {"source": "ipv6helper", "revision": 31953, "mandatory": True},
                {"source": "auc", "target": "owut", "revision": 30931},
                {"source": "kmod-nft-nat6", "revision": 20282, "mandatory": True},
                {"source": "firewall", "target": "firewall4", "revision": 18611},
            ],
        },
        "24.10": {
            "path": "releases/{version}",
            "enabled": False,
            "path_packages": "DEPRECATED",
            "branch_off_rev": 32308,
            "package_changes": [
                {
                    "source": "luci-app-opkg",
                    "target": "luci-app-package-manager",
                    "revision": 32211,
                },
                {"source": "ipv6helper", "revision": 31953, "mandatory": True},
                {"source": "auc", "target": "owut", "revision": 30931},
                {"source": "kmod-nft-nat6", "revision": 20282, "mandatory": True},
                {"source": "firewall", "target": "firewall4", "revision": 18611},
            ],
        },
        "23.05": {
            "path": "releases/{version}",
            "enabled": True,
            "path_packages": "DEPRECATED",
            "branch_off_rev": 26397,
            "package_changes": [
                {"source": "kmod-nft-nat6", "revision": 19160, "mandatory": True},
                {"source": "firewall", "target": "firewall4", "revision": 18611},
            ],
        },
    }
    server_stats: str = ""
    log_level: str = "INFO"
    squid_cache: bool = True
    cache_path: Path = Path.cwd() / "cache"
    misc_path: Path = Path.cwd() / "misc"
    keys_path: Path = Path.cwd() / "keys"


settings = Settings()
