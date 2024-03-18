import redis

class RedisCache:
    def __init__(self,username,password,host,port):
        self.username = str(username)
        self.password = str(password)
        self.host=str(host)
        self.port=str(port)

    def create_connection(self):
        creds_provider = redis.UsernamePasswordCredentialProvider(username=self.username, password=self.password)
        conn=redis.Redis(host=self.host, port=self.port, credential_provider=creds_provider)
        print(conn.ping())
        return conn

      
    
        