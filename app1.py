import requests, os, psutil, sys, jwt, pickle, json, binascii, time, urllib3, base64, datetime, re, socket, threading, ssl, pytz, aiohttp, random
from flask import Flask, request, jsonify
from protobuf_decoder.protobuf_decoder import Parser
from xC4 import * 
from xHeaders import *
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from Pb2 import DEcwHisPErMsG_pb2, MajoRLoGinrEs_pb2, PorTs_pb2, MajoRLoGinrEq_pb2, sQ_pb2, Team_msg_pb2
from cfonts import render, say
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import asyncio

# Disable warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ---------------- GLOBALS ---------------- #
app = Flask(__name__)
loop = None  # Will be set when bot starts
online_writer = None
whisper_writer = None
BOT_UID = None
key = None
iv = None
region = None

Hr = {
    'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Content-Type': "application/x-www-form-urlencoded",
    'Expect': "100-continue",
    'X-Unity-Version': "2018.4.11f1",
    'X-GA': "v1 1",
    'ReleaseVersion': "OB52"
}

# ---------------- UTIL FUNCTIONS ---------------- #
def get_random_color():
    colors = [
        "[FF0000]", "[00FF00]", "[0000FF]", "[FFFF00]", "[FF00FF]", "[00FFFF]",
        "[FFFFFF]", "[FFA500]", "[A52A2A]", "[800080]", "[000000]", "[808080]",
        "[C0C0C0]", "[FFC0CB]", "[FFD700]", "[ADD8E6]", "[90EE90]", "[D2691E]",
        "[DC143C]", "[00CED1]", "[9400D3]", "[F08080]", "[20B2AA]", "[FF1493]",
        "[7CFC00]", "[B22222]", "[FF4500]", "[DAA520]", "[00BFFF]", "[00FF7F]",
        "[4682B4]", "[6495ED]", "[5F9EA0]", "[DDA0DD]", "[E6E6FA]", "[B0C4DE]",
        "[556B2F]", "[8FBC8F]", "[2E8B57]", "[3CB371]", "[6B8E23]", "[808000]",
        "[B8860B]", "[CD5C5C]", "[8B0000]", "[FF6347]", "[FF8C00]", "[BDB76B]",
        "[9932CC]", "[8A2BE2]", "[4B0082]", "[6A5ACD]", "[7B68EE]", "[4169E1]",
        "[1E90FF]", "[191970]", "[00008B]", "[000080]", "[008080]", "[008B8B]",
        "[B0E0E6]", "[AFEEEE]", "[E0FFFF]", "[F5F5DC]", "[FAEBD7]"
    ]
    return random.choice(colors)

async def encrypted_proto(encoded_hex):
    global key, iv
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(encoded_hex, AES.block_size)
    encrypted_payload = cipher.encrypt(padded_message)
    return encrypted_payload

# ---------------- ASYNC BOT FUNCTIONS ---------------- #
async def perform_emote(team_code: str, uids: list, emote_id: int):
    global key, iv, region, online_writer, BOT_UID

    if online_writer is None:
        raise Exception("Bot not connected")

    try:
        # JOIN SQUAD
        EM = await GenJoinSquadsPacket(team_code, key, iv)
        await SEndPacKeT(None, online_writer, 'OnLine', EM)
        await asyncio.sleep(0.12)

        # PERFORM EMOTE
        for uid_str in uids:
            uid = int(uid_str)
            H = await Emote_k(uid, emote_id, key, iv, region)
            await SEndPacKeT(None, online_writer, 'OnLine', H)

        # LEAVE SQUAD
        LV = await ExiT(BOT_UID, key, iv)
        await SEndPacKeT(None, online_writer, 'OnLine', LV)
        await asyncio.sleep(0.03)

        return {"status": "success", "message": "Emote done & bot left"}

    except Exception as e:
        raise Exception(f"Failed to perform emote: {str(e)}")

