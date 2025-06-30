from .utils import run_cmd

def check_fastboot():
    result = run_cmd("fastboot devices")
    return len(result.stdout.strip()) > 0

def reboot_bootloader():
    run_cmd("adb reboot bootloader")

def flash_boot(img_path):
    if not os.path.exists(img_path):
        print("❌ Boot image not found.")
        return False
    result = run_cmd(f"fastboot flash boot {img_path}")
    print(result.stdout)
