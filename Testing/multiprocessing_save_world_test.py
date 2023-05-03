import multiprocessing


def print_func(continent='Asia'):
    print('The name of continent is : ', continent)

if __name__ == "__main__":  # confirms that the code is under main function
    names = ['America', 'Europe', 'Africa']
    procs = []
    proc = multiprocessing.Process(target=print_func)  # instantiating without any argument
    procs.append(proc)
    proc.start()

    # instantiating process with arguments
    for name in names:
        # print(name)
        proc = multiprocessing.Process(target=print_func, args=(name,))
        procs.append(proc)
        proc.start()
    print_func("BBB")

    # complete the processes
    for proc in procs:
        proc.join()