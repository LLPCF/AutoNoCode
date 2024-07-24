import subprocess

class Maintenance:
    def __init__(self) -> None:
        self.npm_path = "C:\\Program Files\\nodejs\\npm.cmd"

    def run_npm_audit_fix(self) -> None:
        print("Running npm audit fix...")
        try:
            print(f"Executing command: {self.npm_path} audit fix")
            result = subprocess.run(
                ["cmd", "/c", self.npm_path, "audit", "fix"],
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                print(
                    f"npm audit fix failed with the following output:\n{result.stdout}\n{result.stderr}"
                )
            else:
                print("npm audit fix completed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"npm audit fix failed: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def check_npm_installation(self) -> bool:
        try:
            print(f"Executing command: {self.npm_path} --version")
            result = subprocess.run(
                ["cmd", "/c", self.npm_path, "--version"],
                capture_output=True,
                text=True,
            )
            print(f"npm version: {result.stdout.strip()}")
            return True
        except FileNotFoundError:
            print("npm is not installed or not found in PATH.")
            return False
        except subprocess.CalledProcessError as e:
            print(f"Error checking npm installation: {e}")
            return False

    def perform_maintenance(self) -> None:
        if self.check_npm_installation():
            self.run_npm_audit_fix()

def main() -> None:
    maintenance = Maintenance()
    maintenance.perform_maintenance()

if __name__ == "__main__":
    main()
