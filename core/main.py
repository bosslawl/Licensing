from assets.modules import *

database = "assets/database/main.sqlite"
app = FastAPI()

@app.get("/")
async def root(request: Request, license = None):
    
    connection = request.headers.get('CF-Connecting-IP')
    database = sqlite3.connect(database)
    cursor = database.cursor()
    
    if license is None:
        print(f'{connection} connected to the API without passing a license key.')
        return {"Status": "Failed", "Reason": "No License Provided"}
    
    current = datetime.utcnow()
    cursor.execute(f'SELECT License FROM Licenses WHERE License = "{license}" AND Expiry > "{current}"')
    result = cursor.fetchone()
    
    if result is None:
        print(f'{connection} connected to the API with an invalid license key.')
        return {"Status": "Failed", "Reason": "Invalid License Provided"}
    
    cursor.execute(f'SELECT Expiry FROM Licenses WHERE License = "{license}" AND expiry > "{current}"')
    expiry = cursor.fetchone()
    cursor.execute(f'SELECT IPv4 FROM Licenses WHERE License = "{license}" AND expiry > "{current}"')
    result = cursor.fetchone()
    
    if result == (None,):
        cursor.execute(f'UPDATE Licenses SET IPv4 = "{connection}" WHERE License = "{license}"')
        database.commit()
        return {"Status": "Success", "Reason": expiry[0]}
    
    elif result[0] != connection:
        print(f'{connection} connected to the API with a valid license key ({license}) but on the incorrect IP.')
        return {"Status": "Failed", "Reason": "Incorrect IP"}
    
    else:	
        return {"Status": "Success", "Reason": expiry[0]}