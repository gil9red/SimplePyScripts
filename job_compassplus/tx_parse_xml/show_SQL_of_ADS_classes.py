#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import xml.etree.ElementTree as ET

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ADS:
    title: str
    props: dict[str, list[str]]
    editors: dict[str, list[str]]
    selectors: dict[str, list[str]]
    filters: dict[str, list[str]]
    sortings: dict[str, list[str]]

    def __bool__(self) -> bool:
        return bool(
            self.props
            or self.editors
            or self.selectors
            or self.filters
            or self.sortings
        )


NS = dict(
    ads="http://schemas.radixware.org/adsdef.xsd",
    xsc="http://schemas.radixware.org/xscml.xsd",
)


def has_text(el: ET.Element) -> bool:
    return any(text.strip() for text in el.itertext())


def get_xml_object_title(el: ET.Element) -> str:
    el_id = el.attrib["Id"]
    el_name = el.attrib["Name"]
    return f"{el_name}({el_id})"


def get_databases_specific_sqml_expression(el: ET.Element, tag_name: str) -> list[str]:
    items = []
    if not el:
        return items

    specific_sqml_expression_el = el.findall(f"./ads:{tag_name}", namespaces=NS)
    for sqml_el in specific_sqml_expression_el:
        if sqml_el and has_text(sqml_el.find("./xsc:Content", namespaces=NS)):
            database = sqml_el.find("./xsc:Database", namespaces=NS).text
            items.append(database)

    return items


def get_exists_condition_names(condition_el: ET.Element) -> list[str]:
    items = []
    if not condition_el:
        return items

    condition_where_el = condition_el.find("./ads:ConditionWhere", namespaces=NS)
    if condition_where_el and has_text(condition_where_el):
        items.append("ConditionWhere")

    condition_from_el = condition_el.find("./ads:ConditionFrom", namespaces=NS)
    if condition_from_el and has_text(condition_from_el):
        items.append("ConditionFrom")

    for tag_name in ["SpecificConditionWhere", "SpecificConditionFrom"]:
        for database in get_databases_specific_sqml_expression(condition_el, tag_name):
            items.append(f"{tag_name}={database}")

    return items


def get_ads_filters(ads_el: ET.Element) -> dict[str, list[str]]:
    obj_by_items = defaultdict(list)

    for filter_el in ads_el.findall(
        "./ads:Presentations/ads:Filters/ads:Filter", namespaces=NS
    ):
        filter_title = get_xml_object_title(filter_el)

        condition_el = filter_el.find("./ads:Condition", namespaces=NS)
        if condition_el and has_text(condition_el):
            obj_by_items[filter_title].append("Condition")

        condition_from_el = filter_el.find("./ads:ConditionFrom", namespaces=NS)
        if condition_from_el and has_text(condition_from_el):
            obj_by_items[filter_title].append("ConditionFrom")

        hint_el = filter_el.find("./ads:Hint", namespaces=NS)
        if hint_el and has_text(hint_el):
            obj_by_items[filter_title].append("Hint")

        for tag_name in ["SpecificCondition", "SpecificConditionFrom", "SpecificHint"]:
            for database in get_databases_specific_sqml_expression(filter_el, tag_name):
                obj_by_items[filter_title].append(f"{tag_name}={database}")

        enabled_sorting_el = filter_el.find("./ads:EnabledSorting", namespaces=NS)
        if enabled_sorting_el:
            enabled_sorting_hint_el = enabled_sorting_el.find(
                "./ads:Hint", namespaces=NS
            )
            if enabled_sorting_hint_el and has_text(enabled_sorting_hint_el):
                obj_by_items[filter_title].append("EnabledSorting/Hint")

            for database in get_databases_specific_sqml_expression(
                enabled_sorting_el, "SpecificHint"
            ):
                obj_by_items[filter_title].append(
                    f"EnabledSorting/SpecificHint={database}"
                )

    return obj_by_items


def get_ads_props(ads_el: ET.Element) -> dict[str, list[str]]:
    prop_by_items = defaultdict(list)

    for prop_el in ads_el.findall("./ads:Properties/ads:Property", namespaces=NS):
        prop_title = get_xml_object_title(prop_el)

        sqml_expression_el = prop_el.find("./ads:SqmlExpression", namespaces=NS)
        if sqml_expression_el and has_text(sqml_expression_el):
            prop_by_items[prop_title].append("SqmlExpression")

        for database in get_databases_specific_sqml_expression(
            prop_el, "SpecificSqmlExpression"
        ):
            prop_by_items[prop_title].append(f"SpecificSqmlExpression={database}")

        parent_select_condition_el = prop_el.find(
            "./ads:Presentation/ads:ParentSelect/ads:ParentSelectCondition",
            namespaces=NS,
        )
        for condition_name in get_exists_condition_names(parent_select_condition_el):
            prop_by_items[prop_title].append(f"ParentSelect/{condition_name}")

    return prop_by_items


def get_ads_editor_presentations(ads_el: ET.Element) -> dict[str, list[str]]:
    obj_by_items = defaultdict(list)

    for presentation_el in ads_el.findall(
        "./ads:Presentations/ads:EditorPresentations/ads:EditorPresentation",
        namespaces=NS,
    ):
        editor_title = get_xml_object_title(presentation_el)

        for child_item_ref_el in presentation_el.findall(
            "./ads:ChildExplorerItems/ads:Item/ads:ChildRef", namespaces=NS
        ):
            condition_el = child_item_ref_el.find("./ads:Condition", namespaces=NS)
            child_sqml_items = get_exists_condition_names(condition_el)
            if child_sqml_items:
                child_ref_title = get_xml_object_title(child_item_ref_el)
                obj_by_items[editor_title].append(
                    f'{child_ref_title}: {", ".join(child_sqml_items)}'
                )

        for child_item_entity_el in presentation_el.findall(
            "./ads:ChildExplorerItems/ads:Item/ads:Entity", namespaces=NS
        ):
            condition_el = child_item_entity_el.find("./ads:Condition", namespaces=NS)
            child_sqml_items = get_exists_condition_names(condition_el)
            if child_sqml_items:
                child_entity_title = get_xml_object_title(child_item_entity_el)
                obj_by_items[editor_title].append(
                    f'{child_entity_title}: {", ".join(child_sqml_items)}'
                )

    return obj_by_items


