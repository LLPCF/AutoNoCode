import logging
import logging
import logging
import os
import subprocess

logger = logging.getLogger(__name__)

# Caminho esperado para npm
npm_path = r"C:\Program Files\nodejs\npm.cmd"

def check_npm() -> None:
    try:
        if os.path.exists(npm_path):
            logger.info(f"npm found at: {npm_path}")

            # Executa o comando 'npm audit fix'
            result = subprocess.run(
                [npm_path, "audit", "fix"], capture_output=True, text=True
            )
            if result.returncode == 0:
                logger.info("npm audit fix executed successfully.")
                logger.info(result.stdout)
            else:
                logger.error("npm audit fix failed.")
                logger.error(result.stderr)
        else:
            logger.error("npm not found at the expected location")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    return None  # Add this line

if __name__ == "__main__":
    check_npm()
    logger.info("NPM check script executed successfully.")
