import requests
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi import FastAPI
from time import time
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
# from starlette.middleware.cors import CORSMiddleware

from flask import Flask
from flask_cors import CORS
from functions import (
    request_ticket_login, request_csrf, 
)


router = APIRouter()

login_url = "https://3de24xplm.com.tw/3dspace/ticket/login"
csrf_url = "https://3de24xplm.com.tw/3dspace/resources/v1/application/CSRF"


cert = "./3de24xplm.crt"
infinite_ticket = "NkM1OEY5NEY3MEYzNEJEN0I3MjZFNDc2MDY2RTRDRjl8bmlra2l8fHx8MHw="
security_context = "VPLMProjectLeader.Company Name.DEMO_CS"



app = FastAPI()
session = requests.Session()


@router.get("/login")
def ticket_login():
    """調用封裝函數，執行 ticket_login"""
    current_time = time()
    if hasattr(app.state, "last_login_time") and (current_time - app.state.last_login_time < 60):
        return {"error": "Please wait before making another login request."}
    
    url = login_url
    response = request_ticket_login(session, url, infinite_ticket, cert)
    app.state.last_login_time = current_time  # 更新上次請求時間
    return response


