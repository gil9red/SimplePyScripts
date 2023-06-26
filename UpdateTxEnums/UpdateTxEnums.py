# -*- encoding: utf-8 -*-

# TXSST-148:
# Нужно написать скрипт, который будет автоматически генерировать классы
# перечеслений на C# в соответствии с этими перечислениями в транзаксисе.
# Особенно актуально для CustInfoKind, т.к. оно периодически обновляется
# и его можно задавать при настройке объектов сценария.

__author__ = "ipetrash"

##############################################################################################################################################
# Список путей к перечислениям в TX
enums_param = (
    'com.tranzaxis/ads/Applications/src/acsIFBAJ3UCLJCJ7GPUOYTFLPG6SA.xml',  # AppContextType
    'com.tranzaxis/ads/Applications/src/acsSD3DHF4ZUFAB3KX35PEJ4OHSTU.xml',  # AppStatus
    'com.tranzaxis/ads/Contracts.Issuing.Auth/src/acsVEXRELGU2LNRDCKSABIFNQAABA.xml',  # AuthKind
    'com.tranzaxis/ads/Contracts.Payee/src/acsJWRSPPZWDZFXDOCLADLICTEX7A.xml',  # BillPayerIdKind
    'com.tranzaxis/ads/Contracts.Payee/src/acsHG4RXL72UPORDMCJAAN7YHKUNI.xml',  # BillStatus
    'com.tranzaxis/ads/Tran/src/acsM46GFSUHXLNRDISQAAAAAAAAAA.xml',  # CardEntryMode
    'com.tranzaxis/ads/Contracts/src/acsVVHXZECSARHYHJKJACJL34DMQ4.xml',  # ContractPaymentScheduleVariant
    'com.tranzaxis/ads/Tran/src/acsJGWPFMH26POBDCS6CEIRCEIRCE.xml',  # CustInfoGroupKind
    'com.tranzaxis/ads/Tran/src/acsUOT6QZNAXLNRDISQAAAAAAAAAA.xml',  # CustInfoKind
    'com.tranzaxis/ads/Tran/src/acs5JBMR3JAQZHOJK5EXTAL4JLG5E.xml',  # Cvv2PresenceIndicator
    'com.tranzaxis/ads/Acquiring/src/acsECWMKIMPR7ORDATEABIFNQAABA.xml',  # DispenseAlgorithms
    'com.tranzaxis/ads/Dictionaries/src/acsFS4HJ5X2GVBAFA5O4GCWJPA5AM.xml',  # ExtDictName
    'com.tranzaxis/ads/Tran/src/acsZT3KQ2Q2FLOBDPRXAAMPGXUWTQ.xml',  # IsoAccountType
    'com.tranzaxis/ads/Tran/src/acsLGE6TVARWXNRDISQABIFNQAABA.xml',  # LifePhase
    'com.tranzaxis/ads/Contracts.Links/src/acsBBORFO465LOBDCSWCEIRCEIRCE.xml',  # LinkKind
    'com.tranzaxis/ads/Contracts.Links/src/acsB5NXRS475LOBDCSWCEIRCEIRCE.xml',  # LinkStatus
    'com.tranzaxis/ads/Acquiring/src/acs5B443MRWQ3ORDC7EABIFNQAABA.xml',  # Operation
    'com.tranzaxis/ads/Tran/src/acsZEICBDYU6RB2JCMWXRPBBJ6664.xml',  # PayeeType
    'com.tranzaxis/ads/Tran/src/acs4FP4ON47XLNRDISQAAAAAAAAAA.xml',  # RefineKind
    'com.tranzaxis/ads/Monitoring/src/acsR4XK344W7VEG5CZDON3LXTG36Q.xml',  # ResetDeviceType
    'com.tranzaxis/ads/Tran/src/acsWJJIQNA4FLOBDPRXAAMPGXUWTQ.xml',  # ReversalReason
    'com.tranzaxis/ads/Tariffs/src/acs2FZR6ZACYXORDIRDAAN7YHKUNI.xml',  # SurchPayer
    'com.tranzaxis/ads/Monitoring/src/acsOESYDXFMGZBJZEHB45NKF63DNQ.xml',  # TermCassetteDeviceKind
    'com.tranzaxis/ads/Monitoring/src/acsABNR6BVIHJHWPNJEEJWWBK4P4E.xml',  # TermCommandKind
    'com.tranzaxis/ads/Monitoring/src/acsTPOMJYIF6NAQVL6AIBKEP3QT5U.xml',  # TermCommandStatus
    'com.tranzaxis/ads/Tokens/src/acs7NER266U2LNRDCKSABIFNQAABA.xml',  # TokenKind
    'com.tranzaxis/ads/Tokens/src/acsKM6XPNGY2LNRDCKSABIFNQAABA.xml',  # TokenStatus
    'com.tranzaxis/ads/Tran/src/acsOL33OVLMSXNRDDXBABIFNQAAAE.xml',  # TranKind
    'com.tranzaxis/ads/Tran/src/acsU47BUCPQWTNRDISQABIFNQAABA.xml',  # TranResult
)

