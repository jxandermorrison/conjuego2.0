from CONFIG import USER, PASSWORD, URL

class Config:
    MONGO_URI = "mongodb+srv://{}:{}@{}".format(USER, PASSWORD, URL)
    LANGUAGES = ["en", "es", "pt"]
