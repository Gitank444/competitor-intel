from github import Github
from config import GITHUB_TOKEN, COMPETITORS
from storage.db import get_last_snapshot, save_snapshot
import json

g = Github(GITHUB_TOKEN)

DEPENDENCY_FILES = [
    "package.json",
    "requirements.txt",
    "Pipfile",
    "pyproject.toml",
    "go.mod",
    "Gemfile",
]

def get_repos(org_name):
    try:
        org = g.get_organization(org_name)
        return list(org.get_repos())
    except Exception as e:
        print(f"Error fetching repos for {org_name}: {e}")
        return []

def get_dependencies(repo):
    deps = {}
    for dep_file in DEPENDENCY_FILES:
        try:
            content = repo.get_contents(dep_file)
            deps[dep_file] = content.decoded_content.decode("utf-8")
        except:
            pass
    return deps

def get_file_structure(repo):
    try:
        contents = repo.get_contents("")
        return [item.path for item in contents]
    except Exception as e:
        print(f"Error getting file structure: {e}")
        return []

def collect_github_signals():
    all_signals = []

    for competitor in COMPETITORS:
        org_name = competitor.get("github_org")
        comp_name = competitor.get("name")

        if not org_name:
            continue

        print(f"Collecting GitHub data for {comp_name}...")
        repos = get_repos(org_name)

        for repo in repos[:5]:
            current_deps = get_dependencies(repo)
            current_structure = get_file_structure(repo)
            current_deps_str = json.dumps(current_deps)
            current_structure_str = json.dumps(current_structure)

            last = get_last_snapshot("github_snapshots", comp_name)
            changes = []

            if last:
                if last[3] != current_deps_str:
                    changes.append(f"Dependency changes in {repo.name}")
                last_structure = json.loads(last[4])
                new_files = set(current_structure) - set(last_structure)
                if new_files:
                    changes.append(f"New files in {repo.name}: {', '.join(new_files)}")
            else:
                changes.append(f"First snapshot for {repo.name}")

            save_snapshot(
                "github_snapshots",
                comp_name,
                repo=repo.name,
                dependencies=current_deps_str,
                file_structure=current_structure_str
            )

            if changes:
                all_signals.append({
                    "competitor": comp_name,
                    "source": "github",
                    "repo": repo.name,
                    "changes": changes
                })

    return all_signals