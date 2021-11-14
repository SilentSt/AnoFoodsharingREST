class SettingsApp:
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    ALGORITHM = "HS256"
    JWT_SECRET = "b216cc83cccf75a18e90ec0912b95eab873f29611a99047b6e0c46ba407c9ad6"
    POSTGRES_CDN = "postgresql+asyncpg://food_user:125KMAJ!kGALa@localhost/food_db"

settings = SettingsApp()