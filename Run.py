import os
import threading


def run(f):
    os.system('python script/' + f)


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
