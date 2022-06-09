
    # else:
    #     inline.add(
    #         types.InlineKeyboardButton(
    #             text=const.ButtonTexts.profile,
    #             callback_data=const.Commands.profile
    #         ),
    #         types.InlineKeyboardButton(
    #             text=const.ButtonTexts.games,
    #             callback_data=const.Commands.games
    #         )
    #     )


# @bot.callback_query_handler(func=lambda call: True)
# @telegram_user
# def query_callback(call: types.CallbackQuery, user: Telegram):
#     match call.data:
#         case const.Commands.edit:
#             inline = types.InlineKeyboardMarkup()

#             inline.add(
#                 types.InlineKeyboardButton(text='Возраст'),
#                 types.InlineKeyboardButton(text='Номер телефона')
#             )

#             msg = bot.send_message(
#                 chat_id=call.message.chat.id,
#                 text='Введите информацию',
#                 reply_markup=inline
#             )

#             bot.register_next_step_handler(
#                 message=msg,
#                 callback=update_info
#             )


# @telegram_user
# def update_info(message: types.Message, user: Telegram):
#     if message.text == 'Возраст':
#         msg = bot.send_message(
#             chat_id=message.chat.id,
#             text='Введите возраст'
#         )

#         bot.register_next_step_handler(
#             message=msg,
#             callback=enter_age
#         )
#     elif message.text == 'Номер телефона':
#         msg = bot.send_message(
#             chat_id=message.chat.id,
#             text='Введите номер телефона'
#         )

#         bot.register_next_step_handler(
#             message=msg,
#             callback=enter_phone_number
#         )


# @telegram_user
# def enter_age(message: types.Message, user: Telegram):
#     if message.text.isdigit():
#         user.age = int(message.text)
#         user.save()
#         bot.send_message(
#             chat_id=message.chat.id,
#             text='Сохранено!'
#         )
#     else:
#         bot.send_message(
#             chat_id=message.chat.id,
#             text='Введите целое число'
#         )


# @telegram_user
# def enter_phone_number(message: types.Message, user: Telegram):
#     if PhoneVerificationSerializer().validate_phone(message.text):
#         user.phone = message.text
#         user.save()

#         bot.send_message(
#             chat_id=message.chat.id,
#             text='Сохранено'
#         )
#     else:
#         bot.send_message(
#             chat_id=message.chat.id,
#             text='Не корректный номер телефона'
#         )
