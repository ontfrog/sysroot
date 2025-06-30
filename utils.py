def run_cmd(cmd: str):
    import subprocess
    print(f"⚙️ Running: {cmd}")
    return subprocess.run(cmd.split(), capture_output=True, text=True)

def confirm(prompt="Continue?"):
    return input(f"{prompt} (y/N): ").lower().strip() in ["y", "yes"]