## Комментарии констант перечислений.
# Ключем является id перечисления, а значением словарь: ключ - имя константы, значение - комментарий константы.
dict_enum_constants_comments = {
    # # AppContextType
    # 'acsIFBAJ3UCLJCJ7GPUOYTFLPG6SA' : {
    #
    # },
    #
    # # AppStatus
    # 'acsSD3DHF4ZUFAB3KX35PEJ4OHSTU' : {
    #
    # },
    #
    # # AuthKind
    # 'acsVEXRELGU2LNRDCKSABIFNQAABA' : {
    #
    # },
    #
    # # BillPayerIdKind
    # 'acsJWRSPPZWDZFXDOCLADLICTEX7A' : {
    #
    # },
    #
    # # BillStatus
    # 'acsHG4RXL72UPORDMCJAAN7YHKUNI' : {
    #
    # },
    #
    # # CardEntryMode
    # 'acsM46GFSUHXLNRDISQAAAAAAAAAA' : {
    #
    # },
    #
    # # ContractPaymentScheduleVariant
    # 'acsVVHXZECSARHYHJKJACJL34DMQ4' : {
    #
    # },
    #
    # # CustInfoGroupKind
    # 'acsJGWPFMH26POBDCS6CEIRCEIRCE' : {
    #
    # },
    #
    # # CustInfoKind
    # 'acsUOT6QZNAXLNRDISQAAAAAAAAAA' : {
    #
    # },

    # Cvv2PresenceIndicator 
    'acs5JBMR3JAQZHOJK5EXTAL4JLG5E': {
        'NotProvided': u'Не предоставлен торговцем.',
        'IllegibleOnCard': u'Имеет неверное значение.',
        'AbsentFromCard': u'Отсутствует на карте.'
    },

    # # DispenseAlgorithms
    # 'acsECWMKIMPR7ORDATEABIFNQAABA' : {
    #
    # },

    # ExtDictName 
    'acsFS4HJ5X2GVBAFA5O4GCWJPA5AM': {
        'Currency': u'Справочник содержит <code>alpha3</code> код валюты, название валюты, символ валюты,\n'
                    u'количество знаков после запятой, разделяющих основные и вспомогательные единицы измерения\n'
                    u'(например, у рубля - 2, т.к. в одном рубле - 100 копеек), и признак того, с какой стороны\n'
                    u'суммы необходимо приписывать символ валюты.',
        'Country': u'Справочник стран. Содержит <code>alpha2</code> и <code>alpha3</code> коды стран.',
        'BankCode': u'Справочник банковский идентификационный кодов (БИК-ов).',
        'User': u'Пользовательский справочник, содержащий любую информацию, разделенную на несколько секций.',
    },

    # # IsoAccountType
    # 'acsZT3KQ2Q2FLOBDPRXAAMPGXUWTQ' : {
    #
    # },
    #
    # # LifePhase
    # 'acsLGE6TVARWXNRDISQABIFNQAABA' : {
    #
    # },
    #
    # # LinkKind
    # 'acsBBORFO465LOBDCSWCEIRCEIRCE' : {
    #
    # },

    # LinkStatus 
    'acsB5NXRS475LOBDCSWCEIRCEIRCE': {
        'A': u'Активная.',
        'IO': u'Только информация.',
        'CO': u'Только приход.',
        'CIO': u'Только приход и информация.',
        'B': u'Заблокирована.',
        'D': u'Деактивирована.',
        'C': u'Закрыта.',
    },

    # Operation 
    'acs5B443MRWQ3ORDC7EABIFNQAABA': {
        'AddPaymentTemplate': u'Управление персональными шаблонами платежей финансового контракта.\n'
                              u'Эти операции используются в интернет-банке.',
        'CancelApplication': u'Аннулирование клиентом заготовки заявления.',
        'CreateLogin': u'Создание токена регистрационного имени.\n'
                       u'В запросе должен быть заполнен Specific.CreateLogin.\n'
                       u'В ответе в Specific.CreateLogin передается идентификатор созданного токена.',
        'CreateVirtualCard': u'Создание виртуальной карты.\n'
                             u'В запросе должен быть заполнен Specific.CreateVirtualCard.',
        'DelPaymentTemplate': u'Управление персональными шаблонами платежей финансового контракта.\n'
                              u'Эти операции используются в интернет-банке.',
        'Exchange': \
            u"""Эта операция допустима только в терминалах, оборудованных устройствами вложения и выдачи купюр.
Обмен валюты: клиент вкладывает одну валюту и получает другую плюс сдачу в валюте вложения.
Получение сдачи от клиента (т.е. дополнительное вложение в валюте выдачи) не поддерживается.
В запросе заполняются rq.Specific.Exchange (InAmt, InCcy) – сумма и валюта вложения,
rq.Money.Ccy – валюта выдачи. Так же для алгоритма выдачи купюр (см. выше) передается информация
о кассетах из OperationRq.Cassettes и OperationRq.Specific.DispenseAlgo.
Сумма выдачи рассчитывается как term.rateGroup.convert(term.operDay, curTime(), inCcy,inAmt, outCcy).
Если точную сумму выдать нельзя, выдается максимальная меньшая сумма в валюте outCcy плюс максимальная
сдача в валюте inCcy.
Выдаваемая сумма с разбивкой по валютам передается в ответе хоста в Withdrawal.Amt и Withdrawal.Ccy,
а покассетная раскладка – в Withdrawal.Cassetes. Информация по сдаче передается в Exchange.Cashback.
При необходимости информировать клиента о сумме, которую он получит в результате обмена, терминал
сначала присылает запрос с установленным флагом Specific.Exchange.CalcOnly и получает в ответе
Withdrawal, Exchange.Cashback. При этом транзакция не выполняется.""",
        'ModifyPaymentTemplate': u'Управление персональными шаблонами платежей финансового контракта.\n'
                                 u'Эти операции используются в интернет-банке.',
        'SetupNotification': u'Управление параметрами своего контракта нотификации.',
        'SubmitApplication': u'Подача клиентом заявления.',
        'UpdateClientInfo': u'Изменение информации по клиенту, предпочтений клиента (например состава\n'
                            u'главной страницы телебанка), названий его контрактов и токенов.',
    },

    # # PayeeType
    # 'acsZEICBDYU6RB2JCMWXRPBBJ6664' : {
    #
    # },

    # RefineKind
    'acs4FP4ON47XLNRDISQAAAAAAAAAA': {
        'CapSign': u'Электронная подпись с карты.',
        'CapOtp': u'Одноразовый пароль с карты.',
        'Callback': u'Одноразовый код.',
        'CustomerContract': u'Контракт клиента.',
        'PayeeContract': u'Контракт получателя платежа.',
        'PaymentParam': u'Параметр платежа.',
        'PaymentTemplate': u'Шаблон платежа.',
        'TranSign': u'Электронная подпись с сертификата.',
        'AuthToken': u'Токен для аутентификации.',
        'UD': u'Пользовательский.',
    },

    # # ResetDeviceType
    # 'acsR4XK344W7VEG5CZDON3LXTG36Q' : {
    #
    # },

    # ReversalReason
    'acsWJJIQNA4FLOBDPRXAAMPGXUWTQ': {
        'Cancel': u'Отмена.',
        'InvalidRes': u'Неверный ответ.',
        'Timeout': u'Тайм-аут.',
        'HardwareError': u'Ошибка оборудования.',
        'DestNotAvail': u'Цель не доступна.',
        'Duplicate': u'Дубликат.',
        'Suspect': u'Подозрение.',
        'InvalidMAC': u'Неверный MAC в ответе.',
    },

    # SurchPayer
    'acs2FZR6ZACYXORDIRDAAN7YHKUNI': {
        'Cust': u'Клиент.',
        'Payee': u'Получатель платежа.',
        'Cash': u'Доплата наличными.',
    },

    # # TermCassetteDeviceKind
    # 'acsOESYDXFMGZBJZEHB45NKF63DNQ' : {
    #
    # },

    # TermCommandKind 
    'acsABNR6BVIHJHWPNJEEJWWBK4P4E': {
        'UNKNOWN': u'Псевдо-тип, не существует на самом деле.',
        'UpdateKeys': u'Обновление рабочих ключей.',
        'PollCounters': u'Запрос счетчиков терминала.\nНа данный момент хостом не передается.',
        'PollState': u'Запрос состояния терминала.',
        'UploadJournal': u'Выгрузить журнал терминала.\nНа данный момент хостом не передается.',
        'Ping': u'Проверка связи.',
        'ResetConnection': u'Оборвать связь с терминалом.\nНа данный момент хостом не передается.',
    },

    # TermCommandStatus
    'acsTPOMJYIF6NAQVL6AIBKEP3QT5U': {
        'MaxExecuted': u'Максимальное значение статуса для исполненных команд.\n'
                       u'Статусы, меньшие этого значения, являются статусами исполненной команды.\n'
                       u'Не является конкретным статусом, служит только для удобства выборок из базы на стороне хоста.',
        'Failed': u'Во время исполнения команды произошла ошибка, команда не выполнена или выполнена частично.',
        'Executed': u'Команда успешно выполнена.',
        'Aborted': u'Выполнение команды отменено.',
        'MaxExecuting': u'Максимальное значение статуса для исполняющихся команд.\n'
                        u'Статусы, меньшие этого значения, являются статусами исполнения команды.\n'
                        u'Не является конкретным статусом, служит только для удобства выборок из базы на стороне хоста.',
        'InProgress': u'В данный момент команда исполняется.',
        'Pending': u'Команда запланирована к исполнению.',
    },

    # # TokenKind
    # 'acs7NER266U2LNRDCKSABIFNQAABA' : {
    #
    # },
    #
    # # TokenStatus
    # 'acsKM6XPNGY2LNRDCKSABIFNQAABA' : {
    #
    # },
    #
    # # TranKind
    # 'acsOL33OVLMSXNRDDXBABIFNQAAAE' : {
    #
    # },
    #
    # # TranResult
    # 'acsU47BUCPQWTNRDISQABIFNQAABA' : {
    #
    # },
}

