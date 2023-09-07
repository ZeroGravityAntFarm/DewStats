from fastapi import APIRouter, HTTPException, Depends, Form
import requests

router = APIRouter()


@router.get("/master")
def get_master():

    master_servers = ['http://ed.thebeerkeg.net/server/list']

    for server in master_servers:
        resp = requests.get(url=server)

    return resp.json()



@router.get("/master/{server_ip}")
def get_server(server_ip):
    server_ip = server_ip.strip("'")
    resp = requests.get(url="http://" + server_ip)

    return resp.json()