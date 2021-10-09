from httpx import AsyncClient
import random, string
import os
import json
import time
import asyncio
import proxy_processor
from tasksio import TaskPool

async def rc(len):
	return os.urandom(len).hex()[len:]

async def send_fr(s, token, user_id):
	headers = {
		'accept': '*/*',
		'accept-encoding': 'gzip, deflate',
		'accept-language': 'en-GB',
		'authorization': token,
		'cookie': f'__dcfduid={await rc(43)}; __sdcfduid={await rc(96)}; __stripe_mid={await rc(18)}-{await rc(4)}-{await rc(4)}-{await rc(4)}-{await rc(18)}; locale=en-GB; __cfruid={await rc(40)}-{"".join(random.choice(string.digits) for i in range(10))}',
		'content-type': 'application/json',
		'origin': 'https://discord.com',
		'referer': 'https://discord.com/channels/@me', 
		'sec-fetch-dest': 'empty', 
		'sec-fetch-mode': 'cors',
		'sec-fetch-site': 'same-origin',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.1.9 Chrome/83.0.4103.122 Electron/9.4.4 Safari/537.36',
		'x-debug-options': 'bugReporterEnabled',
		'x-context-properties': 'eyJsb2NhdGlvbiI6IlVzZXIgUHJvZmlsZSJ9',
		'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjAuMS45Iiwib3NfdmVyc2lvbiI6IjEwLjAuMTc3NjMiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6OTM1NTQsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9',
	}

	try:
		res = await s.put(f'https://discord.com/api/v9/users/@me/relationships/{user_id}', headers=headers, json={}, timeout=100)
		return res
	except Exception as e:
		#print(e)
		pass

async def _send_fr(token, user_id, proxy):
	async with AsyncClient(proxies={'https://': 'http://' + proxy}) as s:
		res = await send_fr(s, token, user_id)
	if res.status_code == 204:
		print(f'[DEBUG] Sent Friend Req to ({user_id}) with token ({token[:31]}...)')
	else:
		print(res.text)
		

async def main():
	with open('data/tokens.txt', 'r') as tokens_file:
		tokens = [line.rstrip('\n') for line in tokens_file]
	print('[DEBUG] '+str(len(tokens))+ ' Tokens Loaded')

	user_id = input('[USER_ID] Please Input the ID of the User you wish to FR Spam: ')

	async with TaskPool(2_00) as pool:
		for token in tokens:
			await pool.put(_send_fr(token, user_id, proxy_processor.GetProxy()))

	

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())