## Типы констант перечислений. В Tx описаны как домены.
# Id домена и тип
domain_EnumType = {
    'dmn5C7MFSCXG5DMHD6VBNNFMOKMCY': 'Str',
    'dmnWCT53VRT25CPTCNKGDWCWBGVFQ': 'Int',
    'dmnTBC4JQ6TK5CPTGM34STTG7FIUY': 'Num',
    'dmnNRLEPU3CWJDPRE3FTOTWC73EWA': 'Bool',
    'dmnY4YSMMGJOFCKJL53ARV2E6KLRY': 'DateTime',
    'dmnI2D2LWCBWNDNXHKDAKMD4N5FEU': 'Bin',
    'dmn4E6ZRYJ3KRH6ZIPOXBIKDOEPGY': 'Xml',
    'dmnDXYK3RG62JHMDIU2WYJWQKUVPA': 'InputFormat',
    'dmnZJ3T2JMIVVGCVMBN7QUUVR6J7A': 'PaymentTemplate',
    'dmnCC6F5XVGSRBQXBYW5FYXLW5SIU': 'PaymentParams',
    'dmnS2VO4BJXZZA5RM7IJEHXIRY62I': 'NotifyContract',
    'dmnJOIYPO6HRBDKJEQW733QDIX5QI': 'NotifyTypes',
    'dmnYZAOFLKQGJALDFNLHZS4ION7DQ': 'ReportPubs',
    'dmnHEK6VMQP5ZA23M5TMHJNUNUVTY': 'UserAttrs',
    'dmn4ZQWE4LREJGM7C3FTOYWJHEZ7M': 'ArrStr',
    'dmnICZAPVCAPFDRLFNYXPZWJWRZW4': 'ArrInt',
    'dmnBAMUXE7FXRARLCIU74E73YLG3E': 'ArrNum',
    'dmn3J7AH6MRVBH4LKJL2ORF6MRS5Y': 'ArrBool',
    'dmnMHBYTBRDVJAOFPBKZW3LWTC3X4': 'ArrDateTime',
}

## Группирование констант перечисления.
# Id домена и группа
domain_Group = {
    'dmnAONDUEY2V5GKTL2BIUJYQMTGJE': 'Applications',
    'dmn4GN4AXEU7RC6RF5FW67R3XUVYM': 'ApplicationTypeDir',
    'dmnRXSMTIMAFRGH7NPS7YBPKWQKS4': 'PaymentBill',
    'dmn54EQWKGI2ZFLLCMI4WPONNQTW4': 'C2Cs',
    'dmnKDQ4OBEFXNDQPJYMYOWM377BMQ': 'Contracts',
    'dmnUQAX7IDOEFF27M3VA3GX4BL2Y4': 'ContractOwnerDoc',
    'dmnPGVZFTTKNRHL3JRQPXTJ4MBMMY': 'Holds',
    'dmnK4W25RE4WFHO7LAHKQY2VOR2IU': 'NotifyContract',
    'dmnYJQUAP3XOZCSBDY7GVQSRCYGEY': 'Payee',
    'dmnPJMGUFSF6NFMLJEJAKC6UDIBOI': 'PaymentParam',
    'dmn2XNW24AFVRDHZP47BTUXYGS7YY': 'PaymentTemplate',
    'dmnLUZVPS5AMFG4ZOWWCB2YX2TPYE': 'PaymentVoucher',
    'dmnF5THD2MAPJHNNO4LWO6TDBAXGQ': 'StandingOrderTypeDir',
    'dmnH6C3ONY5YNCIPMUC34NFDSOLSM': 'Tokens',
    'dmnLWP5UBBN4BBXZJGKFOWMKRE7TY': 'C2CRstrs',
    'dmn4XY2EYNBSJCNDAQIS4KWLWDKZA': 'ContractRstrs',
    'dmn6PSG2FNMI5FSPDU72TFLWZLLJE': 'TokenRstrs',
}

## Атрибуты констант перечисления TranResult.
# В TX об них нет информации, но она нужна, потому придется вручную добавить.
# Id домена и тип.
attribute_EnumItem_TranResult = {
    'Aborted': 'Declined',
    'AccountIsClosed': 'Declined',
    'AcquirerLimitHasBeenReached': 'LimitExceeded',
    'AcquirerLimitWillBeExceeded': 'LimitExceeded',
    'AcquirerRestrictionViolated': 'LimitExceeded',
    'Approved': 'Authorized',
    'ArqcAuthFailed': 'Declined',
    'AuthenticationFailed': 'Declined',
    'CantFindContract': 'InvalidAccount',
    'CapAuthenticationFailed': 'Declined',
    'CavvAuthFailed': 'Declined',
    'ContractDayClosed': 'Declined',
    'ContractIsBlocked': 'Declined',
    'ContractIsClosed': 'Declined',
    'ContractIsNotStarted': 'Declined',
    'ContractIsRestricted': 'Declined',
    'CustContractNotFound': 'InvalidAccount',
    'CustTokenInvalid': 'Declined',
    'Cvv2AuthFailed': 'Declined',
    'CvvAuthFailed': 'Declined',
    'DestNotAvail': 'InvalidDestinationAccount',
    'DuplicateRequest': 'Declined',
    'ExceptionalCardNotFound': 'Declined',
    'FormatError': 'Declined',
    'InstitutionDayClosed': 'Declined',
    'InsufficientAuth': 'Declined',
    'InsufficientFunds': 'InsufficientFunds',
    'InternetPinAuthFailed': 'Declined',
    'InvalidContract': 'InvalidAccount',
    'InvalidContractLink': 'Declined',
    'InvalidLink': 'Declined',
    'InvalidRequest': 'Declined',
    'IssuerLimitHasBeenReached': 'LimitExceeded',
    'IssuerLimitWillBeExceeded': 'LimitExceeded',
    'IssuerRestrictionViolated': 'LimitExceeded',
    'LoginAlreadyRegistered': 'Declined',
    'LoginPasswordExpired': 'Declined',
    'LoginPasswordWasUsed': 'Declined',
    'MacError': 'Declined',
    'NeedConfirmFinPlan': 'HostInfoRequest',
    'NeedConfirmSurcharges': 'HostInfoRequest',
    'NeedCorrection': 'HostInfoRequest',
    'NeedRefine': 'HostInfoRequest',
    'PartyNotExists': 'Declined',
    'PasswordAuthFailed': 'Declined',
    'PayeeCardInvalid': 'InvalidPayeeInfo',
    'PayeeInvalid': 'InvalidPayeeInfo',
    'PaymentParamsInvalid': 'InvalidPayeeInfo',
    'PinAuthFailed': 'IncorrectPIN',
    'Predeclined': 'Declined',
    'Preprocessed': 'HostInfoRequest',
    'ProcessorLimitHasBeenReached': 'LimitExceeded',
    'ProcessorLimitWillBeExceeded': 'LimitExceeded',
    'ProcessorRestrictionViolated': 'LimitExceeded',
    'RecipientRoutingError': 'CommsError',
    'RecipientTokenInvalid': 'Declined',
    'RecipientTokenNotFound': 'Declined',
    'Rejected': 'Declined',
    'RoutingError': 'CommsError',
    'SecretValueTryExceeded': 'Declined',
    'SettlementBalanceExhausted': 'Declined',
    'SettlementDeferred': 'Declined',
    'SignAuthFailed': 'Declined',
    'SystemError': 'Declined',
    'TimeoutRevNotMatched': 'Declined',
    'TokenIsBlocked': 'Declined',
    'TokenIsClosed': 'Declined',
    'TokenIsCompromised': 'Declined',
    'TokenIsDeactivated': 'Declined',
    'TokenIsDomestic': 'Declined',
    'TokenIsExpired': 'Declined',
    'TokenIsLost': 'Declined',
    'TokenIsNotOpened': 'Declined',
    'TokenIsNotStarted': 'Declined',
    'TokenIsReferral': 'Declined',
    'TokenIsRestricted': 'Declined',
    'TokenIsStolen': 'Declined',
    'TokenNotFound': 'Declined',
    'WrongMacKeyId': 'Declined',
    'WrongPinKeyId': 'IncorrectPIN',
}


