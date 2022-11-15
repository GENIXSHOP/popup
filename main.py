import interactions
import sys
import json
import os
import random
import datetime
import time
import requests as ru
import requests
from re import search
from requests import Session, post, get
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup as bs
from re import search
from user_agent import generate_user_agent
from interactions import Button, ButtonStyle, CommandContext, SelectMenu, SelectOption, ActionRow, Modal, TextInput, TextStyleType, Embed

# interaction.response.send_message

f = open('config.json')
data = json.load(f)
token = data['token']
role = data['role_name']
phone = data['phone']


threading = ThreadPoolExecutor(max_workers=int(100000))
client = interactions.Client(token, intents=interactions.Intents.DEFAULT | interactions.Intents.GUILD_MESSAGES)

@client.event
async def on_start():
	print('Online !')
	
@client.command(
	name="popup",
	description="เติมเงินด้วยซองอั่งเปา",
)
async def _popup(ctx: interactions.CommandContext):
	embed = interactions.Embed(title="🧧 เติมเงินด้วยซองอั่งเปา TrueWallet",color=0x344ceb)
	embed.set_image(url="https://www.checkraka.com/uploaded/img/content/130026/aungpao_truewallet_01.jpg")
	start_popup = Button(
		style=ButtonStyle.PRIMARY,
		custom_id="popup",
		label="🧧 เติมเงิน",
	)
	await ctx.channel.send(embeds=embed, components=[start_popup])
	
@client.component("popup")
async def _success(ctx: interactions.CommandContext):
	modal = Modal(
		custom_id="success",
		title="เติมเงินด้วยซองอั่งเปาผ่านบอท",
		components=[
			TextInput(
				style=TextStyleType.SHORT,
				custom_id="text-input-1",
				label=f"ลิงก์ซองอั่งเปา",
				placeholder="https://gift.truemoney.com/campaign/?v=xxxxxxxxxxxxxxxxxx",
			),
		],
	)
	await ctx.popup(modal)
	
@client.modal("success")
async def _done(ctx: CommandContext, one):
	timeout = datetime.datetime.now()
	gg = timeout.strftime("%H:%M:%S")
	url = one[39:]
	res = requests.post(f"https://gift.truemoney.com/campaign/vouchers/{url}/redeem",json={"mobile":f"{phone}","voucher_hash":f"{url}"},headers={"Accept": "application/json","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36","Content-Type": "application/json","Origin": "https://gift.truemoney.com","Accept-Language": "en-US,en;q=0.9","Connection": "keep-alive"})
	if res.status_code == 200:
		data_contry = requests.get("https://ipinfo.io/json")
		embed = interactions.Embed(title="ข้อมูลการเติมเงิน",color=0x17bd27)
		embed.add_field(name='IP',value=data_contry.json()['ip'])
		embed.add_field(name='ชื่อของผู้เติมเงิน',value=res.json()["data"]["owner_profile"]["full_name"])
		embed.add_field(name='จำนวน',value=res.json()["data"]["voucher"]["amount_baht"] + " บาท")
		embed.set_footer(text="เติมเงินสำเร็จ  | " + gg)
		await interactions.send(embeds=embed, ephemeral=True)
		for role in interactions.guild.roles:
			if type(role.name) == f'{role}':
				await interactions.user.add_roles(role)
	else:
		embed = interactions.Embed(title="⚠️ ไม่สามารถทำรายการได้",color=0xeb4034)
		await interactions.send(embeds=embed, ephemeral=True)
	
	
	
	

		
		
client.start()