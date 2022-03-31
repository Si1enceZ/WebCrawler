import os
import threading
import platform


def run(f):
    # Check OS info
    if platform.system() == 'Windows':
        os.system('python script/' + f)
    elif platform.system() == 'Linux':
        os.system('python3 script/' + f)


if __name__ == '__main__':
    try:
        os.makedirs('data')
        os.makedirs('log')
    except FileExistsError:
        pass
    files = os.listdir('script')
    for file in files:
        if file.endswith('.py'):
            t = threading.Thread(target=run, args=[file])
            t.start()
