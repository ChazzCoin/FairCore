import os, json, platform, socket, re, uuid, logging, pwd, subprocess, inspect, shutil
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from F import CONVERT
from F import DICT

from F import LIST

MAC = "Darwin"
LINUX = "Linux"

def popen(*commands):
    process = subprocess.Popen(commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    stdout, stderr = process.communicate()
    return stdout

def run_system(command:str):
    try:
        return os.system(command)
    except:
        return "Unable to run command."

def run_command(*commands, stdout=True):
    commands = LIST.flatten(commands)
    try:
        if not stdout:
            return subprocess.run(commands, stdout=subprocess.PIPE, text=True)
        process = subprocess.run(commands, stdout=subprocess.PIPE, text=True)
        return process.stdout
    except:
        return "Unable to run command."

def move_file(fromFilePath, toFilePath):
    return shutil.move(fromFilePath, toFilePath)

def rename_file(fromFilePath, toFilePath):
    return os.rename(fromFilePath, toFilePath)

def get_os_variable(varName, default=False, toBool=False):
    try:
        raw = os.environ[varName]
        if toBool:
            c = CONVERT.TO_bool(raw)
            return c
        return raw
    except:
        return default

def test(env_file):
    env_vars = []  # or dict {}
    with open(env_file) as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            # if 'export' not in line:
            #     continue
            # Remove leading `export `, if you have those
            # then, split name / value pair
            # key, value = line.replace('export ', '', 1).strip().split('=', 1)
            key, value = line.strip().split('=', 1)
            # os.environ[key] = value  # Load to local environ
            # env_vars[key] = value # Save to a dict, initialized env_vars = {}
            env_vars.append({'name': key, 'value': value})  # Save to a list
    return env_vars

# test1 = test("TEST_BITCH")
# print(test1)

def set_environment_variable(variableName, variableValue):
    os.environ[variableName] = variableValue

# -> System
def run_os_system(strCommand:str):
    return os.system(strCommand)

def run_subprocess_popen(listOfCommands:[]):
    return subprocess.Popen(listOfCommands)

def get_module_path():
    try:
        i = inspect
        paths = DICT.get_from_path_keys(i, "sys", "path", default=False)
        return LIST.get(0, paths, default=False)
    except:
        return False

def get_module_name():
    module_path = get_module_path()
    return get_final_path_name(module_path)

def get_pid():
    return os.getpid()

def get_username():
    return LIST.get(0, pwd.getpwuid(os.getuid()), False)

def get_hostname():
    return socket.gethostname()

def get_os_kernel():
    return platform.system()

def get_os():
    kernel = get_os_kernel()
    if kernel == MAC:
        return "MacOS"
    elif kernel == LINUX:
        return "LinuxOS"
    return "Unknown"

def isMacOS():
    if get_os() == MAC:
        return True
    return False

def isLinuxOS():
    if get_os() == LINUX:
        return True
    return False

def get_architecture():
    return platform.machine()

def get_local_ip_address():
    return socket.gethostbyname(socket.gethostname())

def get_processor():
    return platform.processor()

def get_mac_address():
    return ':'.join(re.findall('..', '%012x' % uuid.getnode()))

def getFullSystemInfo():
    try:
        info = {}
        info['pid'] = get_pid()
        info['user'] = get_username()
        info['platform'] = platform.system()
        info['platform-release'] = platform.release()
        info['platform-version'] = platform.version()
        info['architecture'] = platform.machine()
        info['hostname'] = socket.gethostname()
        info['ip-address'] = socket.gethostbyname(socket.gethostname())
        info['mac-address'] = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        info['processor'] = platform.processor()
        return info
    except Exception as e:
        logging.exception(e)
        return False

# -> Files
def get_path(__file__:str):
    return os.path.dirname(__file__)

def get_cwd():
    return os.getcwd()

def get_final_path_name(path:str):
    count = len(path) -1
    slash_index = -1
    for i in range(count, 0, -1):
        char = path[i]
        if char == "/":
            return path[slash_index+1:]
        slash_index -= 1
    return False

def get_files_in_directory(module_path=None):
    mp = module_path if module_path else get_module_path()
    if mp:
        raw_items = os.scandir(mp)
    else:
        raw_items = os.scandir()
    files = []
    for item in raw_items:
        item: os.DirEntry = item
        if item.is_dir() or item.is_file():
            files.append(item.name)
    return files

def get_parent_directory():
    path = Path(os.getcwd())
    return path.parent.absolute().__str__()

def get_file_BY_searchTerm(sourceTerm, directoryPath=None):
    files = get_files_in_directory(directoryPath)
    for src in files:
        srcSmall = str(src).lower()
        sourceTermSmall = str(sourceTerm).lower()
        if srcSmall.__contains__(sourceTermSmall):
            file = directoryPath + f"/{src}"
            if src.endswith("_sources.txt"):
                source_list = get_file_contents(file, isUrls=True, randomize=True)
            else:
                source_list = get_file_contents(file)
            return source_list

def get_file_contents(file, isUrls=False, randomize=False):
    with open(file, 'r') as f:
        if file.endswith(".json"):
            return load_dict_from_file(file)
        if isUrls:
            https = "https://"
            items = [f"{https if not str(u).startswith('http') else ''}" + u.strip() for u in f.readlines()]
        else:
            items = [u.strip() for u in f.readlines()]
        return LIST.scramble(items) if not randomize else items

def save_dict_to_file(file_name, dic, file_path):
    try:
        with open(f'{file_path}/{file_name}.json', 'w') as f:
            json.dump(dic, f, sort_keys=True, indent=4)
        print(f"Saved File {file_name}.json to Data Directory")
    except Exception as e:
        print(f"Error saving dict. error=[ {e} ]")
        return None

def load_dict_from_file(file):
    try:
        file = open(file)
        data = json.load(file)
        return data
    except Exception as e:
        print(f"No File Found. error=[ {e} ]")
        return None