#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from bs4 import BeautifulSoup


text = """
<item id="31025805">
    <genre>статья в сборнике трудов конференции</genre>
    <type>статья в сборнике трудов конференции</type>
    <source id="31025548">
        <titles>
            <title lang="EN">CEUR Workshop Proceedings</title>
        </titles>
        <titleaddinfo>3</titleaddinfo>
        <volumenumber>1825</volumenumber>
        <volumename>MMIT 2016 - Proceedings of 3rd Russian Conference "Mathematical Modeling and Information Technologies"</volumename>
        <seriesname>MMIT 2016 - Proceedings of 3rd Russian Conference "Mathematical Modeling and Information Technologies"</seriesname>
        <yearpubl>2016</yearpubl>
        <confname>3rd Russian Conference "Mathematical Modeling and Information Technologies", MMIT 2016</confname>
        <confplace>Yekaterinburg</confplace>
        <confdatebegin>16.11.2016</confdatebegin>
    </source>
    <pages>111-117</pages>
    <language>IT</language>
    <yearpubl>2016</yearpubl>
    <cited>0</cited>
    <titles>
        <title lang="EN">Modelling of cash flows by means of Markov processes</title>
    </titles>
    <grnti>270100</grnti>
    <risc>yes</risc>
    <corerisc>yes</corerisc>
    <authors>
        <author num="1" lang="EN">
            <lastname>Timofeeva</lastname>
            <initials>G.A.</initials>
            <authorid>15676</authorid>
            <spin>2292-7833</spin>
            <email>Gtimofeeva@usurt.ru</email>
            <affiliations>
                <affiliation num="1" lang="EN">
                    <orgname>Ural State University of Railway Transport</orgname>
                    <orgid>6766</orgid>
                    <country>rus</country>
                    <town>Yekaterinburg</town>
                </affiliation>
                <affiliation num="2" lang="EN">
                    <orgname>Ural Federal University</orgname>
                    <orgid>290</orgid>
                    <country>rus</country>
                    <town>Yekaterinburg</town>
                </affiliation>
            </affiliations>
        </author>
        <author num="2" lang="EN">
            <lastname>Bozhalkina</lastname>
            <initials>Y.A.</initials>
            <authorid>779136</authorid>
            <spin>6791-5486</spin>
            <email>Bozhalkina@mail.ru</email>
            <affiliations>
                <affiliation num="1" lang="EN">
                    <orgname>Ural State University of Railway Transport</orgname>
                    <orgid>6766</orgid>
                    <country>rus</country>
                    <town>Yekaterinburg</town>
                </affiliation>
            </affiliations>
        </author>
    </authors>
</item>
<item id="29099767">
    <genre>статья в сборнике трудов конференции</genre>
    <type>статья в сборнике трудов конференции</type>
    <source id="29091999">
        <titles>
            <title lang="EN">Mathematical Modeling and Information Technologies</title>
            <title lang="RU">Математическое моделирование и информационные технологии</title>
        </titles>
        <titleaddinfo>Proceedings</titleaddinfo>
        <yearpubl>2016</yearpubl>
        <pagesnumber>275</pagesnumber>
        <publisher>CEUR-WS.org</publisher>
        <confname>3rd Russian Conference "Mathematical Modeling and Information Technologies"</confname>
        <confplace>Екатеринбург</confplace>
        <confdatebegin>16.11.2016</confdatebegin>
        <confdateend>16.11.2016</confdateend>
    </source>
    <pages>111-117</pages>
    <language>RU</language>
    <yearpubl>2016</yearpubl>
    <cited>0</cited>
    <titles>
        <title lang="RU">Моделирование потоков платежей с помощью марковских случайных процессов</title>
    </titles>
    <grnti>270100</grnti>
    <risc>yes</risc>
    <corerisc>no</corerisc>
    <authors>
        <author num="1" lang="EN">
            <lastname>Timofeeva</lastname>
            <initials>G.A.</initials>
            <authorid>15676</authorid>
            <spin>2292-7833</spin>
            <email>Gtimofeeva@mail.ru</email>
            <affiliations>
                <affiliation num="1" lang="EN">
                    <orgname>Public Educational Institution of Higher Professional Education The Ural State University of Railway Transport</orgname>
                    <orgid>6766</orgid>
                    <country>RUS</country>
                    <town>Ekaterinburg</town>
                    <address>Kolmogorov Street 66, Ekaterinburg, Russia, 620034</address>
                </affiliation>
            </affiliations>
        </author>
        <author num="1" lang="RU">
            <lastname>Тимофеева</lastname>
            <initials>Галина Адольфовна</initials>
            <authorid>15676</authorid>
            <spin>2292-7833</spin>
            <email>Gtimofeeva@mail.ru</email>
            <affiliations>
                <affiliation num="1" lang="RU">
                    <orgname>Уральский государственный университет путей сообщения</orgname>
                    <orgid>6766</orgid>
                    <country>RUS</country>
                    <town>Екатеринбург</town>
                    <address>620034  г.Екатеринбург, ул. Колмогорова,66</address>
                </affiliation>
            </affiliations>
        </author>
        <author num="2" lang="EN">
            <lastname>Bozhalkina</lastname>
            <initials>Ya.A.</initials>
            <authorid>779136</authorid>
            <spin>6791-5486</spin>
            <email>bozhalkina@mail.ru</email>
            <affiliations>
                <affiliation num="1" lang="EN">
                    <orgname>Public Educational Institution of Higher Professional Education The Ural State University of Railway Transport</orgname>
                    <orgid>6766</orgid>
                    <country>RUS</country>
                    <town>Ekaterinburg</town>
                    <address>Kolmogorov Street 66, Ekaterinburg, Russia, 620034</address>
                </affiliation>
            </affiliations>
        </author>
        <author num="2" lang="RU">
            <lastname>Божалкина</lastname>
            <initials>Яна Андреевна</initials>
            <authorid>779136</authorid>
            <spin>6791-5486</spin>
            <email>bozhalkina@mail.ru</email>
            <affiliations>
                <affiliation num="1" lang="RU">
                    <orgname>Уральский государственный университет путей сообщения</orgname>
                    <orgid>6766</orgid>
                    <country>RUS</country>
                    <town>Екатеринбург</town>
                    <address>620034  г.Екатеринбург, ул. Колмогорова,66</address>
                </affiliation>
            </affiliations>
        </author>
    </authors>
</item>
"""


def get_title_book(item) -> str:
    titles = item.select("titles")[1]
    return titles.title.text


def get_author_full_name(author_node) -> str:
    return author_node.lastname.text + " " + author_node.initials.text


def get_authors(item) -> list:
    authors = item.select("authors > author")

    # Словарь для хранения номера автора и списка на разных языках
    num_author_by_authors = dict()

    for author in authors:
        num = author["num"]
        if num not in num_author_by_authors:
            num_author_by_authors[num] = []

        num_author_by_authors[num].append(author)

    authors_full_name = []

    for num, authors in num_author_by_authors.items():
        # Тут нечего выбирать
        if len(authors) == 1:
            full_name = get_author_full_name(authors[0])
            authors_full_name.append(full_name)

        else:
            # По умолчанию берем первый элемент
            full_name = get_author_full_name(authors[0])

            for author in authors:
                # Приоритетный язык
                if author["lang"] == "RU":
                    full_name = get_author_full_name(author)
                    break

            authors_full_name.append(full_name)

    return authors_full_name


root = BeautifulSoup(text, "html.parser")

for item in root.select("item"):
    title_book = get_title_book(item)
    print(title_book)

    authors = get_authors(item)
    print(authors)

    print()
