import os
import shutil
from .utils import run_cmd

def backup_boot_image(img_path):
    """Backup original boot image for safety"""
    backup_path = "boot_original.img"
    if not os.path.exists(backup_path):
        print("💾 Backing up original boot image...")
        shutil.copy2(img_path, backup_path)
        print(f"✅ Backup saved as {backup_path}")
    else:
        print("⚠️ Original boot image already backed up")

def unpack_boot(img_path, out_dir="ramdisk"):
    """Unpack boot image with safety checks"""
    try:
        backup_boot_image(img_path)
        
        if os.path.exists(out_dir):
            shutil.rmtree(out_dir)
            
        os.makedirs(out_dir)
        print(f"📂 Unpacking {img_path}...")
        run_cmd(f"unpackbootimg -i {img_path} -o {out_dir}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to unpack boot image: {str(e)}")
        return False

def inject_custom_su(ramdisk_dir):
    """Inject SU logic with SELinux disable"""
    try:
        # Create sbin dir if missing
        sbin_path = f"{ramdisk_dir}/sbin"
        os.makedirs(sbin_path, exist_ok=True)
        
        # Custom SU script with root detection
        su_script = """#!/sbin/sh
# Custom systemless root hook
if [ "$(id -u)" = "0" ]; then
    exec /sbin/sh -c "/system/bin/sh -c 'exec /sbin/su-daemon $@'" su $@
else
    echo '❌ Root denied'
    exit 1
fi"""
        
        with open(f"{sbin_path}/su", "w") as f:
            f.write(su_script)
            
        os.chmod(f"{sbin_path}/su", 0o755)
        print("✅ Custom SU binary injected")
        return True
        
    except Exception as e:
        print(f"❌ SU injection failed: {str(e)}")
        return False

def disable_selinux(ramdisk_dir):
    """Inject SELinux disable logic into init.rc"""
    try:
        init_rc = f"{ramdisk_dir}/init.rc"
        if not os.path.exists(init_rc):
            print("❌ init.rc not found in ramdisk")
            return False
            
        with open(init_rc, "a") as f:
            f.write("\n# Systemless Root Hooks\n")
            f.write("on early-init\n")
            f.write("    write /sys/fs/selinux/enforce 0\n")
            f.write("    exec u:r:untrusted_app:s0 root root -- /sbin/sh -c \"setenforce 0 || true\"\n")
            
        print("✅ SELinux disabled hooks injected")
        return True
        
    except Exception as e:
        print(f"❌ SELinux patch failed: {str(e)}")
        return False

def repack_boot(out_img="boot_patched.img", src_dir="ramdisk"):
    """Repack boot image with enhanced safety"""
    try:
        print("🔥 Repacking boot image with custom root logic...")
        
        # Ensure we have required files
        if not os.path.exists(f"{src_dir}/kernel"):
            print("❌ Kernel not found in ramdisk folder")
            return False
            
        if not os.path.exists(f"{src_dir}/ramdisk.cpio.gz"):
            print("❌ Ramdisk not found in ramdisk folder")
            return False

        # Read and modify cmdline
        with open(f"{src_dir}/cmdline", "r") as f:
            cmdline = f.read().strip()
            
        if "androidboot.selinux=permissive" not in cmdline:
            cmdline += " androidboot.selinux=permissive"

        # Repack with modified cmdline
        run_cmd(
            f"mkbootimg --kernel {src_dir}/zImage "
            f"--ramdisk {src_dir}/ramdisk.cpio.gz "
            f"--cmdline \"{cmdline}\" "
            f"--base 0x00000000 "
            f"-o {out_img}"
        )
                
        print(f"✅ Boot image repacked: {out_img}")
        return True
        
    except Exception as e:
        print(f"❌ Repack failed: {str(e)}")
        return False

def patch_boot(img_path):
    """Full patching workflow with safety checks"""
    print("🔧 Starting systemless root patching...")
    
    if not unpack_boot(img_path):
        return False
        
    if not inject_custom_su("ramdisk"):
        return False
        
    if not disable_selinux("ramdisk"):
        return False
        
    if not repack_boot():
        return False
        
    print("""
    🎉 Root patch complete!
    🔁 Flash the patched boot image using fastboot:
    fastboot flash boot boot_patched.img
    """)
    return True
