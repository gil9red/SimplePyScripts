#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import common


# TODO: сделать
# http://www.pfrf.ru/thm/common/mod/pensCalc/js/public.js
# TODO: добавить аннотации параметрам и возвращаемому значению

# # Служба в армии
# yearsInArmy, monthInArmy, daysInArmy

# # Уход за нетрудоспособными
# careYears, careMonth, careDays

# # Дети, не более 4х
# TODO: посмотреть к каким полям относится и переименвать соответственно и в формулах их использования
# childrenCount1, childrenVac1


# def pens_calc(gender, birthDate, pensionTarif,
#               yearsInArmy, monthInArmy, daysInArmy,
#               careYears, careMonth, careDays,
#               childrenCount1, childrenVac1,
#               retireWorkWithoutPension,
#               careerLength,
#               revenue,
#               SZPeriod
#               ):



# var pensionForm = $(".calc-form")
# var persionFormInputs = pensionForm.find("input,select")
# var calcResult = $(".pensionCalcResult")
# var calcResultToday = $(".pensionCalcResultToday")
# var socialPensionWarning = $("#socialPensionWarning")
# var socialPensionWarning2 = $("#socialPensionWarning2")
# var combinationWarning = $("#combinationWarning")
# var enterParamsWarning = $("#enterParamsWarning")
# var enterGenderWarning = $("#enterGenderWarning")
# var enterBYWarning = $("#enterBYWarning")
# var enterBYWarning2 = $("#enterBYWarning2")
# var enterBYWarning3 = $("#enterBYWarning3")
# var alreadyPensioneer = $("#alreadyPensioneer")
# var wrongFee = $("#wrongFee")
# var noTarif = $("#noTarif")
# var ending = $(".ending")
# var newCoefSummSmall = $(".newCoefSummSmall")
# var personOSsmall = $(".personOSsmall")
#
# var armySection = pensionForm.find('.army-section')

# TODO: возможно будет полезно узнать что скрыто в той секции
# armySection.hide()
# persionFormInputs.filter('[type="radio"][name="noArmy"]').click(function () {
#     if($(this).val() == 2) {
#         armySection.slideDown(150)
#     }
#     else {
#         armySection.slideUp(150)
#     }
# })

# var textInputs = persionFormInputs.filter("input[type='text']")
# var prevValues = []


# var careerPlanQuestions = $("div.careerPlanQuestions")
# var careerPlanSwitch = $("input[name='careerPlan']")
#
# function revealCPQuestionsBlocks(switchValue) {
#     careerPlanQuestions.hide()
#     switch(switchValue) {
#         case '1':
#             //наемный работник
#             careerPlanQuestions.filter(".careerPlan1").show()
#             break
#         case '2':
#             //самозанятый
#             careerPlanQuestions.filter(".careerPlan2").show()
#             break
#         case '3':
#             //совмещающий
#             careerPlanQuestions.show()
#             break
#     }
# }
#
# revealCPQuestionsBlocks(careerPlanSwitch.filter(':checked').val())
# careerPlanSwitch.change(function () {
#     revealCPQuestionsBlocks($(this).val())
# })


# TODO: поле в скрипте не имеет значения, вообще
gender = "1"
# if(gender.length < 1) {
#     enterGenderWarning.show()
#     $(output_area).slideDown()
#     return
# }

# TODO: поле в скрипте не имеет значения, вообще
birthDate = "1992"
# if(!birthDate.match(/\d{4}/)) {
#     enterBYWarning.show()
#     $(output_area).slideDown()
#     return
# }

# TODO: узнать что скрывается за полем
# TODO: пусть будет пока 0
pensionTarif = 0
# var pensionTarif = persionFormInputs.filter('[name="pensionTarif"]:checked')
# if(pensionTarif.length < 1) {
#     noTarif.show()
#     $(output_area).slideDown()
#     return
# }
# pensionTarif = parseInt(pensionTarif.val())

# Общий расчет

# Служба в армии
yearsInArmy = 1
monthInArmy = 0
daysInArmy = 0

# Стаж в армии
VS = ((((yearsInArmy * 12) + monthInArmy) / 12 * 365) + daysInArmy) / 365

