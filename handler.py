from mangum import Mangum
from app.main import app

# Mangum adapter for Lambda
handler = Mangum(app, lifespan="off")