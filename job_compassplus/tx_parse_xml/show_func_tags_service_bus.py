#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from collections import defaultdict
from bs4 import BeautifulSoup, Tag


file_name = r'C:\DEV__TX\trunk_tx\com.tranzaxis\uds\Interfacing.Examples\etc\DinersClub\DinersClub.xml'


root = BeautifulSoup(open(file_name), 'xml')


def get_func_title(func_el: Tag) -> str:
    description = func_el.Description.text if func_el.Description else ''
    attrs_title = ", ".join(f"{k}={v}" for k, v in func_el.attrs.items())
    return f'{attrs_title}. Description: {description}'


def get_funcs_from_user_funcs(node_el: Tag) -> list[Tag]:
    try:
        return [func_el for func_el in node_el.find('UserFuncs', recursive=False).find_all('Func', recursive=False)]
    except:
        return []


def get_funcs_from_user_props(node_el: Tag) -> list[Tag]:
    try:
        return [func_el for func_el in node_el.find('UserProps', recursive=False).find_all('Func')]
    except:
        return []


node_by_funcs = defaultdict(list)

nodes = []
if pipeline_nodes := root.find('PipelineNodes'):
    nodes += pipeline_nodes.find_all('Node')
if other_nodes := root.find('OtherNodes'):
    nodes += other_nodes.find_all('Node')

for node_el in nodes:
    node_title = node_el.Title.text if node_el.Title else ''
    node_class_id = node_el['ClassId']

    parent_title = f"{node_el.name} (Title: {node_title}. ClassId: {node_el['ClassId']}, EntityPid: {node_el['EntityPid']})"

    # Старый стиль хранения в UserFuncs/Func
    for func_el in get_funcs_from_user_funcs(node_el):
        func_title = get_func_title(func_el)
        node_by_funcs[parent_title].append(func_title)

    # Новый стиль хранения в UserProps/Props/Func
    for func_el in get_funcs_from_user_props(node_el):
        func_title = get_func_title(func_el)
        node_by_funcs[parent_title].append(func_title)

    try:
        for stage_el in node_el.TransformStages.find_all('TransformStage', recursive=False):
            parent_title = f"{node_el.name}/Stage#{stage_el.Seq.text} (ClassId: {stage_el['ClassId']}, NodeTitle: {node_title}, NodeClassId: {node_el['ClassId']}, NodeEntityPid: {node_el['EntityPid']})"

            for func_el in get_funcs_from_user_funcs(stage_el):
                func_title = get_func_title(func_el)
                node_by_funcs[parent_title].append(func_title)

            for func_el in get_funcs_from_user_props(stage_el):
                func_title = get_func_title(func_el)
                node_by_funcs[parent_title].append(func_title)

    except:
        pass

i = 1
for node_title, funcs in node_by_funcs.items():
    print(f'{node_title} ({len(funcs)}):')
    for func_title in funcs:
        print(f'    {i}. {func_title}')
        i += 1

    print()

