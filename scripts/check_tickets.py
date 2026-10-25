"""Validate the repository's documented JSON-compatible YAML ticket convention.

No third-party YAML dependency, network access, or repository writes are needed.
This intentionally rejects YAML constructs outside tickets/README.md's subset.
"""

import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIELDS = {
    "schema_version",
    "id",
    "title",
    "type",
    "status",
    "priority",
    "recommended_thinking",
    "milestone",
    "work_packages",
    "hypotheses",
    "depends_on",
    "labels",
    "assignees",
    "created",
    "updated",
    "github_issue",
    "decision",
}
TYPES = {"engineering", "experiment", "decision", "research"}
STATUSES = {"backlog", "ready", "in_progress", "blocked", "done", "cancelled"}
DECISIONS = {"proceed", "revise", "stop"}
THINKING_LEVELS = {"low", "medium", "high", "xhigh"}
SECTIONS = (
    "Recommended thinking",
    "Problem / hypothesis",
    "Scope",
    "Acceptance criteria",
    "Metrics / evidence",
    "Dependencies",
    "Completion record",
)
ID = r"SOAM-\d{3}"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def parse(path):
    lines = path.read_text().splitlines()
    require(lines and lines[0] == "---", f"{path}: missing leading frontmatter")
    require("---" in lines[1:], f"{path}: missing closing frontmatter delimiter")
    end = lines.index("---", 1)
    metadata = {}
    for line in lines[1:end]:
        require(":" in line, f"{path}: expected key: JSON-compatible value")
        key, value = line.split(":", 1)
        require(re.fullmatch(r"[a-z_]+", key), f"{path}: invalid key {key!r}")
        require(key not in metadata, f"{path}: duplicate key {key}")
        try:
            metadata[key] = json.loads(value)
        except json.JSONDecodeError as error:
            raise ValueError(f"{path}: {key} must use the documented YAML subset") from error
    return metadata, "\n".join(lines[end + 1 :])


def check_links(path):
    for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", path.read_text()):
        if re.match(r"[a-z]+://", target):
            continue
        local = target.split("#", 1)[0]
        if local:
            require((path.parent / local).is_file(), f"{path}: broken link {target}")


