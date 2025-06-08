from enum import StrEnum
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent

DEFAULT_CODE_PATH = "src/main/java/com/cerbon"
DEFAULT_RESOURCES_PATH = "src/main/resources"


class Project(StrEnum):
    COMMON = "Common"
    FABRIC = "Fabric"
    FORGE = "Forge"
    NEOFORGE = "NeoForge"


def get_common_code_path(project: Project) -> Path:
    return ROOT_DIR / project / DEFAULT_CODE_PATH


def get_common_resources_path(project: Project) -> Path:
    return ROOT_DIR / project / DEFAULT_RESOURCES_PATH


def rename_folder_structure(project: Project, mod_id: str) -> Path:
    try:
        code_path = get_common_code_path(project)
        ml_template_folder = code_path / "ml_template"
        return ml_template_folder.rename(code_path / mod_id)

    except Exception as e:
        print(f"Error trying to rename folder structure for project {project} with mod id {mod_id}: {e}")


def update_file(file_path: Path, mod_id: str, mod_name: str):
    try:
        with open(file_path, "r+", encoding="utf-8") as f:
            content = f.read()
            content = content.replace("ml_template", mod_id)
            content = content.replace("ModName", mod_name)
            content = content.replace("ML Template", mod_name)
            f.seek(0)
            f.write(content)
            f.truncate()
        # Print only the file name in the updated file message.
        print(f"Updated file: {file_path.name}")

    except Exception as e:
        print(f"Error updating file {file_path}: {e}")


def update_mixin(project: Project, mod_id: str, mod_name: str, resources_dir: Path):
    if project == Project.COMMON:
        mixin = resources_dir / "ml_template-common.mixins.json"
    else:
        mixin = resources_dir / "ml_template.mixins.json"

    update_file(mixin, mod_id, mod_name)

    if project == Project.COMMON:
        mixin_renamed = resources_dir / f"{mod_id}-common.mixins.json"
    else:
        mixin_renamed = resources_dir / f"{mod_id}.mixins.json"

    try:
        mixin.rename(mixin_renamed)
        # Print the rename operation with only file names.
        print(f"Renamed file: from {mixin.name} to {mixin_renamed.name}")
    except Exception as e:
        print(f"Error renaming mixin file for {project} project: {e}")


def configure_common(mod_id: str, mod_name: str):
    try:
        print(f"Configuring {Project.COMMON} project")

        # Code Update
        code_dir = rename_folder_structure(Project.COMMON, mod_id)
        update_file(code_dir / "ModName.java", mod_id, mod_name)
        update_file(code_dir / "platform/Services.java", mod_id, mod_name)
        update_file(code_dir / "mixin/test/TestMixin.java", mod_id, mod_name)

        mod_name_file = code_dir / "ModName.java"
        mod_name_file_renamed = mod_name_file.rename(code_dir / f"{mod_name}.java")
        print(f"Renamed file: from {mod_name_file.name} to {mod_name_file_renamed.name}")

        # Resources Update
        resources_dir = get_common_resources_path(Project.COMMON)
        update_file(resources_dir / "architectury.common.json", mod_id, mod_name)

        ml_template_accesswidener_file = resources_dir / "ml_template.accesswidener"
        new_accesswidener_file = resources_dir / f"{mod_id}.accesswidener"
        ml_template_accesswidener_file.rename(new_accesswidener_file)
        print(f"Renamed file: from {ml_template_accesswidener_file.name} to {new_accesswidener_file.name}")

        update_mixin(Project.COMMON, mod_id, mod_name, resources_dir)
        print()

    except Exception as e:
        print(f"Error configuring {Project.COMMON} project: {e}")


def configure_fabric(mod_id: str, mod_name: str):
    try:
        print(f"Configuring {Project.FABRIC} project")

        # Code Update
        code_dir = rename_folder_structure(Project.FABRIC, mod_id) / 'fabric'
        update_file(code_dir / "ModNameFabric.java", mod_id, mod_name)
        update_file(code_dir / "mixin/test/TestMixin.java", mod_id, mod_name)

        mod_name_file = code_dir / "ModNameFabric.java"
        mod_name_file_renamed = mod_name_file.rename(code_dir / f"{mod_name}Fabric.java")
        print(f"Renamed file: from {mod_name_file.name} to {mod_name_file_renamed.name}")

        # Resources update
        resources_dir = get_common_resources_path(Project.FABRIC)
        update_mixin(Project.FABRIC, mod_id, mod_name, resources_dir)
        update_file(resources_dir / "fabric.mod.json", mod_id, mod_name)
        print()

    except Exception as e:
        print(f"Error configuring {Project.FABRIC} project: {e}")


def configure_forge(mod_id: str, mod_name: str):
    try:
        print(f"Configuring {Project.FORGE} project")

        # Code Update
        code_dir = rename_folder_structure(Project.FORGE, mod_id) / 'forge'
        update_file(code_dir / "ModNameForge.java", mod_id, mod_name)
        update_file(code_dir / "mixin/test/TestMixin.java", mod_id, mod_name)

        mod_name_file = code_dir / "ModNameForge.java"
        mod_name_file_renamed = mod_name_file.rename(code_dir / f"{mod_name}Forge.java")
        print(f"Renamed file: from {mod_name_file.name} to {mod_name_file_renamed.name}")

        # Resources update
        resources_dir = get_common_resources_path(Project.FORGE)
        update_mixin(Project.FORGE, mod_id, mod_name, resources_dir)
        print()

    except Exception as e:
        print(f"Error configuring {Project.FORGE} project: {e}")


def configure_neoforge(mod_id: str, mod_name: str):
    try:
        print(f"Configuring {Project.NEOFORGE} project")

        # Code Update
        code_dir = rename_folder_structure(Project.NEOFORGE, mod_id) / 'neoforge'
        update_file(code_dir / "ModNameNeo.java", mod_id, mod_name)
        update_file(code_dir / "mixin/test/TestMixin.java", mod_id, mod_name)

        mod_name_file = code_dir / "ModNameNeo.java"
        mod_name_file_renamed = mod_name_file.rename(code_dir / f"{mod_name}Neo.java")
        print(f"Renamed file: from {mod_name_file.name} to {mod_name_file_renamed.name}")

        # Resources update
        resources_dir = get_common_resources_path(Project.NEOFORGE)
        update_mixin(Project.NEOFORGE, mod_id, mod_name, resources_dir)
        print()

    except Exception as e:
        print(f"Error configuring {Project.NEOFORGE} project: {e}")


if __name__ == "__main__":
    mod_id = "bclib"
    mod_name = "Bclib"

    configure_common(mod_id, mod_name)
    configure_fabric(mod_id, mod_name)
    configure_forge(mod_id, mod_name)
    configure_neoforge(mod_id, mod_name)
