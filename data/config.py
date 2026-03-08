from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env('./envs/.env')

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot toekn
ADMINS = env.list("ADMINS")
IP = env.str("ip")
NAME = env.str("NAME")
USER = env.str("USER")
PASSWORD = env.str("PASSWORD")
HOST = env.str("HOST")
PORT = env.str("PORT")


