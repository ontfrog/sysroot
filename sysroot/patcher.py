import os
from .utils import run_cmd

def unpack_boot(img_path, out_dir="ramdisk"):
    os.makedirs(out_dir, exist_ok=True)
    run_cmd(f"unpackbootimg -i {img_path} -o {out_dir}")

def repack_boot(out_img="boot_patched.img", src_dir="ramdisk"):
    run_cmd(f"mkbootimg --kernel {src_dir}/zImage --ramdisk {src_dir}/ramdisk.cpio.gz "
            f"--cmdline \"$(cat {src_dir}/ cmdline)\" --base 0x00000000 -o {out_img}")

def inject_su(ramdisk_dir):
    su_script = """#!/sbin/sh
    exec /sbin/su-daemon $@"""

    with open(f"{ramdisk_dir}/sbin/su", "w") as f:
        f.write(su_script)

    os.chmod(f"{ramdisk_dir}/sbin/su", 0o755)
    print("✅ SU script injected into ramdisk.")
