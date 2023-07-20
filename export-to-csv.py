import os
from datetime import datetime
import discord
import csv

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('Bot is ready!')

data_buffer = []

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.name == 'bitcoin':
        content = message.content

        if content.startswith('!csv'):
            await message.delete()

            today = message.created_at.date()
            print(f'Parsing messages from {today}...')
            async for msg in message.channel.history(limit=None):
                if msg.created_at.date() == today:
                    data_buffer.append(msg.content)

            combined_content = "\n".join(data_buffer)
            await parse_message(combined_content, message.channel)


def parse_label(line):
    if ' + ' in line:
        tokens = line.split(' + ')
    else:
        tokens = [line]

    indices = []
    print("Labelling ", line, ", tokens: ", tokens, "\n")

    for r in tokens:
        if ' : ' not in r:
            indices.append(r)
            continue
        start, end = r.split(' : ')
        start_hex = int(start[2:], 16)

        end = start[2:-len(end)] + end
        end_hex = int(end, 16)

        indices.extend([f'P-{hex(i)[2:].upper().zfill(4)}' for i in range(start_hex, end_hex + 1)])

    print("Indices: ", indices, "\n")
    return indices


async def parse_message(content, channel):
    if 'bc1' not in content:
        return
    label_arr = []
    for line in content.splitlines():
        if line.startswith('P-'):
            label_arr = parse_label(line)
            break

    data = []
    current_amount = None
    index = 0
    for line in content.splitlines():
        if line.startswith("bc1"):
            data.append({
                'address': line,
                'amount': current_amount,
                'label': label_arr[index]
            })
            print("Adding ", line, " with amount ", current_amount, " and label ", label_arr[index], ". i = ", index)
            index += 1
        else:
            current_amount = line.split(':')[0].strip()[:-1] + '000'
    for entry in data:
        print(entry)
    await write_csv_row(data)
    await send_csv(channel)


async def write_csv_row(data):
    name = "peach-transacs-" + datetime.now().strftime("%Y-%m-%d-%H-%M") + ".csv"
    if os.path.exists(name):
        os.remove(name)
    with open(name, 'a', newline='') as file:
        fieldnames = ['address', 'amount', 'label']
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=',')

        writer.writeheader()
        for entry in data:
            writer.writerow(entry)


async def send_csv(channel):
    name = "peach-transacs-" + datetime.now().strftime("%Y-%m-%d-%H-%M") + ".csv"
    with open(name, 'rb') as file:
        await channel.send(file=discord.File(file, name))


client.run('TOKEN')