## Атрибуты констант перечисления Operation.
# В TX об них нет информации, но она нужна, потому придется вручную добавить.
# Id домена и тип.
attribute_EnumItem_Operation = {
    'CashDeposit': '[Reversible]',
    'Payment': '[Reversible]',
    'PaymentCredit': '[Reversible]',
    'TerminalRefill': '[Reversible]',
    'Withdrawal': '[Reversible]',
    'Transfer': '[Reversible]',
}

addition_code_CustInfoKind_1 = \
    u"""using G = CustInfoGroupKind;
using T = KindType;
/*enum RadixType {
    UserClass, Enum, Xml,
       Bool,    Int,    Char,    Num,    DateTime,    Str,    Bin,    Clob,    Blob,
    ArrBool, ArrInt, ArrChar, ArrNum, ArrDateTime, ArrStr, ArrBin, ArrClob, ArrBlob,
    ArrEnum
}*/
enum KindType {
    // Если к названиям данных элементов добавить Val, то получится название XML-узла с данными.
    Bin, Xml,
       Str,    Int,    Num,    Bool,    DateTime,
    ArrStr, ArrInt, ArrNum, ArrBool, ArrDateTime,
    //[Obsolete]
    //Statement,
    // XML-узлы с данными называются также, как эти элементы.
    InputFormat, PaymentTemplate, PaymentParams, NotifyContract, NotifyTypes, ReportPubs, UserAttrs,
}
/// <summary>
/// Атрибут, сопоставляющий элементам перечисления CustInfoKind тип данных, которые имеет
/// этот элемент.
/// </summary>
[AttributeUsage(AttributeTargets.Field)]  
sealed class KindTypeAttribute : Attribute {
    private readonly KindType type;
    /// <summary>
    /// Значение атрибута по умолчанию.
    /// </summary>
    public readonly object Default;
    public readonly CustInfoGroupKind? Group;
    public string NS;
    public KindTypeAttribute(KindType type) {
        this.type = type;
        this.Group= null;
    }
    public KindTypeAttribute(KindType type, CustInfoGroupKind group) {
        this.type = type;
        this.Group= group;
    }

    public KindType Kind { get {return type;} }
    public string DefStr { get {return (string)(Default ?? string.Empty);} }
    public int    DefInt { get {return (int)(Default ?? 0);} }
    public double DefNum { get {return (double)(Default ?? 0.0);} }
    public bool   DefBool{ get {return (bool)(Default ?? false);} }

    public string[] DefArrStr { get {return (string[])(Default ?? new string[0]);} }
    public int[]    DefArrInt { get {return (int[])(Default ?? new int[0]);} }
    public double[] DefArrNum { get {return (double[])(Default ?? new double[0]);} }
    public bool[]   DefArrBool{ get {return (bool[])(Default ?? new bool[0]);} }
}"""

addition_code_CustInfoKind_2 = \
    u"""/// <summary>
/// Содержит методы-расширения для различных перечислений.
/// </summary>
internal static partial class Extensions
{
    public static bool isArray(this KindType kind) {
        return kind >= KindType.ArrStr && kind <= KindType.ArrDateTime;
    }
    public static string xmlNodeName(this KindType kind) {
        if (kind <= KindType.ArrDateTime) {
            return kind.ToString() + "Val";
        }
        return kind.ToString();
    }
    public static bool canHaveEditor(this CustInfoKind kind) {
        string name = kind.ToString();
        foreach (KindTypeAttribute a in typeof(CustInfoKind).GetField(name).GetCustomAttributes(typeof(KindTypeAttribute), false)) {
            switch (a.Kind) {
                case KindType.Str:      return true;
                case KindType.Int:      return true;
                case KindType.Num: break;
                case KindType.Bool:     return true;
                case KindType.DateTime: break;
                case KindType.ArrStr:   return true;
                case KindType.ArrInt:   return true;
                case KindType.ArrNum: break;
                case KindType.ArrBool: break;
                case KindType.ArrDateTime: break;
                case KindType.InputFormat: break;
                case KindType.PaymentTemplate: break;
                case KindType.PaymentParams: break;
                case KindType.NotifyContract: break;
                case KindType.NotifyTypes: break;
                case KindType.ReportPubs: break;
                default: break;
            }
            break;
        }
        return false;
    }
    public static Type editorType(this KindType kind) {
        // EnumConfigProperty
        // EnumListConfigProperty
        // IndexedRuleSetConfigProperty
        // LongConfigProperty
        // NodeTreeConfigProperty
        // RuleSetConfigProperty
        // ScriptConfigProperty
        switch (kind) {
            case KindType.Str:      return typeof(StringConfigProperty);
            case KindType.Int:      return typeof(IntConfigProperty);
            case KindType.Num: break;
            case KindType.Bool:     return typeof(BoolConfigProperty);
            case KindType.DateTime: break;
            case KindType.ArrStr:   return typeof(StringListConfigProperty);
            case KindType.ArrInt:   return typeof(IntListConfigProperty);
            case KindType.ArrNum: break;
            case KindType.ArrBool: break;
            case KindType.ArrDateTime: break;
            case KindType.InputFormat: break;
            case KindType.PaymentTemplate: break;
            case KindType.PaymentParams: break;
            case KindType.NotifyContract: break;
            case KindType.NotifyTypes: break;
            case KindType.ReportPubs: break;
            default: break;
        }
        return null;
    }
    public static KindType kindType(this CustInfoKind kind) {
        return kind.meta<CustInfoKind,KindTypeAttribute>().Kind;
    }
}"""

addition_code_TranResult = \
    u"""using AS = TransactionHost.AuthorizationStatus;
/// <summary>
/// Атрибут для отображения кода результата транзакции TranzAxis в код результата транзакции K3A.
/// Не все коды допустимы в любых ситуациях. Всегда возможны только следующие коды K3A:
/// <list>
/// <li>HostTimeout</li>
/// <li>CommsError</li>
/// <li>Authorized</li>
/// <li>IncorrectPIN</li>
/// <li>InvalidAccount</li>
/// <li>Declined</li>
/// <li>HostInfoRequest</li>
/// <li>CardRestricted</li>
/// <li>CardExpired</li>
/// <li>CardInvalid</li>
/// </list>
/// Разъяснения Kalignite содержатся в TXSST-141.
/// </summary>
[AttributeUsage(AttributeTargets.Field)]
internal class ResultAttribute : Attribute {
        public readonly AS Status;
        public ResultAttribute(AS status) { Status = status;}
}
internal static partial class Extensions {
        public static AS translate(this TranResult result) {
                return result.meta<TranResult,ResultAttribute>().Status;
        }
        public static AS? translate(this TranResult? result) {
                if (result == null) return null;
                return result.Value.translate();
        }
}"""
##############################################################################################################################################

