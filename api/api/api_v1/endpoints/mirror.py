from fastapi import APIRouter, HTTPException, Depends, Form
import requests

router = APIRouter()


@router.get("/master")
def get_master():

    master_servers = ['http://ed.thebeerkeg.net/server/list', 'http://master.zgaf.io/list']
    sList = []

    for server in master_servers:
        resp = requests.get(url=server)
        resp = resp.json()

        for server in resp["result"]["servers"]:
            if server not in sList:
                sList.append(server)


    return {
                "listVersion": 1,
                "result": {
                    "code": 0,
                    "servers": sList,
                    "msg": "OK"
                },
                "cache": 30
            }



@router.get("/master/{server_ip}")
def get_server(server_ip):
    server_ip = server_ip.strip("'")
    resp = requests.get(url="http://" + server_ip)

    return resp.json()