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



var pensionForm = $(".calc-form")
var persionFormInputs = pensionForm.find("input,select")
var calcResult = $(".pensionCalcResult")
var calcResultToday = $(".pensionCalcResultToday")
var socialPensionWarning = $("#socialPensionWarning")
var socialPensionWarning2 = $("#socialPensionWarning2")
var combinationWarning = $("#combinationWarning")
var enterParamsWarning = $("#enterParamsWarning")
var enterGenderWarning = $("#enterGenderWarning")
var enterBYWarning = $("#enterBYWarning")
var enterBYWarning2 = $("#enterBYWarning2")
var enterBYWarning3 = $("#enterBYWarning3")
var alreadyPensioneer = $("#alreadyPensioneer")
var wrongFee = $("#wrongFee")
var noTarif = $("#noTarif")
var ending = $(".ending")
var newCoefSummSmall = $(".newCoefSummSmall")
var personOSsmall = $(".personOSsmall")

var armySection = pensionForm.find('.army-section')
armySection.hide()
persionFormInputs.filter('[type="radio"][name="noArmy"]').click(function () {
    if($(this).val() == 2) {
        armySection.slideDown(150)
    }
    else {
        armySection.slideUp(150)
    }
})

var textInputs = persionFormInputs.filter("input[type='text']")
var prevValues = []

textInputs.focus(function () {
    prevValues[$(this).attr('id')] = $(this).val()
    $(this).val('')
})

textInputs.blur(function () {
    $(this).val($(this).val().toString().replace(/,/, '.').replace(/[^\d.,]+/, ''))
    if($(this).val() == '') $(this).val(prevValues[$(this).attr('id')])
})

$(".performCalc").click(function (e) {
    $('.result-top, .result-bottom').hide()
    e.preventDefault()
    recalculateForm('.result-bottom')
})

var careerPlanQuestions = $("div.careerPlanQuestions")
var careerPlanSwitch = $("input[name='careerPlan']")

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


