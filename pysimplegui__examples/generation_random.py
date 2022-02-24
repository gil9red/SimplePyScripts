#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from random import randint

# pip install PySimpleGUI
import PySimpleGUI as sg


sg.theme('SystemDefault')
layout = [
    [sg.Text('Number of digits'), sg.Input(default_text='5', key='ND')],
    [sg.Text('Minimum'), sg.Input(default_text='1', key='Min')],
    [sg.Text('Maximum'), sg.Input(default_text='9', key='Max')],
    [sg.Text(' ', key='OUT')],
    [sg.Button('Generate'), sg.Button('Clear')]
]

window = sg.Window('Generator', layout)


def generate(number: int, min_number: int, max_number: int) -> str:
    return ''.join(str(randint(min_number, max_number)) for _ in range(number))


while True:
    event, values = window.read()
    if event is None or event == sg.WIN_CLOSED:
        break

    if event == 'Generate':
        number, min_number, max_number = int(values['ND']), int(values['Min']), int(values['Max'])
        text = generate(number, min_number, max_number)
        print(text)
        window['OUT'].update(f'Result: {text}')

    if event == 'Clear':
        window.find_element('ND').update('')
        window.find_element('Min').update('')
        window.find_element('Max').update('')
        window.find_element('OUT').update('')
