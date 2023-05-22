import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Set up logging
logging.basicConfig(level=logging.INFO)

bot = Bot(token="6223297692:AAGnjzF2NIdTBUlPsoQ53yIsPAtKbjHMZmw")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

base_url = "http://192.168.10.22:27"

# Define states for login and signup
class LoginState(StatesGroup):
    username = State()
    password = State()

class RegistrationForm(StatesGroup):
    userName = State()
    password = State()
    confirmPassword = State()
    lastName = State()
    firstName = State()
    middleName = State()
    location = State()
    birthDate = State()
    phoneNumber = State()
    gender = State()
    email = State()
    role = State()


# Define a handler for the /start command
@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Welcome! Please use /login or /signup to authenticate.")

# Define a handler for the /login command
@dp.message_handler(commands=["login"])
async def login_command(message: types.Message):
    await message.reply("Please enter your username:")
    await LoginState.username.set()

# Define a handler for receiving the username
@dp.message_handler(state=LoginState.username)
async def receive_username(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["username"] = message.text

    await message.reply("Please enter your password:")
    await LoginState.password.set()

# Define a handler for receiving the password
@dp.message_handler(state=LoginState.password)
async def receive_password(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        username = data["username"]
        password = message.text

    login_url = f"{base_url}/login"
    login_payload = {
        "userName": username,
        "password": password
    }
    response = requests.post(login_url, json=login_payload)

    if response.ok:
        login_data = response.json()
        token = login_data.get("token")
        await message.reply(f"Login successful! Your token: {token}")
    else:
        await message.reply("Login failed. Please try again.")

    await state.finish()



# Handler for the start command
@dp.message_handler(commands=["signup"])
async def cmd_start(message: types.Message):
    # Reset registration form state
    await RegistrationForm.userName.set()
    await message.reply("Welcome to the registration process!\nPlease enter your username:")

# Handler for registration form fields
@dp.message_handler(state=RegistrationForm.userName)
async def process_userName(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['userName'] = message.text
    await RegistrationForm.next()
    await message.reply("Please enter your password:")

@dp.message_handler(state=RegistrationForm.password)
async def process_password(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['password'] = message.text
    await RegistrationForm.next()
    await message.reply("Please confirm your password:")

@dp.message_handler(state=RegistrationForm.confirmPassword)
async def process_confirmPassword(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['confirmPassword'] = message.text
    await RegistrationForm.next()
    await message.reply("Please enter your last name:")

@dp.message_handler(state=RegistrationForm.lastName)
async def process_lastName(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['lastName'] = message.text
    await RegistrationForm.next()
    await message.reply("Please enter your first name:")

@dp.message_handler(state=RegistrationForm.firstName)
async def process_firstName(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['firstName'] = message.text
    await RegistrationForm.next()
    await message.reply("Please enter your middle name:")

@dp.message_handler(state=RegistrationForm.middleName)
async def process_middleName(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['middleName'] = message.text
    await RegistrationForm.next()
    await message.reply("Please enter your location:")

@dp.message_handler(state=RegistrationForm.location)
async def process_location(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['location'] = message.text
    await RegistrationForm.next()
    await message.reply("Please enter your birth date (YYYY-MM-DD):")

@dp.message_handler(state=RegistrationForm.birthDate)
async def process_birthDate(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['birthDate'] = message.text
    await RegistrationForm.next()
    await message.reply("Please enter your phone number:")

@dp.message_handler(state=RegistrationForm.phoneNumber)
async def process_phoneNumber(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phoneNumber'] = message.text
    await RegistrationForm.next()
    await message.reply("Please enter your gender:")

@dp.message_handler(state=RegistrationForm.gender)
async def process_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['gender'] = message.text
    await RegistrationForm.next()
    await message.reply("Please enter your email:")

@dp.message_handler(state=RegistrationForm.email)
async def process_email(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['email'] = message.text
    await RegistrationForm.next()
    await message.reply("Please enter your role:")

# Handler for the last registration form field
@dp.message_handler(state=RegistrationForm.role)
async def process_role(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['role'] = message.text
    # Validate all fields are filled
    if all(data.values()):
        # Submit registration form
        await submit_registration(data)
        await state.finish()
        await message.reply("Registration complete! Thank you.")
    else:
        await message.reply("Please fill in all required fields.")

# Function to submit registration form
async def submit_registration(data):
    url = "http://192.168.10.22/signup"
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        logging.info("Registration successful")
    except requests.exceptions.RequestException as e:
        logging.error(f"Registration failed: {e}")

# Start the bot
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)




# import logging

# from aiogram import Bot, Dispatcher, executor, types 

# API_TOKEN = '6223297692:AAGnjzF2NIdTBUlPsoQ53yIsPAtKbjHMZmw'

# # Configure logging
# logging.basicConfig(level=logging.INFO)

# # Initialize bot and dispatcher
# bot = Bot(token=API_TOKEN)
# dp = Dispatcher(bot)

# @dp.message_handler(commands=['start', 'help'])
# async def send_welcome(message: types.Message):
#     """
#     This handler will be called when user sends `/start` or `/help` command
#     """
#     await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


# @dp.message_handler()
# async def echo(message: types.Message):
#     # old style:
#     # await bot.send_message(message.chat.id, message.text)

#     await message.answer(message.text)


# if __name__ == '__main__':
#     executor.start_polling(dp, skip_updates=True)




    


