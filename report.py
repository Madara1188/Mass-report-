import sys
import asyncio
import json
from pyrogram import Client, filters
from pyrogram.raw.functions.account import ReportPeer
from pyrogram.raw.types import InputReportReasonChildAbuse, InputReportReasonFake, InputReportReasonCopyright, InputReportReasonGeoIrrelevant, InputReportReasonPornography, InputReportReasonIllegalDrugs, InputReportReasonSpam, InputReportReasonPersonalDetails, InputReportReasonViolence, InputPeerChannel

def get_reason(text):
    if text == "Report for child abuse":
        return InputReportReasonChildAbuse()
    elif text == "Report for impersonation":
        return InputReportReasonFake()
    elif text == "Report for copyrighted content":
        return InputReportReasonCopyright()
    elif text == "Report an irrelevant geogroup":
        return InputReportReasonGeoIrrelevant()
    elif text == "Reason for Pornography":
        return InputReportReasonPornography()
    elif text == "Report an illegal drug":
        return InputReportReasonIllegalDrugs()
    elif text == "Report for offensive person detail":
        return InputReportReasonSpam()
    elif text == "Report for spam":
        return InputReportReasonPersonalDetails()
    elif text == "Report for Violence":
        return InputReportReasonViolence()

async def main(message):
    config = json.load(open("config.json"))
    report_reason = get_reason(message)
    target_peer = config['Target']
    
    for account in config["accounts"]:
        session_string = account["Session_String"]
        owner_name = account['OwnerName']
        
        async with Client(name="Session", session_string=session_string) as app:
            try:
                peer = await app.resolve_peer(target_peer)
                peer_id = peer.channel_id
                access_hash = peer.access_hash
                channel = InputPeerChannel(channel_id=peer_id, access_hash=access_hash)
            except Exception as e:
                print(e)
                continue 
            report_peer = ReportPeer(
                peer=channel, 
                reason=report_reason, 
                message=message  # Corrected from `report_reason` to `message`
            )

            try:
                result = await app.send(report_peer)
                print(result, 'Reported by Account', owner_name)
            except BaseException as e:
                print(e)
                print("Failed to report from:", owner_name)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python your_script.py <reason> <message>")
        sys.exit(1)

    # Get command-line arguments
    input_string = sys.argv[1]

    asyncio.run(main(message=input_string))
