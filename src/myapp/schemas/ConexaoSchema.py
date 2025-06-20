from pydantic import BaseModel

class ConexaoSchema(BaseModel):
    database: str
    user: str
    password: str
    host: str
    port: str

    def __str__(self):
        return f"{self.database, self.user, self.password, self.host, self.port}"