# Коэффициент стажа
VSK = VS * common.VSkoef

# Уход за нетрудоспособными
careYears = 1
careMonth = 0
careDays = 0

# Стаж ухода за нетрудоспособными
CR = ((((careYears * 12) + careMonth) / 12 * 365) + careDays) / 365

# Коэффициент ухода
CRK = CR * common.CRkoef

# Дети, не более 4х
childrenCount1 = 1
if childrenCount1 < 0:
    childrenCount1 = 0

elif childrenCount1 > 4:
    childrenCount1 = 4

# TODO: узнать что за childrenVac1
# TODO: и что за стаж
# Стаж
childrenVac1 = 0
if childrenVac1 < 0:
    childrenVac1 = 0
    
elif childrenVac1 > 1.5:
    childrenVac1 = 1.5


# NOTE: только внутри кода объявляется
# Коэффициент
KD = 0.0

if childrenCount1 > 0:
    if childrenCount1 > 0:
        KD += 1.8

    if childrenCount1 > 1:
        KD += 3.6

    if childrenCount1 > 2:
        KD += 5.4

    if childrenCount1 > 3:
        KD += 5.4

    KD *= childrenVac1
    childrenVac1 *= childrenCount1

# Коэффициент за нетрудовые периоды
NK = KD + CRK + VSK

# Стаж за нетрудовые периоды
NS = childrenVac1 + VS + CR

# NOTE: сколько после пенсионного возраста собираешься работать неполучая пенсию
retireWorkWithoutPension = 5
if retireWorkWithoutPension > 10:
    retireWorkWithoutPension = 10

# Расчеты в зависимости от типа занятости
# TODO: узнать возможные варианты значения
careerPlan = '1'

# Наемный работник
def calcEmpl(fee: int, careerLength: int, pensionTarif: int):
    """

    :param fee: Зарплата
    :param careerLength: Стаж
    
    # TODO: узнать что за тариф такой
    :param pensionTarif: 
    :return:
    """

    if fee < 0:
        fee = 0

    if fee > common.ZPM:
        fee = common.ZPM

    if careerLength < 0:
        careerLength = 0

    # TODO: бросать исключение, узнать какой текст тут скрыт
    # if careerLength > 60) {
    #     enterBYWarning3.show()
    #     $(output_area).slideDown()
    #     return false

    # TODO: бросать исключение, узнать какой текст тут скрыт
    # # Зарплата меньше мрот
    # if careerLength > 0 and fee < common.MROT:
    #     wrongFee.show()
    #     $(output_area).slideDown()
    #     return false
    # }

    # Пенсионные коэффициенты за трудовой период
    IPKtrud = (fee / common.ZPM) * common.KNPG[pensionTarif] * (careerLength * 10)

    # TODO: Проследить за S и заменить
    return {
        'S': careerLength,
        'IPKtrud': IPKtrud,
    }

def calcSZ(SZPeriod: int, revenue: int, pensionTarif: int):
    """

    :param revenue: Годовой доход
    :param SZPeriod: Стаж
    
    # TODO: узнать что за тариф такой
    :param pensionTarif: 
    :return:
    """
    
    if SZPeriod < 0:
        SZPeriod = 0

    if revenue < 0:
        revenue = 0

    # TODO: разобраться какие значения может иметь pensionTarif
    SVGDkoeff = 16 if pensionTarif == 0 else 10

    # Сумма страховых взносов на страховую пенсию, начисленных исходя из размера годового дохода
    if revenue < common.GDmax:
        SVGD = (SVGDkoeff * (common.MROT * 0.26 * 12)) / 26
    else:
        SVGD = (SVGDkoeff * (common.MROT * 0.26 * 12) + ((revenue - common.GDmax) * 0.01)) / 26

    # Пенсионные коэффициенты за трудовой период
    IPKtrud = (SVGD / common.MSSV) * SZPeriod * 10

    # TODO: отследить и заменить S
    return {
        'S': SZPeriod, 
        'IPKtrud': IPKtrud
    }

calcPart = None
calcPartEmpl = None
calcPartSZ = None
IPKtrud = None
S = None