import os
import xml.dom.minidom as MD
import re
import sys

class TxEnumItem:
    u"""Класс, описывающий константу TX-перечисления"""

    def __init__(self):
        self.name = None
        self.deprecated = None
        self.value = None
        self.group = None
        self.type = None

    def getName(self):
        u"""Имя константы"""
        return self.name

    def isDeprecated(self):
        u"""Возврат 'true', если константа устарела, иначе 'false'"""
        return self.deprecated

    def getValue(self):
        u"""Значение константы"""
        return self.value

    def getGroup(self):
        u"""Группа, к которой относится константа перечисления. Используется только для перечисления CustInfoKind."""
        return self.group

    def getType(self):  # Ее тип
        u"""Тип константы перечисления. Используется только для перечисления CustInfoKind."""
        return self.type

    def fromXmlDomNode(self, nodeXml):
        u"""Инициализация через xml."""
        self.name = nodeXml.attributes['Name'].value
        self.deprecated = nodeXml.attributes['IsDeprecated'].value
        self.value = nodeXml.getElementsByTagName('Value')[0].firstChild.nodeValue

        domains = nodeXml.getElementsByTagName('Domain')
        if domains.length > 0:
            for domain in domains:
                domain_path = domain.attributes[
                    'Path'].value  # Значение домена. Представляет собой id, разделенные пробелом.
                domain_list = domain_path.split(' ')  # Список путей в домене
                domain_data = domain_list.pop()  # Последний id в пути -- является текущим для данной константы перечисления

                domain_type = domain_EnumType.get(domain_data)  # Тип константы перечисления
                domain_group = domain_Group.get(domain_data)  # Группа, к которой относится константа перечисления

                if domain_type != None:
                    self.type = domain_type

                if domain_group != None:
                    self.group = domain_group


class TxEnum:
    u"""Класс, описывающий TX-перечисление"""

    def __init__(self):
        self.id = None
        self.name = None
        self.valType = None
        self.items = None

    def getId(self):
        u"""Id перечисления"""
        return self.id

    def getName(self):
        u"""Имя перечисления"""
        return self.name

    def getValType(self):
        u"""Тип перечисления. Может быть: 21 (Str), 2 (Int) и 3 (Char)."""
        return self.valType

    def getStrValType(self):
        u"""Тип перечисления как строка."""
        if self.valType == "21":
            return "Str"
        elif self.valType == "2":
            return "Int"
        elif self.valType == "3":
            return "Char"

    def getDescriptionFromTx(self):
        u"""Описание перечисления взятого из TX."""
        return self.descriptionFromTx

    def getItems(self):
        u"""Список констант перечисления"""
        return self.items

    def fromXmlDom(self, path_xml):
        u"""Инициализация через xml."""
        root_xml = MD.parse(path_xml)  # Разбор xml
        ads_enum_definition = root_xml.getElementsByTagName('AdsEnumDefinition')
        self.id = ads_enum_definition[0].attributes['Id'].value
        self.name = ads_enum_definition[0].attributes['Name'].value
        self.valType = ads_enum_definition[0].attributes['ValType'].value
        self.items = []
        self.descriptionFromTx = ''

        # Попытаемся добраться до файла описания перечисления и из него получить русско-язычное описание
        # Составляем относительный путь к файлу локализации
        path_description_xml = os.path.dirname(path_xml)  # Папка, в которой файл перечисления хранится
        path_description_xml = os.path.dirname(path_description_xml)  # На 1 уровень выше
        path_description_xml = os.path.join(path_description_xml, 'locale', 'ru',
                                            'mlb%s.xml' % self.id)  # строим путь до файла локализации
        path_description_xml = os.path.normpath(path_description_xml)  # Приводим слеши к виду, принятому для текущей ОС

        # Файл локализации существует?
        if os.path.exists(path_description_xml):
            # В файле перечисления получаем id описания, которое находится в файле локализации
            description_id = ads_enum_definition[0].attributes.get('DescriptionId')

            if description_id != None:
                description_id = description_id.value  # значение id

                # Выполняем разбор файла локализации
                root_description_xml = MD.parse(path_description_xml)

                # Ищем элементы, хранящие переводы
                description_string = root_description_xml.getElementsByTagName('String')
                for description_string_item in description_string:
                    # Ищем "свой" id
                    if description_string_item.attributes['Id'].value == description_id:
                        # Вытаскиваем перевод
                        self.descriptionFromTx = description_string_item.getElementsByTagName('Value')[
                            0].firstChild.nodeValue
        else:
            print('Description file not exist: ' + path_description_xml)

        for node in root_xml.getElementsByTagName('Item'):
            enumItem = TxEnumItem()
            enumItem.fromXmlDomNode(node)
            self.items.append(enumItem)


def rowsToCSharpXmlComment(rows):
    u"""
    Приводит строки текста к виду c# документарованного комментария.
    """
    # @param rows list[unicode] Список строк текста, который нужно "обернуть" в документирущий комментарий C# <summary>
    # @return unicode Текст в комментарии <summary>, строки которого разделены '\n'

    return u'/// <summary> \n%s/// </summary>' % ''.join([u'/// {}\n'.format(row) + '' for row in rows])


def getSortedEnumItems(enum_items):
    u"""Сортировка констант перечислений по имени"""
    # @param enum_items list[TxEnumItem] Список констант перечисления.
    # @return list[TxEnumItem] Отсортированный по именам констант список.

    return sorted(enum_items, key=lambda x: x.getName())


def addIndentToTextBlock(text, indent=' ' * 4):
    u"""Добавление отступа к блоку текста"""
    # @param text str Текст, к которому будет добавлен отступ.
    # @param indent str Отступ в пробелах.
    # @return str Текст с отступами.

    return ''.join([indent + row + '\n' for row in text.split('\n') if row])


def addRegionBlock(text, name_region):
    u"""Добавление блока директивы region"""
    # @param text str Текст, который нужно поместить в директиву region.
    # @param name_region str Название региона.
    # @return str Текст внутри директивы c# region.

    return '#region %s\n%s#endregion' % (name_region, text)


def addCommentBlockAboutTxEnum(enum):
    u"""Генерация дополнительной информации об перечислении: id и тип"""
    # @param enum TxEnum Перечисление, по которому нужно сгенерировать дополнительную информацию.
    # @return str Текст с комментарием c#, содержащий информацию об перечислении TX.

    return f"/// <RadixEnum id='{enum.getId()}' type='{enum.getStrValType()}'></RadixEnum>\n"


def addStandartUsingDirective():
    u"""Генерация стандартных директив использования пространств имен"""
    # @return str Текст с стандартными директивами using.

    return \
        """using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;"""


def addObsoleteAtribute():
    u"""Генерация атрибута Obsolete"""
    # @return str Текст с атрибутом c# Obsolete.

    return u'[Obsolete("Устарело в оригинальном перечислении")]'


