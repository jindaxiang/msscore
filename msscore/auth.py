from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from msscore.config import get_auth_settings

auth_settings = get_auth_settings()

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = auth_settings.secret_key
ALGORITHM = auth_settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = auth_settings.access_token_expire_minutes

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