if careerPlan == '1':
    # Наемный работник
    calcPart = calcEmpl()
    # TODO: добавить проверку, проверить какое значение может возвращаться из функции и как влияет
    # возврат значения тут
    #
    # if(calcPart === false) return false

    # Стаж
    S = calcPart.S

    # Пенсионные коэффициенты
    IPKtrud = calcPart.IPKtrud

elif careerPlan == '2':
    # Самозанятый
    calcPart = calcSZ()

    # Стаж
    S = calcPart.S

    # Пенсионные коэффициенты
    IPKtrud = calcPart.IPKtrud

elif careerPlan == '3':
    # Совмещающий
    calcPartEmpl = calcEmpl()
    # TODO: добавить проверку, проверить какое значение может возвращаться из функции и как влияет
    # возврат значения тут
    #
    # if(calcPartEmpl === false) return false

    calcPartSZ = calcSZ()

    # Количество пенсионных коэффициентов свыше максимально установленного значения в год, полученных при совмещённой деятельности
    combinePeriod = 0
    # TODO: проверить
    # if(combinePeriod.length < 1) {
    #     combinePeriod = 0
    #     persionFormInputs.filter('#combinePeriod').val(combinePeriod)
    # }
    # TODO: проверить
    # if combinePeriod > Math.min(calcPartEmpl.S, calcPartSZ.S)) {
    #     combinationWarning.show()
    #     $(output_area).slideDown()
    #     return false
    # }

    # Годовой пенсионный коэффициент, получаемый гражданином в года совмещения деятельности
    IPKemp = calcPartEmpl.IPKtrud * combinePeriod / calcPartEmpl.S
    IPKsz = calcPartSZ.IPKtrud * combinePeriod / calcPartSZ.S
    IPKo = (IPKsz + IPKemp) / combinePeriod
    if IPKo > 10:
        IPKo = 10

    IPKis = IPKo * combinePeriod

    # Стаж
    S = calcPartEmpl.S + calcPartSZ.S - combinePeriod

    # Пенсионные коэффициенты
    IPKtrud = (calcPartSZ.IPKtrud - IPKsz) + (calcPartEmpl.IPKtrud - IPKemp) + IPKis
    if combinePeriod == 0:
        IPKtrud = calcPartSZ.IPKtrud + calcPartEmpl.IPKtrud


# Переходный период для наемных и самозанятых
if careerPlan == '1' or careerPlan == '2':
    IPKtrud2015 = 0
    IPKtrud2021 = 0

    fee = 10000
    revenue = 1
    if revenue < 0:
        revenue = 0

    # Сумма страховых взносов на страховую пенсию, начисленных исходя из размера годового дохода
    SVGD = 0
    SVGDkoeff = 16 if pensionTarif == 0 else 10

    if revenue < common.GDmax:
        SVGD = (SVGDkoeff * (common.MROT * 0.26 * 12)) / 26
    else:
        SVGD = (SVGDkoeff * (common.MROT * 0.26 * 12) + ((revenue - common.GDmax) * 0.01)) / 26

    if S > 5:
        IPKtrud2021 = IPKtrud * ((S - 5) / S)

        if careerPlan == '1':
            IPKtrud2015 = fee / common.ZPM * 10

        elif careerPlan == '2':
            IPKtrud2015 = (SVGD / common.MSSV) * 10

    elif S < 6:
        if careerPlan == '1':
            IPKtrud2015 = fee / common.ZPM * 10

        elif careerPlan == '2':
            IPKtrud2015 = (SVGD / common.MSSV) * 10

    # KNPG = 1
    if pensionTarif == '0':
        IPKtrud2015 = (S > 0 ? Math.min(8.26, IPKtrud2015) : 0) + (S > 1 ? Math.min(8.70, IPKtrud2015) : 0) +
            (S > 2 ? Math.min(9.13, IPKtrud2015) : 0) + (S > 3 ? Math.min(9.57, IPKtrud2015) : 0)

    # KNPG = 0.625
    else:
        IPKtrud2015 = (S > 0 ? Math.min(8.26, IPKtrud2015) : 0) + (S > 1 ? Math.min(5.43, IPKtrud2015) : 0) +
            (S > 2 ? Math.min(5.71, IPKtrud2015) : 0) + (S > 3 ? Math.min(5.98, IPKtrud2015) : 0)

    IPKtrud = IPKtrud2015 + IPKtrud2021


