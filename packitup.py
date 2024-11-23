import argparse
import os
import shutil
import sys



def main():
    parser = argparse.ArgumentParser(
        prog = "packitup",
        description = "Creates a directory with pygamengn code and assets for one of the samples.",
    )
    parser.add_argument(
        "-s", "--sample-dir",
        help = "Path to the directory where the code for the sample lives.",
        required = True
    )
    parser.add_argument(
        "-a", "--assets-dir",
        help = "Path to the directory where the assets live. Relative to the value of --sample-dir parameter.",
        default = "../Assets"
    )
    parser.add_argument(
        "-i", "--inventory-dir",
        help = "Path to the sample's inventory directory. Relative to the value of --sample-dir parameter.",
        default = "src"
    )
    parser.add_argument(
        "-o", "--out",
        help = "Output directory.",
        default = "."
    )

    args = parser.parse_args()

    sys.path.append(os.path.join(args.sample_dir, args.inventory_dir))
    from inventory.inventory import fonts, images, sounds

    sample_name = os.path.split(args.sample_dir)[-1]
    out_dir = os.path.join(args.out, sample_name)

    # Create output directory
    try:
        os.makedirs(out_dir)
    except FileExistsError:
        print(f"Output directory {out_dir} already exists. Delete it or use one that doesn't exist.")
        return

    # Copy files
    shutil.copyfile("main.py", os.path.join(out_dir, "main.py"))
    shutil.copyfile("favicon.png", os.path.join(out_dir, "favicon.png"))
    shutil.copytree(
        args.sample_dir,
        os.path.join(out_dir, "Samples", sample_name),
        dirs_exist_ok = True,
        ignore = shutil.ignore_patterns("__pycache__")
    )

    # Copy assets
    assets_in_dir = os.path.join(args.sample_dir, args.assets_dir)
    assets_out_dir = os.path.join(out_dir, "Samples", "Assets")
    copy_asset_list(fonts.values(), assets_in_dir, assets_out_dir)
    copy_asset_list(images.values(), assets_in_dir, assets_out_dir)
    copy_asset_list(sounds.values(), assets_in_dir, assets_out_dir)

    # Copy pygamengn source code
    shutil.copytree(
        os.path.join(args.sample_dir, "..", "..", "src"),
        os.path.join(out_dir, "src"),
        dirs_exist_ok = True,
        ignore = shutil.ignore_patterns("__pycache__")
    )


def copy_asset_list(assets: list[str], in_dir: str, out_dir: str):
    for asset in assets:
        asset_out_dir = os.path.dirname(os.path.join(out_dir, asset))
        if not os.path.isdir(asset_out_dir):
            os.makedirs(asset_out_dir)
        shutil.copyfile(os.path.join(in_dir, asset), os.path.join(out_dir, asset))




if __name__ == "__main__":
    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
    main()
