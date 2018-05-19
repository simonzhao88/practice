import redis


def main():
    client = redis.Redis(host='47.106.136.74', port=8001, password='simon@88')
    if client.ping():
        print(client.keys('*'))
        print(client.get('username').decode('utf-8'))
        print(client.get('password').decode('utf-8'))
        print(list(map(lambda x: x.decode('utf-8'),
                       client.zrange('fba', start=0, end=-1))))


if __name__ == '__main__':
    main()
