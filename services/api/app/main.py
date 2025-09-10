from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from bson import ObjectId

from manager import Manager
man = Manager()


app = FastAPI()
class FieldVals(BaseModel):
    tweets: list[dict]

@app.get('/')
async def app1():
    return  {"message":"Welcome to the Muezzin API",
             "endpoints": " /get_all_text , /get_all_fields_vals , /get_most_threatening_data"}

@app.get("/get_all_text",response_model=FieldVals)
async def get_text():
    text = man.get_fields_values_from_es("text")
    return {"text": text}


@app.get("/get_all_fields_vals",response_model=FieldVals)
async def get_all_fields_vals(field_name):
    values = man.get_fields_values_from_es(field_name)
    return {"values": values}


@app.get("/get_most_threatening_data")
def get_most_threatening_data():
    try:
        man.get_most_threatening_doc()
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)