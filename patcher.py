import os
import shutil
from .utils import run_cmd

def fix_boot_image(img_path):
    if not os.path.exists(img_path):
        print("❌ Boot image not found")
        return False
    if not unpack_boot(img_path):
        return False
    if not inject_custom_su("ramdisk"):
        return False
    if not disable_selinux("ramdisk"):
        return False
    if not repack_boot():
        return False
    from .device import check_fastboot_connection, flash_boot
    if not check_fastboot_connection():
        print("❌ No fastboot device found")
        return False
    print("🔄 Flashing patched boot image...")
    flash_boot("boot_patched.img")
    return True

def backup_boot_image(img_path):
    backup_path = "boot_original.img"
    if not os.path.exists(backup_path):
        shutil.copy2(img_path, backup_path)

def unpack_boot(img_path, out_dir="ramdisk"):
    try:
        backup_boot_image(img_path)
        if os.path.exists(out_dir):
            shutil.rmtree(out_dir)
        os.makedirs(out_dir)
        run_cmd(f"unpackbootimg -i {img_path} -o {out_dir}")
        return True
    except Exception:
        return False

def inject_custom_su(ramdisk_dir):
    try:
        os.makedirs(f"{ramdisk_dir}/sbin", exist_ok=True)
        su_script = """#!/sbin/sh
if [ "$(id -u)" = "0" ]; then
    exec /sbin/sh -c "/system/bin/sh -c 'exec /system/bin/su $@'" su $@
else
    echo '❌ Root denied'
    exit 1
fi"""
        with open(f"{ramdisk_dir}/sbin/su", "w") as f:
            f.write(su_script)
        os.chmod(f"{ramdisk_dir}/sbin/su", 0o755)
        return True
    except Exception:
        return False

def disable_selinux(ramdisk_dir):
    try:
        init_rc = f"{ramdisk_dir}/init.rc"
        with open(init_rc, "a") as f:
            f.write("\non early-init\n")
            f.write("    write /sys/fs/selinux/enforce 0\n")
            f.write("    exec u:r:untrusted_app:s0 root root -- /sbin/sh -c \"setenforce 0\"\n")
        return True
    except Exception:
        return False

def repack_boot(out_img="boot_patched.img", src_dir="ramdisk"):
    try:
        if not os.path.exists(f"{src_dir}/kernel"):
            return False
        if not os.path.exists(f"{src_dir}/ramdisk.cpio.gz"):
            return False
        with open(f"{src_dir}/cmdline", "r") as f:
            cmdline = f.read().strip()
        if "androidboot.selinux=permissive" not in cmdline:
            cmdline += " androidboot.selinux=permissive"
        run_cmd(
            f"mkbootimg --kernel {src_dir}/zImage "
            f"--ramdisk {src_dir}/ramdisk.cpio.gz "
            f"--cmdline \"{cmdline}\" "
            f"--base 0x00000000 -o {out_img}"
        )
        return True
    except Exception:
        return False