def addNamespaceTxEnum():
    u"""Генерация пространства имен перечислений TX"""
    # @return str Текст с директивой, подключающей пространство имен перечислений TX.

    return 'namespace TXSST.Enums.Tx'


def getFirstSubWord(text):
    u"""Функция вернет первое слово строки. Первый символ строки должен быть в верхнем регистре."""
    # @param text str Текст, в котором нужно найти  слово.
    # @return str Первое слово строки, если нашли, иначе весь текст, переданный функции.
    # TODO: доработать алгоритм поиска.

    m = re.search(r"[A-Z0-9][a-z0-9].+?[A-Z0-9]", text)
    sub_word = text
    if m is not None:
        sub_word = m.group(0)  # Первое слово строки.
        sub_word = sub_word[:-1]  # убираем последний символ -- при данной регулярке, будет захвачен лишний символ.

    return sub_word


def addCustInfoKindAttribute(item_enum):
    u"""Добавление атрибута перечисления CustInfoKind"""
    # @param item_enum TxEnumItem Константа перечисления.
    # @return str Текст с атрибутом c#, который содержит информацию об типе и группе элемента перечисления.

    item_group = item_enum.getGroup()  # Группа
    item_type = item_enum.getType()  # Тип

    attribute = ''
    if item_group != None and item_type != None:
        attribute += '[KindType(T.%s, G.%s)] ' % (item_type, item_group)

    elif item_type != None:
        attribute += '[KindType(T.%s)] ' % item_type

    elif item_group != None:
        attribute += '[KindType(G.%s)] ' % item_group

    return attribute


def get_max_length_name_items_enum(enum_items):
    u"""Возвращает максимальную длину имени константы."""
    # @param item_enums list[TxEnumItem] Список констант перечисления.
    # @return int Максимальная длина имени констант в списке.

    max_length = -1
    for item in enum_items:  # Переберем все элементы перечисления
        length = len(item.getName())  # Определим количество символов в имени константы
        # Определим максимальную длину
        if length > max_length:
            max_length = length

    return max_length


def addItemEnumFromType(item_enum, val_type, max_length_name_items=-1):
    u"""Генерация константы перечисления, в зависимости от ее типа"""
    # @param item_enum TxEnumItem Константа перечисления.
    # @param val_type str Тип перечисления.
    # @param max_length_name_items int Максимальная длина имени констант в списке.
    # @return str Текст с константой перечисления в c#.

    enum_text = ''
    value = item_enum.getValue()  # Значение
    total_name = value if val_type == "21" else item_enum.getName()  # Имя

    # Для типа str равный 21, имя константы перечисления берется из Value
    if val_type == "21":  # Если тип Str
        enum_text = total_name

    # Для типа int равный 2, константы перечисления имеют заданное значение, а имя берется из name
    elif val_type == "2":  # Если тип Int
        indent = ""  # Отступ в пробелах перед пробелом. Нужен для выравнивания знака '='
        if max_length_name_items != -1:  # Если значение максимальной длины имени перечисления указана
            # Найдем разницу между длинами констант текущего перечисления и константы, имеющей максимальную длину имени
            diff = max_length_name_items - len(total_name)
            if diff > 0:
                indent = diff * " "
        enum_text = total_name + indent + " = " + value

    return enum_text


def addItemEnum(item_enum, enum, additional_attribute='', max_length_name_items=-1):
    u"""Общая функция генерации элементов перечисления"""
    # @param item_enum TxEnumItem Константа перечисления.
    # @param additional_attribute str Строка с дополнительным атрибутом.
    # @param max_length_name_items int Максимальная длина имени констант в списке.
    # @return str Текст с константой перечисления в c#. К константе перечисления добавляются комментарии и атрибуты.

    text = ''
    value = item_enum.getValue()  # Значение

    enum_id = enum.getId()
    val_type = enum.getValType()  # Тип перечисления, бывает трех видов: 21 -- Str, 2 -- Int, 3 -- Char
    total_name = value if val_type == "21" else item_enum.getName()  # Имя        

    # Добавление комментариев к элементам перечисления
    enum_constants = dict_enum_constants_comments.get(enum_id)
    if enum_constants != None:  # Это перечисление есть в словаре
        constants_comment = enum_constants.get(total_name)
        if constants_comment != None:  # Эта константа перечисления есть в словаре
            rows = constants_comment.split('\n')
            text += rowsToCSharpXmlComment(rows) + '\n'

    # Если флаг стоит, добавляем атрибут Obsolete
    if item_enum.isDeprecated() == 'true':
        text += addObsoleteAtribute() + '\n'

    # Добавление дополнительных атрибутов
    if additional_attribute:
        text += additional_attribute

    text += addItemEnumFromType(item_enum, val_type, max_length_name_items) + ",\n"
    return text


def load_TranResult_Enum(enum, sort, namespace_indent, enum_indent, access):
    u"""Генерация кода для перечисления TranResult"""
    # @param enum TxEnum Перечисление.
    # @param sort bool True - если нужно упорядочить константы перечисления по имени.
    # @param namespace_indent str Отступ внутри пространства имен.
    # @param enum_indent str Отступ внутри перечисления.
    # @param access str Доступ к перечислению, может быть public, private или protected.
    # @return str Текст с перечислением в c#.

    enum_name = enum.getName()  # Имя перечисления
    enum_tx_description = enum.getDescriptionFromTx()  # Описание перечисления, взятое из TX

    ## Первая строка генерированного кода
    # Пространство имен по умолчанию
    text = ''
    text += addStandartUsingDirective() + '\n'
    text += 'using K3A.Hosts;\n'
    text += '\n'
    text += addNamespaceTxEnum() + '\n{\n';

    namespace_text = addition_code_TranResult + '\n \n'

    # Добавим комментарий к перечислению.
    if enum_tx_description != '':
        rows = enum_tx_description.split('\n')  # Каждую строку комментария на отдельную строку
        namespace_text += rowsToCSharpXmlComment(rows) + '\n'  # Добавление комментария

    namespace_text += addCommentBlockAboutTxEnum(enum)
    namespace_text += access + " enum " + enum_name + "\n{\n"

    enum_items_text = ''
    enum_items = getSortedEnumItems(enum.getItems()) if sort else enum.getItems()
    for item in enum_items:
        value = item.getValue()  # Значение

        # Для TranResult выполняется индивидуальная обработка.
        # В TX нет информации об атрибутах этого перечисления, но они нужны, потому придется вручную добавить.
        attribute = attribute_EnumItem_TranResult.get(value)
        attribute = ('[Result(AS.%s)]' % attribute + " ") if attribute != None else ''
        enum_items_text += addItemEnum(item, enum, attribute)

    namespace_text += addIndentToTextBlock(enum_items_text, enum_indent) + '}'
    text += addIndentToTextBlock(namespace_text, namespace_indent) + '}'
    return text


