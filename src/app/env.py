DATABASE_URL = 'postgresql+asyncpg://alexey_yamushev:Aliluya_312@localhost/postgres'  # Полный путь подключения БД 
REDIS_URL = 'redis://localhost:6379?decode_responses=True'  # Полный путь подключения redis
SECRET_KEY = 'opigiyfdrsrdtfyuhj0i0=65er6yuijokpu9t7657e6dtfyguhijo8t76e54drtfvbjnjo7t6rdtrtcgvhbjnkmkpiu98yt7fyvhbjkkpgyg'  # Секретный ключ для JWT
ALGORITHM = 'HS256'  # Алгоритм JWT
ACCESS_TOKEN_EXPIRE_MINUTES = 15 # Время экспирации токена в минутах
COCKIE_MAX_AGE = 60 * ACCESS_TOKEN_EXPIRE_MINUTES # Время жизни куки в браузере в секундах
REDIS_CACHE_EXP = 60 * ACCESS_TOKEN_EXPIRE_MINUTES # Время жизни записи в редисе в секундах
PASS_SALT = 'pkjhgyftdrsetdrftgh87468ryiueiwkvuhyibrhfnjdksfomewlfIHUGYFTDYFGHIJugyftvghbjfgyweshf'  # Соль для хеширования паролей