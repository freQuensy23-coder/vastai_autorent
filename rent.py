import subprocess
import re
import paramiko
from loguru import logger
def pickup_first_available_gpu(index_of_gpu):
    # Define the command
    cmd = """vastai search offers 'dph < 0.6 num_gpus=1 gpu_name=RTX_A6000 rented=False'"""

    # Run the command and capture output
    output = subprocess.check_output(cmd, shell=True, text=True)

    print('output is \n', output)
    # Parse the output to extract the IDs
    ids = re.findall(r'^(\d+)', output, re.MULTILINE)

    # Select the first ID
    if ids:
        first_id = ids[index_of_gpu]
        print(f"{index_of_gpu} ID:", first_id)
        return first_id
    else:
        print("No IDs found in the output.")



from config import VASTAPIKey
def activate_vastai_env():
    cmd = f"""vastai set api-key {VASTAPIKey}"""
    output = subprocess.check_output(cmd, shell=True, text=True)
    print('output is ', output)

def rent_gpu_by_id(first_id):
    cmd = f"""vastai create instance {first_id} --image pytorch/pytorch --disk 40 --env '-p 8081:80801/udp -h billybob' --ssh --direct --onstart-cmd "env | grep _ >> /etc/environment; echo 'starting up'";"""
    output = subprocess.check_output(cmd, shell=True, text=True)
    index_of_gpu = 1
    while 'no_such_ask' in output:
        ID_instance = pickup_first_available_gpu(index_of_gpu)
        cmd = f"""vastai create instance {ID_instance} --image pytorch/pytorch --disk 40 --env '-p 8081:80801/udp -h billybob' --ssh --direct --onstart-cmd "env | grep _ >> /etc/environment; echo 'starting up'";"""
        output = subprocess.check_output(cmd, shell=True, text=True)
        print('output is ', output)
    print("GPU was successfully rented!")


def get_current_machines():
    cmd = f"""vastai show instances"""
    output = subprocess.check_output(cmd, shell=True, text=True)
    print("output is ", output)
    # Регулярное выражение для извлечения значений SSH Addr и SSH Port
    elements = output.split('\n')
    if len(elements) < 2:
        return None
    # Нахождение индексов элементов 'SSH Addr' и 'SSH Port'
    parameters_of_machine = re.split('\s+', elements[1])
    ssh_addr = parameters_of_machine[9]
    ssh_port = parameters_of_machine[10]

    # Формирование строки из значений SSH Addr и SSH Port, разделенных пробелами
    result = f"{ssh_addr} {ssh_port}"
    print("Values of SSH Addr and SSH Port:", result)
    return ssh_addr, ssh_port


INSTALL_NGROK_CMD = """curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
  | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
  | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install ngrok"""
from config import NGROKToken
NGROK_ADD_CONF = f"""ngrok config add-authtoken {NGROKToken}"""

def connect_to_server(ssh_addr, ssh_port):
    # Подключение к удаленному серверу по SSH
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # Указание пути до приватного ключа
    private_key_path = './id_rsa'

    # Загрузка приватного ключа
    private_key = paramiko.RSAKey.from_private_key_file(private_key_path)
    ssh_client.connect(hostname=ssh_addr, port=ssh_port, username='root', pkey=private_key)

    # Выполнение команды на удаленном сервере
    commands = [
        "apt update && apt install wget",
        "wget --continue https://github.com/ollama/ollama/releases/download/v0.1.28/ollama-linux-amd64",
        "sudo chmod +x ollama-linux-amd64",
        "tmux new-session -d -s ollama_session './ollama-linux-amd64 serve'",
        "./ollama-linux-amd64 pull mixtral:8x7b-instruct-v0.1-q6_K",
        INSTALL_NGROK_CMD,
        NGROK_ADD_CONF,
        "ngrok http --domain=ray-evolved-gannet.ngrok-free.app 11434"
    ]

    last_command = "zrok share reserved %s localhost:11434"
    # Выполнение команд
    for command in commands:
        logger.info(f"Executing command: {command}")
        stdin, stdout, stderr = ssh_client.exec_command(command)

        # Ожидание завершения выполнения команды
        exit_status = stdout.channel.recv_exit_status()

        # Проверка успешности выполнения команды
        if exit_status != 0:
            logger.error(f"Command '{command}' failed with exit code {exit_status}")
            print("Output of the command:")
            for line in stderr:
                print(line.strip())
        else:
            logger.info(f"Command '{command}' executed successfully")
            result_last_command = stdout.read().decode('utf-8')
            logger.info(f"stdout of the following command is {result_last_command}")
            print("Output of the command:")
            for line in stdout:
                print(line.strip())

    stdin, stdout, stderr = ssh_client.exec_command(command)
    # Получение результатов выполнения команды
    print("Output of the command:")
    for line in stdout:
        print(line.strip())

    # Закрытие SSH-соединения
    ssh_client.close()

def wait_until_machine_started():
    cmd = f"""vastai show instances"""
    output = subprocess.check_output(cmd, shell=True, text=True)
    print("output is ", output)
    # Регулярное выражение для извлечения значений SSH Addr и SSH Port
    elements = output.split('\n')
    if len(elements) < 2:
        return None
    # Нахождение индексов элементов 'SSH Addr' и 'SSH Port'
    parameters_of_machine = re.split('\s+', elements[1])
    ID_INSTANCE = parameters_of_machine[0]
    status = parameters_of_machine[2]
    while status != "running":
        sleep(2)
        cmd = f"""vastai show instances"""
        output = subprocess.check_output(cmd, shell=True, text=True)
        print("output is ", output)
        # Регулярное выражение для извлечения значений SSH Addr и SSH Port
        elements = output.split('\n')
        if len(elements) < 2:
            return None
        # Нахождение индексов элементов 'SSH Addr' и 'SSH Port'
        parameters_of_machine = re.split('\s+', elements[1])
        status = parameters_of_machine[2]
        ID_INSTANCE = parameters_of_machine[0]
    sleep(2)
    logger.info(f"instance {ID_INSTANCE} successfully started")


def rent_and_setup_new_llm():
    activate_vastai_env()
    first_id = pickup_first_available_gpu(0)
    rent_gpu_by_id(first_id)
    ssh_addr, ssh_port = get_current_machines()
    sleep(1000)
    wait_until_machine_started() #TODO wait until status is running
    connect_to_server(ssh_addr, ssh_port)

# def rent_and_setup_new_llm_by_id(first_id):
#     ssh_addr, ssh_port = get_current_machines()
#     wait_until_machine_started() #TODO wait until status is running
#     connect_to_server(ssh_addr, ssh_port)


from time import sleep
if __name__ == "__main__":
    rent_and_setup_new_llm()
