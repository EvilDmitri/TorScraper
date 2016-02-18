import time
import datetime

import tor_controller

tor = tor_controller.Tor()
tor.connect()


def clear_old_circuits():
    status = tor.getinfo("circuit-status").split('\r\n')
    if len(status) > 2:
        for item in status[1:]:
            print item
            if item == '.':
                break
            close(item.split()[0])
    else:
        first_line = status[0].split('=')
        if len(first_line) > 1 and first_line[1] != u'':
            # There is only one circuit
            close(status[0].split('=')[1].split()[0])


def close(number):
    tor.closecircuit(number)


# def extend():
#     tor.extendcircuit('0')


def write(data_str):
    with open('data.txt', 'a') as data_file:
        data_file.write(data_str + '\n')


def get_from_fingerprint(relay_hash):
    router = tor.getinfo('dir/server/fp/' + relay_hash).split('\r\n')
    for line in router:
        if line.startswith('router '):
            ip = line.split()[2]
            return ip
    return ''


def ip_to_country(ip):
    answer = tor.getinfo('ip-to-country/' + ip).split('\r\n')[0]
    print 'country', answer
    return answer.split('=')[1]


def get_data():
    data = ''
    tor.extendcircuit('0')
    data += str(datetime.datetime.now()).split('.')[0] + ' '

    status = tor.getinfo("circuit-status")
    circuit_number = status.split(' ')[0]
    circuit_hashes = status.split(' ')[2].split(',')

    for hash in circuit_hashes:
        ip = ''
        relay_name = hash.split('~')[1]
        relay_hash = hash.split('~')[0]
        if relay_name != 'Unnamed':
            # print tor.getinfo('version desc/name/' + relay_name)
            router = tor.getinfo('version desc/name/' + relay_name).split('\r\n')
            # print router
            for line in router:
                if line.startswith('router '):
                    print line
                    ip = line.split()[2]
            if ip == '':
                ip = get_from_fingerprint(relay_hash[1:])
        else:
            ip = get_from_fingerprint(relay_hash[1:])

        country = ip_to_country(ip)
        data += ip + ':' + country + ','

    if data.endswith(','):
        data = data[:-1]

    write(data)

    close(circuit_number)


if __name__ == '__main__':
    tor.setconf('FetchUselessDescriptors', '1')

    for num in xrange(0, 25000):
        clear_old_circuits()
        get_data()

    tor.close()
