import argparse
from .device import check_fastboot, reboot_bootloader, flash_boot
from .patcher import unpack_boot, repack_boot, inject_su

def main():
    parser = argparse.ArgumentParser(description="SysRoot CLI - Native Systemless Root Tool")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("detect-fastboot", help="Detect fastboot device")
    subparsers.add_parser("reboot-bootloader", help="Reboot to bootloader")
    boot_parser = subparsers.add_parser("extract-boot", help="Extract boot image")
    boot_parser.add_argument("bootimg", help="Path to boot.img file")

    patch_parser = subparsers.add_parser("patch-boot", help="Patch boot image with SU")
    patch_parser.add_argument("bootimg", help="Path to boot.img file")

    flash_parser = subparsers.add_parser("flash-boot", help="Flash patched boot image")
    flash_parser.add_argument("bootimg", help="Path to patched boot image")

    args = parser.parse_args()

    if args.command == "detect-fastboot":
        if check_fastboot():
            print("📱 Fastboot device detected.")
        else:
            print("❌ No fastboot device found.")

    elif args.command == "reboot-bootloader":
        reboot_bootloader()

    elif args.command == "extract-boot":
        unpack_boot(args.bootimg)
        print("📂 Boot image extracted.")

    elif args.command == "patch-boot":
        unpack_boot(args.bootimg)
        inject_su("ramdisk")
        repack_boot()
        print("🔥 Boot image patched with SU.")

    elif args.command == "flash-boot":
        flash_boot(args.bootimg)

    else:
        parser.print_help()
