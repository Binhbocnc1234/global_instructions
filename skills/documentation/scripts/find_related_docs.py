from __future__ import annotations

import argparse
from pathlib import Path
import sys

from docs_tool_lib import DOC_LINK_FIELDS, doc_identifiers, doc_link_points_to, load_docs, normalize_doc_id, value_list


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Find outgoing and incoming typed document links.")
    parser.add_argument("--id", required=True, help="Document id or file stem.")
    parser.add_argument("--root", default="./Documentation", help="Documentation root.")
    args = parser.parse_args()

    root = Path(args.root)
    if not root.exists():
        print(f"Documentation root not found: {root}")
        return 1

    docs = load_docs(root)
    target_id = normalize_doc_id(args.id)
    target_docs = [doc for doc in docs if target_id in doc_identifiers(doc)]
    rows = []

    for doc in docs:
        is_target_doc = doc in target_docs
        for field in DOC_LINK_FIELDS:
            links = value_list(doc.frontmatter.get(field))
            if is_target_doc:
                for item in links:
                    rows.append(("outgoing", field, str(doc.path.relative_to(root)), item))

            if any(doc_link_points_to(item, doc, target_doc) for item in links for target_doc in target_docs):
                rows.append(("incoming", field, str(doc.path.relative_to(root)), args.id))

    print("Direction\tField\tSource\tTarget")
    for row in sorted(rows):
        print("\t".join(row))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