def get_ads_selector_presentations(ads_el: ET.Element) -> dict[str, list[str]]:
    obj_by_items = defaultdict(list)

    for presentation_el in ads_el.findall(
        "./ads:Presentations/ads:SelectorPresentations/ads:SelectorPresentation",
        namespaces=NS,
    ):
        selector_title = get_xml_object_title(presentation_el)

        condition_el = presentation_el.find("./ads:Condition", namespaces=NS)
        for condition_name in get_exists_condition_names(condition_el):
            obj_by_items[selector_title].append(condition_name)

        addons_el = presentation_el.find("./ads:Addons", namespaces=NS)
        if addons_el:
            default_hint_el = addons_el.find("./ads:DefaultHint", namespaces=NS)
            if default_hint_el and has_text(default_hint_el):
                obj_by_items[selector_title].append("Addons/DefaultHint")

            specific_hint_el = addons_el.find("./ads:SpecificHint", namespaces=NS)
            for database in get_databases_specific_sqml_expression(
                specific_hint_el, "SpecificDefaultHint"
            ):
                obj_by_items[selector_title].append(
                    f"Addons/SpecificDefaultHint={database}"
                )

    return obj_by_items


def get_ads_sortings(ads_el: ET.Element) -> dict[str, list[str]]:
    obj_by_items = defaultdict(list)

    sorting_el = ads_el.find(
        "./ads:Presentations/ads:Sortings/ads:Sorting", namespaces=NS
    )
    if sorting_el:
        sorting_title = get_xml_object_title(sorting_el)

        hint_el = sorting_el.find("./ads:Hint", namespaces=NS)
        if hint_el and has_text(hint_el):
            obj_by_items[sorting_title].append("Hint")

        specific_hint_el = sorting_el.find("./ads:SpecificHint", namespaces=NS)
        for database in get_databases_specific_sqml_expression(
            specific_hint_el, "SpecificHint"
        ):
            obj_by_items[sorting_title].append(f"SpecificHint={database}")

    return obj_by_items


def get_ads(model_path: Path) -> ADS | None:
    model = ET.fromstring(model_path.read_text(encoding="utf-8"))
    ads_el = model.find("./ads:AdsClassDefinition", namespaces=NS)
    if not ads_el:
        return

    return ADS(
        title=get_xml_object_title(ads_el),
        props=get_ads_props(ads_el),
        editors=get_ads_editor_presentations(ads_el),
        selectors=get_ads_selector_presentations(ads_el),
        filters=get_ads_filters(ads_el),
        sortings=get_ads_sortings(ads_el),
    )


def get_ads_list(branch_dir: Path | str) -> dict[str, list[ADS]]:
    if isinstance(branch_dir, str):
        branch_dir = Path(branch_dir)

    layer_module_by_ads_list = defaultdict(list)

    for layer_dir in branch_dir.glob("*"):
        if not layer_dir.is_dir():
            continue

        layer_ads_dir = layer_dir / "ads"
        if layer_ads_dir.is_dir():
            layer = layer_dir.name
            for module_path in layer_ads_dir.glob("*/src"):
                module = module_path.parent.name
                layer_module = f"{layer}/{module}"

                for class_path in module_path.glob("*.xml"):
                    if ads := get_ads(class_path):
                        layer_module_by_ads_list[layer_module].append(ads)

    return layer_module_by_ads_list


def process(path: str):
    indent1 = "    "
    indent2 = indent1 * 2
    indent3 = indent1 * 3
    indent4 = indent1 * 4
    for layer_module, ads_list in get_ads_list(path).items():
        print(layer_module)

        for ads in ads_list:
            print(indent1 + ads.title)

            prop_by_sqmls = ads.props
            if prop_by_sqmls:
                print(indent2 + "Props:")
                for prop, items in prop_by_sqmls.items():
                    print(indent3 + f'{prop}: {", ".join(items)}')

            editor_by_sqmls = ads.editors
            if editor_by_sqmls:
                print(indent2 + "Editor presentations:")
                for editor, items in editor_by_sqmls.items():
                    print(indent3 + f"{editor}:")
                    for sqml in items:
                        print(indent4 + f"{sqml}")

            selector_by_sqmls = ads.selectors
            if selector_by_sqmls:
                print(indent2 + "Selector presentations:")
                for selector, items in selector_by_sqmls.items():
                    print(indent3 + f'{selector}: {", ".join(items)}')

            filter_by_sqmls = ads.filters
            if filter_by_sqmls:
                print(indent2 + "Filters:")
                for filter_name, items in filter_by_sqmls.items():
                    print(indent3 + f'{filter_name}: {", ".join(items)}')

            sorting_by_sqmls = ads.sortings
            if sorting_by_sqmls:
                print(indent2 + "Sortings:")
                for sorting, items in sorting_by_sqmls.items():
                    print(indent3 + f'{sorting}: {", ".join(items)}')

            print()

        print("\n" + "-" * 100 + "\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Shows ADS entities with SQL definitions"
    )
    parser.add_argument(
        "path_trunk",
        metavar="/PATH/TO/TRUNK",
        help="Path to TX source tree (the directory containing branch.xml)",
    )
    args = parser.parse_args()

    process(args.path_trunk)
