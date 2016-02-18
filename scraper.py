import time
import datetime

import tor_controller
tor = tor_controller.Tor()
tor.connect()


def clear_old_circuits():
    status = tor.getinfo("circuit-status").split('\r\n')
    # print status
    if len(status) > 2:
        for item in status[1:]:
            if item == '.':
                break
            close(item.split()[0])
    else:
        first_line = status[0].split('=')
        if len(first_line) > 1 and first_line[1] != u'':
            # There is a one circuit
            close(status[0].split('=')[1].split()[0])


def close(number):
    tor.closecircuit(number)


# def extend():
#     tor.extendcircuit('0')


def write(data_str):
    with open('data.txt', 'a') as data_file:
        data_file.write(data_str)


def get_data():
    data = ''
    # tor.extendcircuit('0')
    # time.sleep(0.8)  # circuit should be established
    # data += str(datetime.datetime.now()).split('.')[0] + ' '
    status = tor.getinfo("circuit-status")
    # print status
    circuit_number = status.split(' ')[0]
    circuit_hashes = status.split(' ')[2].split(',')
    print circuit_hashes
    for hash in circuit_hashes:
        relay_name = hash.split('~')[1]

        if relay_name != 'Unnamed':
            router = tor.getinfo('version desc/name/' + relay_name).split('\r\n')[2]
            print router
            if router.startswith('router'):
                ip = router.split()[2]
                print ip, '\n'
            else:
                relay_hash = hash.split('~')[0]
                relay_hash = relay_hash[1:]
                router = tor.getinfo('dir/server/fp/' + relay_hash).split('\r\n')[1]
                # print router
                if router.startswith('router'):
                    ip = router.split()[2]
                    print ip, '\n'

if __name__ == '__main__':
    # clear_old_circuits()
    get_data()

    tor.close()
