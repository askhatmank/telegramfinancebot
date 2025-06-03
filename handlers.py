from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from calculations import *
from keyboards import get_main_kb
from logger import logger
import logging

router = Router()
logger = logging.getLogger(__name__)

class CalcStates(StatesGroup):
    waiting_for_credit = State()
    waiting_for_mortgage = State()
    waiting_for_deposit = State()
    waiting_for_vacation = State()

def format_currency(amount: float) -> str:
    return f"{amount:,.0f} ₸".replace(",", " ")

def parse_input(text: str) -> list[float]:
    # Обрабатывает числа с пробелами, запятыми и точками
    return [float(x.replace(',', '.')) for x in text.split()]

@router.message(F.text == '/start')
async def start_cmd(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "💰 Финансовый калькулятор\nВыберите опцию:",
        reply_markup=get_main_kb()
    )

# ===== КРЕДИТ =====
@router.message(F.text == 'Кредит')
async def credit_cmd(message: Message, state: FSMContext):
    await state.set_state(CalcStates.waiting_for_credit)
    await message.answer(
        "Введите параметры кредита через пробел:\n"
        "Сумма Срок(лет) Ставка(%)\n"
        "Пример: 5 000 000 5 10"
    )

@router.message(CalcStates.waiting_for_credit)
async def calculate_credit_handler(message: Message, state: FSMContext):
    try:
        nums = parse_input(message.text)
        if len(nums) != 3:
            raise ValueError("Нужно ровно 3 числа!")
            
        payment, total, over = calculate_credit(*nums)
        await message.answer(
            f"📊 Результат по кредиту:\n"
            f"• Ежемесячный платеж: {format_currency(payment)}\n"
            f"• Общая выплата: {format_currency(total)}\n"
            f"• Переплата: {format_currency(over)}"
        )
        await state.clear()
    except Exception as e:
        await message.answer(f"❌ Ошибка: {str(e)}\nПопробуйте снова:")

# ===== ИПОТЕКА =====
@router.message(F.text == 'Ипотека')
async def mortgage_cmd(message: Message, state: FSMContext):
    await state.set_state(CalcStates.waiting_for_mortgage)
    await message.answer(
        "Введите параметры ипотеки через пробел:\n"
        "Сумма Срок(лет) Ставка(%) [Страховка(%)]\n"
        "Пример: 10 000 000 20 7 1.5"
    )

@router.message(CalcStates.waiting_for_mortgage)
async def calculate_mortgage_handler(message: Message, state: FSMContext):
    try:
        nums = parse_input(message.text)
        if len(nums) not in (3, 4):
            raise ValueError("Нужно 3 или 4 числа!")
            
        insurance = nums[3] if len(nums) > 3 else 0.0
        payment, total, over = calculate_mortgage(nums[0], nums[1], nums[2], insurance)
        
        response = (
            f"🏠 Результат по ипотеке:\n"
            f"• Ежемесячный платеж: {format_currency(payment)}\n"
            f"• Общая сумма: {format_currency(total)}\n"
            f"• Переплата: {format_currency(over)}"
        )
        if insurance > 0:
            response += f"\n• Страховка: {insurance}% годовых"
            
        await message.answer(response)
        await state.clear()
    except Exception as e:
        await message.answer(f"❌ Ошибка: {str(e)}\nПопробуйте снова:")

# ===== ДЕПОЗИТ =====
@router.message(F.text == 'Депозит')
async def deposit_cmd(message: Message, state: FSMContext):
    await state.set_state(CalcStates.waiting_for_deposit)
    await message.answer(
        "Введите параметры депозита через пробел:\n"
        "Сумма Срок(лет) Ставка(%) Капитализация(раз в год)\n"
        "Пример: 1 000 000 3 8 12"
    )

@router.message(CalcStates.waiting_for_deposit)
async def calculate_deposit_handler(message: Message, state: FSMContext):
    try:
        nums = parse_input(message.text)
        if len(nums) != 4:
            raise ValueError("Нужно ровно 4 числа!")
            
        total, profit = calculate_deposit(*nums)
        await message.answer(
            f"🏦 Результат по депозиту:\n"
            f"• Итоговая сумма: {format_currency(total)}\n"
            f"• Доход: {format_currency(profit)}"
        )
        await state.clear()
    except Exception as e:
        await message.answer(f"❌ Ошибка: {str(e)}\nПопробуйте снова:")

# ===== ОТПУСК =====
@router.message(F.text == 'Отпуск')
async def vacation_cmd(message: Message, state: FSMContext):
    await state.set_state(CalcStates.waiting_for_vacation)
    await message.answer(
        "Введите параметры отпуска через пробел:\n"
        "Бюджет Дни Расход_в_день\n"
        "Пример: 200 000 7 15 000"
    )

@router.message(CalcStates.waiting_for_vacation)
async def calculate_vacation_handler(message: Message, state: FSMContext):
    try:
        nums = parse_input(message.text)
        if len(nums) != 3:
            raise ValueError("Нужно ровно 3 числа!")
            
        spent, remaining = calculate_vacation(*nums)
        await message.answer(
            f"✈️ Результат по отпуску:\n"
            f"• Общие расходы: {format_currency(spent)}\n"
            f"• Останется: {format_currency(remaining)}"
        )
        await state.clear()
    except Exception as e:
        await message.answer(f"❌ Ошибка: {str(e)}\nПопробуйте снова:")

# Обработчик неизвестных команд
@router.message()
async def unknown_input(message: Message):
    await message.answer("Пожалуйста, выберите тип расчета из меню ниже", reply_markup=get_main_kb())