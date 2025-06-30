from .utils import run_cmd

def auto_detect_boot_image():
    print("🔍 Detecting boot image source...")
    result = run_cmd("adb shell getprop ro.boot.mode")
    if "recovery" in result.stdout:
        print("📱 Device in recovery mode. Trying extraction...")
        result = run_cmd("adb backup -f boot_backup.ab -noapk com.android.recovery")
        if result.returncode != 0:
            return None
        result = run_cmd("dd if=boot_backup.ab bs=24 skip=1 of=boot_stock.img")
        if result.returncode != 0:
            return None
        return "boot_stock.img"
    return None

def check_fastboot_connection():
    result = run_cmd("fastboot devices")
    return bool(result.stdout.strip())

def flash_boot(img_path):
    print("🔄 Flashing boot image...")
    run_cmd(f"fastboot flash boot {img_path}")
    run_cmd("fastboot reboot")