# ---------------- FLASK ROUTES ---------------- #
@app.route('/join')
def join_team():
    global loop

    team_code = request.args.get('tc')
    uids = [request.args.get(f'uid{i}') for i in range(1,7)]
    uids = [uid for uid in uids if uid]

    emote_id_str = request.args.get('emote_id')
    if not team_code or not emote_id_str:
        return jsonify({"status": "error", "message": "Missing tc or emote_id"})

    try:
        emote_id = int(emote_id_str)
    except:
        return jsonify({"status": "error", "message": "emote_id must be integer"})

    if not uids:
        return jsonify({"status": "error", "message": "Provide at least one UID"})

    if not loop:
        return jsonify({"status": "error", "message": "Bot not started yet"})

    # Schedule coroutine in existing loop
    asyncio.run_coroutine_threadsafe(
        perform_emote(team_code, uids, emote_id),
        loop
    )

    return jsonify({
        "status": "success",
        "team_code": team_code,
        "uids": uids,
        "emote_id": emote_id_str,
        "message": "Emote triggered"
    })

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

# ---------------- MAIN BOT SYSTEM ---------------- #
async def MaiiiinE():
    global loop, key, iv, region, BOT_UID

    # BOT UID
    BOT_UID = 14988895945  # Separate BOT UID

    # BOT LOGIN UID/PASSWORD (example)
    Uid, Pw = '4271931522', '76354302535BB6C038A33C33BAA3E2AAC1A644627A49688409887A1A91537817'

    # LOGIN
    open_id, access_token = await GeNeRaTeAccEss(Uid, Pw)
    if not open_id or not access_token:
        print("Error - Invalid Account")
        return

    PyL = await EncRypTMajoRLoGin(open_id, access_token)
    MajoRLoGinResPonsE = await MajorLogin(PyL)
    if not MajoRLoGinResPonsE:
        print("Target Account banned or not registered")
        return

    MajoRLoGinauTh = await DecRypTMajoRLoGin(MajoRLoGinResPonsE)
    region = MajoRLoGinauTh.region
    ToKen = MajoRLoGinauTh.token
    key = MajoRLoGinauTh.key
    iv = MajoRLoGinauTh.iv
    timestamp = MajoRLoGinauTh.timestamp
    TarGeT = MajoRLoGinauTh.account_uid

    loop = asyncio.get_running_loop()  # <--- Set loop globally

    LoGinDaTa = await GetLoginData(MajoRLoGinauTh.url, PyL, ToKen)
    LoGinDaTaUncRypTinG = await DecRypTLoGinDaTa(LoGinDaTa)
    OnLinePorTs = LoGinDaTaUncRypTinG.Online_IP_Port
    ChaTPorTs = LoGinDaTaUncRypTinG.AccountIP_Port
    OnLineiP, OnLineporT = OnLinePorTs.split(":")
    ChaTiP, ChaTporT = ChaTPorTs.split(":")

    # START CHAT + ONLINE TASKS
    AutHToKen = await xAuThSTarTuP(int(TarGeT), ToKen, int(timestamp), key, iv)
    ready_event = asyncio.Event()

    task1 = asyncio.create_task(
        TcPChaT(ChaTiP, ChaTporT, AutHToKen, key, iv,
                LoGinDaTaUncRypTinG, ready_event, region)
    )
    await ready_event.wait()
    task2 = asyncio.create_task(
        TcPOnLine(OnLineiP, OnLineporT, key, iv, AutHToKen)
    )

    # START FLASK THREAD
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    print(render('DEV', colors=['white','green'], align='center'))
    print(f"BOT UID: {BOT_UID} | Region: {region}")

    await asyncio.gather(task1, task2)

# ---------------- ENTRY POINT ---------------- #
async def StarTinG():
    while True:
        try:
            await asyncio.wait_for(MaiiiinE(), timeout=7*60*60)
        except asyncio.TimeoutError:
            print("Token expired! Restarting...")
        except Exception as e:
            print(f"Error TCP: {e} => Restarting...")

if __name__ == '__main__':
    asyncio.run(StarTinG())