from requests import Session

session = Session()

asu_url = "http://localhost:8000"


def reload_all():
    versions = session.get("https://downloads.immortalwrt.org/.versions.json").json()[
        "versions_list"
    ]
    for version in versions:
        print(f"Reloading {version}")
        targets = session.get(
            f"https://downloads.immortalwrt.org/releases/{version}/.targets.json"
        )
        if targets.status_code == 404:
            print(f"Targets not found for {version}")
            continue
        targets = targets.json()
        for target in targets:
            print(f"Reloading {version}/{target}")
            session.get(
                f"{asu_url}/api/v1/update/{version}/{target}",
                headers={"X-Update-Token": "changeme"},
            )

    targets = session.get(
        "https://downloads.immortalwrt.org/snapshots/.targets.json"
    ).json()
    for target in targets:
        print(f"Reloading SNAPSHOT/{target}")
        session.get(
            f"{asu_url}/api/v1/update/SNAPSHOT/{target}",
            headers={"X-Update-Token": "changeme"},
        )


reload_all()