# TODO: какое-то обнуление значений в редакторе полей
# if(careerPlan == '1') {
#     persionFormInputs.filter('#SZPeriod').val(0)
#     persionFormInputs.filter('#revenue').val(0)
# }
# else {
#     if(careerPlan == '2') {
#         persionFormInputs.filter('#careerLength').val(0)
#         persionFormInputs.filter('#fee').val(0)
#     }
# }

# Пенсионные коэффициенты
IPK = (IPKtrud + NK) * common.SPKop[retireWorkWithoutPension]

# Общий стаж
OS = S + NS

# # NOTE: Установка значений
# newCoefSummSmall.html((Math.round(IPK * 100) / 100).toString())
# personOSsmall.html((Math.round(OS * 100) / 100).toString())


var WR = OS.toString().substr(-1)

ending.html('лет')

if(WR == 1) {
    ending.html('год')
}
else {
    if(WR >= 2 && WR <= 4) {
        ending.html('года')
    }
}

# пересчёт права выхода на пенсию по стажу (каждому году свой минимальный стаж)
$(output_area).hide()
if(S == 0 && OS < 8) {
    socialPensionWarning.show()
    $(output_area).slideDown()
    return false
}

if(S == 1 && OS < 9) {
    socialPensionWarning.show()
    $(output_area).slideDown()
    return false
}

if(S == 2 && OS < 10) {
    socialPensionWarning.show()
    $(output_area).slideDown()
    return false
}

if(S == 3 && OS < 11) {
    socialPensionWarning.show()
    $(output_area).slideDown()
    return false
}

if(S == 4 && OS < 12) {
    socialPensionWarning.show()
    $(output_area).slideDown()
    return false
}

if(S == 5 && OS < 13) {
    socialPensionWarning.show()
    $(output_area).slideDown()
    return false
}

if(S == 6 && OS < 14) {
    socialPensionWarning.show()
    $(output_area).slideDown()
    return false
}

if(S == 7 && OS < 15) {
    socialPensionWarning.show()
    $(output_area).slideDown()
    return false
}

//пересчёт права выхода на пенсию по ИПК (каждому году свой минимальный ИПК)
if(S == 0 && IPK < 11.4) {
    socialPensionWarning.show()
    $(output_area).slideDown()
    return false
}

if(S == 1 && IPK < 13.8) {
    socialPensionWarning.show()
    $(output_area).slideDown()
    return false
}

if(S == 2 && IPK < 16.2) {
    socialPensionWarning.show()
    $(output_area).slideDown()
    return false
}

if(S == 3 && IPK < 18.6) {
    socialPensionWarning.show()
    $(output_area).slideDown()
    return false
}

if(S == 4 && IPK < 21) {
    socialPensionWarning2.show()
    $(output_area).slideDown()
    return false
}

if(S == 5 && IPK < 23.4) {
    socialPensionWarning.show()
    $(output_area).slideDown()
    return false
}

if(S == 6 && IPK < 25.8) {
    socialPensionWarning.show()
    $(output_area).slideDown()
    return false
}

if(S == 7 && IPK < 28.2) {
    socialPensionWarning.show()
    $(output_area).slideDown()
    return false
}

if(S == 8 && IPK < 30) {
    socialPensionWarning.show()
    $(output_area).slideDown()
    return false
}

# Страховая пенсия
SP = (common.FIKS * common.BPKop[retireWorkWithoutPension]) + (IPK * common.CPK)

var newCoefSummCont = $("#newCoefSumm")
newCoefSummCont.html((Math.round(IPK * 100) / 100).toString())

var pensionIPartCont = $("#pensionIPart")
pensionIPartCont.html((Math.round(SP * 100) / 100).toString())

var personOSCont = $("#personOS")
personOSCont.html((Math.round(OS * 100) / 100).toString())
