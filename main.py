import discord, time, random, asyncio, requests

from discord import message

client = discord.Client(intents=discord.Intents.all())
token = 'MTIwOTQ5NTgzMTIzODE1NjM1OQ.GV77tG.NKGgxwxwGY7C9ljvZsBFFblAFEVNA_D6cXuogI'  #봇 토큰
prefix = "!"
idA, moneyA, timeA = [], [], []

try:
  f = open("UserData.txt", "r")
except:
  f = open("UserData.txt", "w")
  f.close()
  f = open("UserData.txt", "r")
while True:
  line = f.readline()
  if not line:
    break
  line = line.split(",")
  idA.append(line[0])
  moneyA.append(int(line[1]))
  timeA.append(int(line[2]))
f.close()


@client.event
async def on_ready():

  print(client.user.name)
  print('성공적으로 봇이 시작되었습니다')
  game = discord.Game('바다서버 도박 활성화')
  await client.change_presence(status=discord.Status.online, activity=game)
  ch = client.get_channel(1209494626969329717)
  await ch.send(f"✅ **바다봇이 시작하였습니다**")


@client.event
async def on_message(message):
  cmd = message.content.split(" ")[0]
  args = message.content.split(" ")[1:]
  ID = str(message.author.id)

  if cmd == prefix + "도움말":
    embed = discord.Embed(title="명령어", description="봇 명령어", color=0x62C1CC)
    embed.add_field(name="도박",
                    value="잔액, 돈줘, 도박 <금액>, 올인, 랭킹, 송금 <금액> <@대상>",
                    inline=True)
    await message.channel.send("", embed=embed)

  if cmd == prefix + "돈줘":
    TIME = int(time.time())
    if ID in idA:
      if TIME - timeA[idA.index(ID)] < 3600:  # 시간이 아직 안 지났을 때
        embed = discord.Embed(title="",
                              description="1시간 마다 받을 수 있습니다.",
                              color=0xFF0000)
        await message.channel.send(embed=embed)
        return
      elif TIME - timeA[idA.index(ID)] >= 3600:
        timeA[idA.index(ID)] = int(time.time())
    give = random.randrange(1, 10) * random.randrange(1000, 10000)
    if ID in idA:  # ID가 있으면 돈을 더함
      moneyA[idA.index(ID)] += give
    elif not ID in idA:  # ID가 없으면 배열에 새로 추가
      idA.append(ID)
      moneyA.append(give)
      timeA.append(int(time.time()))
    embed = discord.Embed(
        title="",
        description=format(give, ",d") + "원 만큼 받았습니다. 현재 돈: " +
        format(moneyA[idA.index(ID)], ",d") + "원",
        color=0x00FF00,
    )
    await message.channel.send(embed=embed)

  if cmd == prefix + "잔액":
    if ID in idA:  # ID가 있을 때
      embed = discord.Embed(
          title="",
          description=format(moneyA[idA.index(ID)], ",d") + " 원",
          color=0x118811,
      )
      await message.channel.send(embed=embed)
    elif not ID in idA:  # ID가 없을 때
      embed = discord.Embed(title="", description="0 원", color=0x118811)
      await message.channel.send(embed=embed)

  if cmd == prefix + "올인":
    if not ID in idA or moneyA[idA.index(ID)] <= 0:  # 돈이 부족할 때
      embed = discord.Embed(title="", description="돈이 부족합니다.", color=0xFF0000)
      await message.channel.send(embed=embed)
      return
    give = random.randrange(2, 10)  # 성공확률 : 4/9
    count = await message.channel.send("배수 정하는 중 ...")
    await asyncio.sleep(2)
    await count.edit(content="만약 성공하면 건 돈의 " + str(give) + "배 를 얻어요")
    await asyncio.sleep(2)
    if give % 3 == 0:
      moneyA[idA.index(ID)] *= give
      await count.edit(content="올인 성공! 현재 돈: " +
                       format(moneyA[idA.index(ID)], ",d") + "원")
    elif give % 3 != 0:
      moneyA[idA.index(ID)] = 0
      await count.edit(content="올인 실패... 현재 돈: " +
                       format(moneyA[idA.index(ID)], ",d") + "원")

  if cmd == prefix + "도박":
    if len(args) != 1:  # 인자 수가 잘못됬을 때
      embed = discord.Embed(title="오류",
                            description="사용법: !도박 돈",
                            color=0xFF0000)
      await message.channel.send(embed=embed)
      return
    if args[0].isdecimal() == False:  # 숫자가 입력되지 않았을 때
      embed = discord.Embed(title="",
                            description="숫자만 입력해 주세요!",
                            color=0xFF0000)
      await message.channel.send(embed=embed)
      return
    args[0] = int(args[0])
    if not ID in idA or moneyA[idA.index(ID)] - args[0] < 0:  # 돈이 부족할 때
      embed = discord.Embed(title="", description="돈이 부족합니다!", color=0xFF0000)
      await message.channel.send(embed=embed)
      return
    moneyA[idA.index(ID)] -= args[0]
    give = random.randrange(2, 5)  # 성공확률 4/9
    count = await message.channel.send("배수 정하는 중 ...")
    await asyncio.sleep(1)
    await count.edit(content="만약 성공하면 건 돈의 " + str(give) + "배 를 얻어요")
    await asyncio.sleep(1)
    if give % 3 == 0:
      moneyA[idA.index(ID)] += give * args[0]
      await count.edit(content="도박 성공! 현재 돈: " +
                       format(moneyA[idA.index(ID)], ",d") + "원")
    elif give % 3 != 0:
      await count.edit(content="도박 실패... 현재 돈: " +
                       format(moneyA[idA.index(ID)], ",d") + "원")
  if cmd == prefix + "랭킹":
    rank, rankA = "", []  # 모든 id와 돈을 담아 정렬할 2차원 배열 rankA
    for i in range(0, len(idA)):
      rankA.append([idA[i], moneyA[i]])
    rankA = sorted(rankA, reverse=True, key=lambda x: x[1])
    for i in range(0, 10):
      try:
        rank += (str(i + 1) + "위 <@" + rankA[i][0] + "> : " +
                 format(rankA[i][1], ",d") + "\n")
      except:
        break
    embed = discord.Embed(title="돈 랭킹", description=rank, color=0xD8AA2D)
    await message.channel.send(embed=embed)

  if cmd == prefix + "송금":
    if len(args) != 2 or args[0][3:-1] in idA:  # 만약 인자 수가 잘못됬거나 순서가 바뀌었을 때
      embed = discord.Embed(title="오류",
                            description="사용법: !송금 돈 @유저이름",
                            color=0xFF0000)
      await message.channel.send(embed=embed)
      return
    if not args[1][3:-1] in idA:  # 송금대상의 ID가 없을 때
      embed = discord.Embed(title="오류",
                            description="송금대상이 등록된 ID가 아닙니다",
                            color=0xFF0000)
      await message.channel.send(embed=embed)
      return
    if not ID in idA:  # 송금자의 ID가 없을 때
      embed = discord.Embed(title="오류",
                            description="잔액이 부족합니다",
                            color=0xFF0000)
      await message.channel.send(embed=embed)
      return
    if args[0].isdecimal() == False:  # 숫자가 입력되지 않았을 때
      embed = discord.Embed(title="오류",
                            description="숫자를 입력해주세요",
                            color=0xFF0000)
      await message.channel.send(embed=embed)
      return
    if moneyA[idA.index(ID)] < int(args[0]):  # 잔액이 부족할 때
      embed = discord.Embed(title="오류",
                            description="잔액이 부족합니다",
                            color=0xFF0000)
      await message.channel.send(embed=embed)
      return
    else:  # 모든 이상이 없을 때
      moneyA[idA.index(ID)] -= int(args[0])
      moneyA[idA.index(str(args[1][3:-1]))] += int(args[0])
      embed = discord.Embed(title="송금",
                            description="송금을 성공하였습니다",
                            color=0x118811)
      await message.channel.send(embed=embed)

  if cmd == prefix + "한강":
    page = requests.get("https://hangang.winsub.kr/",
                        headers={"User-Agent": "Mozilla/5.0"})
    msg = ":droplet: 현재 한강 물 온도 : "
    msg += page.text[244:252]
    embed = discord.Embed(title="", description=msg, color=0x2EFEF7)
    await message.channel.send(embed=embed)

  f = open("UserData.txt", "w")  # 바뀐 데이터 저장
  for i in range(0, len(idA), 1):
    f.write(str(idA[i]) + "," + str(moneyA[i]) + "," + str(timeA[i]) + "\n")
  f.close()
  print(ID, cmd)


client.run(token)
