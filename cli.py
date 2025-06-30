import argparse
import os
from sysroot.patcher import patch_boot, inject_custom_su, repack_boot, unpack_boot

def main():
    parser = argparse.ArgumentParser(description="SysRoot CLI - Native Systemless Root Tool")
    subparsers = parser.add_subparsers(dest="command")

    # patch-boot command
    patch_parser = subparsers.add_parser("patch-boot", help="Patch boot image with SU")
    patch_parser.add_argument("bootimg", help="Path to stock boot image")

    # inject-su command
    inject_parser = subparsers.add_parser("inject-su", help="Inject SU binary into unpacked ramdisk")
    inject_parser.add_argument("ramdisk_dir", help="Path to unpacked ramdisk folder")

    # detect-fastboot command
    subparsers.add_parser("detect-fastboot", help="Detect fastboot device")

    # flash-boot command (for flashing)
    flash_parser = subparsers.add_parser("flash-boot", help="Flash patched boot image")
    flash_parser.add_argument("bootimg", help="Path to patched boot image")

    args = parser.parse_args()

    if args.command == "patch-boot":
        if patch_boot(args.bootimg):
            print("✅ Patch completed successfully!")
        else:
            print("❌ Patch failed. Check logs.")

    elif args.command == "inject-su":
        if os.path.isdir(args.ramdisk_dir):
            if inject_custom_su(args.ramdisk_dir):
                print("✅ SU injected into ramdisk")
            else:
                print("❌ SU injection failed")
        else:
            print("❌ Ramdisk folder does not exist")

    elif args.command == "detect-fastboot":
        from sysroot.device import check_fastboot_connection
        if check_fastboot_connection():
            print("📱 Fastboot device detected.")
        else:
            print("❌ No fastboot device found.")

    elif args.command == "flash-boot":
        from sysroot.device import flash_boot
        if os.path.exists(args.bootimg):
            flash_boot(args.bootimg)
        else:
            print("❌ Boot image file not found")

    else:
        parser.print_help()