def load_CustInfoKind_Enum(enum, sort, namespace_indent, enum_indent, access):
    u"""Генерация кода для перечисления CustInfoKind"""
    # @param enum TxEnum Перечисление.
    # @param sort bool True - если нужно упорядочить константы перечисления по имени.
    # @param namespace_indent str Отступ внутри пространства имен.
    # @param enum_indent str Отступ внутри перечисления.
    # @param access str Доступ к перечислению, может быть public, private или protected.
    # @return str Текст с перечислением в c#.

    enum_name = enum.getName()  # Имя перечисления
    enum_tx_description = enum.getDescriptionFromTx()  # Описание перечисления, взятое из TX

    ## Первая строка генерированного кода
    # Пространство имен по умолчанию
    text = addStandartUsingDirective() + '\n'
    text += 'using K3A.Common;\n\n'
    text += addNamespaceTxEnum() + '\n{\n'

    namespace_text = addition_code_CustInfoKind_1 + '\n \n'  # Добавление дополнительного кода, связанного с перечислением CustInfoKind

    # Добавим комментарий к перечислению.
    if enum_tx_description != '':
        rows = enum_tx_description.split('\n')  # Каждую строку комментария на отдельную строку
        namespace_text += rowsToCSharpXmlComment(rows) + '\n'  # Добавление комментария

    namespace_text += addCommentBlockAboutTxEnum(enum)
    namespace_text += access + " enum " + enum_name + "\n{\n"

    enum_items_text = ''  # Весь блок текста внутри перечисления, будет добавлять в эту переменную
    enum_items = enum.getItems()  # Все элементы перечисления
    enum_items_with_obsolete = []  # Устаревшие элементы перечисления
    enum_items_without_obsolete = []  # Все элементы перечисления, кроме устаревших

    # TODO: доработать алгоритм получения списков устаревших элементов перечисления и всех остальных.
    for item in enum_items:
        if item.isDeprecated() == 'true':
            enum_items_with_obsolete.append(item)
        else:
            enum_items_without_obsolete.append(item)

    ## Сначала добавим устаревшие элементы перечисления
    # Если sort == True, тогда отсортируем список элементов перечислений
    enum_items = getSortedEnumItems(enum_items_with_obsolete) if sort else enum_items_with_obsolete
    for item in enum_items:
        attribute = addCustInfoKindAttribute(item)  # Получение уникального для CustInfoKind атрибута
        enum_items_text += addItemEnum(item, enum, attribute)

    # Поместим в директиву region
    enum_items_text = addRegionBlock(enum_items_text, u'Obsolete - Все устаревшие константы перечислений')
    ##

    ## Теперь добавим все оставшиеся элементы перечисления
    # Выполним группирование констант перечисления по первому слову в имени: ApplicationAttrs и ApplicationId -- Application,
    # BillAmt и BillCcy -- Bill, и т.д.

    enum_items_text += '\n \n'

    # Словарь, ключем которого будет первое слово констант перечисления, а значением список этих констант
    dict_group_enum_items = dict()

    enum_items = enum_items_without_obsolete  # Список элементов перечисления без устаревших элементов
    for item in enum_items:  # Переберем все элементы
        sub_word = getFirstSubWord(item.getName())  # Определим первое слово в имени константы
        if dict_group_enum_items.has_key(sub_word):  # Элемент с таким ключом существует
            items = dict_group_enum_items.get(sub_word)  # Получим список
            items.append(item)  # Добавим в список
        else:
            dict_group_enum_items[sub_word] = list()  # Создадим список, если его нет

    enum_groups = dict_group_enum_items.keys()  # Список имен групп, словаря

    # Возможно, группы нужно сгенерировать в отсортированном виде
    enum_groups = sorted(enum_groups) if sort else enum_groups
    for group_name in enum_groups:  # Переберем все группы
        # Получение списка констант перечисления, относящихся к данной группе
        groups = dict_group_enum_items.get(group_name)
        group_region_text = ''  # В данной переменной будет хранится блок констант перечислений
        for item in groups:  # Перебор элементов группы
            attribute = addCustInfoKindAttribute(item)  # Получение уникального для CustInfoKind атрибута
            group_region_text += addItemEnum(item, enum, attribute)

        # Поместим в директиву region
        enum_items_text += addRegionBlock(group_region_text, group_name) + '\n \n'
    ##

    namespace_text += addIndentToTextBlock(enum_items_text, enum_indent) + '}' + '\n \n'
    namespace_text += addition_code_CustInfoKind_2  # Добавление дополнительного кода, связанного с перечислением CustInfoKind
    text += addIndentToTextBlock(namespace_text, namespace_indent) + '}'
    return text


def load_Operation_Enum(enum, sort, namespace_indent, enum_indent, access):
    u"""Генерация кода для перечисления Operation"""
    # @param enum TxEnum Перечисление.
    # @param sort bool True - если нужно упорядочить константы перечисления по имени.
    # @param namespace_indent str Отступ внутри пространства имен.
    # @param enum_indent str Отступ внутри перечисления.
    # @param access str Доступ к перечислению, может быть public, private или protected.
    # @return str Текст с перечислением в c#.

    enum_name = enum.getName()  # Имя перечисления
    enum_tx_description = enum.getDescriptionFromTx()  # Описание перечисления, взятое из TX

    ## Первая строка генерированного кода
    # Пространство имен по умолчанию
    text = ""
    text += addStandartUsingDirective() + '\n'
    text += 'using K3A.Common;\n'
    text += '\n'
    text += addNamespaceTxEnum() + '\n{\n'

    namespace_text = ''
    addition_code = u'[AttributeUsage(AttributeTargets.Field)]\n'
    addition_code += u'sealed class ReversibleAttribute : Attribute {}\n \n'
    namespace_text += addition_code

    # Добавим комментарий к перечислению.
    if enum_tx_description != '':
        rows = enum_tx_description.split('\n')  # Каждую строку комментария на отдельную строку
        namespace_text += rowsToCSharpXmlComment(rows) + '\n'  # Добавление комментария

    namespace_text += addCommentBlockAboutTxEnum(enum)
    namespace_text += access + " enum " + enum_name + "\n{\n"

    enum_items_text = ''
    enum_items = getSortedEnumItems(enum.getItems()) if sort else enum.getItems()
    for item in enum_items:
        value = item.getValue()  # Значение

        # Для Operation выполняется индивидуальная обработка.
        # В TX нет информации об атрибутах этого перечисления, но они нужны, потому придется вручную добавить.
        attribute = attribute_EnumItem_Operation.get(value)
        attribute = (attribute + " ") if attribute != None else ''
        enum_items_text += addItemEnum(item, enum, attribute)

    namespace_text += addIndentToTextBlock(enum_items_text, enum_indent) + '\n}'
    text += addIndentToTextBlock(namespace_text, namespace_indent) + '}'
    return text


def loadCommonEnum(enum, sort, namespace_indent, enum_indent, access):
    u"""Генерация кода перечислений."""
    # @param enum TxEnum Перечисление.
    # @param sort bool True - если нужно упорядочить константы перечисления по имени.
    # @param namespace_indent str Отступ внутри пространства имен.
    # @param enum_indent str Отступ внутри перечисления.
    # @param access str Доступ к перечислению, может быть public, private или protected.
    # @return str Текст с перечислением в c#.

    enum_name = enum.getName()  # Имя перечисления
    enum_tx_description = enum.getDescriptionFromTx()  # Описание перечисления, взятое из TX

    ## Первая строка генерированного кода
    # Пространство имен по умолчанию
    text = ""
    text += addStandartUsingDirective() + '\n'
    text += '\n'
    text += addNamespaceTxEnum() + '\n{\n'

    namespace_text = ''

    # Добавим комментарий к перечислению.
    if enum_tx_description != '':
        rows = enum_tx_description.split('\n')  # Каждую строку комментария на отдельную строку
        namespace_text += rowsToCSharpXmlComment(rows) + '\n'  # Добавление комментария

    namespace_text += addCommentBlockAboutTxEnum(enum)
    namespace_text += access + " enum " + enum_name + "\n{\n"

    enum_items_text = ''
    enum_items = getSortedEnumItems(enum.getItems()) if sort else enum.getItems()

    # Максимальная длина имени константы. Нужно для выравнивания значений константы при типе Int.
    max_length = get_max_length_name_items_enum(enum_items)

    for item in enum_items:  # Перебираем все элементы перечисления
        enum_items_text += addItemEnum(item, enum,
                                       max_length_name_items=max_length)  # Генерация и добавление элементов перечисления

    namespace_text += addIndentToTextBlock(enum_items_text, enum_indent) + '}'
    text += addIndentToTextBlock(namespace_text, namespace_indent) + '}'
    return text


