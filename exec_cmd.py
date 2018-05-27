import logging
import subprocess

logger = logging.getLogger(__file__)

def run(cmd):
    stdout=None
    error=False
    try:
        p = subprocess.run(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding='utf-8')  # type: subprocess.CompletedProcess
        stdout=p.stdout
    except subprocess.CalledProcessError as e:
        logger.error("Received non-zero code %s", e.returncode)
        error=True
        stdout=p.stdout

    for line in p.stdout.split('\n'):
        logger.info('> %s', line)

    if error:
        raise RuntimeError("Command returned non-zero code")

