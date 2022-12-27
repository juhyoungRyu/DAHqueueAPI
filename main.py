from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import database
from pydantic import BaseModel

app = FastAPI()
PORT = 8000

origins = ["*"]

origins = ["http://localhost:3000", "http://localhost:8000", 'http://10.0.2.2']

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class newClient(BaseModel):
    guest: str
    pet: str


class deleteID(BaseModel):
    one: list
    two: list


@app.get('/wait')
async def waiting():
    return (database.fakeDB)


@app.get('/next')
async def next():
    db = database.fakeDB

    if db['other']:
        first_value_other = db['other'][0]
        db['two'].append(first_value_other)
        del db['other'][0]
        for i in db['other']:
            i['id'] -= 1

    if len(db['two']) > 0:
        first_value = db['two'][0]
        db['one'].append(first_value)
        del db['two'][0]
        for i in db['two']:
            i['id'] -= 1

    if len(db['one']) > 0:
        db['now']['guest'] = db['one'][0]['guest']
        db['now']['pet'] = db['one'][0]['pet']
        del db['one'][0]
        for i in db['one']:
            i['id'] -= 1
    else:
        db['now']['guest'] = ''
        db['now']['pet'] = ''

    return {'message': '정상적으로 완료되었습니다.'}


@app.post('/new')
async def new(newClient: newClient):
    new = {'pet': newClient.pet, 'guest': newClient.guest}
    db = database.fakeDB
    if (len(db['one']) == 0 and db['now']['guest'] == ''):
        db['now']['guest'] = new['guest']
        db['now']['pet'] = new['pet']
    elif (len(db['one']) != 5):
        new['id'] = len(db['one']) + 1
        db['one'].append(new)
    elif (len(db['two']) != 5):
        new['id'] = len(db['two']) + 1
        db['two'].append(new)
    else:
        new['id'] = len(db['other']) + 1
        db['other'].append(new)
    return {"message": '정상적으로 등록되었습니다.'}


@app.post('/delete')
async def delete(lists: deleteID):
    one_sid = 0
    two_sid = 0
    db = database.fakeDB

    if lists.one:
        temp = []
        db['one'] = filter(lambda item: item['id'] not in lists.one, db['one'])

        for i in db['one']:
            temp.append(i)

        for i in range(len(temp)):
            temp[i]['id'] = i + 1

        db['one'] = temp

        one_sid = 5 - len(db['one'])

    if lists.two:
        temp = []
        print(lists.two)
        db['two'] = filter(lambda item: item['id'] not in lists.two, db['two'])

        for i in db['two']:
            print(i)
            temp.append(i)

        for i in range(len(temp)):
            temp[i]['id'] = i + 1

        db['two'] = temp
        temp = []

        two_sid = 5 - len(db['two'])

    for _ in range(one_sid):
        if db['two']:
            temp = []
            temp.append(db['two'][0])
            temp[0]['id'] = len(db['one']) + 1
            del db['two'][0]

            db['one'].append(temp[0])

            for j in db['two']:
                j['id'] -= 1

    for _ in range(two_sid):
        if db['other']:
            temp.append(db['other'][0])
            temp[0]['id'] = len(db['two']) + 1
            del db['other'][0]

            db['two'].append(temp[0])
            del temp[0]

            for j in db['other']:
                j['id'] -= 1

    return {"message": '정상적으로 삭제되었습니다.'}