def validate(root=ROOT):
    tickets = {}
    paths = {}
    for path in sorted((root / "tickets").glob("SOAM-*.md")):
        metadata, body = parse(path)
        require(set(metadata) == FIELDS, f"{path}: missing/unknown fields {set(metadata) ^ FIELDS}")
        ident = metadata["id"]
        require(isinstance(ident, str) and re.fullmatch(ID, ident), f"{path}: invalid ID")
        require(path.name.startswith(ident + "-"), f"{path}: filename/ID mismatch")
        require(ident not in tickets, f"Duplicate ticket ID {ident}")
        require(
            type(metadata["schema_version"]) is int and metadata["schema_version"] == 2,
            f"{ident}: unsupported schema",
        )
        require(
            isinstance(metadata["title"], str) and metadata["title"].strip(),
            f"{ident}: empty title",
        )
        require(metadata["type"] in TYPES, f"{ident}: invalid type")
        require(metadata["status"] in STATUSES, f"{ident}: invalid status")
        require(metadata["priority"] in {"P0", "P1", "P2", "P3"}, f"{ident}: invalid priority")
        require(
            metadata["milestone"] in {*(f"M{i}" for i in range(9)), "MX"},
            f"{ident}: unknown milestone",
        )
        for field in ("work_packages", "hypotheses", "depends_on", "labels", "assignees"):
            values = metadata[field]
            require(
                isinstance(values, list) and all(isinstance(v, str) and v for v in values),
                f"{ident}: {field} must be a list of nonempty strings",
            )
            require(len(values) == len(set(values)), f"{ident}: duplicate {field}")
        require(
            set(metadata["work_packages"]) <= {f"WP-{i:02d}" for i in range(14)},
            f"{ident}: unknown work package",
        )
        require(
            set(metadata["hypotheses"]) <= {f"H{i}" for i in range(1, 9)},
            f"{ident}: unknown hypothesis",
        )
        require(
            {
                f"type:{metadata['type']}",
                f"priority:{metadata['priority']}",
                f"milestone:{metadata['milestone']}",
            }
            <= set(metadata["labels"]),
            f"{ident}: labels disagree with metadata",
        )
        for key in ("created", "updated"):
            value = metadata[key]
            require(
                isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value),
                f"{ident}: {key} must be a quoted ISO date",
            )
            date.fromisoformat(value)
        require(metadata["updated"] >= metadata["created"], f"{ident}: updated before created")
        issue = metadata["github_issue"]
        require(
            issue is None
            or (
                isinstance(issue, str)
                and re.fullmatch(r"https://github\.com/[^/]+/[^/]+/issues/[1-9]\d*", issue)
            ),
            f"{ident}: invalid issue URL",
        )
        decision = metadata["decision"]
        if metadata["type"] == "decision" and metadata["status"] == "done":
            require(decision in DECISIONS, f"{ident}: completed decision lacks an outcome")
        else:
            require(decision is None, f"{ident}: only completed decision tickets have an outcome")
        thinking = metadata["recommended_thinking"]
        require(thinking in THINKING_LEVELS, f"{ident}: invalid recommended thinking")
        for section in SECTIONS:
            require(f"## {section}\n" in body, f"{ident}: missing {section} section")
        rationale = body.split("## Recommended thinking\n", 1)[1].split("\n## ", 1)[0].strip()
        prefix = f"**{thinking}** — "
        require(
            rationale.startswith(prefix) and rationale[len(prefix):].strip(),
            f"{ident}: missing rationale or thinking level disagrees with frontmatter",
        )
        acceptance = body.split("## Acceptance criteria\n", 1)[1].split("\n## ", 1)[0]
        require(
            re.search(r"^- \[[ x]\] .+", acceptance, re.MULTILINE), f"{ident}: missing checkboxes"
        )
        completion = body.split("## Completion record\n", 1)[1].strip()
        if metadata["status"] == "done":
            require("- [ ]" not in acceptance, f"{ident}: done with unchecked acceptance criteria")
            require(
                completion and not completion.startswith("Not started"),
                f"{ident}: done without completion record",
            )
        if metadata["status"] == "blocked":
            require(
                "## Blockers\n" in body and body.split("## Blockers\n", 1)[1].strip(),
                f"{ident}: blocked without an explanation",
            )
        if metadata["status"] == "cancelled":
            require(
                completion and not completion.startswith("Not started"),
                f"{ident}: cancellation needs a reason/replacement",
            )
        dependencies = body.split("## Dependencies\n", 1)[1].split("\n## ", 1)[0]
        require(
            set(re.findall(ID, dependencies)) == set(metadata["depends_on"]),
            f"{ident}: body/frontmatter dependencies disagree",
        )
        tickets[ident], paths[ident] = metadata, path
        check_links(path)
    require(tickets, "No tickets found")
    for ident, ticket in tickets.items():
        require(set(ticket["depends_on"]) <= tickets.keys(), f"{ident}: unknown dependency")
        require(ident not in ticket["depends_on"], f"{ident}: self-dependency")
    visiting, visited = set(), set()

    def visit(ident):
        require(ident not in visiting, f"Dependency cycle at {ident}")
        if ident in visited:
            return
        visiting.add(ident)
        for parent in tickets[ident]["depends_on"]:
            visit(parent)
        visiting.remove(ident)
        visited.add(ident)

    for ident in tickets:
        visit(ident)
    for ident, ticket in tickets.items():
        if ticket["status"] in {"ready", "in_progress", "done"}:
            for parent in ticket["depends_on"]:
                dependency = tickets[parent]
                require(dependency["status"] == "done", f"{ident}: dependency {parent} is not done")
                require(
                    dependency["type"] != "decision" or dependency["decision"] == "proceed",
                    f"{ident}: decision {parent} does not permit proceeding",
                )
    table = root / "PRIORITIES.md"
    found, orders = set(), set()
    for line in table.read_text().splitlines():
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != 7 or not re.match(r"\[SOAM-\d{3}:", cells[1]):
            continue
        ident = re.search(ID, cells[1]).group()
        require(
            ident in tickets and ident not in found, f"Priority table: unknown/duplicate {ident}"
        )
        found.add(ident)
        require(
            cells[0].isdigit() and int(cells[0]) not in orders, f"{ident}: invalid/duplicate order"
        )
        orders.add(int(cells[0]))
        ticket = tickets[ident]
        expected = f"[{ident}: {ticket['title']}](tickets/{paths[ident].name})"
        require(cells[1] == expected, f"{ident}: priority-table title/link differs")
        require(
            cells[2:5] == [ticket["priority"], ticket["status"], ticket["milestone"]],
            f"{ident}: priority table metadata is stale",
        )
        require(
            cells[5] == ticket["recommended_thinking"],
            f"{ident}: priority-table thinking level is stale",
        )
        require(
            set(re.findall(ID, cells[6])) == set(ticket["depends_on"]),
            f"{ident}: priority-table dependencies differ",
        )
    require(found == tickets.keys(), f"Priority table missing tickets: {tickets.keys() - found}")
    for path in (
        table,
        root / "README.md",
        root / "docs/ROADMAP.md",
        root / "tickets/README.md",
        root / "tickets/TEMPLATE.md",
    ):
        check_links(path)
    template, _ = parse(root / "tickets/TEMPLATE.md")
    require(set(template) == FIELDS, "Ticket template fields differ from schema")
    templates = sorted((root / ".github/ISSUE_TEMPLATE").glob("*.md"))
    require(templates, "Missing native GitHub issue templates")
    for path in templates:
        header, _ = parse(path)
        require(
            set(header) == {"name", "about", "title", "labels", "assignees"},
            f"{path}: unexpected native template metadata",
        )
        require(
            isinstance(header["name"], str) and len(header["name"]) > 3 and header["about"],
            f"{path}: missing template name/about",
        )
    return len(tickets), len(templates)


if __name__ == "__main__":
    try:
        tickets, templates = validate()
    except (ValueError, TypeError, KeyError, OSError) as error:
        print(f"Ticket validation failed: {error}", file=sys.stderr)
        sys.exit(1)
    print(
        f"Validated {tickets} tickets, ordering/dependencies/links, and {templates} GitHub templates."
    )
