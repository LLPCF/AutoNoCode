import logging
import logging
import logging
import logging
import logging
import logging
import logging
import logging
import logging
logger = logging.getLogger(__name__)
import os
import subprocess

# Caminho esperado para npm
npm_path = r"C:\Program Files\nodejs\npm.cmd"

def check_npm() -> None:
    try:
        if os.path.exists(npm_path):
            print(f"npm found at: {npm_path}")

            # Executa o comando 'npm audit fix'
            result = subprocess.run(
                [npm_path, "audit", "fix"], capture_output=True, text=True
            )
            if result.returncode == 0:
                print("npm audit fix executed successfully.")
                print(result.stdout)
            else:
                print("npm audit fix failed.")
                print(result.stderr)
        else:
            print("npm not found at the expected location")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    check_npm()
    print("NPM check script executed successfully.")
