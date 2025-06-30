import argparse
import os
from sysroot.patcher import fix_boot_image
from sysroot.device import auto_detect_boot_image

def main():
    parser = argparse.ArgumentParser(description="SysRoot CLI - Native Systemless Root Tool")
    subparsers = parser.add_subparsers(dest="command")

    # Add commands
    subparsers.add_parser("auto-patch", help="Auto-detect boot image and patch")
    subparsers.add_parser("patch-boot", help="Patch boot image with SU")
    subparsers.add_parser("flash-boot", help="Flash patched boot image")

    args = parser.parse_args()

    if args.command == "auto-patch":
        from sysroot.patcher import fix_boot_image
        boot_img = auto_detect_boot_image()
        if not boot_img:
            boot_img = input("📁 Enter boot image path: ").strip()
        if fix_boot_image(boot_img):
            print("🎉 Patch complete!")
        else:
            print("❌ Patch failed")

    elif args.command == "patch-boot":
        from sysroot.patcher import patch_boot
        if patch_boot(args.bootimg):
            print("✅ Patch completed successfully!")
        else:
            print("❌ Patch failed")

    elif args.command == "flash-boot":
        from sysroot.device import flash_boot
        if os.path.exists(args.bootimg):
            flash_boot(args.bootimg)
        else:
            print("❌ Boot image not found")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
