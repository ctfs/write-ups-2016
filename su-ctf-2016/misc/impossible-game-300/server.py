#!/usr/bin/env python3

import sys
# This code uses WebSockets which requires Python 3.5 or newer
assert sys.version_info >= (3,5)

# This code uses asyncio.timeout() which requires asyncio 3.4.4 or newer
import pkg_resources
assert pkg_resources.get_distribution("asyncio").version >= '3.4.4'

import asyncio
import websockets
import numpy as np
import random
import hashlib, itertools, binascii


N = 100
MAX_GUESSES = N//2
TIMEOUT = 61	# 1 extra second to account for RTT
HOST = ''
PORT = 8998
ALIGN = len(str(N-1))
PAD = '0' * ALIGN

CHALLENGE_SIZE = 22
ANSWER_SIZE = 32
assert(ANSWER_SIZE % 4 == 0)

# STATUS CODES
CHALLENGE = '0'
RE_ARRANGED = '1'
GIVE_GUESS = '2'
# UNACCEPTABLE = '3'
GREATE_GUESS = '4'
WRONG_GUESS = '5'
BYE = '6'
FLAG_IS = '7'


async def client_handler(websocket, path):
	# print(websocket)

	async def send_string(msg):
		try:
			await websocket.send(msg)
		except Exception as e:
			print(e)
			return False
		return True
	
	# Client should provide a proof of work
	answ = random.randint(0, 2**ANSWER_SIZE - 1)
	answ = hex(answ)[2:]
	answ = answ.zfill(ANSWER_SIZE//4)

	chal = hashlib.md5(answ.encode("utf8")).hexdigest()
	chal = bin(int(chal, 16))[2:]
	chal = chal[:CHALLENGE_SIZE].zfill(CHALLENGE_SIZE)

	if not await send_string(CHALLENGE + chal): return

	try:
		with asyncio.timeout(TIMEOUT):
			answer = await websocket.recv()
		if len(answer) != ANSWER_SIZE//4:
			print("Invalid response length.")
			# await send_string(UNACCEPTABLE)
			return

		_chal = hashlib.md5(answer.encode("utf8")).hexdigest()
		_chal = bin(int(_chal, 16))[2:]
		_chal = _chal[:CHALLENGE_SIZE].zfill(CHALLENGE_SIZE)
		if _chal != chal:
			print("Invalid response to challenge.")
			# await send_string(UNACCEPTABLE)
			return
	except Exception as e:
		print(e)
		return

	# Initial permutation, persists during a session
	phi = np.random.permutation(N)

	i = 0
	while i < N:
		found = False

		# Current permutation and its inverse
		# Persists until a right guess, or until N/2 wrong guesses
		rho = np.random.permutation(N)
		rho_inv = np.argsort(rho)

		result = rho[phi[rho_inv]]

		if not await send_string(RE_ARRANGED + str(i).zfill(ALIGN)): return

		for j in range(0, MAX_GUESSES):
			try:
				if not await send_string(GIVE_GUESS + str(j).zfill(ALIGN)): return
				with asyncio.timeout(TIMEOUT):
					answer = await websocket.recv()
				if len(answer) > 3:
					raise Exception("Input too long")
				guess = int(answer)
				actual = result[guess]			
			except Exception as e:
				print(e)
				return
			if actual == i:
				if not await send_string(GREATE_GUESS + PAD): return
				found = True
				# print('---> GREAT!')
				break
			# print('--->' + str(actual))
			if not await send_string(WRONG_GUESS + str(actual).zfill(ALIGN)): return

		if found:
			i += 1
		else:
			await send_string(BYE + PAD)
			return

	await send_string(FLAG_IS + 'SharifCTF{flagfalgflag}')

server = websockets.serve(client_handler, HOST, PORT)
loop = asyncio.get_event_loop()
loop.run_until_complete(server)
loop.run_forever()
