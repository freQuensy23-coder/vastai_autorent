import subprocess
import re


def pickup_first_available_gpu():
    # Define the command
    cmd = """vastai search offers 'reliability > 0.98 num_gpus=1 gpu_name=RTX_3090 rented=False'"""

    # Run the command and capture output
    output = subprocess.check_output(cmd, shell=True, text=True)

    print('output is ', output)
    # Parse the output to extract the IDs
    ids = re.findall(r'^(\d+)', output, re.MULTILINE)

    # Select the first ID
    if ids:
        first_id = ids[0]
        print("First ID:", first_id)
    else:
        print("No IDs found in the output.")

    return first_id


def rent_gpu_by_id(first_id):
    cmd = f"""vastai create instance {first_id} --image openziti/zrok --ssh --direct --env '-e ZROK_ENABLE_TOKEN=GkaGItMPbZ' --onstart-cmd 'apt-get update && apt install wget && wget https://github.com/ollama/ollama/releases/download/v0.1.28/ollama-linux-amd64 && cd ollama-linux-amd64 && ./ollama-linux-amd64 pull mixtral:8x7b-instruct-v0.1-q6_K
&& ./ollama-linux-amd64 serve & && zrok share public localhost:11434'"""
    output = subprocess.check_output(cmd, shell=True, text=True)

    print('output is ', output)


if __name__ == "__main__":
    first_id = pickup_first_available_gpu()
    rent_gpu_by_id(first_id)
