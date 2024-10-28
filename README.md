# Telegram-aiogram-python

### Импортируемые библиотеки
- `asyncio`: библиотека для написания асинхронного кода.
- `logging`: для ведения журналов (логирования) событий.
- `subprocess`: для выполнения команд операционной системы.
- `pyscreenshot`: для создания скриншотов экрана.
- `wave` и `pyaudio`: для записи звука.
- `os` и `sys`: для работы с файловой системой и системными функциями.
- `aiogram`: библиотека для создания ботов в Telegram.
- `datetime`: для работы с датой и временем.

### Настройка кодировки
```python
sys.stdin.reconfigure(encoding='cp866')
sys.stdout.reconfigure(encoding='cp866')
sys.stderr.reconfigure(encoding='cp866')
```
Эти строки устанавливают кодировку ввода и вывода в `cp866`, что может быть полезно для работы с русскоязычными текстами в консоли.

### Настройка логирования и инициализация бота
```python
logging.basicConfig(level=logging.INFO)
bot = Bot(token="YOUR_BOT_TOKEN")
dp = Dispatcher()
dp["Start_Time"] = datetime.now().strftime("%d.%m.%Y %H:%M")
```
- `logging.basicConfig`: настраивает уровень логирования на `INFO`.
- `Bot(token="YOUR_BOT_TOKEN")`: создаёт экземпляр бота с указанным токеном.
- `Dispatcher()`: создаёт диспетчер для обработки сообщений.
- `Start_Time`: сохраняет текущее время в формате "дд.мм.гггг чч:мм".

### Функции бота
1. **Screen()**:
   - Создает скриншот экрана и сохраняет его в файл с именем, содержащим текущую дату.
   - Возвращает имя файла скриншота.

2. **SoundREC(seconds)**:
   - Записывает звук в течение заданного количества секунд и сохраняет его в формате WAV.
   - Возвращает имя файла записи.

3. **Команды бота**:
   - `cmd_Start`: отвечает на команду `/start`, отправляя приветственное сообщение и текущее время старта.
   - `cmd_Screen`: обрабатывает команду `/screen`, создает скриншот и отправляет его пользователю.
   - `cmd_CMD`: обрабатывает команду `/cmd`, выполняет указанную команду операционной системы и отправляет результат пользователю.
   - `cmd_Rec`: обрабатывает команду `/rec`, записывает звук на заданное количество секунд и отправляет файл пользователю.
   - `cmd_Video`: (не реализована в данном коде, но предполагается) обрабатывает команду `/video`, записывает видео на заданное количество секунд и отправляет файл пользователю.

### Основная функция
```python
async def main():
    dp.message.register(cmd_Start, Command("Start", "start"))
    dp.message.register(cmd_Screen, Command("Screen", "screen"))
    dp.message.register(cmd_CMD, Command("CMD", "cmd"))
    dp.message.register(cmd_Rec, Command("Rec", "rec"))
    dp.message.register(cmd_Video, Command("Video", "video"))
    await dp.start_polling(bot)