def loadEnumFromXml(path, save_dir, log, save, sort, access, indent_namespace, indent_enum):
    u"""Загрузка, генерация и сохранения перечисления от xml-файла конфигурации TX."""
    # @param path str Путь к TX перечислению
    # @param save_dir str Путь к папке, в которую будут сохранены перечисления
    # @param log  bool Вывод в консоль процесс выполнения скрипта
    # @param save bool Выполнять сохранение сгенерированных файлов
    # @param sort bool True - если нужно упорядочить константы перечисления по имени.
    # @param access str Модификатор доступа.
    # @param indent_namespace int Количество пробелов в отступе пространства имен.
    # @param indent_enum int Количество пробелов в отступе перечисления.

    path = os.path.normpath(path)  # Меняем слеши на слеши в стиле текущей ОС
    text = ""

    if os.path.exists(path):  # Проверка существования файла
        if log:
            print("\n" + path)

        enum = TxEnum()  # Создаем объект перечисления
        enum.fromXmlDom(path)  # Заполнение объекта из xml-файла
        enum_id = enum.getId()  # Id перечисления
        enum_name = enum.getName()  # Имя перечисления

        indent_namespace_str = " " * indent_namespace  # Отступ внутри пространства имен перечислений (TXSST.Enums.Tx)
        indent_enum_str = " " * indent_enum  # Отступ внутри блока enum

        if enum_id == 'acsU47BUCPQWTNRDISQABIFNQAABA':  # Индивидуально для TranResult
            text = load_TranResult_Enum(enum, sort, indent_namespace_str, indent_enum_str, access)

        elif enum_id == 'acs5B443MRWQ3ORDC7EABIFNQAABA':  # Индивидуально для Operation
            text = load_Operation_Enum(enum, sort, indent_namespace_str, indent_enum_str, access)

        elif enum_id == 'acsUOT6QZNAXLNRDISQAAAAAAAAAA':  # Индивидуально для CustInfoKind
            text = load_CustInfoKind_Enum(enum, sort, indent_namespace_str, indent_enum_str, access)

        else:  # Все остальные перечисления
            text = loadCommonEnum(enum, sort, indent_namespace_str, indent_enum_str, access)

        if log is True:
            print(text)

        if save is True:  # Сохраняем в файл
            fileName = os.path.normpath(save_dir + "/" + enum_name + ".cs")  # создаем путь к файлу перечисления
            f = open(fileName, 'w')
            f.write(text.encode('utf-8'))  # Сохраняем в utf-8
            f.close()

    else:
        print('ERROR!!! FILE NOT EXIST!!! file = "' + path + '"')

    return text


import time
import argparse

# TODO: Словарь с комментариями к константам перечислений вытащить в отдельный файл
# TODO: Конфигурация генератора:
#           * Детальная настройка добавления комментариев к перечислениям:
#               * Комментарий к перечислению
#               * Дополнительная информация о перечислении: /// <RadixEnum ...
#               * Комментарий к элементу перечисления (если есть комментарий)
#           * Показывать расширенный результат: сколько всего файлов было распарсено, сколько неудачно (с выводом пути неудачных файлов)
#           * После прикрепления комментариев к перечислению и константам перечисления показывать какие перечисления и
#             константы перечисления остались (т.е. при парсинге их не нашлось в перечислении TX)
#           * Стили кода:
#               * Перенос фигурных скобок


def main(namespace):
    # @param namespace argparse.Namespace Содержит переданные в аргументах объекты.

    path_tx_dir = namespace.tx_dir  # Путь к директории с TX
    path_save_dir = os.path.normpath(namespace.save_dir)  # Путь к директории сохранения
    log = namespace.log
    save = namespace.save
    sort = namespace.sort
    access = namespace.access
    indent_namespace = namespace.indent_namespace
    indent_enum = namespace.indent_enum

    t = time.time()

    print(u'Папка TX: %s' % path_tx_dir)
    print(u'Папка сохранения: %s' % path_save_dir)

    # Если папка сохранения не существует и мы намерены сохранять сгенерированные файлы, создаем ее
    if save:
        os.makedirs(path_save_dir, exist_ok=True)

    # Перебираем пути к файлам перечисления
    for enum in enums_param:
        abs_path = os.path.join(path_tx_dir, enum)  # Склеиваем путь к перечислению
        loadEnumFromXml(abs_path, path_save_dir, log, save, sort, access, indent_namespace, indent_enum)  # Обрабатываем

    print(u"\nВремя выполнения: %.3f секунд." % (time.time() - t))

def create_parser():
    parser = argparse.ArgumentParser(prog="UpdateTxEnums",
                                     description=u"Cкрипт генерирует классы перечислений на C# в соответствии с этими перечислениями в транзаксисе.",
                                     epilog=u"(с) Compass-Plus 2014. Автор: Илья Петраш. Автор не несет ответственности за работу скрипта.")
    parser.add_argument('-tx_dir',
                        help=u'Путь к директории с TX.',
                        type=str)
    parser.add_argument('-save_dir',
                        help=u'Путь к директории, в которую будут сохранены сгенерированные классы перечислений.\n',
                        type=str)
    parser.add_argument('-log',
                        help=u'Вывод процесса выполнения скрипта в консоль.',
                        action='store_true',
                        default=False)
    parser.add_argument('-save',
                        help=u'Сохранение сгенерированных перечислений в папку -save_dir.',
                        action='store_true',
                        default=False)
    parser.add_argument('-sort',
                        help=u'Упорядочение констант перечисления по имени.',
                        action='store_true',
                        default=False)
    parser.add_argument('-access', help=u'Модификатор доступа перечислений. По умолчанию: public.',
                        type=str,
                        choices=['public', 'private', 'protected', 'internal', 'protected internal'],
                        default='public')
    parser.add_argument('-indent_namespace', help=u'Отступ в пробелах в пространстве имен. По умолчанию: 4.',
                        type=int,
                        default=4)
    parser.add_argument('-indent_enum', help=u'Отступ в пробелах в перечислениях. По умолчанию: 4.',
                        type=int,
                        default=4)
    return parser


if __name__ == '__main__':
    parser = create_parser()

    # sys.argv = [sys.argv[0]
    #     , '-tx_dir=D:\Tx\dev'
    #     # , '-save_dir=D:\TX_ENUMS'
    #     , '-log'
    #     # , '-save'
    #     , '-sort'
    #     # , '-indent_namespace=2'
    #     # , '-indent_enum=2'
    #     # , '-access=private'
    # ]

    if len(sys.argv) == 1:
        parser.print_help()
    else:
        namespace = parser.parse_args()
        main(namespace)