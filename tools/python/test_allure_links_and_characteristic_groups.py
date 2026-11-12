"""Execute the merged BSL logic in OneScript; no running 1C service required."""

import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class MergedFeatureTests(unittest.TestCase):
    def test_allure_links_append_and_characteristic_groups_stay_groups(self):
        allure = next(
            (ROOT / "features/Libraries/allure/step_definitions").glob(
                "*/Forms/*/Ext/Form/Module.bsl"
            )
        )
        source = allure.read_text(encoding="utf-8-sig")
        function = re.search(
            r"Функция ЯДобавляюСсылкуВОтчетAllure\([^\n]*\n.*?КонецФункции",
            source,
            re.S,
        )
        self.assertIsNotNone(function)
        serializer = (ROOT / "plugins/СериализаторMXL/Ext/ObjectModule.bsl").read_text(
            encoding="utf-8-sig"
        )
        expressions = re.findall(
            r"Если (\(Метаданные\.Справочники\.Содержит\([^\n]+?ЭтоГруппа) Тогда",
            serializer,
        )
        self.assertEqual(len(expressions), 2)
        with tempfile.TemporaryDirectory(prefix="vanessa-merge-unit-") as temporary:
            directory = Path(temporary)
            (directory / "allure.os").write_text(
                "Перем Ванесса Экспорт;\n" + function.group(), encoding="utf-8"
            )
            (directory / "gateway.os").write_text(GATEWAY, encoding="utf-8")
            (directory / "collection.os").write_text(COLLECTION, encoding="utf-8")
            predicates = "\n".join(
                f"Функция Группа{index}(Метаданные, МетаСсылка, Ссылка,"
                f" Мета, Объект) Экспорт\nВозврат {expression};\nКонецФункции"
                for index, expression in enumerate(expressions)
            )
            (directory / "groups.os").write_text(predicates, encoding="utf-8")
            (directory / "test.os").write_text(SCENARIO, encoding="utf-8")
            result = subprocess.run(
                [os.environ["OSCRIPT"], str(directory / "test.os")],
                cwd=directory,
                capture_output=True,
            )
            self.assertEqual(
                result.returncode,
                0,
                (result.stdout + result.stderr).decode("utf-8", errors="replace"),
            )


GATEWAY = """
Перем Результат Экспорт;
Функция ПолучитьСостояниеVanessaBehavior() Экспорт
 Возврат Новый Структура("ТекущийСценарий",
  Новый Структура("РезультатПрохожденияТестовСценария", Результат));
КонецФункции
Результат = Новый Структура;
"""
COLLECTION = """
Перем Имя Экспорт;
Функция Содержит(Элемент) Экспорт
 Возврат Элемент = Имя;
КонецФункции
"""
SCENARIO = """
Процедура Проверить(Условие, Причина)
 Если НЕ Условие Тогда ВызватьИсключение Причина; КонецЕсли;
КонецПроцедуры
Шаг = ЗагрузитьСценарий("allure.os");
Шлюз = ЗагрузитьСценарий("gateway.os");
Шаг.Ванесса = Шлюз;
Проверить(Шаг.ЯДобавляюСсылкуВОтчетAllure("https://example.org/build/12"),
  "step result" );
Шаг.ЯДобавляюСсылкуВОтчетAllure("https://example.org/report/12");
Ссылки = Шлюз.Результат.СписокСсылок;
Проверить(Ссылки.Количество() = 2, "append rather than overwrite");
Проверить(Ссылки[0].Значение.url = "https://example.org/build/12", "first link");
Проверить(Ссылки[1].Значение.name = "https://example.org/report/12", "link name");
Проверить(Ссылки[1].Значение.type = "custom", "link type");
Ссылки.Очистить();
Ссылки.Добавить(Новый Структура("name,url,type", "tag", "https://example.org/tag",
  "issue"));
Шаг.ЯДобавляюСсылкуВОтчетAllure("https://example.org/extra");
Проверить(Ссылки[0].Значение.type = "issue" И Ссылки.Количество() = 2,
  "preserve tag links" );
Справочники = ЗагрузитьСценарий("collection.os"); Справочники.Имя = "catalog";
Планы = ЗагрузитьСценарий("collection.os"); Планы.Имя = "characteristic";
Метаданные = Новый Структура("Справочники,ПланыВидовХарактеристик", Справочники, Планы);
Группы = ЗагрузитьСценарий("groups.os");
Для Каждого Мета Из СтрРазделить("catalog,characteristic,exchange", ",") Цикл
 Для Каждого Флаг Из СтрРазделить("true,false", ",") Цикл
  Объект = Новый Структура("ЭтоГруппа", Флаг = "true");
  Ожидается = Мета <> "exchange" И Флаг = "true";
  Проверить(Группы.Группа0(Метаданные, Мета, Объект, Мета, Объект) = Ожидается,
  "export group mode" );
  Проверить(Группы.Группа1(Метаданные, Мета, Объект, Мета, Объект) = Ожидается,
  "serialization group mode" );
 КонецЦикла;
КонецЦикла;
Объект = Новый Структура;
Проверить(НЕ Группы.Группа0(Метаданные, "exchange", Объект, "exchange", Объект),
  "non-hierarchical references" );
Проверить(НЕ Группы.Группа1(Метаданные, "exchange", Объект, "exchange", Объект),
  "non-hierarchical objects" );
"""
