"""Behavioral test of production BSL classifier through installed OneScript.
TestClient objects are doubles; this is not a native UI acceptance test.
Run with OSCRIPT pointing to an installed OneScript interpreter.
"""

import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

SOURCE = (
    Path(__file__).resolve().parents[2]
    / "VanessaAutomation/Forms/КлиентТестирования/Ext/Form/Module.bsl"
)


class ModalDialogTests(unittest.TestCase):
    def test_documents_warnings_and_closed_windows(self):
        source = SOURCE.read_text(encoding="utf-8-sig")
        functions = []
        for name in (
            "ЭтоМодальныйДиалог",
            "ЭтоЗаголовокОкнаМодальногоДиалога",
            "НайтиПолеТекстаПредупреждения",
        ):
            match = re.search(
                r"Функция " + name + r"\([^\n]*\n.*?КонецФункции", source, re.S
            )
            self.assertIsNotNone(match, name)
            functions.append(match.group())
        with tempfile.TemporaryDirectory(prefix="vanessa-modal-") as temporary:
            root = Path(temporary)
            (root / "classifier.os").write_text(
                "Перем Ванесса;\n"
                + "\n".join(functions)
                + '\nВанесса = Новый Структура("Версия8315ИлиВыше", Истина);\n',
                encoding="utf-8",
            )
            (root / "type.os").write_text(
                "// TestClient type identity\n", encoding="utf-8"
            )
            (root / "window.os").write_text(WINDOW, encoding="utf-8")
            (root / "test.os").write_text(SCENARIO, encoding="utf-8")
            result = subprocess.run(
                [os.environ.get("OSCRIPT", "oscript"), str(root / "test.os")],
                cwd=root,
                capture_output=True,
            )
            self.assertEqual(
                result.returncode,
                0,
                (result.stdout + result.stderr).decode("utf-8", errors="replace"),
            )


WINDOW = r"""
Перем НачальнаяСтраница Экспорт;
Перем Основное Экспорт;
Перем Заголовок Экспорт;
Перем ИмяФормы Экспорт;
Перем Поле Экспорт;
Перем Закрыто Экспорт;
Функция НайтиОбъект(Вид = Неопределено, Второй = Неопределено,
    Имя = Неопределено) Экспорт
    Если Закрыто Тогда ВызватьИсключение "Окно закрыто"; КонецЕсли;
    Если Вид <> Неопределено Тогда Возврат ЭтотОбъект; КонецЕсли;
    Если Имя = Поле Тогда
        Возврат Новый Структура("ТекстЗаголовка", "Сообщение");
    КонецЕсли;
    Возврат Неопределено;
КонецФункции
НачальнаяСтраница = Ложь;
Основное = Ложь;
Заголовок = "Документ";
ИмяФормы = "";
Поле = "";
Закрыто = Ложь;
"""
SCENARIO = r"""
Процедура Проверить(Значение, Ожидалось, Случай)
    Если Значение <> Ожидалось Тогда ВызватьИсключение Случай; КонецЕсли;
КонецПроцедуры
ПодключитьСценарий("type.os", "ТестируемаяФорма");
Классификатор = ЗагрузитьСценарий("classifier.os");
Окно = ЗагрузитьСценарий("window.os");
Проверить(Классификатор.ЭтоМодальныйДиалог(Окно), Ложь,
    "Показанный документ не является предупреждением");
Для Каждого Имя Из СтрРазделить("message,Поле,ErrorInfo", ",") Цикл
    Окно.Поле = Имя;
    Проверить(Классификатор.ЭтоМодальныйДиалог(Окно), Истина, "Предупреждение " + Имя);
КонецЦикла;
Окно.Поле = "";
Окно.ИмяФормы = "MessageBox";
Проверить(Классификатор.ЭтоМодальныйДиалог(Окно), Истина, "Именованный диалог");
Окно.ИмяФормы = "";
Окно.Закрыто = Истина;
Проверить(Классификатор.ЭтоМодальныйДиалог(Окно), Ложь, "Закрывшееся окно");
Сообщить("PASS: document, three warning fields, named dialog, closed window");
"""
if __name__ == "__main__":
    unittest.main()