"""
Node/Stage#1 (ClassId: aclFZFQDAPB2BDMBBDUE44VOUW66Q, NodeTitle: Stop List Request, NodeClassId: aclZUJW4J4EZ5GUBEPQEX7NUXKZSA, NodeEntityPid: 319) (2):
    1. ClassGUID=aclDNZFNZC3RBCBFLFRTXPHWDYLFU, ProfileVersion=1, OwnerPid=110, OwnerEntityId=tblTDP5BP5ZXBEOTJX74NH43PEPJA, OwnerClassId=aclFZFQDAPB2BDMBBDUE44VOUW66Q, OwnerPropId=pru5S5NKVTPLVCR5EC23E46WNXNP4, Profile=Tran::TranXsd:Request transform(Transformer.Base transformer, Radix::ServiceBus::SbXsd:PipelineMessageRq rq, Xml xmlRq) throws PipelineException. Description: Request
    2. ClassGUID=aclULCQ4C47UVHSVKA7JO7V3O6VBU, ProfileVersion=0, OwnerPid=110, OwnerEntityId=tblTDP5BP5ZXBEOTJX74NH43PEPJA, OwnerClassId=aclFZFQDAPB2BDMBBDUE44VOUW66Q, OwnerPropId=pruXTAMEVDGJZBOHPLCWVX3MHDG4E, Profile=Xml transform(Radix::ServiceBus.Nodes::Transformer transformer, Radix::ServiceBus::SbXsd:PipelineMessageRs rs, Tran::TranXsd:Response tranRs, Xml inXmlRq, Tran::TranXsd:Request outTranRq) throws PipelineException. Description: Response

Node (Title: IsStopList. ClassId: aclP3F7MNUSNVHJRAMR2454ZA4GCQ, EntityPid: 318) (1):
    3. ClassGUID=aclYRODMAM7AZB55JOWOVGSJ2TL4I, ProfileVersion=0, OwnerPid=318, OwnerEntityId=tblPNJV5QTXIBGJPBHK64RO3LH73A, OwnerClassId=aclP3F7MNUSNVHJRAMR2454ZA4GCQ, OwnerPropId=pru5WVR5OZMIRC4VC6QHUQZ66EBWM, Profile=boolean check(Radix::ServiceBus.Nodes::Router.Jml router, Radix::ServiceBus::SbXsd:PipelineMessageRq rq, Tran::TranXsd:Request tranRq) throws PipelineException. Description: Is stop list request

Node/Stage#1 (ClassId: acl2QQ7GRLAFNE73NPWZJ4I4CLSMU, NodeTitle: System Event, NodeClassId: acl4TJBHQN7PJBZFLBHDI3WHSWDSY, NodeEntityPid: 329) (2):
    4. ClassGUID=acl2G2QDD5EXRBCROWISX5QR5CUCA, ProfileVersion=0, OwnerPid=113, OwnerEntityId=tblTDP5BP5ZXBEOTJX74NH43PEPJA, OwnerClassId=acl2QQ7GRLAFNE73NPWZJ4I4CLSMU, OwnerPropId=pruPSTIRHU6HRH2TJTGTE6XD6NZTI, Profile=Xml transform(Transformer transformer, ServiceBus::SbXsd:PipelineMessageRq rq, Xml inRq) throws PipelineException. Description: Request
    5. ClassGUID=aclIB36HWWSIZFGHBNZC4SXAYP2J4, ProfileVersion=0, OwnerPid=113, OwnerEntityId=tblTDP5BP5ZXBEOTJX74NH43PEPJA, OwnerClassId=acl2QQ7GRLAFNE73NPWZJ4I4CLSMU, OwnerPropId=pruVGX63H52ZRFMNAAH5JHB6U5LGM, Profile=Xml transform(Transformer transformer, ServiceBus::SbXsd:PipelineMessageRs rs, Xml inRs, Xml inRq, Xml outRq) throws PipelineException. Description: Response

Node (Title: IsEcho. ClassId: aclXL4IP5OEDFAXRMDKNVVVBOXHWU, EntityPid: 331) (1):
    6. ClassGUID=aclTQ77FRM62VEKFP3EI3JEFTG2RY, ProfileVersion=0, OwnerPid=331, OwnerEntityId=tblPNJV5QTXIBGJPBHK64RO3LH73A, OwnerClassId=aclXL4IP5OEDFAXRMDKNVVVBOXHWU, OwnerPropId=pruGU2USFURD5ATXP63WVDT5SISS4, Profile=boolean check(Router.Jml router, ServiceBus::SbXsd:PipelineMessageRq rq) throws PipelineException. Description: Is echo request

Node/Stage#1 (ClassId: aclFZFQDAPB2BDMBBDUE44VOUW66Q, NodeTitle: Reverse Request, NodeClassId: aclZUJW4J4EZ5GUBEPQEX7NUXKZSA, NodeEntityPid: 330) (2):
    7. ClassGUID=aclDNZFNZC3RBCBFLFRTXPHWDYLFU, ProfileVersion=1, OwnerPid=114, OwnerEntityId=tblTDP5BP5ZXBEOTJX74NH43PEPJA, OwnerClassId=aclFZFQDAPB2BDMBBDUE44VOUW66Q, OwnerPropId=pru5S5NKVTPLVCR5EC23E46WNXNP4, Profile=Tran::TranXsd:Request transform(Transformer.Base transformer, Radix::ServiceBus::SbXsd:PipelineMessageRq rq, Xml xmlRq) throws PipelineException. Description: Request
    8. ClassGUID=aclULCQ4C47UVHSVKA7JO7V3O6VBU, ProfileVersion=0, OwnerPid=114, OwnerEntityId=tblTDP5BP5ZXBEOTJX74NH43PEPJA, OwnerClassId=aclFZFQDAPB2BDMBBDUE44VOUW66Q, OwnerPropId=pruXTAMEVDGJZBOHPLCWVX3MHDG4E, Profile=Xml transform(Radix::ServiceBus.Nodes::Transformer transformer, Radix::ServiceBus::SbXsd:PipelineMessageRs rs, Tran::TranXsd:Response tranRs, Xml inXmlRq, Tran::TranXsd:Request outTranRq) throws PipelineException. Description: Response

Node (Title: IsInvalid. ClassId: aclXL4IP5OEDFAXRMDKNVVVBOXHWU, EntityPid: 324) (1):
    9. ClassGUID=aclTQ77FRM62VEKFP3EI3JEFTG2RY, ProfileVersion=0, OwnerPid=324, OwnerEntityId=tblPNJV5QTXIBGJPBHK64RO3LH73A, OwnerClassId=aclXL4IP5OEDFAXRMDKNVVVBOXHWU, OwnerPropId=pruGU2USFURD5ATXP63WVDT5SISS4, Profile=boolean check(Router.Jml router, ServiceBus::SbXsd:PipelineMessageRq rq) throws PipelineException. Description: Is invalid request

Node/Stage#1 (ClassId: aclDOHZLYSOGNBYFINCWBZ55XXKZE, NodeTitle: Auth-Rev Request, NodeClassId: acl3ZJO3VQ23JFWXNIZOFG36TF7BI, NodeEntityPid: 322) (2):
    10. ClassGUID=aclOFZ6CPB4Z5GKTHWQOSEILOHLPI, ProfileVersion=1, OwnerPid=111, OwnerEntityId=tblTDP5BP5ZXBEOTJX74NH43PEPJA, OwnerClassId=aclDOHZLYSOGNBYFINCWBZ55XXKZE, OwnerPropId=pru2ZBAAHQB5VE3NMNQNLDKE4L2LI, Profile=Tran::TranXsd:Response transform(Transformer.Base transformer, Radix::ServiceBus::SbXsd:PipelineMessageRs rs, Xml xmlRs, Tran::TranXsd:Request inTranRq, Xml outXmlRq) throws PipelineException. Description: Response
    11. ClassGUID=aclTA2OUEEOOBAVFF36IOH5FQIXYM, ProfileVersion=1, OwnerPid=111, OwnerEntityId=tblTDP5BP5ZXBEOTJX74NH43PEPJA, OwnerClassId=aclDOHZLYSOGNBYFINCWBZ55XXKZE, OwnerPropId=pruA3BKZH2TBVGPXJ6BFCY377Y3XE, Profile=Xml transform(Transformer.Base transformer, Radix::ServiceBus::SbXsd:PipelineMessageRq rq, Tran::TranXsd:Request tranRq) throws PipelineException. Description: Request

Node/Stage#1 (ClassId: aclFZFQDAPB2BDMBBDUE44VOUW66Q, NodeTitle: Auth Request, NodeClassId: aclZUJW4J4EZ5GUBEPQEX7NUXKZSA, NodeEntityPid: 333) (2):
    12. ClassGUID=aclDNZFNZC3RBCBFLFRTXPHWDYLFU, ProfileVersion=1, OwnerPid=116, OwnerEntityId=tblTDP5BP5ZXBEOTJX74NH43PEPJA, OwnerClassId=aclFZFQDAPB2BDMBBDUE44VOUW66Q, OwnerPropId=pru5S5NKVTPLVCR5EC23E46WNXNP4, Profile=Tran::TranXsd:Request transform(Transformer.Base transformer, Radix::ServiceBus::SbXsd:PipelineMessageRq rq, Xml xmlRq) throws PipelineException. Description: Request
    13. ClassGUID=aclULCQ4C47UVHSVKA7JO7V3O6VBU, ProfileVersion=0, OwnerPid=116, OwnerEntityId=tblTDP5BP5ZXBEOTJX74NH43PEPJA, OwnerClassId=aclFZFQDAPB2BDMBBDUE44VOUW66Q, OwnerPropId=pruXTAMEVDGJZBOHPLCWVX3MHDG4E, Profile=Xml transform(Radix::ServiceBus.Nodes::Transformer transformer, Radix::ServiceBus::SbXsd:PipelineMessageRs rs, Tran::TranXsd:Response tranRs, Xml inXmlRq, Tran::TranXsd:Request outTranRq) throws PipelineException. Description: Response

Node (Title: Echo Request. ClassId: aclXM5EJPEZFFBGBGEXO4W3T7ZJFM, EntityPid: 321) (1):
    14. ClassGUID=aclSQEW5FAQJ5EBFPU57S47V5XJYU, ProfileVersion=0, OwnerPid=321, OwnerEntityId=tblPNJV5QTXIBGJPBHK64RO3LH73A, OwnerClassId=aclXM5EJPEZFFBGBGEXO4W3T7ZJFM, OwnerPropId=pruTDGMAUN2LNECHHZUYWBLOQ5EFM, Profile=ServiceBus::SbXsd:PipelineMessageRs process(Processor.Jml processor, ServiceBus::SbXsd:PipelineMessageRq rq) throws PipelineException. Description: Echo request

Node/Stage#1 (ClassId: aclDOHZLYSOGNBYFINCWBZ55XXKZE, NodeTitle: Admin Request, NodeClassId: acl3ZJO3VQ23JFWXNIZOFG36TF7BI, NodeEntityPid: 332) (2):
    15. ClassGUID=aclOFZ6CPB4Z5GKTHWQOSEILOHLPI, ProfileVersion=1, OwnerPid=115, OwnerEntityId=tblTDP5BP5ZXBEOTJX74NH43PEPJA, OwnerClassId=aclDOHZLYSOGNBYFINCWBZ55XXKZE, OwnerPropId=pru2ZBAAHQB5VE3NMNQNLDKE4L2LI, Profile=Tran::TranXsd:Response transform(Transformer.Base transformer, Radix::ServiceBus::SbXsd:PipelineMessageRs rs, Xml xmlRs, Tran::TranXsd:Request inTranRq, Xml outXmlRq) throws PipelineException. Description: Response
    16. ClassGUID=aclTA2OUEEOOBAVFF36IOH5FQIXYM, ProfileVersion=1, OwnerPid=115, OwnerEntityId=tblTDP5BP5ZXBEOTJX74NH43PEPJA, OwnerClassId=aclDOHZLYSOGNBYFINCWBZ55XXKZE, OwnerPropId=pruA3BKZH2TBVGPXJ6BFCY377Y3XE, Profile=Xml transform(Transformer.Base transformer, Radix::ServiceBus::SbXsd:PipelineMessageRq rq, Tran::TranXsd:Request tranRq) throws PipelineException. Description: Request

Node (Title: isSystem. ClassId: aclXL4IP5OEDFAXRMDKNVVVBOXHWU, EntityPid: 317) (1):
    17. ClassGUID=aclTQ77FRM62VEKFP3EI3JEFTG2RY, ProfileVersion=0, OwnerPid=317, OwnerEntityId=tblPNJV5QTXIBGJPBHK64RO3LH73A, OwnerClassId=aclXL4IP5OEDFAXRMDKNVVVBOXHWU, OwnerPropId=pruGU2USFURD5ATXP63WVDT5SISS4, Profile=boolean check(Router.Jml router, ServiceBus::SbXsd:PipelineMessageRq rq) throws PipelineException. Description: Is system request

Node (Title: TryCatch. ClassId: aclXM5EJPEZFFBGBGEXO4W3T7ZJFM, EntityPid: 328) (1):
    18. ClassGUID=aclSQEW5FAQJ5EBFPU57S47V5XJYU, ProfileVersion=0, OwnerPid=328, OwnerEntityId=tblPNJV5QTXIBGJPBHK64RO3LH73A, OwnerClassId=aclXM5EJPEZFFBGBGEXO4W3T7ZJFM, OwnerPropId=pruTDGMAUN2LNECHHZUYWBLOQ5EFM, Profile=ServiceBus::SbXsd:PipelineMessageRs process(Processor.Jml processor, ServiceBus::SbXsd:PipelineMessageRq rq) throws PipelineException. Description: Catch exception

Node/Stage#1 (ClassId: aclDOHZLYSOGNBYFINCWBZ55XXKZE, NodeTitle: Stop List Request, NodeClassId: acl3ZJO3VQ23JFWXNIZOFG36TF7BI, NodeEntityPid: 316) (2):
    19. ClassGUID=aclOFZ6CPB4Z5GKTHWQOSEILOHLPI, ProfileVersion=1, OwnerPid=109, OwnerEntityId=tblTDP5BP5ZXBEOTJX74NH43PEPJA, OwnerClassId=aclDOHZLYSOGNBYFINCWBZ55XXKZE, OwnerPropId=pru2ZBAAHQB5VE3NMNQNLDKE4L2LI, Profile=Tran::TranXsd:Response transform(Transformer.Base transformer, Radix::ServiceBus::SbXsd:PipelineMessageRs rs, Xml xmlRs, Tran::TranXsd:Request inTranRq, Xml outXmlRq) throws PipelineException. Description: Response
    20. ClassGUID=aclTA2OUEEOOBAVFF36IOH5FQIXYM, ProfileVersion=1, OwnerPid=109, OwnerEntityId=tblTDP5BP5ZXBEOTJX74NH43PEPJA, OwnerClassId=aclDOHZLYSOGNBYFINCWBZ55XXKZE, OwnerPropId=pruA3BKZH2TBVGPXJ6BFCY377Y3XE, Profile=Xml transform(Transformer.Base transformer, Radix::ServiceBus::SbXsd:PipelineMessageRq rq, Tran::TranXsd:Request tranRq) throws PipelineException. Description: Request

Node (Title: Invalid Request. ClassId: aclXM5EJPEZFFBGBGEXO4W3T7ZJFM, EntityPid: 315) (1):
    21. ClassGUID=aclSQEW5FAQJ5EBFPU57S47V5XJYU, ProfileVersion=0, OwnerPid=315, OwnerEntityId=tblPNJV5QTXIBGJPBHK64RO3LH73A, OwnerClassId=aclXM5EJPEZFFBGBGEXO4W3T7ZJFM, OwnerPropId=pruTDGMAUN2LNECHHZUYWBLOQ5EFM, Profile=ServiceBus::SbXsd:PipelineMessageRs process(Processor.Jml processor, ServiceBus::SbXsd:PipelineMessageRq rq) throws PipelineException. Description: Invalid request

Node (Title: IsAdmin. ClassId: aclP3F7MNUSNVHJRAMR2454ZA4GCQ, EntityPid: 326) (1):
    22. ClassGUID=aclYRODMAM7AZB55JOWOVGSJ2TL4I, ProfileVersion=0, OwnerPid=326, OwnerEntityId=tblPNJV5QTXIBGJPBHK64RO3LH73A, OwnerClassId=aclP3F7MNUSNVHJRAMR2454ZA4GCQ, OwnerPropId=pru5WVR5OZMIRC4VC6QHUQZ66EBWM, Profile=boolean check(Radix::ServiceBus.Nodes::Router.Jml router, Radix::ServiceBus::SbXsd:PipelineMessageRq rq, Tran::TranXsd:Request tranRq) throws PipelineException. Description: Is admin request

Node/Stage#1 (ClassId: aclFZFQDAPB2BDMBBDUE44VOUW66Q, NodeTitle: Admin Request, NodeClassId: aclZUJW4J4EZ5GUBEPQEX7NUXKZSA, NodeEntityPid: 325) (2):
    23. ClassGUID=aclDNZFNZC3RBCBFLFRTXPHWDYLFU, ProfileVersion=1, OwnerPid=112, OwnerEntityId=tblTDP5BP5ZXBEOTJX74NH43PEPJA, OwnerClassId=aclFZFQDAPB2BDMBBDUE44VOUW66Q, OwnerPropId=pru5S5NKVTPLVCR5EC23E46WNXNP4, Profile=Tran::TranXsd:Request transform(Transformer.Base transformer, Radix::ServiceBus::SbXsd:PipelineMessageRq rq, Xml xmlRq) throws PipelineException. Description: Request
    24. ClassGUID=aclULCQ4C47UVHSVKA7JO7V3O6VBU, ProfileVersion=0, OwnerPid=112, OwnerEntityId=tblTDP5BP5ZXBEOTJX74NH43PEPJA, OwnerClassId=aclFZFQDAPB2BDMBBDUE44VOUW66Q, OwnerPropId=pruXTAMEVDGJZBOHPLCWVX3MHDG4E, Profile=Xml transform(Radix::ServiceBus.Nodes::Transformer transformer, Radix::ServiceBus::SbXsd:PipelineMessageRs rs, Tran::TranXsd:Response tranRs, Xml inXmlRq, Tran::TranXsd:Request outTranRq) throws PipelineException. Description: Response

Node (Title: Endpoint.NetHub. ClassId: aclQCQNNJMW4FCNZCRN2D5GNWKOKA, EntityPid: 6341) (5):
    25. ClassGUID=aclDUAVIDYVPZD4ZDUJBHXWJV7VTE, ProfileVersion=0, OwnerPid=6341, OwnerEntityId=tbl5HP4XTP3EGWDBRCRAAIT4AGD7E, OwnerClassId=aclQCQNNJMW4FCNZCRN2D5GNWKOKA, OwnerPropId=pru6HZ4WT3ULJBYTCTHWO5NFYXI5U, Profile=Str extractUniqueKey(byte[] data) throws PipelineException. Description: 
    26. ClassGUID=aclQPC7P4UWZ5BQ5OIJAMWF3SY5X4, ProfileVersion=0, OwnerPid=6341, OwnerEntityId=tbl5HP4XTP3EGWDBRCRAAIT4AGD7E, OwnerClassId=aclQCQNNJMW4FCNZCRN2D5GNWKOKA, OwnerPropId=pruK7UNBG2GCZDFVAEGA3NFR2U72Q, Profile=int insertStan(byte[] data, int prevStan) throws PipelineException. Description: 
    27. ClassGUID=aclKZFUEXWYNJCFPPKI6T2B5ERAZU, ProfileVersion=0, OwnerPid=6341, OwnerEntityId=tbl5HP4XTP3EGWDBRCRAAIT4AGD7E, OwnerClassId=aclQCQNNJMW4FCNZCRN2D5GNWKOKA, OwnerPropId=pruLXJ7LZAFXRD5ZDHXXBU24324SE, Profile=byte[] prepareEchoTestRq() throws PipelineException. Description: 
    28. ClassGUID=aclBKU3COGRUVGLZABNOJSKU5PUM4, ProfileVersion=0, OwnerPid=6341, OwnerEntityId=tbl5HP4XTP3EGWDBRCRAAIT4AGD7E, OwnerClassId=aclQCQNNJMW4FCNZCRN2D5GNWKOKA, OwnerPropId=pruNHYZI7WV4ZGDPDCXONZQWDWP2Y, Profile=boolean isRequest(byte[] data, Common::Map<Str,Str> parsingVars) throws NetHubFormatError, PipelineException. Description: 
    29. ClassGUID=aclNJQPXOGPZVAJPCCRI26IFRTZHY, ProfileVersion=0, OwnerPid=6341, OwnerEntityId=tbl5HP4XTP3EGWDBRCRAAIT4AGD7E, OwnerClassId=aclQCQNNJMW4FCNZCRN2D5GNWKOKA, OwnerPropId=pruQ4URE5BVGVAB7HIHPXE2JN5LBY, Profile=boolean isCorrelated(byte[] rq, Common::Map<Str,Str> rqParsingVars, byte[] rs, Common::Map<Str,Str> rsParsingVars) throws NetHubFormatError, PipelineException. Description: 

Node (Title: Incoming.Rtp. ClassId: aclSJWDDYSTAJDNFGAKPB5ENWPCVQ, EntityPid: 16983) (1):
    30. ClassGUID=aclJUSHZQABQZFDVC3BHF2R4SDRNY, ProfileVersion=0, OwnerPid=16983, OwnerEntityId=tblKG37PKEBQPNRDB46AALOMT5GDM, OwnerClassId=aclSJWDDYSTAJDNFGAKPB5ENWPCVQ, OwnerPropId=pruUHNT6SGVYFGQNLYXBL6PRVG4RQ, OwnerExtGuid=7B74FE964CFA4446A91C6857A5C71145, Profile=Xml mask(Xml mess) throws PipelineException. Description: 

Node (Title: Outgoing.Rtp. ClassId: aclDL54XGQDBZCETH2Y35V52MIKXA, EntityPid: 16984) (1):
    31. ClassGUID=aclJUSHZQABQZFDVC3BHF2R4SDRNY, ProfileVersion=0, OwnerPid=16984, OwnerEntityId=tblKG37PKEBQPNRDB46AALOMT5GDM, OwnerClassId=aclDL54XGQDBZCETH2Y35V52MIKXA, OwnerPropId=pru4437EDZTLFCQROXATBM4NHG3WQ, OwnerExtGuid=8F4A6616021B43D49CD7714A39A26961, Profile=Xml mask(Xml mess) throws PipelineException. Description:   
"""