function recalculateForm(output_area) {
    var genderInput = persionFormInputs.filter('[name="gender"]') //выбор пола

    if(genderInput.length < 1) {
        enterGenderWarning.show()
        $(output_area).slideDown()
        return
    }

    var birthDateVal = persionFormInputs.filter('#birthDate').val() //заполнен год рождения
    if(!birthDateVal.match(/\d{4}/)) {
        enterBYWarning.show()
        $(output_area).slideDown()
        return
    }

    var personTariff = persionFormInputs.filter('[name="pensionTarif"]:checked')
    if(personTariff.length < 1) {
        noTarif.show()
        $(output_area).slideDown()
        return
    }
    personTariff = parseInt(personTariff.val())

    // Общий расчет

    // Служба в армии
    var VSyears = parseInt(persionFormInputs.filter('[name="yearsInArmy"]').val())
    var VSmonth = parseInt(persionFormInputs.filter('[name="monthInArmy"]').val())
    var VSdays = parseInt(persionFormInputs.filter('[name="daysInArmy"]').val())

    // Стаж
    var VS = ((((VSyears * 12) + VSmonth) / 12 * 365) + VSdays) / 365

    // Коэффициент
    var VSK = VS * common.VSkoef

    // Уход за нетрудоспособными
    var CRyears = parseInt(persionFormInputs.filter('[name="careYears"]').val())
    var CRmonth = parseInt(persionFormInputs.filter('[name="careMonth"]').val())
    var CRdays = parseInt(persionFormInputs.filter('[name="careDays"]').val())

    // Стаж
    var CR = ((((CRyears * 12) + CRmonth) / 12 * 365) + CRdays) / 365

    // Коэффициент
    var CRK = CR * common.CRkoef

    // Дети, не более 4х
    var D = parseInt(persionFormInputs.filter('#childrenCount1').val())
    if(D < 0) {
        D = 0
    }
    else {
        if(D > 4) D = 4
    }

    // Стаж
    var DO = parseFloat(persionFormInputs.filter('#childrenVac1').val())
    if(DO < 0) {
        DO = 0
    }
    else {
        if(DO > 1.5) DO = 1.5
    }

    // Коэффициент
    var KD = 0

    if(D > 0) {
        KD = DO * (D > 0 ? 1.8 + (D > 1 ? 3.6 + (D > 2 ? 5.4 + (D > 3 ? (5.4) : 0) : 0) : 0) : 0)
        DO = DO * D
    }

    // Коэффициент за нетрудовые периоды
    var NK = KD + CRK + VSK

    // Стаж за нетрудовые периоды
    var NS = DO + VS + CR

    var retireWork = persionFormInputs.filter('#retireWorkWithoutPension').val()
    if(retireWork > 10) retireWork = 10

    // Расчеты в зависимости от типа занятости
    var careerPlan = persionFormInputs.filter('[name="careerPlan"]:checked').val()

    # Наемный работник
    def calcEmpl(fee: int, careerLength: int, personTariff: int):
        """

        :param fee: Зарплата
        :param careerLength: Стаж
        
        # TODO: узнать что за тариф такой
        :param personTariff: 
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
        IPKtrud = (fee / common.ZPM) * common.KNPG[personTariff] * (careerLength * 10)

        # TODO: Проследить за S и заменить
        return {
            'S': careerLength,
            'IPKtrud': IPKtrud,
        }

    def calcSZ(SZPeriod: int, revenue: int, personTariff: int):
        """

        :param revenue: Годовой доход
        :param SZPeriod: Стаж
        
        # TODO: узнать что за тариф такой
        :param personTariff: 
        :return:
        """
        
        if SZPeriod < 0:
            SZPeriod = 0

        if revenue < 0:
            revenue = 0

        # TODO: разобраться какие значения может иметь personTariff
        SVGDkoeff = 16 if personTariff == 0 else 10

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

    var calcPart = null
    var calcPartEmpl = null
    var calcPartSZ = null
    var IPKtrud = null
    var S = null
    //var selhoz = 0
    switch(careerPlan) {
        case '1':
            //наемный работник
            calcPart = calcEmpl()
            if(calcPart === false) return false

            //selhoz = persionFormInputs.filter('#careerSelHoz').val()

            // Стаж
            S = calcPart.S

            // Пенсионные коэффициенты
            IPKtrud = calcPart.IPKtrud

            break
        case '2':
            //самозанятый
            calcPart = calcSZ()

            // Стаж
            S = calcPart.S

            // Пенсионные коэффициенты
            IPKtrud = calcPart.IPKtrud

            break
        case '3':
            //совмещающий
            calcPartEmpl = calcEmpl()
            if(calcPartEmpl === false) return false

            calcPartSZ = calcSZ()

            //selhoz = persionFormInputs.filter('#careerSelHoz').val()

            // Количество пенсионных коэффициентов свыше максимально установленного значения в год, полученных при совмещённой деятельности
            var So = persionFormInputs.filter('#combinePeriod').val()
            if(So.length < 1) {
                So = 0
                persionFormInputs.filter('#combinePeriod').val(So)
            }
            if(So > Math.min(calcPartEmpl.S, calcPartSZ.S)) {
                combinationWarning.show()
                $(output_area).slideDown()
                return false
            }

            // Годовой пенсионный коэффициент, получаемый гражданином в года совмещения деятельности
            var IPKemp = calcPartEmpl.IPKtrud * So / calcPartEmpl.S
            var IPKsz = calcPartSZ.IPKtrud * So / calcPartSZ.S
            var IPKo = (IPKsz + IPKemp) / So
            if(IPKo > 10) IPKo = 10
            var IPKis = IPKo * So

            // Стаж
            S = calcPartEmpl.S + calcPartSZ.S - So

            // Пенсионные коэффициенты
            IPKtrud = (calcPartSZ.IPKtrud - IPKsz) + (calcPartEmpl.IPKtrud - IPKemp) + IPKis
            if(So == 0) {
                IPKtrud = calcPartSZ.IPKtrud + calcPartEmpl.IPKtrud
            }

            break
    }

    // Переходный период для наемных и самозанятых
    if(careerPlan == '1' || careerPlan == '2') {
        var IPKtrud2021 = 0
        var ZP = persionFormInputs.filter('#fee').val()
        var IPKtrud2015 = 0
        var GD = parseInt(persionFormInputs.filter('#revenue').val())
        if(GD.length < 1) {
            GD = 0
        }
        if(GD < 0) GD = 0

        // Сумма страховых взносов на страховую пенсию, начисленных исходя из размера годового дохода
        var SVGD = 0
        var SVGDkoeff = 0
        if(personTariff == 0) {
            SVGDkoeff = 16
        }
        else {
            SVGDkoeff = 10
        }

        if(GD < common.GDmax) {
            SVGD = (SVGDkoeff * (common.MROT * 0.26 * 12)) / 26
        }
        else {
            SVGD = (SVGDkoeff * (common.MROT * 0.26 * 12) + ((GD - common.GDmax) * 0.01)) / 26
        }

        if(S > 5) {
            IPKtrud2021 = IPKtrud * ((S - 5) / S)
            if(careerPlan == '1') {
                IPKtrud2015 = ZP / common.ZPM * 10
            }
            else {
                if(careerPlan == '2') {
                    IPKtrud2015 = (SVGD / common.MSSV) * 10
                }
            }
        }
        if(S < 6) {
            IPKtrud2021 = 0
            if(careerPlan == '1') {
                IPKtrud2015 = ZP / common.ZPM * 10
            }
            else {
                if(careerPlan == '2') {
                    IPKtrud2015 = (SVGD / common.MSSV) * 10
                }
            }
        }

        if(personTariff == '0') { //KNPG = 1
            IPKtrud2015 = (S > 0 ? Math.min(8.26, IPKtrud2015) : 0) + (S > 1 ? Math.min(8.70, IPKtrud2015) : 0) +
                (S > 2 ? Math.min(9.13, IPKtrud2015) : 0) + (S > 3 ? Math.min(9.57, IPKtrud2015) : 0)
        }
        else { //KNPG = 0.625
            IPKtrud2015 = (S > 0 ? Math.min(8.26, IPKtrud2015) : 0) + (S > 1 ? Math.min(5.43, IPKtrud2015) : 0) +
                (S > 2 ? Math.min(5.71, IPKtrud2015) : 0) + (S > 3 ? Math.min(5.98, IPKtrud2015) : 0)
        }


        IPKtrud = IPKtrud2015 + IPKtrud2021

    }

    if(careerPlan == '1') {
        persionFormInputs.filter('#SZPeriod').val(0)
        persionFormInputs.filter('#revenue').val(0)
    }
    else {
        if(careerPlan == '2') {
            persionFormInputs.filter('#careerLength').val(0)
            persionFormInputs.filter('#fee').val(0)
        }
    }

    // Пенсионные коэффициенты
    var IPK = (IPKtrud + NK) * common.SPKop[retireWork]

    // Общий стаж
    var OS = S + NS

    newCoefSummSmall.html((Math.round(IPK * 100) / 100).toString())
    personOSsmall.html((Math.round(OS * 100) / 100).toString())

    if(lang == 'ru') {
        newCoefSummSmall.html(newCoefSummSmall.html().replace(/\./, ","))
        personOSsmall.html(personOSsmall.html().replace(/\./, ","))
    }

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

    //пересчёт права выхода на пенсию по стажу (каждому году свой минимальный стаж)
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

    // Страховая пенсия
    var SP = (common.FIKS * common.BPKop[retireWork] /** common.CSH[selhoz]*/) +
        (IPK * common.CPK)

    var newCoefSummCont = $("#newCoefSumm")
    newCoefSummCont.html((Math.round(IPK * 100) / 100).toString())
    
    var pensionIPartCont = $("#pensionIPart")
    pensionIPartCont.html((Math.round(SP * 100) / 100).toString())
    
    var personOSCont = $("#personOS")
    personOSCont.html((Math.round(OS * 100) / 100).toString())
}
