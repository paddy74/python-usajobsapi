"""Generate the code reference pages."""

from pathlib import Path

import mkdocs_gen_files


def gen_ref_pages(root_dir, source_dir, output_dir) -> None:
    for path in sorted(source_dir.rglob("*.py")):
        module_path = path.relative_to(source_dir).with_suffix("")
        doc_path = path.relative_to(source_dir).with_suffix(".md")
        full_doc_path = Path(output_dir, doc_path)

        module_parts = module_path.parts

        if module_parts[-1] == "__main__":
            continue
        if module_parts[-1] == "__init__":
            module_parts = module_parts[:-1]

        full_parts = (source_dir.name,) + module_parts
        if not module_parts:
            identifier = source_dir.name
        else:
            identifier = ".".join(full_parts)

        with mkdocs_gen_files.open(full_doc_path, "w") as fd:
            print("::: " + identifier, file=fd)

        mkdocs_gen_files.set_edit_path(full_doc_path, path.relative_to(root_dir))


root = Path(__file__).parent.parent
src = root / "usajobsapi"
gen_ref_pages(root, src, "ref")
