from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu_kb(is_admin: bool = False) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text="Business", callback_data="biz:list"),
         InlineKeyboardButton(text="Rules", callback_data="rules:list")],
        [InlineKeyboardButton(text="AI", callback_data="ai:menu"),
         InlineKeyboardButton(text="Stats", callback_data="stats:me")],
        [InlineKeyboardButton(text="Promo", callback_data="promo:redeem")],
    ]
    if is_admin:
        rows.append([InlineKeyboardButton(text="Admin", callback_data="admin:panel")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def ai_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Settings", callback_data="ai:settings")],
        [InlineKeyboardButton(text="Clear memory", callback_data="ai:clear")],
        [InlineKeyboardButton(text="API key", callback_data="ai:apikey")],
        [InlineKeyboardButton(text="Back", callback_data="menu:main")],
    ])

def rules_list_kb(rules) -> InlineKeyboardMarkup:
    rows = []
    for r in rules[:20]:
        rows.append([InlineKeyboardButton(text=f"#{r.id} {r.name} ({'ON' if r.is_active else 'OFF'})",
                                          callback_data=f"rule:open:{r.id}")])
    rows.append([InlineKeyboardButton(text="New rule", callback_data="rule:new")])
    rows.append([InlineKeyboardButton(text="Back", callback_data="menu:main")])
    return InlineKeyboardMarkup(inline_keyboard=rows)
