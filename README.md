# Vanessa Automation

[![GitHub release](https://img.shields.io/github/release/Pr-Mex/vanessa-automation.svg)](docs/Changelog.md)
[![Build Status](http://vanessa.bit-erp.ru/buildStatus/icon?job=VAFullCheck)](http://vanessa.bit-erp.ru/job/VAFullCheck/)
[![GitHub Releases](https://img.shields.io/github/downloads/Pr-Mex/vanessa-automation/latest/total?style=flat-square)](https://github.com/Pr-Mex/vanessa-automation/releases)
[![GitHub All Releases](https://img.shields.io/github/downloads/Pr-Mex/vanessa-automation/total?style=flat-square)](https://github.com/Pr-Mex/vanessa-automation/releases)
[![telegram](https://img.shields.io/badge/telegram-chat-green.svg)](https://t.me/testspro1c)

> [!NOTE]
> **Адаптированный форк `infostart-hub/vanessa-automation-aiadopted`** на базе [`Pr-Mex/vanessa-automation`](https://github.com/Pr-Mex/vanessa-automation) для экосистемы **[1С · AI Pipeline](https://github.com/infostart-hub/vanessa-ai-pipeline)**.
> Включает расширенный встроенный MCP-сервер (`MCPVA`) для автономной работы ИИ-агентов с живым сеансом 1С: горячий перезапуск `restart_vanessa` (`VAExtension_ПерезапускVA`), `manage_editor`, чтение активного элемента и подбор шагов (`get_active_form_element`, `get_form_element_steps`), выполнение шага на загруженном сценарии (`execute_feature_step`), машиночитаемые ответы `format=json` (`get_test_results`, `get_vanessa_automation_state`), запись действий пользователя (`user_actions_recording`), точки останова по `(file, line)`, идентификацию клиентов тестирования по `(PID + StartTime)`, устойчивое закрытие менеджера при обрыве связи с TestClient, а также воспроизводимую сборку через [`mise.toml`](mise.toml) и инструкцию для macOS **[`docs/use-cases/macos-build.md`](docs/use-cases/macos-build.md)**.

## Документация

https://pr-mex.github.io/vanessa-automation/dev

## Лицензии

* основная лицензия продукта - BSD v3
* лицензии стороннего кода - Apache License, GitHub CLA, Freeware, etc
