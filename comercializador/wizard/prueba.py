import subprocess

result = subprocess.run(["./script.sh"], capture_output=True, shell=True, text=True)


print(result.stdout)