import json
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


def update_mixin(project: Project, mod_id: str, resources_dir: Path):
    if project == Project.COMMON:
        mixin = resources_dir / "ml_template-common.mixins.json"

    else:
        mixin = resources_dir / "ml_template.mixins.json"

    with open(mixin, 'r+') as f:
        mixin_json = json.load(f)
        mixin_json["package"] = str(mixin_json["package"]).replace("ml_template", mod_id)
        f.seek(0)
        json.dump(mixin_json, f, indent=2)
        f.truncate()
        print(f"Updated mixin file from {project} project")

    mixin_renamed = resources_dir / f"{mod_id}-common.mixins.json" if project == Project.COMMON else resources_dir / f"{mod_id}.mixins.json"

    mixin.rename(mixin_renamed)
    print(f"Renamed mixin file from {project} project to {mixin_renamed}")


def updated_java_file(java_path: Path, mod_id: str, mod_name: str):
    with open(java_path, "r+") as f:
        java_code = f.read()
        java_code = java_code.replace("ml_template", mod_id)
        java_code = java_code.replace("ModName", mod_name)
        java_code = java_code.replace("ML Template", mod_name)
        f.seek(0)
        f.write(java_code)
        f.truncate()


def configure_common(mod_id: str, mod_name: str):
    try:
        print(f"Configuring {Project.COMMON} project")

        # Code Update
        code_dir = rename_folder_structure(Project.COMMON, mod_id)
        updated_java_file(code_dir / "ModName.java", mod_id, mod_name)
        updated_java_file(code_dir / "platform/Services.java", mod_id, mod_name)
        updated_java_file(code_dir / "mixin/test/TestMixin.java", mod_id, mod_name)

        mod_name_file = code_dir / "ModName.java"
        mod_name_file.rename(code_dir / f"{mod_name}.java")

        # Resources Update
        resources_dir = get_common_resources_path(Project.COMMON)
        with open(resources_dir / "architectury.common.json", "r+") as f:
            architecture_json = json.load(f)
            architecture_json["accessWidener"] = f"{mod_id}.accesswidener"
            f.seek(0)
            json.dump(architecture_json, f, indent=2)
            f.truncate()
            print("Updated architectury.common.json file")

        ml_template_accesswidener_file = resources_dir / "ml_template.accesswidener"
        ml_template_accesswidener_file.rename(resources_dir / f"{mod_id}.accesswidener")
        print("Renamed accesswidener")

        update_mixin(Project.COMMON, mod_id, resources_dir)

    except Exception as e:
        print(f"Error configuring {Project.COMMON} project: {e}")


def configure_fabric(mod_id: str, mod_name: str):
    print(f"Configuring {Project.FABRIC} project")

    # Code Update
    code_dir = rename_folder_structure(Project.FABRIC, mod_id) / 'fabric'
    updated_java_file(code_dir / "ModNameFabric.java", mod_id, mod_name)
    updated_java_file(code_dir / "mixin/test/TestMixin.java", mod_id, mod_name)

    # Resources update
    resources_dir = get_common_resources_path(Project.FABRIC)
    update_mixin(Project.FABRIC, mod_id, resources_dir)
    with open(resources_dir / "fabric.mod.json", "r+") as f:
        fabric_mod_file = f.read()
        fabric_mod_file = fabric_mod_file.replace("ml_template", mod_id)
        fabric_mod_file = fabric_mod_file.replace("ModName", mod_name)
        f.seek(0)
        f.write(fabric_mod_file)
        f.truncate()

    mod_name_file = code_dir / "ModNameFabric.java"
    mod_name_file.rename(code_dir / f"{mod_name}Fabric.java")


def configure_forge():
    pass


def configure_neoforge():
    pass


if __name__ == "__main__":
    configure_fabric("bclib", "Bclib")
